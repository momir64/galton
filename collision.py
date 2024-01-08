import numpy as np


def circle_circle(ball1, ball2, collisions):
    distance = ball2.position - ball1.position
    distane_norm = np.linalg.norm(distance)
    penetration = ball1.radius + ball2.radius - distane_norm
    if penetration >= 0:
        collisions.append(Collision(penetration, distance / distane_norm, ball1.speed - ball2.speed, ball1, ball2))


def circle_line(ball, line, collisions):
    closest_point = line.start + (np.dot(ball.position - line.start, line.vector) / line.length2) * line.vector
    if np.isclose(np.linalg.norm(closest_point - line.start) + np.linalg.norm(closest_point - line.end), line.length, atol=0.1):
        distance = closest_point - ball.position
        distane_norm = np.linalg.norm(distance)
        penetration = ball.radius + line.radius - distane_norm
        if penetration >= 0:
            collisions.append(Collision(penetration, distance / distane_norm, ball.speed, ball, line))


class Collision:
    def __init__(self, penetration, normal, relativeSpeed, obj1, obj2):
        self.relativeSpeed = relativeSpeed
        self.normal = normal
        self.penetration = penetration
        self.obj1 = obj1
        self.obj2 = obj2
