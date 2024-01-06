from collision import circle_circle, circle_line
from collision import Collision
from circle import Circle
from line import Line
import numpy as np


class Engine:
    def __init__(self):
        self.peg_collisions = []
        self.line_collisions = []
        self.lines = []
        self.balls = []
        self.pegs = []

    def update(self, dt):
        for ball in self.balls:
            ball.update(dt)

        self.find_collisions()
        for collisions in [self.peg_collisions, self.line_collisions]:
            for c in collisions:
                i = self.balls.index(c.ball)
                correction = (c.penetration * 0.2) * c.normal
                impulse = -correction - np.dot(c.relativeSpeed, c.normal) * c.normal * (1 + c.ball.restitution)  # * c.ball.mass
                self.balls[i].applyImpulse(impulse, dt)
            collisions.clear()

    def find_collisions(self):
        for ball in self.balls:
            for peg in self.pegs:
                circle_circle(ball, peg, self.peg_collisions)
            for line in self.lines:
                circle_line(ball, line, self.line_collisions)
