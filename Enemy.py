import pygame
import random
from pygame.locals import *
import time
import Ray
import Grid
import Button
import Stack
import heapq

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


class Enemy:
    def __init__(self, id, sprite, size, difficulty, location, breed, health=10):
        self.ID = id
        self.health = health
        self.breed = breed
        self.location = location
        self.difficulty = difficulty
        self.sprite = pygame.image.load(sprite)
        self.rays = []
        self.size = size
        self.direction = random.randint(0, 3)

    def create_heap(self, walls, raysize):
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
            if shortest_distance <= self.size * (raysize + 1.5):
                heapq.heappush(wall_q, (shortest_distance, wall))
        return wall_q

    def create_rays(self, walls):
        self.rays = []
        raysize = 10
        wall_q = self.create_heap(walls, raysize)
        qty = 1
        if self.difficulty == 1:
            fov = 30
            start_angle = (self.direction * 90) - (fov/2)
            for angle in range(0, int(fov)*qty):
                ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (raysize + 0.5), angle/qty + start_angle)
                ray.cast(wall_q)
                self.rays.append(ray)

    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.location)

    def draw_rays(self, window):
        for ray in self.rays:
            pygame.draw.aaline(window, blue, ray.start, ray.end)
