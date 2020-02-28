import pygame
from pygame.locals import *
import threading
import random
import Grid
import Player
import Button
import Enemy
import Item
import math
from pygame import mixer
pygame.init()

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)             # loads and starts the background music but turns off the volume and loops it


clock = pygame.time.Clock()         # used to regulate frames per second

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
gold = (255, 223, 0)        # colour variables global used to set colours of objects when drawing (in hex values)


def Reverse(tuples):            # reverses tuples used to reverse coordinates in wrong format
    new_tup = tuples[::-1]
    return new_tup


def text_objects(text, font):                       # from pygame class used to draw text to the screen
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text, centre, win):             # draws the text to the screen
    large_text = pygame.font.Font("freesansbold.ttf", 30)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = centre
    win.blit(text_surface, text_rect)


# checks for events such as key presses or mouse presses used to quit from the game and to check if mouse clicked in game
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


# draws a background onto the screen in circles (scalable for resolutions)
def background(colour1, ratio, win):
    x, y = win.get_size()
    radius = int(x/(ratio*2))
    for yratio in range(0, int(y/radius)):
        for xratio in range(0, (ratio + 1)):
            pygame.draw.circle(win, colour1, (int(x*xratio/ratio), 0 + yratio*radius*2), radius)


# this creates the window that is used to show the game (has parts to it that would have been used for scalability)
# it takes an aspect ratio and creates a window based on that and the screen height and width
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


# collects pixel positions of every position in the maze (top left corner) and stores in a list called locations that is
# 1 to 1 with grid.positions (coordinates list) useful when trying to move sprites in pixels and when drawing onto certain tiles
# creates a wall list of all walls defined by their start and end locations used for ray casting and line of sight algorithm for enemies
# returns square_width which just indicates how large a block on the maze is for drawing purposes
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


# draws the back of the maze (one large rectangle) that indicates the map area
def draw_back(grid, win):
    width, height = win.get_size()
    if width >= height:
        square_width = (height / grid.width)
        draw_point = (width - (square_width * grid.width)) / 2
        pygame.draw.rect(win, whiteblue, (draw_point, 0, height, height))


# draws the walls of the generated maze (map or grid) onto the screen by drawing lines
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


# draws enemy rays onto the screen (which is the feild of view) then draws the enemies onto the screen in their positions
def draw_enemies(enemies, window):
    for enemy in enemies:
        draw_rays(enemy[0], window)
    for enemy in enemies:
        draw_enemy(enemy[0], window)


# creates enemies avoiding creating enemies on top of one another which helps spread the enemies evenly across the map
def create_enemy(quantity, walls, difficulty, locations, square_width, grid):
    enemies = []
    used_spots = [None]
    y = None
    if difficulty == 1:
        for ID in range(0, quantity):
            while y in used_spots:
                y = random.randint(0, (grid.width ** 2 - 1))
            used_spots.append(y)
            location = locations[y]
            position = grid.positions[locations.index(location)]
            enemy = Enemy.Enemy(ID, "sprites/blob.png", int(square_width), difficulty, location, position, "monkey", math.ceil(grid.width/3))
            # mathematical calculations in this instantiation of an enemy are used so that the enemies number of steps moved is based of the size of the maze (proportional to)
            enemy.create_rays(walls)        # casts rays onto the walls of the maze
            enemies.append((enemy, y))
    return enemies


# draws enemies onto the screen in their location
def draw_enemy(enemy, window):
    enemy.draw(window)


# is used to work out where the mouse is (on what block it is on) when it is the players turn in game to draw the path the
# player will go to if the player presses on that position
def Coordinates(square_width, locations):
    mouse_pos = pygame.mouse.get_pos()
    block = None
    index = None
    for i, location in enumerate(locations):
        if (location[0] <= mouse_pos[0] < location[0] + square_width) and (location[1] <= mouse_pos[1] < location[1] + square_width):
            block = location
            index = i
            break
    return block, index


