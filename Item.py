import pygame

darkred = (139, 0, 0)
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


# item class that stores the values positions sprites and types of item
class Item:
    def __init__(self, sprite, size, position, location, value=50, kind="loot"):
        self.sprite = pygame.image.load(sprite)
        self.value = value
        self.position = position
        self.size = size
        self.location = location
        self.type = kind

    # used to draw item to the screen
    def draw(self, window):
        self.sprite = pygame.transform.scale(self.sprite, (int(self.size), int(self.size)))
        window.blit(self.sprite, self.location)
