import pygame
from pygame.locals import *
import time
import Grid
import Button
import Stack
import Ray
import Enemy
pygame.init()

clock = pygame.time.Clock()

darkorange = (255, 140, 0)
lightgreen = (0, 255, 127)
whitegreen = (0, 255, 200)
black = (0, 0, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
lightblue = (0, 125, 255)
whiteblue = (0, 200, 255)
white = (255, 255, 255)


class Stack:
    def __init__(self):
        self.stack = []

    def isempty(self):
        if len(self.stack) == 0:
            return True
        return False

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.isempty():
            top = self.stack.pop(len(self.stack)-1)
            return top
        else:
            raise IndexError("Stack empty")

    def peek(self):
        return self.stack[len(self.stack) - 1]

    def instack(self, value):
        if value in self.stack:
            return True
        return False

"""
# eat

# eat


# eat


def alter_window(aspect_ratio):
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h
    if screen_w * aspect_ratio > screen_h:
        width = int(screen_h / aspect_ratio)
        height = int(screen_h)
    else:
        width = int(screen_w)
        height = int(screen_w * aspect_ratio)
    win = pygame.display.set_mode((width, height - 100), FULLSCREEN)
    pygame.display.set_caption("I am the gamer")
    return win, width, height


def check_if_quit(run):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            return run
    if keys[pygame.K_ESCAPE]:
        run = False
        return run
    return run


bob = Enemy.Enemy(1, "sprites/blob.png", 1, (500, 900), "snot", "ass")

wall1 = ((400, 200), (500, 750))
wall2 = ((300, 150), (700, 800))
wall3 = ((1800, 900), (800, 30))
walls = [wall1, wall2, wall3]
bob.create_rays(walls)

run = True
win, width, height = alter_window(9/16)
win.fill(white)

while run:
    run = check_if_quit(run)
    bob.draw(win)
    pygame.display.update()
    clock.tick(144)

    for each in bob.rays:
        pygame.draw.aaline(win, darkorange, each.start, each.end, 50)

    pygame.draw.line(win, purple, wall1[0], wall1[1], 3)
    pygame.draw.line(win, purple, wall2[0], wall2[1], 3)
    pygame.draw.line(win, purple, wall3[0], wall3[1], 3)
pygame.quit()
"""