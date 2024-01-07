from constants import *
import numpy as np
from pygame import gfxdraw
import pygame


class Circle:
    def __init__(self, position, radius, color, restitution=0, gravity=np.zeros(2)):
        self.restitution, self.gravity = restitution, gravity
        self.color = color
        self.position = position
        self.radius = radius

        self.speed = np.zeros(2)
        # self.force = np.zeros(2)
        # self.applyGravity()

    def update(self, dt):
        self.speed += self.gravity * dt  # / self.mass
        self.position += self.speed * dt * DISTANCE2PIXEL

    #     self.force = np.zeros(2)
    #     self.applyGravity()

    # def applyGravity(self):
    #     self.force += np.array([0, self.mass * self.gravity])

    def applyImpulse(self, impulse, dt):
        self.speed += impulse  # / self.mass
        self.position += self.speed * dt * DISTANCE2PIXEL

    def print(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (int(x + self.position[0]), int(y + self.position[1])), self.radius)
        # gfxdraw.aacircle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
        # gfxdraw.filled_circle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
