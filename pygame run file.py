import pygame
from pygame.locals import *
import threading
import time
import random
import Grid
import Player
import Button
import Stack
import Enemy
import Item
import math
import sys
pygame.init()

clock = pygame.time.Clock()

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


def check_events(run):
    press = False
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                press = True
    return run, press


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
        line_width = 3
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


def create_enemy(walls, difficulty, locations, square_width, grid):
    enemies = []
    used_spots = [None]
    y = None
    if difficulty == 1:
        for ID in range(0, 1):
            while y in used_spots:
                y = random.randint(0, (grid.width ** 2 - 1))
            used_spots.append(y)
            location = locations[y]
            position = grid.positions[locations.index(location)]
            enemy = Enemy.Enemy(ID, "sprites/blob.png", int(square_width), difficulty, location, position, "monkey")
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


# ASSTIT FUCER
def draw_to_mouse(grid, block, index, locations, square_width, win, prev_position, player):
    path = None
    if block and grid.positions[index] != prev_position:
        path = get_path(grid, index, player)
        draw_path(grid, path, locations, square_width, win)
    if index is not None:
        return grid.positions[index], path
    else:
        return None, path


def get_path(grid, index, player):
    path = grid.PathFinding(player.location, grid.positions[index])
    restricted_path = [path[0][0]]
    remaining_steps = player.steps
    for index, location in enumerate(path[0]):
        if index != 0:
            weight = grid.matrix[grid.GetMatrixIndex(Reverse(path[0][index - 1]))][grid.GetMatrixIndex(Reverse(location))]
            if remaining_steps - weight >= 0:
                remaining_steps -= weight
                restricted_path.append(location)
    return restricted_path, (player.steps - remaining_steps)


def draw_path(grid, path, locations, square_width, win):
    for i, node in enumerate(path[0]):
        location1 = locations[grid.positions.index(node)]
        try:
            location2 = locations[grid.positions.index(path[0][i+1])]
            pygame.draw.line(win, red, ((location1[0] + square_width/2), (location1[1] + square_width/2)), ((location2[0] + square_width/2), (location2[1] + square_width/2)), 3)
        except IndexError:
            break


def create_player(grid, locations, enemies, square_width):
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


