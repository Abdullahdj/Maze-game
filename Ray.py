import math
import pygame
from pygame.locals import *
import time
import Grid
import Button
import Stack
import Enemy
import PQ
import heapq
import copy

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


def to_rad(angle):
    angle = angle*(math.pi/180)
    return angle


class Ray:
    # angle is in absolute value north being 180 degrees
    def __init__(self, start_pos, length, angle):
        self.length = length
        self.start = start_pos
        self.angle = to_rad(angle)
        self.end = (start_pos[0] + length * (math.sin(self.angle)), start_pos[1] + length * (math.cos(self.angle)))

    def cast(self, wall_q):
        wall_points = {}
        walls = copy.copy(wall_q)
        heapq.heapify(walls)
        for index in range(0, len(walls)):
            try:
                wall = heapq.heappop(walls)[1]
            except IndexError:
                break
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]

            x3 = self.start[0]
            y3 = self.start[1]
            x4 = self.end[0]
            y4 = self.end[1]

            # actually calculate rays if above condition is not met
            den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
            if den != 0:
                t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
                u = - ((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den
                if 0 <= t <= 1 and 0 <= u <= 1:
                    point = ((x1 + t*(x2 - x1)), (y1 + t*(y2 - y1)))
                    wall_points[wall] = [point, ((((self.start[0] - point[0]) ** 2) + ((self.start[1] - point[1]) ** 2)) ** (1 / 2))]  # pythagorean theorem
                else:
                    point = None
                    wall_points[wall] = [point, None]
            else:
                point = None
                wall_points[wall] = [point, None]

        closest = [None, None]
        for wall in wall_points:
            if closest[0] is None:
                closest = wall_points[wall]
            elif (wall_points[wall])[1] is not None:
                if closest[1] > (wall_points[wall])[1]:
                    closest = wall_points[wall]
        if closest[0] is not None:
            self.end = closest[0]
        return closest[0]


"""
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


wall1 = ((400, 200), (500, 750))
wall2 = ((300, 150), (700, 800))
wall3 = ((1800, 900), (800, 30))
walls = [wall1, wall2, wall3]


run = True
win, width, height = alter_window(9/16)
win.fill(white)

while run:
    pygame.display.update()
    clock.tick(144)
    run = check_if_quit(run)
    ray = Ray((1000, 540), 5000, 180)
    ray.end = pygame.mouse.get_pos()
    yo = ray.cast(walls)
    if yo:
        ray.end = yo
        pygame.draw.aaline(win, darkorange, ray.start, ray.end, 50)
    else:
        pygame.draw.aaline(win, blue, ray.start, ray.end, 50)

    pygame.draw.line(win, purple, wall1[0], wall1[1], 10)
    pygame.draw.line(win, purple, wall2[0], wall2[1], 10)
    pygame.draw.line(win, purple, wall3[0], wall3[1], 10)


pygame.quit()
"""