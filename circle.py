from constants import DISTANCE2PIXEL
from pygame import gfxdraw
import numpy as np
import pygame


class Circle:
    def __init__(self, position, radius, color, mass=0, restitution=0, gravity=0):
        self.mass, self.restitution, self.gravity = mass, restitution, gravity
        self.color = color
        self.position = position
        self.radius = radius

        self.speed = np.zeros(2)
        self.force = np.zeros(2)
        self.applyGravity()

    def update(self, dt):
        self.speed += self.force * dt # / self.mass
        self.position += self.speed * dt * DISTANCE2PIXEL
        self.force = np.zeros(2)
        self.applyGravity()

    def applyGravity(self):
        self.force += np.array([0, self.mass * self.gravity])

    def applyImpulse(self, impulse, dt):
        self.speed += impulse # / self.mass
        self.position += self.speed * dt * DISTANCE2PIXEL

    def print(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (int(x + self.position[0]), int(y + self.position[1])), self.radius)
        # gfxdraw.aacircle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
        # gfxdraw.filled_circle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