def animate_player(items, grid, locations, player, path, speed, enemies, win):
    for index, next_position in enumerate(path[0]):
        pixel_location = locations[grid.positions.index(player.location)]
        next_pixel_location = locations[grid.positions.index(next_position)]
        if pixel_location[0] == next_pixel_location[0]:
            distance = -(pixel_location[1] - next_pixel_location[1])
            direction = "y"
        else:
            distance = -(pixel_location[0] - next_pixel_location[0])
            direction = "x"

        for x in range(0, speed):
            if direction == "y" and index != 0:
                pixel_location = (pixel_location[0], pixel_location[1] + distance/speed)
                win.fill(green)
                draw_back(grid, win)
                draw_grid(grid, win)
                display_player_health(player, win)
                display_score(player, win)
                draw_items(items, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
            if direction == "x" and index != 0:
                pixel_location = (pixel_location[0] + distance/speed, pixel_location[1])
                win.fill(green)
                draw_back(grid, win)
                draw_grid(grid, win)
                display_player_health(player, win)
                display_score(player, win)
                draw_items(items, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
            pygame.mouse.get_pressed()
        player.location = next_position
        player.check_for_items(items)
        clock.tick(60)
        pygame.display.update()
        win.fill(green)
        draw_back(grid, win)
        draw_grid(grid, win)
        display_player_health(player, win)
        display_score(player, win)
        draw_items(items, win)
    player.location = Reverse(player.location)


# ok it works
def animate_enemies(items, grid, walls, locations, enemies, path, speed, player, win):
    for enemy, ID in enemies:
        for index, location in enumerate(path[enemy]):
            new_pixel_location = locations[grid.positions.index(location)]
            if enemy.location[0] == new_pixel_location[0]:
                distance = -(enemy.location[1] - new_pixel_location[1])
                direction = "y"
            else:
                distance = - (enemy.location[0] - new_pixel_location[0])
                direction = "x"

            for x in range(0, speed):
                if direction == "x" and index != 0:
                    enemy.location = (enemy.location[0] + distance/speed, enemy.location[1])
                    enemy.player_remembered()
                    if distance > 0:
                        enemy.direction = 1
                    else:
                        enemy.direction = 3
                    draw_back(grid, win)
                    display_player_health(player, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    enemy.draw(win)
                    draw_enemies(enemies, win)
                    draw_grid(grid, win)
                    draw_items(items, win)
                    pygame.display.update()
                    clock.tick(60)
                if direction == "y" and index != 0:
                    enemy.location = (enemy.location[0], enemy.location[1] + distance/speed)
                    enemy.player_remembered()
                    if distance > 0:
                        enemy.direction = 0
                    else:
                        enemy.direction = 2
                    draw_back(grid, win)
                    display_player_health(player, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    draw_enemies(enemies, win)
                    enemy.draw(win)
                    draw_grid(grid, win)
                    draw_items(items, win)
                    pygame.display.update()
                    clock.tick(60)
                pygame.mouse.get_pressed()
            enemy.location = new_pixel_location[:]
            enemy.player_remembered()


# remember last location that the player was spotted in (will move towards you for one turn after being spotted)
def move_enemies(grid, locations, enemies, walls, player):
    paths = {}               # dictionary storing the enemy along with the path it takes in order to animate
    for enemy in enemies:
        path = [enemy[0].position]
        steps = enemy[0].steps
        while steps > 0:
            new_position = None
            direction = None
            while enemy[0].state == "searching" and steps > 0 and enemy[0].last_known_location == None:                 # check if there is a last known location
                direction = random.randint(0, 3)
                if direction == 0:
                    new_position = (enemy[0].position[0], enemy[0].position[1] + 1)
                elif direction == 1:
                    new_position = (enemy[0].position[0] + 1, enemy[0].position[1])
                elif direction == 2:
                    new_position = (enemy[0].position[0], enemy[0].position[1] - 1)
                else:   # direction == 3
                    new_position = (enemy[0].position[0] - 1, enemy[0].position[1])

                if type(grid.GetMatrixIndex(Reverse(new_position))) == int:
                    weight = grid.matrix[grid.GetMatrixIndex(Reverse(new_position))][grid.GetMatrixIndex(Reverse(enemy[0].position))]
                    if weight != float("inf") and steps >= weight:
                        enemy[0].position = new_position
                        enemy[0].direction = direction
                        enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                        enemy[0].player_remembered()
                        path.append(new_position)
                        steps -= weight
                        enemy[0].find_player(player, walls, locations, grid)
                    else:
                        "unvisitable"
                else:
                    "out of map"

            if (enemy[0].state == "alert" and steps > 0) or enemy[0].last_known_location != None:
                if enemy[0].location == locations[grid.positions.index(Reverse(player.location))]:
                    break
                path_to_player, weight = grid.PathFinding(Reverse(enemy[0].position), Reverse(player.location))
                if weight <= steps:
                    for index, location in enumerate(path_to_player):
                        if index != 0:
                            path.append(location)
                            enemy[0].position = location
                            enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                            enemy[0].player_remembered()
                            steps -= 1
                else:
                    for location in path_to_player:
                        if steps + 1 > 0:
                            steps -= 1
                            path.append(location)
                            enemy[0].position = location
                            enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                            enemy[0].player_remembered()
        paths[enemy[0]] = path
        enemy[0].position = path[0]
        enemy[0].location = locations[grid.positions.index(enemy[0].position)]

    return paths
#  wherever there is steps -= 1 change to matrix weightings

def display_player_health(player, win):
    width, height = pygame.display.get_surface().get_size()
    message_display(("Health: " + str(player.health)), (width*15/192, height*5/108), win)


def gridMake(amount,gridList):
    grid = Grid.Grid(amount)
    gridList[0] = grid


def create_items(number_of_items, square_width, grid, locations):
    # also create a key separately
    items = []
    for x in range(0, number_of_items):
        sprite = random.choice(["sprites/pile_o_coins.png", "sprites/chest_o_coins.png", "sprites/ruby.png"])
        index = random.randint(0, (grid.width**2)-1)
        position = grid.positions[index]
        location = locations[grid.positions.index(Reverse(position))]
        item = Item.Item(sprite, square_width, position, location)
        items.append(item)
    return items


def draw_items(items, win):
    for item in items:
        item.draw(win)


def game_loop(win, difficulty=1, savefile=""):
    global grid
    if difficulty == 1:
        gridList = [0]
        mainThread =threading.Thread(target=gridMake,
                                     args=(10, gridList))
        mainThread.start()
        grid = gridList[0]
        grid.CreateMaze()
        grid.CreateMatrix()
    run = True
    win.fill(green)
    locations, walls, square_width = collect_locations(win, grid)
    draw_back(grid, win)
    enemies = create_enemy(walls, difficulty, locations, square_width, grid)

    checker = 1
    while checker != 0:
        player = create_player(grid, locations, enemies, square_width)
        counter = 0
        for enemy in enemies:                     # This block of code prevents player from being in the same position as enemy by checking if enemy sees them and reinitialising if they can
            enemy[0].find_player(player, walls, locations, grid)
            enemy[0].last_known_location = None
            if enemy[0].state == "alert":
                counter += 1
        checker = counter

    items = create_items(grid.width, square_width, grid, locations)

    draw_grid(grid, win)
    draw_items(items, win)
    mouse_position = None
    pressed = False
    turn = "player"
    path = [[player.location], 0]

    while run:
        display_player_health(player, win)
        if pygame.mouse.get_rel() != (0, 0):
            block, index = Coordinates(square_width, locations)
            if block and grid.positions[index] != mouse_position:    # if statements are here so that the dijkstra is only run when the cursor changes block for efficiency
                draw_back(grid, win)
                draw_grid(grid, win)
                draw_items(items, win)
            mouse_position, temp = draw_to_mouse(grid, block, index, locations, square_width, win, mouse_position, player)
            if temp != None:
                path = temp

        if pressed and turn == "player":
            block, index = Coordinates(square_width, locations)
            if index is not None:
                path = get_path(grid, index, player)
                animate_player(items, grid, locations, player, path, 8, enemies, win)
                turn = "enemy"

        elif turn == "enemy":
            if index is not None:
                path = get_path(grid, index, player)
            enemy_paths = move_enemies(grid, locations, enemies, walls, player)
            pygame.time.wait(150)
            animate_enemies(items, grid, walls, locations, enemies, enemy_paths, 4, player, win)
            draw_back(grid, win)
            for enemy in enemies:
                enemy[0].create_rays(walls)
                enemy[0].position = enemy_paths[enemy[0]][-1]
                enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                enemy[0].check_if_player_hit(player, locations, grid)              # checks if by the end of the movement the enemy has hit the player if this is true then the player will lose health
            enemy_paths = None
            draw_enemies(enemies, win)
            draw_grid(grid, win)
            draw_items(items, win)

            turn = "player"
            # move enemy

        for enemy in enemies:
            enemy[0].find_player(player, walls, locations, grid)

        draw_player(grid, locations, player, win)
        draw_enemies(enemies, win)
        pygame.display.update()
        if player.health <= 0:
            game_over_screen(50, win)
            run = False
        clock.tick(144)
        win.fill(green)
        draw_back(grid, win)
        draw_grid(grid, win)
        draw_items(items, win)
        draw_path(grid, path, locations, square_width, win)
        run, pressed = check_events(run)
        display_score(player, win)


def display_score(player, win):
    width, height = pygame.display.get_surface().get_size()
    score = player.calculate_score()
    message_display(("Score:" + str(score)), (width*15/192, height*20/108), win)


def game_over_screen(player, win):
    width, height = pygame.display.get_surface().get_size()
    time = pygame.time.get_ticks()
    red_val = 0
    while pygame.time.get_ticks() - time < 9000:
        win.fill((int(red_val), 0, 0))
        message_display("YOU LOSE", (int(width/2) - int(width/50), int(height/2) - int(height/50)), win)
        red_val = (red_val + 0.2) % 255
        pygame.display.update()



def menu(run):
    win, width, height = alter_window(9/16)
    # buttons all in terms of height and width of screen
    quit = Button.Button(int(width/20), height*(12/15), int(width/3), int(height/10), white, black, "Quit")
    play = Button.Button(int(width/20), int(height*(8/15)), int(width/3), int(height/10), white, black, "Play")
    options = Button.Button(int(width/20), int(height*(10/15)), int(width/3), int(height/10), white, black, "Options")
    time = pygame.time.get_ticks()
    win.fill(whiteblue)
    background(lightblue, 10, win)

    while run:
        pygame.display.update()
        if (pygame.time.get_ticks() - time) % 2000 < 1000:
            win.fill(whiteblue)
            background(lightblue, 10, win)
        else:
            win.fill(lightblue)
            background(whiteblue, 10, win)
        clock.tick(144)
        run = check_events(run)[0]
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


loading = True
running = True
running = menu(running)
pygame.quit()
