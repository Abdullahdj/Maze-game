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


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


class Player:
    def __init__(self, sprite, size, location, steps=10, health=10):
        self.max_health = 10
        self.health = health
        self.collected_items = []
        self.location = location                        # in y,x format when represented graphically
        self.sprite = pygame.image.load(sprite)
        self.size = size
        self.steps = steps

    def check_for_items(self, items):
        remove = []
        for item in items:
            if self.location == Reverse(item.position):            # there is a special case in python that means that removing an item from a list whilst iterating through causes the next item to be skipped
                remove.append(item)
        for item in remove:
            self.collected_items.append(item)
            items.remove(item)


    def calculate_score(self):
        score = int(self.health/self.max_health * 10)
        for item in self.collected_items:
            score += item.value
        return score

    def lose_health(self, damage):
        self.health -= damage

    def draw(self, pixel_location, window):
        self.sprite = pygame.transform.scale(self.sprite, (int(self.size), int(self.size)))
        window.blit(self.sprite, pixel_location)
        pygame.draw.circle(window, green, (int(pixel_location[0] + 1/2*self.size), int(pixel_location[1] + 1/2*self.size)), 3, 3)   # This is the part of you the enemy can see (green circle look closely)
