from pygame import gfxdraw
from constants import *
import numpy as np
import pygame
import math


class Line:
    def __init__(self, x1, y1, x2, y2, width, color, restitution=LINE_RESTITUTION):
        self.start = np.array([x1, y1])
        self.end = np.array([x2, y2])
        self.vector = self.end - self.start
        self.length = np.linalg.norm(self.vector)
        self.length2 = self.length * self.length
        self.restitution = restitution
        self.radius = width / 2
        self.width = width
        self.color = color

        center = (self.start + self.end) / 2.0
        angle = math.atan2(y1 - y2, x1 - x2)
        cos_angle, sin_angle = np.cos(angle), np.sin(angle)
        length_over_2, width_over_2 = self.length / 2.0, width / 2.0
        UL = (center[0] + length_over_2 * cos_angle - width_over_2 * sin_angle, center[1] + width_over_2 * cos_angle + length_over_2 * sin_angle)
        UR = (center[0] - length_over_2 * cos_angle - width_over_2 * sin_angle, center[1] + width_over_2 * cos_angle - length_over_2 * sin_angle)
        BL = (center[0] + length_over_2 * cos_angle + width_over_2 * sin_angle, center[1] - width_over_2 * cos_angle + length_over_2 * sin_angle)
        BR = (center[0] - length_over_2 * cos_angle + width_over_2 * sin_angle, center[1] - width_over_2 * cos_angle - length_over_2 * sin_angle)
        self.rect = np.array([UL, UR, BR, BL])

    def print(self, screen, x, y):
        if DRAWAA:
            rect = self.rect + np.array([x, y])
            gfxdraw.aapolygon(screen, rect, self.color)
            gfxdraw.filled_polygon(screen, rect, self.color)
        else:
            pygame.draw.line(screen, self.color, (x + self.start[0], y + self.start[1]), (x + self.end[0], y + self.end[1]), self.width)