# draws the path up to the mouse using dijkstra and for efficiencies sake only draws the path and calculates it when
# the mouse changes block coordinates
def draw_to_mouse(grid, block, index, locations, square_width, win, prev_position, player):
    path = None
    if block and grid.positions[index] != prev_position:
        path = get_path(grid, index, player)
        draw_path(grid, path, locations, square_width, win)
    if index is not None:
        return grid.positions[index], path
    else:
        return None, path


# gets the path to the mouse and the weight of that path from the player and restricts that path to only the nodes that can be visited
# within the amount of steps th player can take
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


# draws a path onto the screen that the player will take if mouse is clicked
def draw_path(grid, path, locations, square_width, win):
    for i, node in enumerate(path[0]):
        location1 = locations[grid.positions.index(node)]
        try:
            location2 = locations[grid.positions.index(path[0][i+1])]
            pygame.draw.line(win, purple, ((location1[0] + square_width/2), (location1[1] + square_width/2)), ((location2[0] + square_width/2), (location2[1] + square_width/2)), 3)
        except IndexError:
            break


# creates the player avoiding positions of enemies on the maze so the player cannot spawn on top of an enemy
# also checks if a player already exists (after continuing once the game is won) and moves over the health and collected items across
def create_player(grid, locations, enemies, square_width, player):
    unvisitable = []
    for enemy in enemies:
        unvisitable.append(enemy[0].location)
    while True:
        location = random.choice(grid.positions)
        if location not in unvisitable:
            break
    if player is None:
        player = Player.Player("sprites/player.png", square_width, location, math.ceil(grid.width/3) + 2, math.ceil(3*(len(enemies)/2)))
    else:
        collected_items = player.collected_items
        # remove dungeon key
        for item in collected_items:
            if item.type == "key":
                collected_items.remove(item)

        health_remaining = player.health
        player = Player.Player("sprites/player.png", square_width, location, math.ceil(grid.width/3) + 2, math.ceil(3*(len(enemies)/2)))
        player.health = health_remaining
        player.collected_items = collected_items
    return player


# draws player onto screen (converts position in coordinates into pixel positions)
def draw_player(grid, locations, player, win):
    player.draw(locations[grid.positions.index(Reverse(player.location))], win)


# draws the enemy rays onto the screen
def draw_rays(enemy, window):
    enemy.draw_rays(window)


