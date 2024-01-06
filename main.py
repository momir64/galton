from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from board import Board
from constants import *
import pygame.freetype
import pygame_widgets
import pygame
import sys

BOARD_X = 450
BOARD_Y = 40
BOARD_WIDTH = 510
BOARD_HEIGHT = 720
BALL_NUMBER = 17  # 134
BALL_RADIUS = 7  # 6
BALL_MASS = 1
PEG_RADIUS = 5
BIN_NUMBER = 10
RESTITUTION = 0.5
GRAVITY = 9.81


def start():
    global board, update
    BALL_RADIUS = ballRadiusSlider.getValue()
    BALL_NUMBER = ballNumberSlider.getValue()
    PEG_RADIUS = pegRadiusSlider.getValue()
    BIN_NUMBER = binNumberSlider.getValue()
    RESTITUTION = restitutionSlider.getValue()
    GRAVITY = gravitySlider.getValue()
    update = True
    board = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, BALL_MASS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY)


pygame.init()
pygame.display.set_caption("Galtonova daska")
screen = pygame.display.set_mode((1000, 800))
font1 = pygame.font.Font("roboto_mono.ttf", 24)
font2 = pygame.freetype.Font("roboto_mono.ttf", 16)
pygame.display.set_icon(pygame.image.load("icon.png"))

text1, textRect1 = font2.render("Broj kuglica", WHITE, GRAY1)
text2, textRect2 = font2.render("Veličina kuglica", WHITE, GRAY1)
text3, textRect3 = font2.render("Veličina klinova", WHITE, GRAY1)
text4, textRect4 = font2.render("Broj pregrada", WHITE, GRAY1)
text5, textRect5 = font2.render("Gravitaciona konstanta", WHITE, GRAY1)
text6, textRect6 = font2.render("Koeficijent restitucije", WHITE, GRAY1)
textRect1.center = (225, 70)
textRect2.center = (225, 170)
textRect3.center = (225, 270)
textRect4.center = (225, 370)
textRect5.center = (225, 470)
textRect6.center = (225, 570)

ballNumberSlider = Slider(screen, 60, 100, 330, 12, min=1, max=450, initial=17, colour=GRAY3, handleColour=GRAY4)
ballRadiusSlider = Slider(screen, 60, 200, 330, 12, min=3, max=19, initial=7, colour=GRAY3, handleColour=GRAY4)
pegRadiusSlider = Slider(screen, 60, 300, 330, 12, min=3, max=19, initial=5, colour=GRAY3, handleColour=GRAY4)
binNumberSlider = Slider(screen, 60, 400, 330, 12, min=3, max=16, initial=10, colour=GRAY3, handleColour=GRAY4)
gravitySlider = Slider(screen, 60, 500, 330, 12, min=0.1, max=50, initial=9.81, step=0.01, colour=GRAY3, handleColour=GRAY4)
restitutionSlider = Slider(screen, 60, 600, 330, 12, min=0, max=1, initial=0.5, step=0.01, colour=GRAY3, handleColour=GRAY4)

update = False
t0 = pygame.time.get_ticks()
board = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, BALL_MASS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY)
button = Button(screen, 60, 690, 330, 70, text="Pokreni", inactiveColour=GRAY2, hoverColour=GRAY3, pressedColour=GRAY3, textColour=WHITE, font=font1, onClick=start)

while True:
    screen.fill(GRAY1)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)
    screen.blit(text5, textRect5)
    screen.blit(text6, textRect6)
    events = pygame.event.get()
    t = pygame.time.get_ticks()
    t0, dt = t, (t - t0) / 1000.0
    pygame_widgets.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if BALL_NUMBER != ballNumberSlider.getValue() or BALL_RADIUS != ballRadiusSlider.getValue() or PEG_RADIUS != pegRadiusSlider.getValue() or BIN_NUMBER != binNumberSlider.getValue():
        BALL_RADIUS = ballRadiusSlider.getValue()
        BALL_NUMBER = ballNumberSlider.getValue()
        PEG_RADIUS = pegRadiusSlider.getValue()
        BIN_NUMBER = binNumberSlider.getValue()
        binNumberSlider.max = min(16, (BOARD_WIDTH - 2 * BORDER) // (BALL_RADIUS * 3))
        binNumberSlider.setValue(min(binNumberSlider.max, BIN_NUMBER))
        ballNumberSlider.max = min(450, (BOARD_WIDTH - 2 * BORDER) // (BALL_RADIUS * 2 + BALL_GAP) * (BALL_END) // (BALL_RADIUS * 2 + BALL_GAP) + (10 if BALL_RADIUS == 3 else 0))
        ballNumberSlider.setValue(min(ballNumberSlider.max, BALL_NUMBER))
        board = Board(screen, BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT, BALL_NUMBER, BALL_RADIUS, BALL_MASS, PEG_RADIUS, BIN_NUMBER, RESTITUTION, GRAVITY)
        update = False

    if RESTITUTION != restitutionSlider.getValue() or GRAVITY != gravitySlider.getValue():
        RESTITUTION = restitutionSlider.getValue()
        GRAVITY = gravitySlider.getValue()
        board.update_gravity(GRAVITY)
        board.update_restitution(RESTITUTION)

    if update:
        board.update(0.01)
    board.print()

    pygame.display.update()
