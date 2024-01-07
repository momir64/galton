import numpy as np


def circle_circle(ball, peg, collisions):
    distance = peg.position - ball.position
    distane_norm = np.linalg.norm(distance)
    penetration = ball.radius + peg.radius - distane_norm
    if penetration >= 0:
        collisions.append(Collision(penetration, distance / distane_norm, ball.speed, ball, peg))


def circle_line(ball, line, collisions):
    closest_point = line.start + (np.dot(ball.position - line.start, line.vector) / line.length2) * line.vector
    if np.isclose(np.linalg.norm(closest_point - line.start) + np.linalg.norm(closest_point - line.end), line.length, atol=0.1):
        distance = closest_point - ball.position
        distane_norm = np.linalg.norm(distance)
        penetration = ball.radius - distane_norm
        if penetration >= 0:
            collisions.append(Collision(penetration, distance / distane_norm, ball.speed, ball, line))


class Collision:
    def __init__(self, penetration, normal, relativeSpeed, ball, obstacle):
        self.relativeSpeed = relativeSpeed
        self.normal = normal
        self.penetration = penetration
        self.ball = ball
        self.obstacle = obstacle
