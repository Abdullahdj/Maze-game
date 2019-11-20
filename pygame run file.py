import pygame
from pygame.locals import *
import time
import random
import Grid
import Button
import Stack
import Enemy
pygame.init()

clock = pygame.time.Clock()


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
    large_text = pygame.font.Font("freesansbold.ttf", 50)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = centre
    win.blit(text_surface, text_rect)


def check_if_quit(run):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            return run
    if keys[pygame.K_ESCAPE]:
        run = False
        return run
    return run


def background(colour1, ratio, win):
    x, y = win.get_size()
    radius = int(x/(ratio*2))
    for yratio in range(0, int(y/radius)):
        for xratio in range(0, (ratio + 1)):
            pygame.draw.circle(win, colour1, (int(x*xratio/ratio), 0 + yratio*radius*2), radius)


def alter_window(aspect_ratio):
    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h
    if screen_w * aspect_ratio > screen_h:
        width = int(screen_h / aspect_ratio)
        height = int(screen_h)
    else:
        width = int(screen_w)
        height = int(screen_w * aspect_ratio)
    win = pygame.display.set_mode((width, height), FULLSCREEN)
    pygame.display.set_caption("Dungeon Hunter")
    return win, width, height


def collect_locations(win, grid):
    grid.walls = []
    locations = []
    width, height = win.get_size()
    if width >= height:
        square_width = int(height / grid.width)
        draw_point = (width - (square_width * grid.width)) / 2
        for x in range(0, grid.width):
            for y in range(0, grid.width):
                pygame.draw.rect(win, whiteblue, (draw_point + (x * square_width), square_width*y, square_width, square_width))
                top_right_x = (draw_point + (x * square_width))
                top_right_y = square_width*y
                locations.append((top_right_x, top_right_y))
                if grid.maze[y][x][0] == 1:
                    grid.walls.append([(top_right_x, top_right_y), (top_right_x + square_width, top_right_y)])
                if grid.maze[y][x][1] == 1:
                    grid.walls.append([(top_right_x, top_right_y), (top_right_x, top_right_y + square_width)])
                if grid.maze[y][x][2] == 1:
                    grid.walls.append([(top_right_x, top_right_y + square_width), (top_right_x + square_width, top_right_y + square_width)])
                if grid.maze[y][x][3] == 1:
                    grid.walls.append([(top_right_x + square_width, top_right_y), (top_right_x + square_width, top_right_y + square_width)])
        grid.walls = list(set(map(tuple, grid.walls)))
        return locations, grid.walls, square_width


def draw_grid(grid, win):
    width, height = win.get_size()
    if width >= height:
        square_width = int(height / grid.width)
        draw_point = (width - (square_width * grid.width))/2
        line_width = 5
        for x in range(0, grid.width):
            for y in range(0, grid.width):
                top_right_x = (draw_point + (x * square_width))
                top_right_y = square_width * y
                if grid.maze[y][x][0] == 1:
                    pygame.draw.line(win, darkorange, (top_right_x, top_right_y), (top_right_x + square_width, top_right_y), line_width)
                if grid.maze[y][x][1] == 1:
                    pygame.draw.line(win, darkorange, (top_right_x, top_right_y), (top_right_x, top_right_y + square_width), line_width)
                if grid.maze[y][x][2] == 1:
                    pygame.draw.line(win, darkorange, (top_right_x, top_right_y + square_width), (top_right_x + square_width, top_right_y + square_width), line_width)
                if grid.maze[y][x][3] == 1:
                    pygame.draw.line(win, darkorange, (top_right_x + square_width, top_right_y), (top_right_x + square_width, top_right_y + square_width), line_width)


def create_enemy(walls, difficulty, locations, square_width, window):
    enemies = []
    used_spots = [None]
    y = None
    if difficulty == 1:
        for ID in range(0, 2):
            while y in used_spots:
                y = random.randint(0, (grid.width ** 2 - 1))
            used_spots.append(y)
            location = locations[y]
            enemy = Enemy.Enemy(ID, "sprites/blob.png", square_width, difficulty, location, "monkey")
            enemy.create_rays(walls)
            enemies.append((enemy, y))
        for enemy in enemies:
            draw_rays(enemy[0], window)
        for enemy in enemies:
            draw_enemy(enemy[0], window)
    return enemies


def draw_enemy(enemy, window):
    enemy.draw(window)


def draw_rays(enemy, window):
    enemy.draw_rays(window)


def game_loop(win, difficulty=1, savefile=""):
    global grid
    if difficulty == 1:
        grid = Grid.Grid(10)
        grid.CreateMaze()
    run = True
    win.fill(whitegreen)
    locations, walls, square_width = collect_locations(win, grid)
    enemies = create_enemy(walls, difficulty, locations, square_width, win)
    draw_grid(grid, win)
    while run:
        pygame.display.update()
        clock.tick(144)
        run = check_if_quit(run)


def menu(run):
    win, width, height = alter_window(9/16)
    # buttons all in terms of height and width of screen
    quit = Button.Button(int(width/20), height*(12/15), int(width/3), int(height/10), white, black, "Quit")
    play = Button.Button(int(width/20), int(height*(8/15)), int(width/3), int(height/10), white, black, "Play")
    options = Button.Button(int(width/20), int(height*(10/15)), int(width/3), int(height/10), white, black, "Options")
    while run:
        pygame.display.update()
        win.fill(whiteblue)
        background(lightblue, 10, win)
        clock.tick(144)
        run = check_if_quit(run)
# buttons
        # play
        play.check_on_button()
        play_clicked = play.check_clicked()
        play.draw_button(win)
        if play_clicked:
            game_loop(win)

        # options
        options.check_on_button()
        options_clicked = options.check_clicked()
        options.draw_button(win)

        # quit
        quit.check_on_button()
        quit_clicked = quit.check_clicked()
        quit.draw_button(win)

        # event actors
        if quit_clicked:
            run = False
    return run


running = True
running = menu(running)
pygame.quit()
