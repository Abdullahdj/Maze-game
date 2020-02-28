import random
import Stack
import PQ


def Reverse(tuples):                # Some coordinates used are in (y,x) due to the way lists work as result a function that reverses tuples
    new_tup = tuples[::-1]
    return new_tup


class Grid:
    def __init__(self, width=0):
        if type(width) != int or int(width) == 0:      # this line checks if width is 0 and sets the grid size to 1
            self.width = 1
        else:
            self.width = int(width)
        self.positions = []  # positions are like indices on the grid 2d array and these match 1 to 1 with locations ("ordinally") with locations (pixel co-ords) from pygame run file
        self.walls = None
        self.maze = []      # a 2D array containing the maze layout (this begins as a grid of completely blocked of nodes and has layers overlapped onto it to make a full maze)
        self.layer = []            # As described in documented design a layer has a path created onto it (a single path that passes from one location to another with no loops) this is overlapped onto the maze
        self.template = []      # used for efficiency better to copy a template of an all blocked off grid then to recreate it every time you run the code. Looks like a maze where no nodes are connected
        self.matrix = None      # this is the matrix representation of the maze (graph data type) (a 2d array storing weightings of connection between nodes)
        self.matrix_map = None      # a dictionary used to map coordinates in (y, x) format to their indexes on the matrix. maps nodes to indexes

    def CreateTemplate(self):
        self.template = []
        for x in range(0, self.width):
            self.template.append([])
            for y in range(0, self.width):
                self.template[x].append([1, 1, 1, 1])
    # creates a template of a completely blocked off grid (no nodes (which are positions on the grid) are connected)

    def OverlapMaze(self):
        for y in range(0, self.width):
            for x in range(0, self.width):
                for nwse in range(0, 4):
                    if self.layer[y][x][nwse] == 0:
                        self.maze[y][x][nwse] = 0
    # function takes a layer with a single path and overlaps it onto the maze (by removing walls that don't exist on the layer)

    def CreateGrid(self):
        self.maze = self.template.copy()
    # makes the maze into a completely blocked off maze (no nodes connected) (only done when initially before generating an actual maze)

    def CreateGridCopy(self):
        self.layer = self.template.copy()  # Need mutable array (fixed size) for this can only get immutable tuple      #In format NWSE (compass) [N,W,S,E] walls   #indexes in (y,x) format (for graphical output)

    def ChooseDirection(self, current_position, history, omit, omitlist):
        PossibleDirections = [0, 1, 2, 3]       # this is an array containing the directions the maze snake (refer to documented design maze generation) can take legally without breaking its rules
        if (current_position[0] - 1) < 0:
            PossibleDirections.remove(0)
        if (current_position[1] - 1) < 0:
            PossibleDirections.remove(1)
        # checks north and west of the snake to see if the snake is going out of the map (grid) in those directions removes these from the possible directions snake can travel
        # no index error since python allows for negative indexes

        try:
            self.layer[current_position[0] + 1][current_position[1]]
        except IndexError:
            PossibleDirections.remove(2)
        try:
            self.layer[current_position[0]][current_position[1] + 1]
        except IndexError:
            PossibleDirections.remove(3)
            # checks south and east to see if the snake is going outside the map in those directions and removes those from possible directions snake can travel
        # (if there is an index error the index is outside the map)

        copylist = PossibleDirections[:]
        # copylist is used since if an item is removed from a list you are currently
        # iterating through then the next item in that list after the removed item is skipped and not iterated on

        # Check for previously visited paths using history Stack that stores previously visited nodes by the snake and remove those nodes so the snake doesn't go over itself
        # this is necessary to allow the maze to create a perfect maze or an imperfect maze rather than just imperfect
        for direction in copylist:
            if direction == 0:
                if history.instack([current_position[0] - 1, current_position[1]]) or [current_position[0] - 1, current_position[1]] in omitlist:
                    PossibleDirections.remove(direction)
            elif direction == 1:
                if history.instack([current_position[0], current_position[1] - 1]) or [current_position[0], current_position[1] - 1] in omitlist:
                    PossibleDirections.remove(direction)
            elif direction == 2:
                if history.instack([current_position[0] + 1, current_position[1]]) or [current_position[0] + 1, current_position[1]] in omitlist:
                    PossibleDirections.remove(direction)
            elif direction == 3:
                if history.instack([current_position[0], current_position[1] + 1]) or [current_position[0], current_position[1] + 1] in omitlist:
                    PossibleDirections.remove(direction)
        copylist = PossibleDirections[:]
        if omit in copylist:
            PossibleDirections.remove(omit)

        # Return random direction from the directions that are left over after all illegal directions are removed
        if len(PossibleDirections) != 0:
            direction = PossibleDirections[random.randint(0, len(PossibleDirections) - 1)]
            return len(PossibleDirections), direction   # if there is somewhere that the snake can visit then return the amount of directions and the chosen direction
        else:
            return len(PossibleDirections), 4
            # if there is nowhere the snake can go then return the direction 4 which (corresponds to error no direction) and the amount of legal directions

    def CheckUnvisitedNode(self):
        coordinates = []
        unvisitable_nodes_exist = False
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[y])):
                if self.maze[y][x] == [1, 1, 1, 1]:
                    coordinates.append([y, x])
                    unvisitable_nodes_exist = True
        return unvisitable_nodes_exist, coordinates
    # checks every node in the maze (the final maze which is used) to see if there are any nodes which are [1,1,1,1] which means the node is impossible to visit

    # this creates the entire maze of self.width * self.width size
    # there are many references to snake in this code refer to documented design if any confusion arises
    def CreateMaze(self):
        self.CreateTemplate()       # initialise a template of an entirely blocked off maze used for efficiency (better to create once and copy then create over and over)
        self.CreateGrid()           # initialise the maze as an entirely blocked of maze (only done here) walls are removed to create the maze in the end
        if self.width != 1:     # checks if the maze is only 1 block long (really only here for consistency sake)
            history = Stack.Stack()      # Note that data in the History stack should be in [y,x] format
            Omit = None         # if the snake gets stuck in a dead-end then once the snake has backed out of the dead-end far enough it will avoid going in that direction again using this variable
            OmitList = []       # list of directions to omit just in case the snake gets stuck between more than one dead-end that it created for itself
            UnvisitableNodesExist = True       # variable is used to check if the maze is complete or not (if there are locations that cannot be visited)
            Position = [int(self.width/2), int(self.width/2)]   # sets the position of the snake initially as the center of the maze but stores the location of the snake's head
            Exit = [int(self.width/2), int(self.width/2)]
            # Exit sets the exit position initially which is the position that the snake has to reach before the layer is
            # overlapped onto self.maze set as bottom corner initially but is changed to a random unvisited node that isn't adjacent to the snake's starting
            # position (to prevent 2 nodes connected that are blocked off)
            while UnvisitableNodesExist:        # while there are unvisitable nodes in the actual maze
                break_now = False       # variable used to break the snake out of its loop and copy the template onto the maze once to make a maze more or less sparse
                self.CreateGridCopy()   # creates a layer of blocked off nodes for the snake to create a path on that will eventually be overlapped onto the full maze
                while Position != Exit:  # while snake isn't at the exit position that was designated (while it is creating the path)
                    AmountOfDirections, Direction = self.ChooseDirection(Position, history, Omit, OmitList)   # Directions in order correspond to NWSE     Choose random direction

                    if self.maze[Position[0]][Position[1]].count(1) == 1:
                        break_now = True
                    # by changing the value checked against for this if statement, you can control how sparse the maze will be
                    # the snake will no longer generate a path once it reaches a location that already has x open walls
                    # on it where x is the number checked against in the if statement. This is used for both efficiency
                    # maze sparsity and choosing between mathematically perfect and imperfect mazes
                    Omit = None

                    # Break walls, change snake position, add last position to stack based on the direction randomly chosen
                    if Direction == 0:
                        self.layer[Position[0]][Position[1]][0] = 2
                        self.layer[Position[0] - 1][Position[1]][2] = 0
                        history.push(Position)
                        Position = [Position[0] - 1, Position[1]]
                    elif Direction == 1:
                        self.layer[Position[0]][Position[1]][1] = 0
                        self.layer[Position[0]][Position[1] - 1][3] = 0
                        history.push(Position)
                        Position = [Position[0], Position[1] - 1]
                    elif Direction == 2:
                        self.layer[Position[0]][Position[1]][2] = 0
                        self.layer[Position[0] + 1][Position[1]][0] = 0
                        history.push(Position)
                        Position = [Position[0] + 1, Position[1]]
                    elif Direction == 3:
                        self.layer[Position[0]][Position[1]][3] = 0
                        self.layer[Position[0]][Position[1] + 1][1] = 0
                        history.push(Position)
                        Position = [Position[0], Position[1] + 1]

                    # Repeats until a route that hasn't been explored is used by snake (code below)
                    # (It may go back through the old path over and over until the new path is randomly chosen)
                    # this occurs only if snake has nowhere to go and will use the stack to go back on the locations the
                    # snake has previously been to to check for alternative paths
                    elif Direction == 4:
                        PositionToOmit = None
                        while AmountOfDirections == 0:
                            AmountOfDirections, Direction = self.ChooseDirection(Position, history, Omit, OmitList)
                            Omit = None
                            try:
                                LastPosition = history.pop()
                                if LastPosition[0] == Position[0]:
                                    if LastPosition[1] == Position[1] + 1:
                                        # East
                                        self.layer[Position[0]][Position[1]][3] = 1
                                        self.layer[LastPosition[0]][LastPosition[1]][1] = 1
                                        Omit = 1
                                    # West
                                    elif LastPosition[1] == Position[1] - 1:
                                        self.layer[Position[0]][Position[1]][1] = 1
                                        self.layer[LastPosition[0]][LastPosition[1]][3] = 1
                                        Omit = 3
                                elif LastPosition[1] == Position[1]:
                                    # South
                                    if LastPosition[0] == Position[0] + 1:
                                        self.layer[Position[0]][Position[1]][2] = 1
                                        self.layer[LastPosition[0]][LastPosition[1]][0] = 1
                                        Omit = 0
                                    # North
                                    elif LastPosition[0] == Position[0] - 1:
                                        self.layer[Position[0]][Position[1]][0] = 1
                                        self.layer[LastPosition[0]][LastPosition[1]][2] = 1
                                        Omit = 2
                                PositionToOmit = Position
                                Position = LastPosition
                            except IndexError:
                                OmitList = []
                                AmountOfDirections = 4
                        OmitList.append(PositionToOmit)
                    if break_now:
                        break

                # once the layer has been created (a single path is created by the snake) then the layer is overlapped onto the maze
                self.OverlapMaze()
                history = Stack.Stack()     # history stack is reset for a new snake
                Omit = None         # direction to omit and directions to omit are reset to none and empty for the new snake
                OmitList = []
                UnvisitableNodesExist, UnvisitedNodes = self.CheckUnvisitedNode()           # the actual maze is checked to find any unvisitable nodes
                # if there aren't any then the maze is generated and the loop is done so we break out of it
                if UnvisitableNodesExist is False:
                    break
                Position = random.choice(UnvisitedNodes)    # otherwise a new exit and start position are chosen from the list of unvisitable nodes

    def CreateMatrix(self):     # creates the matrix representation of the maze (a graph data-type used for Dijkstra path-finding)
        matrix = []
        matrix_map = {}
        index = 0
        y = 0
        for row in self.maze:
            x = 0
            for node in row:
                matrix_map[(y, x)] = index
                self.positions.append((y, x))
                x += 1
                index += 1
            y += 1
        for k in range(0, self.width**2):
            matrix.append([])
            for i in range(0, self.width**2):
                matrix[k].append(float("inf"))
        x = 0
        y = 0
        for row in self.maze:
            for node in row:
                current_index = matrix_map[(y, x)]
                if node[0] == 0:
                    target_index = matrix_map[(y - 1, x)]
                    matrix[current_index][target_index] = 1
                    matrix[target_index][current_index] = 1
                if node[1] == 0:
                    target_index = matrix_map[(y, x - 1)]
                    matrix[current_index][target_index] = 1
                    matrix[target_index][current_index] = 1
                if node[2] == 0:
                    target_index = matrix_map[(y + 1, x)]
                    matrix[current_index][target_index] = 1
                    matrix[target_index][current_index] = 1
                if node[3] == 0:
                    target_index = matrix_map[(y, x + 1)]
                    matrix[current_index][target_index] = 1
                    matrix[target_index][current_index] = 1
                x += 1
                x = x % self.width
            y += 1
            y = y % self.width
        self.matrix_map = matrix_map
        self.matrix = matrix
        # this peice of code (above) checks every node in the maze (generated) and checks it against every other node in
        # the maze to see if there is a connection between them or not if there is a connection then that connection is assigned a weighting of 1
        # a matrix map is created alongside this to link positions in the maze ((y,x) co-ordinates) to indexes in the matrix

    # this is used in path finding to link locations in co-ordinates to their matrix indexes used in pygame run file to
    def GetMatrixIndex(self, location):      # location looks like (y, x)
        try:
            return self.matrix_map[location]
        except KeyError:
            return False

    def GetMazeLocation(self, index):       # gets the position in (y,x) format off of the index in the matrix
        for key, value in self.matrix_map.items():
            if index == value:
                return key

    # gets all neighbours of a node (y,x) used for Dijkstra path finding (all nodes that you can visit from that node)
    def GetNeighbours(self, node):
        index = self.GetMatrixIndex(node)
        neighbours = PQ.Heap()
        for finder in range(0, self.width**2):
            if self.matrix[index][finder] != float("inf"):
                neighbours.push(self.matrix[index][finder], self.GetMazeLocation(finder))
        return neighbours

    # Dijkstra path finding algorithm that takes a source and an exit node and based off of that creates a path between
    # them of shortest weighting refer to documented design for an explanation of this
    def PathFinding(self, source, exit):
        exit = Reverse(exit)
        if source == exit:
            return [[Reverse(source)], 0]
        unvisited = PQ.Heap()
        visited = PQ.Heap()
        # create queue filled with unvisited nodes
        for location in self.positions:
            unvisited.push(float("inf"), location)
        unvisited.edit(0, source, None)

        while not visited.InQueue(exit) and not unvisited.empty():
            current_node = unvisited.pull()
            visited.push(current_node[0], current_node[1][1], current_node[1][0])
            neighbours = self.GetNeighbours(current_node[1][1])
            while not neighbours.empty():
                neighbour = neighbours.pull()
                if not visited.InQueue(neighbour[1][1]):
                    distance_to = current_node[0] + neighbour[0]
                    unvisited.edit(distance_to, neighbour[1][1], current_node[1][1])

        path = []
        weight = visited.queue[-1][0]
        path.append(exit)
        current_node = visited.queue[-1][1][0]
        while current_node != source:
            for item in visited.queue:
                if item[1][1] == current_node:
                    path.append(item[1][1])
                    current_node = item[1][0]
                    break
        path.append(source)
        path.reverse()
        path = list(map(Reverse, path))
        return path, weight
