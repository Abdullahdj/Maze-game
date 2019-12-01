import pygame
import random
from pygame.locals import *
import time
import Ray
import Grid
import Button
import Stack

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

    def create_rays(self, walls):
        qty = 1
        raysize = 2
        if self.difficulty == 1:
            fov = 360
            start_angle = (self.direction * 90) - (fov/2)
            for angle in range(0, int(fov)*qty+1):
                ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (raysize + 0.5), angle/qty + start_angle)
                ray.cast(walls, raysize)
                self.rays.append(ray)

    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.location)

    def draw_rays(self, window):
        for ray in self.rays:
            pygame.draw.aaline(window, white, ray.start, ray.end)
