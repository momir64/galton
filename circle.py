from pygame import gfxdraw
from constants import *
import numpy as np
import itertools
import pygame


class Circle:
    id_counter = itertools.count()

    def __init__(self, position, radius, color, restitution=0, gravity=np.zeros(2)):
        self.restitution, self.gravity = restitution, gravity
        self.id = next(Circle.id_counter)
        self.position = position
        self.speed = np.zeros(2)
        self.radius = radius
        self.color = color

    def update(self, dt):
        self.speed += self.gravity * dt
        self.position += self.speed * dt * DISTANCE2PIXEL

    def applyImpulse(self, impulse, dt):
        self.speed += impulse
        self.position += self.speed * dt * DISTANCE2PIXEL

    def print(self, screen, x, y):
        if DRAWAA:
            gfxdraw.aacircle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
            gfxdraw.filled_circle(screen, int(x + self.position[0]), int(y + self.position[1]), self.radius, self.color)
        else:
            pygame.draw.circle(screen, self.color, (int(x + self.position[0]), int(y + self.position[1])), self.radius)

    def __hash__(self):
        return self.id

    def __eq__(self, __value: object):
        return self.id == __value.id
