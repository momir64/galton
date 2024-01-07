from engine import Engine
from circle import Circle
from constants import *
from line import Line
import numpy as np
import pygame


class Board:
    def __init__(self, screen, x, y, width, height, ballNum, ballRadius, pegRadius, binNum, restitution, gravity):
        self.screen = screen
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.ballNum, self.ballRadius = ballNum, ballRadius
        self.pegRadius = pegRadius
        self.binNum = binNum
        self.restitution, self.gravity = restitution, np.array([0, gravity])

        self.engine = Engine()

        self.add_bins()
        self.add_pegs()
        self.add_balls()
        self.add_border()
        self.add_funnel()

    def add_ball(self, ball):
        self.engine.balls.append(ball)

    def add_line(self, line):
        self.engine.lines.append(line)

    def add_peg(self, peg):
        self.engine.pegs.append(peg)

    def add_balls(self):
        self.add_circles(self.ballNum, BALL_GAP, BALL_END, BALL_GAP, self.add_ball, self.ballRadius, ORANGE, self.restitution)

    def add_pegs(self):
        end = self.height - BIN_HEIGHT - 4 * BORDER
        self.add_circles(2048, PEG_START, end, self.ballRadius * 4, self.add_peg, self.pegRadius, GRAY2, PEG_RESTITUTION)

    def add_circles(self, n, start, end, margin, add2group, radius, color, restitution):
        row = 0
        while n > 0:
            rowMax = (self.width - 2 * BORDER) // (margin + 2 * radius) - row % 2
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
        width = self.width / self.binNum
        for i in range(1, self.binNum):
            self.add_line(Line(i * width - BORDER / 2, self.height - BORDER - BIN_HEIGHT, i * width - BORDER / 2, self.height - BORDER, GRAY2))
            self.add_line(Line(i * width + BORDER / 2, self.height - BORDER - BIN_HEIGHT, i * width + BORDER / 2, self.height - BORDER, GRAY2))
            self.add_peg(Circle(np.array([i * width, self.height - BORDER - BIN_HEIGHT]), BORDER // 2, GRAY2))

    def add_funnel(self):
        self.add_line(Line(BORDER, FUNNEL_START - BORDER / 2, (self.width - self.ballRadius * 2.5 - BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT - BORDER / 2, GRAY2))
        self.add_line(Line(BORDER, FUNNEL_START + BORDER / 2, (self.width - self.ballRadius * 2.5 - BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT + BORDER / 2, GRAY2))
        self.add_line(Line(self.width - BORDER, FUNNEL_START - BORDER / 2, (self.width + self.ballRadius * 2.5 + BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT - BORDER / 2, GRAY2))
        self.add_line(Line(self.width - BORDER, FUNNEL_START + BORDER / 2, (self.width + self.ballRadius * 2.5 + BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT + BORDER / 2, GRAY2))
        self.add_peg(Circle(np.array([(self.width - self.ballRadius * 2.5 - BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT]), BORDER // 2, GRAY2))
        self.add_peg(Circle(np.array([(self.width + self.ballRadius * 2.5 + BORDER) / 2, FUNNEL_START + FUNNEL_HEIGHT]), BORDER // 2, GRAY2))

    def add_border(self):
        self.add_line(Line(BORDER, BORDER, self.width - BORDER, BORDER, GRAY2))
        self.add_line(Line(BORDER, BORDER, BORDER, self.height - BORDER, GRAY2))
        self.add_line(Line(BORDER, self.height - BORDER, self.width - BORDER, self.height - BORDER, GRAY2))
        self.add_line(Line(self.width - BORDER, BORDER, self.width - BORDER, self.height - BORDER, GRAY2))

    def print(self):
        pygame.draw.rect(self.screen, GRAY3, (self.x, self.y, self.width, self.height))
        for ball in self.engine.balls:
            ball.print(self.screen, self.x, self.y)
        self.fill()
        for obstacles in [self.engine.lines, self.engine.pegs]:
            for obstacle in obstacles:
                obstacle.print(self.screen, self.x, self.y)

    def fill(self):
        pygame.draw.line(self.screen, GRAY2, (self.x, self.y + BORDER / 2), (self.x + self.width - 1, self.y + BORDER / 2), BORDER)
        pygame.draw.line(self.screen, GRAY2, (self.x + BORDER / 2, self.y), (self.x + BORDER / 2, self.y + self.height - 1), BORDER)
        pygame.draw.line(self.screen, GRAY2, (self.x, self.y + self.height - BORDER / 2), (self.x + self.width - 1, self.y + self.height - BORDER / 2), BORDER)
        pygame.draw.line(self.screen, GRAY2, (self.x + self.width - BORDER / 2, self.y), (self.x + self.width - BORDER / 2, self.y + self.height - 1), BORDER)
        pygame.draw.line(self.screen, GRAY2, (self.x + BORDER, self.y + FUNNEL_START), (self.x + (self.width - self.ballRadius * 2.5 - BORDER) / 2, self.y + FUNNEL_START + FUNNEL_HEIGHT), BORDER)
        pygame.draw.line(self.screen, GRAY2, (self.x + self.width - BORDER, self.y + FUNNEL_START), (self.x + (self.width + self.ballRadius * 2.5 + BORDER) / 2, self.y + FUNNEL_START + FUNNEL_HEIGHT), BORDER)
        width = self.width / self.binNum
        for i in range(1, self.binNum):
            pygame.draw.line(self.screen, GRAY2, (self.x + i * width, self.y + self.height - BORDER - BIN_HEIGHT), (self.x + i * width, self.y + self.height - BORDER), BORDER)

    def update_restitution(self, restitution):
        self.restitution = restitution
        for ball in self.engine.balls:
            ball.restitution = restitution

    def update_gravity(self, gravity):
        self.gravity = np.array([0, gravity])
        for ball in self.engine.balls:
            ball.gravity = self.gravity

    def update(self, dt):
        self.engine.update(dt)
        for ball in self.engine.balls:
            if ball.position[1] > self.height:
                self.engine.balls.remove(ball)
