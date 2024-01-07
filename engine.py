from collision import circle_circle, circle_line
from collision import Collision
from circle import Circle
from line import Line
import numpy as np


class Engine:
    def __init__(self, rows, cols, gridSize):
        self.grid = [[[]] * cols for _ in range(rows)]
        self.gridSize = gridSize
        self.collisions = []
        self.rows = rows
        self.cols = cols
        self.lines = []
        self.balls = []
        self.pegs = []

    def update(self, dt):
        for ball in self.balls:
            ball.update(dt)

        self.find_collisions()
        for c in self.collisions:
            i = self.balls.index(c.ball)
            correction = (c.penetration * 0.3) * c.normal
            impulse = -correction - np.dot(c.relativeSpeed, c.normal) * c.normal * (1 + c.ball.restitution * c.obstacle.restitution)  # * c.ball.mass
            self.balls[i].applyImpulse(impulse, dt)
        self.collisions.clear()

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
                    circle_circle(ball, obstacle, self.collisions)
                if isinstance(obstacle, Line):
                    circle_line(ball, obstacle, self.collisions)
            for ball2 in self.balls:
                if ball != ball2:
                    circle_circle(ball, ball2, self.collisions)
