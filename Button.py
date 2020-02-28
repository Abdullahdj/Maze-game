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
pink = (255, 105, 180)          # global variables of colour hex values


# creates a text object
def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


# displays text to screen
def message_display(text, centre, win):
    large_text = pygame.font.Font("freesansbold.ttf", int((win.get_size()[0])*(1/20)))
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = centre
    win.blit(text_surface, text_rect)


# this is all my own code and creation since buttons don't exist in pygame
class Button:
    def __init__(self, x, y, width, height, colour, border, text=""):
        self.x = x
        self.y = y
        self.border = border
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text

    # draws button onto the win (screen) in their positions as defined by the attributes
    def draw_button(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        message_display(self.text, (self.x + int(self.width / 2), self.y + int(self.height / 2)), win)

    # checks if the mouse is on top of the button by checking using maths
    # if it is on the button the colour of the button is changed to dark green
    # otherwise it is set to light green
    def check_on_button(self):
        current_pos = pygame.mouse.get_pos()
        if (self.x <= current_pos[0] <= self.x + self.width) and (self.y <= current_pos[1] <= self.y + self.height):
            self.colour = lightgreen
            return True             # true is returned if mouse is on button
        else:
            self.colour = whitegreen
            return False            # false is returned if its not

    # if button is clicked the button colour is changed to a dark shade of green indicating a button press
    # a value true is returned if the mouse is on the button and it is pressed
    # otherwise false is returned
    def check_clicked(self):
        on_button = self.check_on_button()
        if on_button:
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                self.colour = green
                return True
        return False
