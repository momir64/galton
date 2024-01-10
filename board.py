from engine import Engine
from circle import Circle
from constants import *
from line import Line
import numpy as np
import pygame


class Board(Engine):
    def __init__(self, screen, x, y, width, height, ballNum, ballRadius, pegRadius, binNum, restitution, gravity, pool):
        super().__init__(width, height, 20, pool)
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.ballNum, self.ballRadius = ballNum, ballRadius
        self.pegRadius = pegRadius
        self.binNum = binNum
        self.restitution, self.gravity = restitution, gravity

        self.add_bins()
        self.add_pegs()
        self.add_balls()
        self.add_border()
        self.add_funnel()

    def add_balls(self):
        self.add_circles(self.ballNum, BALL_GAP, BALL_END, BALL_GAP, self.add_ball, self.ballRadius, ORANGE, self.restitution)

    def add_pegs(self):
        end = self.height - BIN_HEIGHT - 3 * BORDER
        self.add_circles(2048, PEG_START, end, self.ballRadius * PEG_GAP, self.add_peg, self.pegRadius, GRAY2, PEG_RESTITUTION)

    def add_circles(self, n, start, end, margin, add2group, radius, color, restitution):
        row = 0
        while n > 0:
            rowMax = int((self.width - 2 * BORDER) // (margin + 2 * radius) - row % 2)
            cols = min(n, rowMax)
            for i in range(cols):
                center = (self.width - cols * (margin + 2 * radius) + margin) / 2
                x = center + radius + i * (margin + 2 * radius)
                y = BORDER + start + radius + row * (margin / 2 + 2 * radius)
                if y + radius > end:
                    continue
                add2group(Circle(np.array([x, y], float), radius, color, restitution, self.gravity))
            n -= rowMax
            row += 1

    def add_bins(self):
        width = (self.width - BORDER * 2) / self.binNum
        for i in range(1, self.binNum):
            self.add_line(Line(i * width + BORDER, self.height - BORDER - BIN_HEIGHT, i * width + BORDER, self.height - BORDER, BORDER, GRAY2))
            self.add_peg(Circle(np.array([BORDER + i * width, self.height - BORDER - BIN_HEIGHT]), BORDER // 2, GRAY2))

    def add_funnel(self):
        self.add_line(Line(BORDER / 2, FUNNEL_START, (self.width - self.ballRadius * FUNNEL_GAP - BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT, FUNNEL_WIDTH, GRAY2))
        self.add_line(Line(self.width - BORDER / 2, FUNNEL_START, (self.width + self.ballRadius * FUNNEL_GAP + BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT, FUNNEL_WIDTH, GRAY2))
        self.add_peg(Circle(np.array([(self.width - self.ballRadius * FUNNEL_GAP - BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT]), FUNNEL_WIDTH // 2, GRAY2))
        self.add_peg(Circle(np.array([(self.width + self.ballRadius * FUNNEL_GAP + BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT]), FUNNEL_WIDTH // 2, GRAY2))

    def add_border(self):
        self.add_line(Line(0, BORDER / 2, self.width - 1, BORDER / 2, BORDER, GRAY2))
        self.add_line(Line(BORDER / 2, 0, BORDER / 2, self.height - 1, BORDER, GRAY2))
        self.add_line(Line(0, self.height - BORDER / 2, self.width - 1, self.height - BORDER / 2, BORDER, GRAY2))
        self.add_line(Line(self.width - BORDER / 2, 0, self.width - BORDER / 2, self.height - 1, BORDER, GRAY2))

    def print(self):
        pygame.draw.rect(self.screen, GRAY3, (self.x, self.y, self.width, self.height))
        for objects in [self.balls, self.lines, self.pegs]:
            for object in objects:
                object.print(self.screen, self.x, self.y)

    def update_restitution(self, restitution):
        self.restitution = restitution
        for ball in self.balls:
            ball.restitution = restitution

    def update_gravity(self, gravity):
        self.gravity = np.array([0, gravity])
        for ball in self.balls:
            ball.gravity = self.gravity

    def update(self, dt):
        super().update(dt)
        for ball in self.balls:
            margin = max(BORDER, ball.radius)
            if (not margin < ball.position[0] < BOARD_WIDTH - margin) or (not margin < ball.position[1] < BOARD_HEIGHT - margin):
                self.balls.remove(ball)
