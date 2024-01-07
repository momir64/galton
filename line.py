from constants import *
import numpy as np
import pygame

class Line:
    def __init__(self, x1, y1, x2, y2, color, restitution=LINE_RESTITUTION):
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])
        self.vector = self.end - self.start
        self.length = np.linalg.norm(self.vector)
        self.length2 = self.length * self.length
        self.restitution = restitution
        self.color = color

    def print(self, screen, x, y):
        # pygame.draw.line(screen, self.color, (x + self.start[0], y + self.start[1]), (x + self.end[0], y + self.end[1]))
        pygame.draw.aaline(screen, self.color, (x + self.start[0], y + self.start[1]), (x + self.end[0], y + self.end[1]))
