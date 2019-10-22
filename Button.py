import pygame
from pygame.locals import *

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


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text, centre, win):
    large_text = pygame.font.Font("freesansbold.ttf", int((win.get_size()[0])*(1/20)))
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = centre
    win.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, width, height, colour, border, text=""):
        self.x = x
        self.y = y
        self.border = border
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text

    def draw_button(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        message_display(self.text, (self.x + int(self.width / 2), self.y + int(self.height / 2)), win)

    def check_on_button(self):
        current_pos = pygame.mouse.get_pos()
        if (self.x <= current_pos[0] <= self.x + self.width) and (self.y <= current_pos[1] <= self.y + self.height):
            self.colour = lightgreen
            return True
        else:
            self.colour = whitegreen
            return False

    def check_clicked(self):
        on_button = self.check_on_button()
        if on_button:
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                self.colour = green
                return True
        return False
