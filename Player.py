import pygame
from pygame.locals import *
import time
import random
import Grid
import Button
import Stack
import Enemy

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


class Player:
    def __init__(self, sprite, size, location, steps=5, health=10):
        self.health = health
        self.location = location
        self.sprite = pygame.image.load(sprite)
        self.size = size
        self.steps = steps

    def draw(self, pixel_location, window):
        self.sprite = pygame.transform.scale(self.sprite, (int(self.size), int(self.size)))
        window.blit(self.sprite, pixel_location)
