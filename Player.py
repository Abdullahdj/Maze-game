import pygame

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
    def __init__(self, sprite, size, location, steps=10, health=10):            # default values for health and steps are overwritten usually in code
        self.max_health = health
        self.health = health
        self.collected_items = []
        self.location = location                        # in x,y coordinate format when represented graphically
        self.sprite = pygame.image.load(sprite)
        self.size = size
        self.steps = steps

    # checks if the player is on the same location as loot and picks up the items and stores them in collected_items
    def check_for_items(self, items):
        remove = []
        for item in items:
            if self.location == Reverse(item.position):       # there is a special case in python that means that removing an
                remove.append(item)                           # item from a list whilst iterating through causes the next item to be skipped
        for item in remove:
            self.collected_items.append(item)
            items.remove(item)

    # calculates the players score by basing it off the players health and the items that the player has in their collected_items
    # each item has a value attribute which is added to the total score and the score is returned
    def calculate_score(self):
        score = int(self.health/self.max_health * 500)
        for item in self.collected_items:
            score += item.value
        return score

    # checks if the player is on the exit and also has the key in their collected_items
    def check_if_exit(self, exit):
        key_found = False
        for item in self.collected_items:
            if item.type == "key":
                key_found = True
        if self.location == exit[1] and key_found:
            return True
        else:
            return False

    # reduces the players health by the damage dealt (by an enemy)
    def lose_health(self, damage):
        self.health -= damage

    # draws the player onto the screen using its coordinates and converting them into pixel coordinates and drawing those onto the screen
    def draw(self, pixel_location, window):
        self.sprite = pygame.transform.scale(self.sprite, (int(self.size), int(self.size)))
        window.blit(self.sprite, pixel_location)
        pygame.draw.circle(window, green, (int(pixel_location[0] + 1/2*self.size), int(pixel_location[1] + 1/2*self.size)), 3, 3)   # This is the part of you the enemy can see (green circle look closely)
