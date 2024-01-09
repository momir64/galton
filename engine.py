from collision import circle_circle, circle_line
from circle import Circle
from constants import *
import multiprocessing
from line import Line
import numpy as np
import itertools


class Engine:
    def __init__(self, width, height, gridSize, pool):
        self.rows = height // gridSize + 1
        self.cols = width // gridSize + 1
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        self.gridSize = gridSize
        self.ball_collisions = []
        self.collisions = []
        self.pool = pool
        self.lines = []
        self.balls = []
        self.pegs = []

    def add_ball(self, ball):
        self.balls.append(ball)
        # self.grid[ball.position[1] // self.gridSize][ball.position[0] // self.gridSize].append(ball)

    def add_line(self, line):
        self.lines.append(line)
        start = (line.start // self.gridSize).astype("int")
        end = (line.end // self.gridSize).astype("int")
        r_start, r_end = max(0, min((start[1], end[1]))), min(max(start[1], end[1]) + 1, self.rows)
        c_start, c_end = max(0, min((start[0], end[0]))), min(max(start[0], end[0]) + 1, self.cols)
        for row in range(r_start, r_end):
            for col in range(c_start, c_end):
                self.grid[row][col].append(line)

    def add_peg(self, peg):
        self.pegs.append(peg)
        self.grid[int(peg.position[1] // self.gridSize)][int(peg.position[0] // self.gridSize)].append(peg)

    def update(self, dt):
        for ball in self.balls:
            ball.update(dt)

        self.find_collisions()
        for collision in self.collisions:
            i = self.balls.index(collision.obj1)
            correction = (collision.penetration * CORRECTION_OBSTACLES) * collision.normal
            impulse = -correction - np.dot(collision.relativeSpeed, collision.normal) * collision.normal * (1 + collision.obj1.restitution * collision.obj2.restitution)
            self.balls[i].applyImpulse(impulse, dt)
        self.collisions.clear()

        pairs = list(itertools.combinations(self.balls, 2))
        if len(pairs) <= multiprocessing.cpu_count():
            self.find_ball_collisions(pairs)
        else:
            self.find_ball_collisions_parallel(pairs)
        for collision in self.ball_collisions:
            ball1 = self.balls.index(collision.obj1)
            ball2 = self.balls.index(collision.obj2)
            correction = (collision.penetration * CORRECTION_BALLS) * collision.normal
            impulse = -correction - np.dot(collision.relativeSpeed, collision.normal) * collision.normal * collision.obj1.restitution
            self.balls[ball1].applyImpulse(impulse, dt)
            self.balls[ball2].applyImpulse(-impulse, dt)
        self.ball_collisions.clear()

    def find_collisions(self):
        for ball in self.balls:
            position = (ball.position // self.gridSize).astype("int")
            r_start, c_start = max(0, position[1] - 1), max(0, position[0] - 1)
            r_end, c_end = min(self.rows, position[1] + 2), min(self.cols, position[0] + 2)
            obstacles = set()
            for row in range(r_start, r_end):
                for col in range(c_start, c_end):
                    for obstacle in self.grid[row][col]:
                        obstacles.add(obstacle)
            for obstacle in obstacles:
                if isinstance(obstacle, Circle):
                    collision = circle_circle(ball, obstacle)
                elif isinstance(obstacle, Line):
                    collision = circle_line(ball, obstacle)
                if collision:
                    self.collisions.append(collision)

    def find_ball_collisions(self, pairs):
        for balls in pairs:
            collision = circle_circle(balls[0], balls[1])
            if collision:
                self.ball_collisions.append(collision)

    def find_ball_collisions_parallel(self, pairs):
        chunk_size = len(pairs) // multiprocessing.cpu_count()
        chunks = [pairs[i : i + chunk_size] for i in range(0, len(pairs), chunk_size)]
        results = self.pool.map(find_ball_collisions_part, chunks)
        for result in results:
            self.ball_collisions.extend(result)


def find_ball_collisions_part(pairs):
    collisions = []
    for pair in pairs:
        collision = circle_circle(pair[0], pair[1])
        if collision:
            collisions.append(collision)
    return collisions
