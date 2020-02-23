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
pink = (255, 105, 180)


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

    def cast(self, wall_q):         # relies on enemy class for creating a wall queue
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
