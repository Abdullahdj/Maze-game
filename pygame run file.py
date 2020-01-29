import pygame
from pygame.locals import *
import time
import random
import Grid
import Player
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
pink = (255, 105, 180)


def Reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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
        square_width = (height / grid.width)
        draw_point = (width - (square_width * grid.width)) / 2
        for x in range(0, grid.width):
            for y in range(0, grid.width):
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


def draw_back(grid, win):
    width, height = win.get_size()
    if width >= height:
        square_width = (height / grid.width)
        draw_point = (width - (square_width * grid.width)) / 2
        pygame.draw.rect(win, pink, (draw_point, 0, height, height))


def draw_grid(grid, win):
    width, height = win.get_size()
    if width >= height:
        square_width = (height / grid.width)
        draw_point = (width - (square_width * grid.width))/2
        line_width = 1
        for x in range(0, grid.width):
            for y in range(0, grid.width):
                top_right_x = (draw_point + (x * square_width))
                top_right_y = square_width * y
                if grid.maze[y][x][0] == 1:
                    pygame.draw.line(win, black, (top_right_x, top_right_y), (top_right_x + square_width, top_right_y), line_width)
                if grid.maze[y][x][1] == 1:
                    pygame.draw.line(win, black, (top_right_x, top_right_y), (top_right_x, top_right_y + square_width), line_width)
                if grid.maze[y][x][2] == 1:
                    pygame.draw.line(win, black, (top_right_x, top_right_y + square_width), (top_right_x + square_width, top_right_y + square_width), line_width)
                if grid.maze[y][x][3] == 1:
                    pygame.draw.line(win, black, (top_right_x + square_width, top_right_y), (top_right_x + square_width, top_right_y + square_width), line_width)


def draw_enemies(enemies, window):
    for enemy in enemies:
        draw_rays(enemy[0], window)
    for enemy in enemies:
        draw_enemy(enemy[0], window)


def create_enemy(walls, difficulty, locations, square_width, grid, window):
    enemies = []
    used_spots = [None]
    y = None
    if difficulty == 1:
        for ID in range(0, 1):
            while y in used_spots:
                y = random.randint(0, (grid.width ** 2 - 1))
            used_spots.append(y)
            location = locations[y]
            enemy = Enemy.Enemy(ID, "sprites/blob.png", int(square_width), difficulty, location, "monkey")
            enemy.create_rays(walls)
            enemies.append((enemy, y))
    return enemies


def draw_enemy(enemy, window):
    enemy.draw(window)


def Coordinates(square_width, locations):
    mouse_pos = pygame.mouse.get_pos()
    block = None
    index = None
    for i, location in enumerate(locations):
        if (location[0] <= mouse_pos[0] < location[0] + square_width) and (
                location[1] <= mouse_pos[1] < location[1] + square_width):
            block = location
            index = i
            break
    return block, index


def draw_to_mouse(grid, locations, square_width, win, prev_position, player):

    block, index = Coordinates(square_width, locations)

    if block and grid.positions[index] != prev_position:
        global path
        path = grid.PathFinding(player.location, grid.positions[index])
        draw_path(grid, path, locations, square_width, player.location, win)
    if index is not None:
        return grid.positions[index]
    else:
        return None


def draw_path(grid, path, locations, square_width, player, win):
    for i, node in enumerate(path[0]):
        location1 = locations[grid.positions.index(node)]
        try:
            location2 = locations[grid.positions.index(path[0][i+1])]
            pygame.draw.line(win, red, ((location1[0] + square_width/2), (location1[1] + square_width/2)), ((location2[0] + square_width/2), (location2[1] + square_width/2)), 3)
        except IndexError:
            break


def create_player(grid, enemies, square_width):
    unvisitable = []
    for enemy in enemies:
        unvisitable.append(enemy[0].location)
    while True:
        location = random.choice(grid.positions)
        if location not in unvisitable:
            break

    player = Player.Player("sprites/player.png", square_width, location)
    return player


def draw_player(grid, locations, player, win):
    player.draw(locations[grid.positions.index(Reverse(player.location))], win)


def draw_rays(enemy, window):
    enemy.draw_rays(window)


def game_loop(win, difficulty=1, savefile=""):
    global grid
    if difficulty == 1:
        grid = Grid.Grid(20)
        grid.CreateMaze()
        grid.CreateMatrix()
    run = True
    win.fill(purple)
    locations, walls, square_width = collect_locations(win, grid)
    draw_back(grid, win)
    enemies = create_enemy(walls, difficulty, locations, square_width, grid, win)
    player = create_player(grid, enemies, square_width)
    draw_grid(grid, win)
    mouse_position = None

    while run:

        if pygame.mouse.get_rel() != (0, 0):
            block, index = Coordinates(square_width, locations)
            if block and grid.positions[index] != mouse_position:
                draw_back(grid, win)
                draw_grid(grid, win)
            mouse_position = draw_to_mouse(grid, locations, square_width, win, mouse_position, player)
        draw_player(grid, locations, player, win)
        draw_enemies(enemies, win)
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
            quit.draw_button(win)
            options.draw_button(win)
            pygame.display.update()
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
            pygame.display.update()
            run = False
    return run


running = True
running = menu(running)
pygame.quit()
