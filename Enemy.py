import pygame
import random
from pygame.locals import *
import time
import Ray
import Grid
import Button
import Stack
import heapq
import numpy
import math

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


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def find_angle_given_coordinates(coordinate1, coordinate2):
    x_difference = coordinate2[0] - coordinate1[0]
    y_difference = coordinate2[1] - coordinate1[1]
    angle = None
    if x_difference != 0 and y_difference != 0:
        angle = math.degrees(numpy.arctan(abs(y_difference/x_difference)))
        if x_difference > 0 and y_difference > 0:
            angle += 90
        elif x_difference < 0 and y_difference > 0:
            angle = 270 - angle
        elif x_difference < 0 and y_difference < 0:
            angle += 270
        elif x_difference > 0 and y_difference < 0:
            angle = 90 - angle
    if x_difference == 0 and y_difference == 0:
        angle = 90
    elif x_difference == 0:
        if y_difference > 0:
            angle = 180
        else:
            angle = 0
    elif y_difference == 0:
        if x_difference > 0:
            angle = 90
        else:
            angle = 270
    return angle



class Enemy:
    def __init__(self, id, sprite, size, difficulty, location, breed, health=10):
        self.ID = id
        self.state = "searching"
        self.health = health
        self.breed = breed
        self.location = location
        self.difficulty = difficulty
        self.sprite = pygame.image.load(sprite)
        self.steps = 10
        self.rays = []
        self.size = size
        self.direction = random.randint(0, 3)  #
        self.fov = 30

    def create_heap(self, walls):
        wall_q = []
        heapq.heapify(wall_q)
        for wall in walls:
            x1 = wall[0][0]
            y1 = wall[0][1]
            x2 = wall[1][0]
            y2 = wall[1][1]
            x3 = self.location[0] + self.size / 2
            y3 = self.location[1] + self.size / 2
            # check if wall is even worth calculating (this is an efficiency improvement)
            shortest_distance = abs((y2 - y1) * x3 - (x2 - x1) * y3 + x2 * y1 - y2 * x1) / (((y2 - y1) ** 2) + ((x2 - x1) ** 2)) ** (1 / 2.0)
            if shortest_distance <= self.size * (self.steps + 1.5):
                heapq.heappush(wall_q, (shortest_distance, wall))
        return wall_q

    def find_player(self, player, walls, locations, grid):
        ray = ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (self.steps + 0.5), 0)
        ray.end = (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2)
        wall_q = self.create_heap(walls)
        ray.cast(wall_q)
        if ray.end != (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2):
            self.state = "searching"
        else:
            angle = find_angle_given_coordinates(ray.start, ray.end)
            lower = (self.direction * 90 - self.fov/2)     # lower bound
            if lower < 0:
                lower = 360 - lower
            upper = (self.direction * 90 + self.fov/2)
            if upper > 359:
                upper = upper - 360
            if lower <= angle <= upper:
                self.state = "alert"

    def create_rays(self, walls):
        self.rays = []
        wall_q = self.create_heap(walls)
        qty = 1
        if self.difficulty == 1:
            start_angle = (self.direction * 90) - (self.fov/2)
            for angle in range(0, int(self.fov)*qty):
                ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (self.steps + 0.5), angle/qty + start_angle)
                ray.cast(wall_q)
                self.rays.append(ray)

    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.location)

    def draw_rays(self, window):
        for ray in self.rays:
            pygame.draw.aaline(window, blue, ray.start, ray.end)
