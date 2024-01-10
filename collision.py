import numpy as np


def circle_circle(ball1, ball2):
    distance = ball2.position - ball1.position
    distane_norm = np.linalg.norm(distance)
    penetration = ball1.radius + ball2.radius - distane_norm
    if penetration >= 0:
        if distane_norm:
            normal = distance / distane_norm
        else:
            normal = np.random.rand(2)
            normal = normal / np.linalg.norm(normal)
        return Collision(penetration, normal, ball1.speed - ball2.speed, ball1, ball2)
    return None


def circle_line(ball, line):
    closest_point = line.start + (np.dot(ball.position - line.start, line.vector) / line.length2) * line.vector
    if np.isclose(np.linalg.norm(closest_point - line.start) + np.linalg.norm(closest_point - line.end), line.length, atol=0.1):
        distance = closest_point - ball.position
        distane_norm = np.linalg.norm(distance)
        penetration = ball.radius + line.radius - distane_norm
        if penetration >= 0:
            return Collision(penetration, distance / distane_norm, ball.speed, ball, line)
    return None


class Collision:
    def __init__(self, penetration, normal, relativeSpeed, obj1, obj2):
        self.relativeSpeed = relativeSpeed
        self.normal = normal
        self.penetration = penetration
        self.obj1 = obj1
        self.obj2 = obj2
