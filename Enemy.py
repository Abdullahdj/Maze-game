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


def to_degree(angle):
    return angle*(180/math.pi)


def calculateDistance(coordinate1, coordinate2):
    dist = math.sqrt((coordinate2[0] - coordinate1[0])**2 + (coordinate2[1] - coordinate1[1])**2)
    return dist


# broken
def find_angle_given_coordinates(coordinate1, coordinate2):
    if coordinate1 == coordinate2:
        return 0

    if coordinate1[0] == coordinate2[0]:
        if coordinate1[1] < coordinate2[1]:
            return 0
        else:
            return 180
    elif coordinate1[1] == coordinate2[1]:
        if coordinate1[0] < coordinate2[0]:
            return 90
        else:
            return 270
    else:
        x_difference = coordinate2[0] - coordinate1[0]
        y_difference = coordinate2[1] - coordinate1[1]
        angle_x_axis = to_degree(math.atan(abs(y_difference/x_difference)))
        if y_difference > 0:
            if x_difference > 0:
                angle = 90 - angle_x_axis
            else:
                angle = 270 + angle_x_axis
        else:
            if x_difference > 0:
                angle = 90 + angle_x_axis
            else:
                angle = 270 - angle_x_axis
        return angle


class Enemy:
    def __init__(self, id, sprite, size, difficulty, location, position, breed, damage=3, health=10):
        self.ID = id
        self.state = "searching"
        self.damage = damage
        self.health = health
        self.breed = breed
        self.location = location            # location in pixels
        self.position = position
        self.difficulty = difficulty
        self.sprite = pygame.image.load(sprite)
        self.last_known_location = None             # last known player location in pixels
        self.steps = 2
        self.ray_size = 10
        self.rays = []
        self.size = size
        self.direction = random.randint(0, 3)
        self.fov = 60

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
            if shortest_distance <= self.size * (self.ray_size + 1.5):
                heapq.heappush(wall_q, (shortest_distance, wall))
        return wall_q

    def find_player(self, player, walls, locations, grid):
        if locations[grid.positions.index(Reverse(player.location))] == self.location:
            self.state = "alert"
            self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
            self.player_remembered()
            return
        ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (self.ray_size + 0.5), 0)
        ray.end = (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2)
        distance = calculateDistance(ray.start, ray.end)
        if distance > self.size * (self.ray_size + 0.5):
            self.state = "searching"
            return
        wall_q = self.create_heap(walls)
        ray.cast(wall_q)
        if ray.end != (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2):
            self.state = "searching"
            return
        else:
            angle = find_angle_given_coordinates(ray.start, ray.end)   # fov = 30
            if self.fov >= 360:
                self.state = "alert"
                self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                self.player_remembered()
            if self.direction == 0:
                if angle >= (360 - self.fov/2) or angle <= (self.fov/2):
                    self.state = "alert"
                    self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                    self.player_remembered()
                else:
                    self.state = "searching"
            elif self.direction == 1:
                if self.fov/2 >= 90:
                    if angle >= (360 - ((self.fov / 2) - 90)) or angle <= (90 + self.fov / 2):
                        self.state = "alert"
                        self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                        self.player_remembered()
                    else:
                        self.state = "searching"
                else:
                    if 90 - (self.fov / 2) <= angle <= 90 + (self.fov / 2):
                        self.state = "alert"
                        self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                        self.player_remembered()
                    else:
                        self.state = "searching"
            elif self.direction == 2:
                if (180 - self.fov / 2) <= angle <= 180 + (self.fov / 2):
                    self.state = "alert"
                    self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                    self.player_remembered()
                else:
                    self.state = "searching"
            else:
                if self.fov / 2 >= 90:
                    if angle >= 270 - self.fov / 2 or angle <= ((self.fov / 2) - 90):
                        self.state = "alert"
                        self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                        self.player_remembered()
                    else:
                        self.state = "searching"
                else:
                    if (270 - self.fov / 2) <= angle <= 270 + (self.fov / 2):
                        self.state = "alert"
                        self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                        self.player_remembered()
                    else:
                        self.state = "searching"

    def create_rays(self, walls):
        self.rays = []
        wall_q = self.create_heap(walls)
        qty = 1
        if self.difficulty == 1:
            start_angle = (self.direction * 90) - (self.fov/2)
            for angle in range(0, int(self.fov)*qty):
                ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (self.ray_size + 0.5), angle/qty + start_angle)
                ray.cast(wall_q)
                self.rays.append(ray)

    def player_remembered(self):
        if self.last_known_location is not None:
            if self.location == self.last_known_location:
                self.last_known_location = None

    def check_if_player_hit(self, player, locations, grid):
        if self.location == locations[grid.positions.index(Reverse(player.location))]:
            player.lose_health(self.damage)

    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.location)

    def draw_rays(self, window):
        for ray in self.rays:
            if self.state == "alert":
                pygame.draw.aaline(window, red, ray.start, ray.end)
            elif self.last_known_location != None:      # colour of rays is made orange if the enemy spotted you but can't see you
                pygame.draw.aaline(window, darkorange, ray.start, ray.end)
            else:
                pygame.draw.aaline(window, blue, ray.start, ray.end)
