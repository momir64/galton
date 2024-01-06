import numpy as np


def projectSpeed(speed, vector):
    return vector * np.dot(speed, vector) / np.dot(vector, vector)


def circle_circle(circle1, circle2, collisions):
    distance = circle2.position - circle1.position
    distane_norm = np.linalg.norm(distance)
    if distane_norm <= circle1.radius + circle2.radius:
        penetration = circle1.radius + circle2.radius - distane_norm
        collisions.append(Collision(penetration, distance / distane_norm, circle1.speed - circle2.speed, circle1, circle2))


def circle_line(ball, line, collisions):
    line_vector = line.end - line.start
    closest_point = line.start + np.dot(ball.position - line.start, line_vector) / np.linalg.norm(line_vector) ** 2 * line_vector

    if np.isclose(np.linalg.norm(closest_point - line.start) + np.linalg.norm(closest_point - line.end), np.linalg.norm(line.end - line.start), atol=0.1):
        distance = closest_point - ball.position
        distane_norm = np.linalg.norm(distance)
        if distane_norm <= ball.radius:
            collisions.append(Collision(ball.radius - distane_norm, distance / distane_norm, ball.speed, ball, line))


class Collision:
    def __init__(self, penetration, normal, relativeSpeed, ball, obstacle):
        self.relativeSpeed = relativeSpeed
        self.normal = normal
        self.penetration = penetration
        self.ball = ball
        self.obstacle = obstacle
