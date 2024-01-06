from collision import circle_circle, circle_line
from collision import Collision
from circle import Circle
from line import Line
import numpy as np


class Engine:
    def __init__(self):
        self.collisions = []
        self.obstacles = []
        self.balls = []

    def update(self, dt):
        for ball in self.balls:
            ball.update(dt)

        self.find_collisions()
        for collision in self.collisions:
            i = self.balls.index(collision.ball)
            impulse = -np.dot(collision.relativeSpeed, collision.normal) * collision.ball.mass * collision.normal * (1 + collision.ball.restitution)
            self.balls[i].applyImpulse(impulse, dt)
        self.collisions.clear()

    def find_collisions(self):
        for ball in self.balls:
            for obstacle in self.obstacles:
                if isinstance(obstacle, Circle):
                    circle_circle(ball, obstacle, self.collisions)
                elif isinstance(obstacle, Line):
                    circle_line(ball, obstacle, self.collisions)
