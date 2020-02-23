import pygame
from pygame.locals import *
import time
import random
import Grid
import Player
import Button
import Stack
import Enemy
import sys
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


def draw_to_mouse(grid, locations, square_width, win, prev_position, player):
    block, index = Coordinates(square_width, locations)
    if block and grid.positions[index] != prev_position:
        path = get_path(grid, index, player)
        draw_path(grid, path, locations, square_width, win)
    if index is not None:
        return grid.positions[index]
    else:
        return None


def get_path(grid, index, player):
        path = grid.PathFinding(player.location, grid.positions[index])
        return path


def draw_path(grid, path, locations, square_width, win):
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


def animate_player(grid, locations, player, path, speed, enemies, win):
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
                draw_back(grid, win)
                draw_grid(grid, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
            if direction == "x" and index != 0:
                pixel_location = (pixel_location[0] + distance/speed, pixel_location[1])
                draw_back(grid, win)
                draw_grid(grid, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
        player.location = next_position
        clock.tick(60)
        pygame.display.update()
        draw_back(grid, win)
        draw_grid(grid, win)


# do this differently to player animation  ITS STILL FUCKING BROKEN (fix when you move more than one step)
def animate_enemies(grid, walls, locations, enemies, path, speed, player, win):
    print(path)
    for enemy, ID in enemies:
        for index, location in enumerate(path[enemy]):
            new_pixel_location = locations[grid.positions.index(location)]
            if enemy.location[0] == new_pixel_location[0]:
                distance = -(enemy.location[1] - new_pixel_location[1])
                direction = "y"
            if enemy.location[1] == new_pixel_location[1]:
                distance = - (enemy.location[0] - new_pixel_location[0])
                direction = "x"

            for x in range(0, speed):
                if direction == "x" and index != 0:
                    enemy.location = (enemy.location[0] + distance/speed, enemy.location[1])
                    draw_back(grid, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    enemy.draw(win)
                    draw_grid(grid, win)
                    pygame.display.update()
                    clock.tick(60)
                if direction == "y" and index != 0:
                    enemy.location = (enemy.location[0], enemy.location[1] + distance/speed)
                    draw_back(grid, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    enemy.draw(win)
                    draw_grid(grid, win)
                    pygame.display.update()
                    clock.tick(60)
            enemy.location = new_pixel_location[:]






# works but now you need to animate and then you need to remember last location that the player was spotted in
def move_enemies(grid, locations, enemies, walls, player):
    paths = {}               # dictionary storing the enemy along with the path it takes in order to animate
    for enemy in enemies:
        path = [enemy[0].position]
        steps = enemy[0].steps
        while steps > 0:
            new_position = None
            direction = None
            while enemy[0].state == "searching" and steps > 0:
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
                        path.append(new_position)
                        steps -= weight
                        enemy[0].find_player(player, walls, locations, grid)
                    else:
                        "unvisitable"
                else:
                    "out of map"

            # broken completely

            if enemy[0].state == "alert" and steps > 0:
                if enemy[0].location == locations[grid.positions.index(Reverse(player.location))]:
                    break
                path_to_player, weight = grid.PathFinding(Reverse(enemy[0].position), Reverse(player.location))
                if weight <= steps:
                    for index, location in enumerate(path_to_player):
                        if index != 0:
                            path.append(location)
                            enemy[0].position = location
                            enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                            steps -= 1
                else:
                    for location in path_to_player:
                        if steps + 1 > 0:
                            steps -= 1   # y infinite?!?!!!?!?!??
                            path.append(location)
                            enemy[0].position = location
                            enemy[0].location = locations[grid.positions.index(enemy[0].position)]
        paths[enemy[0]] = path
        enemy[0].position = path[0]
        enemy[0].location = locations[grid.positions.index(enemy[0].position)]
    return paths

#  wherever there is steps -= 1 change to matrix weightings




def game_loop(win, difficulty=1, savefile=""):
    global grid
    if difficulty == 1:
        grid = Grid.Grid(15)
        grid.CreateMaze()
        grid.CreateMatrix()
    run = True
    win.fill(green)
    locations, walls, square_width = collect_locations(win, grid)
    draw_back(grid, win)
    enemies = create_enemy(walls, difficulty, locations, square_width, grid)

    checker = 1
    while checker != 0:
        player = create_player(grid, enemies, square_width)
        counter = 0
        for enemy in enemies:
            enemy[0].find_player(player, walls, locations, grid)
            if enemy[0].state == "alert":
                counter += 1
        checker = counter

    draw_grid(grid, win)
    mouse_position = None
    pressed = False
    turn = "player"

    while run:
        if pygame.mouse.get_rel() != (0, 0):
            block, index = Coordinates(square_width, locations)
            if block and grid.positions[index] != mouse_position:    # if statements are here so that the dijkstra is only run when the cursor changes block for efficiency
                draw_back(grid, win)
                draw_grid(grid, win)
            mouse_position = draw_to_mouse(grid, locations, square_width, win, mouse_position, player)

        if pressed and turn == "player":
            block, index = Coordinates(square_width, locations)
            if index is not None:
                path = get_path(grid, index, player)
                animate_player(grid, locations, player, path, 5, enemies, win)
                player.location = Reverse(grid.positions[index])
            turn = "enemy"

        elif turn == "enemy":
            enemy_paths = move_enemies(grid, locations, enemies, walls, player)
            pygame.time.wait(150)
            animate_enemies(grid, walls, locations, enemies, enemy_paths, 10, player, win)
            draw_back(grid, win)
            for enemy in enemies:
                enemy[0].create_rays(walls)
                enemy[0].position = enemy_paths[enemy[0]][-1]
                enemy[0].location = locations[grid.positions.index(enemy[0].position)]
            enemy_paths = None
            draw_enemies(enemies, win)
            draw_grid(grid, win)

            turn = "player"
            # move enemy

        for enemy in enemies:
            enemy[0].find_player(player, walls, locations, grid)


        draw_player(grid, locations, player, win)
        draw_enemies(enemies, win)
        pygame.display.update()
        clock.tick(144)
        run, pressed = check_events(run)


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


running = True
running = menu(running)
pygame.quit()
