from os import environ

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from multiprocessing import Pool
from circle import Circle
from board import Board
from constants import *
import multiprocessing
import pygame.freetype
import pygame_widgets
import numpy as np
import pygame
import sys

if __name__ == "__main__":
    POOL = Pool(processes=multiprocessing.cpu_count())

    def start():
        global board, update
        BALL_RADIUS, BALL_NUMBER, PEG_RADIUS, BIN_NUMBER = ballRadiusSlider.getValue(), ballNumberSlider.getValue(), pegRadiusSlider.getValue(), binNumberSlider.getValue()
        RESTITUTION, GRAVITY = restitutionSlider.getValue(), gravitySlider.getValue()
        board = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY, POOL)
        if update:
            balls.clear()
        for ball in balls:
            board.add_ball(ball)
        update = True
        # print(f"{BALL_RADIUS}, {BALL_NUMBER}, {PEG_RADIUS}, {BIN_NUMBER}, {RESTITUTION:.2}, {float(GRAVITY):.4}")

    pygame.init()
    pygame.display.set_caption("Galtonova daska")
    screen = pygame.display.set_mode((1000, 800))
    font1 = pygame.font.Font("roboto_mono.ttf", 24)
    font2 = pygame.freetype.Font("roboto_mono.ttf", 16)
    pygame.display.set_icon(pygame.image.load("icon.png"))

    options, titles = ["Broj kuglica", "Veličina kuglica", "Veličina klinova", "Broj pregrada", "Koeficijent gravitacije", "Koeficijent restitucije"], []
    for i, option in enumerate(options):
        titles.append(font2.render(option, WHITE, GRAY1))
        titles[i][1].center = (225, 70 + i * 100)

    ballNumberSlider = Slider(screen, 60, 100, 330, 12, min=1, max=BALL_NUMBER_MAX, initial=BALL_NUMBER, colour=GRAY3, handleColour=GRAY4)
    ballRadiusSlider = Slider(screen, 60, 200, 330, 12, min=5, max=15, initial=BALL_RADIUS, colour=GRAY3, handleColour=GRAY4)
    pegRadiusSlider = Slider(screen, 60, 300, 330, 12, min=4, max=21, initial=PEG_RADIUS, colour=GRAY3, handleColour=GRAY4)
    binNumberSlider = Slider(screen, 60, 400, 330, 12, min=3, max=BIN_NUMBER_MAX, initial=BIN_NUMBER, colour=GRAY3, handleColour=GRAY4)
    gravitySlider = Slider(screen, 60, 500, 330, 12, min=0.1, max=50, initial=GRAVITY, step=0.01, colour=GRAY3, handleColour=GRAY4)
    restitutionSlider = Slider(screen, 60, 600, 330, 12, min=0.15, max=0.6, initial=RESTITUTION, step=0.01, colour=GRAY3, handleColour=GRAY4)
    button = Button(screen, 60, 690, 330, 70, text="Pokreni", inactiveColour=GRAY2, hoverColour=GRAY3, pressedColour=GRAY3, textColour=WHITE, font=font1, onClick=start)
    board, update, balls = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY, POOL), False, []
    t0, dt, dt2 = pygame.time.get_ticks(), 0, 0

    while True:
        screen.fill(GRAY1)
        for title in titles:
            screen.blit(*title)
        events = pygame.event.get()
        pygame_widgets.update(events)
        t = pygame.time.get_ticks()
        dt0 = (t - t0) / 1000.0
        t0, dt, dt2 = t, dt + dt0, dt2 + dt0

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos, margin = np.array(pygame.mouse.get_pos(), float) - np.array([BOARD_X, BOARD_Y]), max(BORDER, BALL_RADIUS)
                is_inside = margin < pos[0] < BOARD_WIDTH - margin and margin < pos[1] < BOARD_HEIGHT - margin

        if pygame.mouse.get_pressed()[0] == True and dt2 >= COOLDOWN and is_inside:
            pos, margin = np.array(pygame.mouse.get_pos(), float) - np.array([BOARD_X, BOARD_Y]), max(BORDER, BALL_RADIUS)
            if margin < pos[0] < BOARD_WIDTH - margin and margin < pos[1] < BOARD_HEIGHT - margin:
                ball, dt2 = Circle(pos, BALL_RADIUS, ORANGE, RESTITUTION, GRAVITY), 0
                board.add_ball(ball)
                balls.append(ball)

        if BALL_NUMBER != ballNumberSlider.getValue() or BALL_RADIUS != ballRadiusSlider.getValue() or PEG_RADIUS != pegRadiusSlider.getValue() or BIN_NUMBER != binNumberSlider.getValue():
            BALL_RADIUS, BALL_NUMBER, PEG_RADIUS, BIN_NUMBER = ballRadiusSlider.getValue(), ballNumberSlider.getValue(), pegRadiusSlider.getValue(), binNumberSlider.getValue()
            BALL_NUMBER_MAX = (BOARD_WIDTH - 2 * BORDER) // (BALL_RADIUS * 2 + BALL_GAP) * (BALL_END) // (BALL_RADIUS * 2 + BALL_GAP)
            BIN_NUMBER_MAX = (BOARD_WIDTH - 4 * BORDER) // (BALL_RADIUS * 4)
            ballNumberSlider.max, binNumberSlider.max = min(450, BALL_NUMBER_MAX), min(16, BIN_NUMBER_MAX)
            ballNumberSlider.setValue(min(ballNumberSlider.max, BALL_NUMBER))
            binNumberSlider.setValue(min(binNumberSlider.max, BIN_NUMBER))
            board, update = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY, POOL), False
            balls.clear()

        if RESTITUTION != restitutionSlider.getValue() or GRAVITY != gravitySlider.getValue():
            RESTITUTION, GRAVITY = restitutionSlider.getValue(), gravitySlider.getValue()
            board.update_restitution(RESTITUTION)
            board.update_gravity(GRAVITY)

        if update and dt >= DT:
            board.update(DT)
            dt = 0

        board.print()
        pygame.display.update()