# using the path that was generated when moving the mouse the player is moved across the map using that path
def animate_player(items, grid, locations, player, path, speed, enemies, exit, square_width, win):
    for index, next_position in enumerate(path[0]):
        pixel_location = locations[grid.positions.index(player.location)]
        next_pixel_location = locations[grid.positions.index(next_position)]
        if pixel_location[0] == next_pixel_location[0]:
            distance = -(pixel_location[1] - next_pixel_location[1])
            direction = "y"
        else:
            distance = -(pixel_location[0] - next_pixel_location[0])
            direction = "x"

        # this is where the animation begins and interpolation is done
        # the distance and direction where calculated before and based on the distance and the speed value the player is
        # moved a fraction of the distance in the direction of the next node and this is repeated until he reaches the node
        for x in range(0, speed):
            if direction == "y" and index != 0:
                pixel_location = (pixel_location[0], pixel_location[1] + distance/speed)
                win.fill(lightblue)
                draw_back(grid, win)
                draw_exit(exit, square_width, win)
                draw_grid(grid, win)
                display_turn("player", win)
                display_player_health(player, win)
                display_score_ingame(player, win)
                draw_items(items, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
            if direction == "x" and index != 0:
                pixel_location = (pixel_location[0] + distance/speed, pixel_location[1])
                win.fill(lightblue)
                draw_back(grid, win)
                draw_exit(exit, square_width, win)
                draw_grid(grid, win)
                display_turn("player", win)
                display_player_health(player, win)
                display_score_ingame(player, win)
                draw_items(items, win)
                player.draw(pixel_location, win)
                draw_enemies(enemies, win)
                clock.tick(60)
                pygame.display.update()
            pygame.mouse.get_pressed()
        player.location = next_position
        player.check_for_items(items)       # checks for items that are on the players position and collects them
        clock.tick(60)
        pygame.display.update()
        win.fill(lightblue)
        draw_back(grid, win)
        draw_exit(exit, square_width, win)      # this is all just re-drawing all assets onto the screen
        draw_grid(grid, win)
        display_turn("player", win)
        display_player_health(player, win)
        display_score_ingame(player, win)
        draw_items(items, win)
    player.location = Reverse(player.location)


# this animates the enemies based on a generated path in a similar way to before (as animate_player())
def animate_enemies(items, grid, walls, locations, enemies, path, speed, player, exit, square_width, win):
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
                    draw_exit(exit, square_width, win)
                    display_player_health(player, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    enemy.draw(win)
                    draw_enemies(enemies, win)
                    draw_grid(grid, win)
                    display_turn("enemy", win)
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
                    draw_exit(exit, square_width, win)
                    display_player_health(player, win)
                    enemy.create_rays(walls)
                    player.draw(locations[grid.positions.index(Reverse(player.location))], win)
                    enemy.find_player(player, walls, locations, grid)
                    enemy.draw_rays(win)
                    draw_enemies(enemies, win)
                    enemy.draw(win)
                    draw_grid(grid, win)
                    display_turn("enemy", win)
                    draw_items(items, win)
                    pygame.display.update()
                    clock.tick(60)
                pygame.mouse.get_pressed()
            enemy.location = new_pixel_location[:]
            enemy.player_remembered()               # checks if the enemy still remembers the location of the player at the end of the movement


# remember last location that the player was spotted in (will move towards you for one turn after being spotted)
# the code makes sure to only allow the player to move a certain number of steps towards you (set by enemy.steps)
def move_enemies(grid, locations, enemies, walls, player):
    paths = {}        # dictionary storing the enemy along with the path it takes in order to animate (stores enemy with path it will take)
    for enemy in enemies:           # generates the enemies path using rule based ai and Dijkstra
        path = [enemy[0].position]
        steps = enemy[0].steps
        while steps > 0:
            new_position = None
            direction = None
            # if the enemy is searching and hasn't seen you recently (exact rules explained in enemy class)
            # then it will choose a random direction to move in and add that to the path for animation
            while enemy[0].state == "searching" and steps > 0 and enemy[0].last_known_location == None:
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

            # if the player is alert (which means the enemy can see you) then it will use Dijkstra to move towards you
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

            # when an enemy sees you the location it sees you in is stored in its memory
            # then if it cannot see you it will move towards the direction it last spotted you until it reaches that position
            # or until it reaches the location it remembered you in then it wipes its memory of you
            if enemy[0].last_known_location is not None:
                if enemy[0].location == locations[grid.positions.index(Reverse(player.location))]:
                    break
                path_to_player, weight = grid.PathFinding(Reverse(enemy[0].position), grid.positions[locations.index(enemy[0].last_known_location)])
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
        enemy[0].player_remembered()
    return paths


# displays players health onto screen
def display_player_health(player, win):
    width, height = pygame.display.get_surface().get_size()
    message_display(("Health: " + str(player.health)), (width*15/192, height*5/108), win)


# creates items randomly onto the map and places them in random locations across them maze
# guarantees a key will be made
# items are stored in a list called items in the game_loop()
# overlap of items is inconsequential and as a result is allowed
def create_items(number_of_items, square_width, grid, locations):
    # create a key separately
    items = []
    index = random.randint(0, (grid.width ** 2) - 1)
    position = grid.positions[index]
    location = locations[grid.positions.index(Reverse(position))]
    items.append(Item.Item("sprites/key.png", square_width, position, location, 300, "key"))

    # create loot randomly and scatter randomly across map
    for x in range(0, number_of_items - 1):
        sprite = random.choice(["sprites/pile_o_coins.png", "sprites/chest_o_coins.png", "sprites/ruby.png"])
        index = random.randint(0, (grid.width**2)-1)
        position = grid.positions[index]
        location = locations[grid.positions.index(Reverse(position))]
        item = Item.Item(sprite, square_width, position, location)
        items.append(item)
    return items


# draws items in their positions onto the screen
def draw_items(items, win):
    for item in items:
        item.draw(win)


def choose_exit(grid, locations):   # creates a list that stores values of exit tile such as matrix position grid position and pixel position
    exit = []
    location = random.choice(locations)
    position = grid.positions[locations.index(location)]
    exit.append(location)
    exit.append(Reverse(position))
    return exit


# draws the exit block in gold
def draw_exit(exit, square_width, win):
    pygame.draw.rect(win, gold, (exit[0][0], exit[0][1], square_width, square_width))


# game_loop the entire game runs here
def game_loop(win, difficulty, player=None):
    if difficulty == 1:         # maze is generated randomly with its matrix created alongside
        grid = Grid.Grid(20)
        grid.CreateMaze()
        grid.CreateMatrix()
    run = True              # used to break out of game loop or not
    win.fill(lightblue)
    locations, walls, square_width = collect_locations(win, grid)
    # creates locations (list of pixel coordinates corresponding to maze.position coordinates by index)
    # creates a list of walls which are line objects defined by start and end positions

    draw_back(grid, win)
    enemies = create_enemy(math.ceil(grid.width / 2), walls, difficulty, locations, square_width, grid)         # creates enemies (quantity is based on the size of maze)

    # This block of code prevents player from being in the same position as enemy by checking if enemy sees them and reinitialising if they can
    # it prevents the player from starting in the line of sight of the enemy
    checker = 1
    while checker != 0:
        player = create_player(grid, locations, enemies, square_width, player)
        counter = 0
        for enemy in enemies:
            enemy[0].find_player(player, walls, locations, grid)
            enemy[0].last_known_location = None
            if enemy[0].state == "alert":
                counter += 1
        checker = counter

    items = create_items(int(grid.width*1.5), square_width, grid, locations)    # creates items randomly across map
    exit = choose_exit(grid, locations)          # exit is in [location (pixels), position (co-ord)] format
    # exit is chosen randomly and can only be accessed if you have the dungeon key you can walk over the exit without going through
    # this allows the players to continue collecting loot if they wish without having to avoid the exit if they have the key

    turn = "player"     # sets turn to player at first
    draw_grid(grid, win)
    display_turn(turn, win)
    draw_items(items, win)      # draws onto the screen
    mouse_position = None
    pressed = False
    turn = "player"
    path = [[player.location], 0]   # sets the path as a path leading nowhere from the player with a weight of 0 done to prevent an error of no path existing

    while run:
        display_player_health(player, win)

        # this chunk of code is here to check if the mouse has moved to a different block
        # this is done to determine whether or not to run Dijkstra for efficiency sake
        # it will draw the path to the screen as well
        if pygame.mouse.get_rel() != (0, 0):        # if mouse has moved
            block, index = Coordinates(square_width, locations)
            if block and grid.positions[index] != mouse_position:    # if statements are here so that the dijkstra is only run when the cursor changes block for efficiency
                draw_back(grid, win)
                draw_exit(exit, square_width, win)
                draw_grid(grid, win)
                draw_items(items, win)
            mouse_position, temp = draw_to_mouse(grid, block, index, locations, square_width, win, mouse_position, player)
            if temp != None:
                path = temp

        # this chunk of code is the players turn
        if pressed and turn == "player":
            block, index = Coordinates(square_width, locations)
            if index is not None:
                path = get_path(grid, index, player)    # gets the path from the player to the mouse
                animate_player(items, grid, locations, player, path, 8, enemies, exit, square_width, win)   # animates and moves the player along that path
                turn = "enemy"  # sets turn to enemy because the players turn is done

        # this chunk of code creates enemy movements for every enemy and animates all of the movements
        # at the very end of their turn the enemies will deal damage to the player if the enemy and the player are in the same location
        elif turn == "enemy":
            if index is not None:
                path = get_path(grid, index, player)
            enemy_paths = move_enemies(grid, locations, enemies, walls, player)     # creates enemy paths
            pygame.time.wait(150)
            animate_enemies(items, grid, walls, locations, enemies, enemy_paths, 3, player, exit, square_width, win)    # animates enemy path

            draw_back(grid, win)
            draw_exit(exit, square_width, win)
            for enemy in enemies:
                enemy[0].create_rays(walls)
                enemy[0].position = enemy_paths[enemy[0]][-1]
                enemy[0].location = locations[grid.positions.index(enemy[0].position)]
                enemy[0].check_if_player_hit(player, locations, grid)
            # checks if by the end of the movement the enemy has hit the player if this is true then the player will lose health

            # resets enemy paths
            enemy_paths = None
            draw_enemies(enemies, win)
            draw_grid(grid, win)
            draw_items(items, win)

            turn = "player"       # sets turn to player

        # checks if player is visible for every enemy
        for enemy in enemies:
            enemy[0].find_player(player, walls, locations, grid)

        draw_player(grid, locations, player, win)
        draw_enemies(enemies, win)                  # draws onto screen
        pygame.display.update()

        # if the players health reaches 0 then the game is lost and the player is taken to the loss screen and the game loop stops running
        if player.health <= 0:
            game_over_screen(player, win)
            run = False
        # directly after this the player is sent back to the main menu

        clock.tick(144)
        win.fill(lightblue)
        draw_back(grid, win)
        draw_exit(exit, square_width, win)
        draw_grid(grid, win)                # just draws onto screen all assets and collects events
        draw_items(items, win)
        draw_path(grid, path, locations, square_width, win)
        display_turn(turn, win)
        run, pressed = check_events(run)    # if escape is pressed the code exits. mouse presses are also collected
        display_score_ingame(player, win)

        # checks if player has one and takes them to the you win screen if they decide not to continue then the program
        # will go back to the menu
        # if they choose to continue the dungeon key is removed from them and 300 points are lost but they have the
        # opportunity to continue collecting loot and points
        player_won = player.check_if_exit(exit)
        if player_won:
            you_win_screen(player, win)
            run = False
    # as an aside the player will always have 2 steps more than the enemy to make the game challenging but playable


# displays score onto screen
def display_score_ingame(player, win):
    width, height = pygame.display.get_surface().get_size()
    score = player.calculate_score()
    message_display(("Score:" + str(score)), (width*15/192, height*20/108), win)


# shows turn on screen
def display_turn(turn, win):
    width, height = pygame.display.get_surface().get_size()
    message_display(("Turn: " + turn), (width*15/192, height*30/108), win)


# takes the player to calculate the score
# is a screen shown when a player leaves a maze
# it fades in
def you_win_screen(player, win):
    width, height = pygame.display.get_surface().get_size()

    time = pygame.time.get_ticks()
    gold_val1 = 0
    gold_val2 = 0
    while pygame.time.get_ticks() - time < 11000:
        win.fill((int(gold_val1), int(gold_val2), 0))
        message_display("YOU WIN!!", (int(width/2) - int(width/50), int(height/2) - int(height/50)), win)
        message_display(("SCORE:" + str(player.calculate_score())), (int(width/2) - int(width/50), int(height/2) + int(height/10)), win)
        gold_val1 = (gold_val1 + 0.2) % 255
        gold_val2 = (gold_val2 + 0.182745) % 233    # this chunk of code gradually increases the gold hex value to create
        pygame.display.update()                     # a fade in effect for a set period of time
        clock.tick(60)

    # button instantiation all buttons in this code is relative to the screen size (all of this nea)
    continue_button = Button.Button(int(width/20), height*(12/15), int(width/3), int(height/10), white, black, "Continue")
    quit_button = Button.Button(int(12*width/20), height*(12/15), int(width/3), int(height/10), white, black, "Quit")

    # gives the player two options after they beat a level; either quit or continue
    # all of the remaining code is drawing the buttons onto the screen and waiting for the user input
    run = True
    while run:
        win.fill(gold)
        message_display("YOU WIN!!", (int(width / 2) - int(width / 50), int(height / 2) - int(height / 50)), win)
        message_display(("SCORE:" + str(player.calculate_score())), (int(width / 2) - int(width / 50), int(height / 2) + int(height / 10)), win)

        # continue button
        continue_button.check_on_button()
        continue_clicked = continue_button.check_clicked()
        continue_button.draw_button(win)
        if continue_clicked:
            continue_button.draw_button(win)
            quit_button.draw_button(win)
            pygame.display.update()
            game_loop(win, 1, player)

        # quit button
        quit_button.check_on_button()
        quit_button_clicked = quit_button.check_clicked()
        quit_button.draw_button(win)
        if quit_button_clicked:
            pygame.display.update()
            break

        run = check_events(run)[0]

        pygame.display.update()
        clock.tick(60)


# a screen that fades in red and waits a while it shows the score and "YOU LOSE"
# once this is done it will go back to the code it came from (in my game that is just straight to the menu screen)
def game_over_screen(player, win):
    width, height = pygame.display.get_surface().get_size()
    time = pygame.time.get_ticks()
    red_val = 0
    while pygame.time.get_ticks() - time < 9000:
        win.fill((int(red_val), 0, 0))
        message_display("YOU LOSE", (int(width/2) - int(width/50), int(height/2) - int(height/50)), win)
        message_display(("SCORE:" + str(player.calculate_score())), (int(width/2) - int(width/50), int(height/2) + int(height/10)), win)
        red_val = (red_val + 0.2) % 255
        pygame.display.update()


# an options menu containing the option to turn music on or off
def options_menu(playing, win):

    # all buttons are instantiated the music button text is based on whether or not the music is playing or not
    width, height = pygame.display.get_surface().get_size()
    time = pygame.time.get_ticks()
    run = True
    if not playing:
        music = Button.Button(int(width / 2.5), height * (12 / 15), int(width / 3), int(height / 10), white, black, "Music: OFF")
    else:
        music = Button.Button(int(width / 2.5), height * (12 / 15), int(width / 3), int(height / 10), white, black, "Music: ON")
    back = Button.Button(int(width / 2.5), int(height * (8 / 15)), int(width / 3), int(height / 10), white, black, "Go back")

    # checks for user input if user chooses to go back or to turn music on or off
    while run:
        pygame.display.update()
        if (pygame.time.get_ticks() - time) % 2000 < 1000:
            win.fill(whiteblue)                         # this part literally just animates the background with an effect
            background(lightblue, 10, win)
        else:
            win.fill(lightblue)
            background(whiteblue, 10, win)

        # music button
        music.check_on_button()
        pygame.time.wait(50)
        music_clicked = music.check_clicked()
        music.draw_button(win)
        if music_clicked:
            back.draw_button(win)
            if not playing:
                pygame.mixer.music.set_volume(0.2)      # sets volume of music to 0.2 which starts the music essentially
                playing = True
                music.text = "Music: ON"
            else:
                pygame.mixer.music.set_volume(0)    # turns music volume off
                music.text = "Music: OFF"
                playing = False

        # back button
        back.check_on_button()
        back_clicked = back.check_clicked()
        back.draw_button(win)
        if back_clicked:
            music.draw_button(win)
            pygame.display.update()
            run = False

        pygame.display.update()
        clock.tick(60)
        run = check_events(run)[0]
    return playing


def menu(run):
    # instantiates the play options and quit buttons placing them relative to screen height and width (scalable)
    win, width, height = alter_window(9/16)
    # buttons all in terms of height and width of screen
    quit = Button.Button(int(width/20), height*(12/15), int(width/3), int(height/10), white, black, "Quit")
    play = Button.Button(int(width/20), int(height*(8/15)), int(width/3), int(height/10), white, black, "Play")
    options = Button.Button(int(width/20), int(height*(10/15)), int(width/3), int(height/10), white, black, "Options")
    time = pygame.time.get_ticks()
    win.fill(whiteblue)
    background(lightblue, 10, win)
    playing_music = False   # sets music playing to false but this is changed in options menu

    # checks for user input and draws buttons onto screen and based on input and performs actions based on those inputs
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
            game_loop(win, 1)

        # options
        options.check_on_button()
        options_clicked = options.check_clicked()
        options.draw_button(win)
        if options_clicked:
            quit.draw_button(win)
            playing_music = options_menu(playing_music, win)


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
running = menu(running)     # this small part of code is where the entire program starts
pygame.quit()
