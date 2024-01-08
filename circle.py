from constants import *
import numpy as np
from pygame import gfxdraw
import pygame

CIRCLE_ID = 0


class Circle:
    def __init__(self, position, radius, color, restitution=0, gravity=np.zeros(2)):
        global CIRCLE_ID
        self.restitution, self.gravity = restitution, gravity
        self.position = position
        self.speed = np.zeros(2)
        self.radius = radius
        self.color = color
        self.id = CIRCLE_ID
        CIRCLE_ID += 1

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

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id
