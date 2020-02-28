import pygame
import random
import Ray
import heapq
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


# converts radians to degrees
def to_degree(angle):
    return angle*(180/math.pi)


# calculates the distance between two coordinates
def calculateDistance(coordinate1, coordinate2):
    dist = math.sqrt((coordinate2[0] - coordinate1[0])**2 + (coordinate2[1] - coordinate1[1])**2)
    return dist


# calculates the angle between two coordinates in terms of nwse where south is 0 degrees
# east is 90 degrees
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
    def __init__(self, id, sprite, size, difficulty, location, position, breed, steps, damage=2):
        self.ID = id
        self.state = "searching"
        self.damage = damage
        self.breed = breed
        self.location = location            # location in pixels
        self.position = position            # position in coordinates
        self.difficulty = difficulty
        self.sprite = pygame.image.load(sprite)
        self.last_known_location = None             # last known player location in pixels
        self.steps = steps
        self.ray_size = 10
        self.rays = []
        self.size = size
        self.direction = random.randint(0, 3)
        self.fov = 60

    # creates a heap of walls ordered by the distance from the player
    # this heap is used to calculate ray intersections because if the rays are calculated against the closest walls first
    # then as soon as an intersection is found the code breaks out of calculating intersections
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
            # check if wall is even worth calculating (this is an efficiency improvement) (checks if distance is within the ray length of enemy)
            shortest_distance = abs((y2 - y1) * x3 - (x2 - x1) * y3 + x2 * y1 - y2 * x1) / (((y2 - y1) ** 2) + ((x2 - x1) ** 2)) ** (1 / 2.0)
            if shortest_distance <= self.size * (self.ray_size + 1.5):
                heapq.heappush(wall_q, (shortest_distance, wall))
        return wall_q

    # draws a ray from the enemy to the player and calculates whether or not that ray hits walls in between reaching the player
    # also checks if the ray is within the enemies field of view in the direction the enemy is facing
    # it should be noted that the player is only spotted if the centre of the player is visible to the enemy
    def find_player(self, player, walls, locations, grid):
        if locations[grid.positions.index(Reverse(player.location))] == self.location:  # if player is in the same location as the player
            self.state = "alert"
            self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
            self.player_remembered()
            return  # breaks out of code for efficiency

        # creates the ray up to the player
        ray = Ray.Ray((self.location[0] + self.size/2, self.location[1] + self.size/2), self.size * (self.ray_size + 0.5), 0)
        ray.end = (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2)
        distance = calculateDistance(ray.start, ray.end)    # calculates the distance to the player

        if distance > self.size * (self.ray_size + 0.5):    # if the player is too far away for the ray to reach then the enemies state is set to searching
            self.state = "searching"
            return  # breaks out of code for efficiency

        # creates the heap of walls and casts the ray onto the walls to find the closest intersection (this changes the rays end point)
        wall_q = self.create_heap(walls)
        ray.cast(wall_q)
        # if the ray end point is no longer the players position then the ray doesn't reach the player so the player isn't detected
        if ray.end != (locations[grid.positions.index(Reverse(player.location))][0] + self.size/2, locations[grid.positions.index(Reverse(player.location))][1] + self.size/2):
            self.state = "searching"
            return        # breaks out of code for efficiency

        # here the player is visible to the enemy but the enemy may not be facing the player so now we are calculating
        # the angle to the player from the enemy
        else:
            angle = find_angle_given_coordinates(ray.start, ray.end)   # calculates angle between player and enemy

            # if the field of view is greater than 360 then the player is definately visible
            if self.fov >= 360:
                self.state = "alert"
                self.last_known_location = locations[grid.positions.index(Reverse(player.location))]
                self.player_remembered()    # adds the players location to last_known_location so player is still
                                            # being tracked when enemy no longer sees player

            # all of this is checking to see if the enemy is facing the player and the player is within the field of view
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

    # creates the enemies rays with a start point from the player and end point radiating around the field of view
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

    # checks if enemy is on the players last seen location
    # if the enemy is on the location then the last_known_location is set to None
    # this prompts the enemy to move randomly
    def player_remembered(self):
        if self.last_known_location is not None:
            if self.location == self.last_known_location:
                self.last_known_location = None

    # checks if the enemy is on the player and if so deals damage to the player
    def check_if_player_hit(self, player, locations, grid):
        if self.location == locations[grid.positions.index(Reverse(player.location))]:
            player.lose_health(self.damage)

    # draws the enemy onto the window (screen)
    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.location)

    # draws rays onto the screen
    def draw_rays(self, window):
        for ray in self.rays:
            if self.state == "alert":
                pygame.draw.aaline(window, red, ray.start, ray.end)
            elif self.last_known_location != None:      # colour of rays is made orange if the enemy spotted you but can't see you
                pygame.draw.aaline(window, darkorange, ray.start, ray.end)
            else:
                pygame.draw.aaline(window, blue, ray.start, ray.end)
