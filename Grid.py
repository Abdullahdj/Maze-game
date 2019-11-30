import random
import Stack
import time
import PQ
import heapq


class Grid:
    def __init__(self, width=0):
        if type(width) != int or int(width) == 0:
            self.width = 1
        else:
            self.width = int(width)
        self.positions = []
        self.walls = None
        self.maze = []
        self.layer = []
        self.matrix = None
        self.matrix_map = None
        self.adj_list = None

    def OverlapMaze(self):
        for y in range(0, self.width):
            for x in range(0, self.width):
                for nwse in range(0, 4):
                    if self.layer[y][x][nwse] == 0:
                        self.maze[y][x][nwse] = 0

    def CreateGrid(self):
        self.maze = []
        for x in range(0, self.width):
            self.maze.append([])
            for y in range(0, self.width):
                self.maze[x].append([1, 1, 1, 1])

    def CreateGridCopy(self):
        self.layer = []
        for x in range(0, self.width):
            self.layer.append([])
            for y in range(0, self.width):
                self.layer[x].append([1, 1, 1, 1])  # Need mutable array (fixed size) for this can only get immutable tuple      #In format NWSE(compass)   #indexes in (y,x) format (for graphical output)

    def ChooseDirection(self, current_position, history, omit, omitlist):
        PossibleDirections = [0, 1, 2, 3]
        if (current_position[0] - 1) < 0:
            PossibleDirections.remove(0)
        if (current_position[1] - 1) < 0:
            PossibleDirections.remove(1)

        try:
            self.layer[current_position[0] + 1][current_position[1]]
        except IndexError:
            PossibleDirections.remove(2)
        try:
            self.layer[current_position[0]][current_position[1] + 1]
        except IndexError:
            PossibleDirections.remove(3)

        # So far enough to omit impossible directions however stack needs to be implemented first before proceeding to remove visited directions
        # My code was broken because python is a bad bad language
        copylist = PossibleDirections[:]
        # Check for previously visited paths using history Stack
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

        # Return random direction
        if len(PossibleDirections) != 0:
            direction = PossibleDirections[random.randint(0, len(PossibleDirections) - 1)]
            return len(PossibleDirections), direction
        return len(PossibleDirections), 4

    def CheckUnvisitedNode(self):
        coordinates = []
        unvisitable_nodes_exist = False
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[y])):
                if self.maze[y][x] == [1, 1, 1, 1]:
                    coordinates.append([y, x])
                    unvisitable_nodes_exist = True
        return unvisitable_nodes_exist, coordinates

    def CreateMaze(self):
        self.CreateGrid()
        if self.width != 1:
            history = Stack.Stack()      # Note that data in the History stack should be in [y,x] format
            Omit = None
            OmitList = []
            UnvisitableNodesExist = True
            Position = [int(self.width/2), int(self.width/2)]
            Exit = [int(self.width/2), int(self.width/2)]    # will adjust to be random later this is for testing purposes
            while UnvisitableNodesExist:
                self.CreateGridCopy()
                while (Position != Exit):
                    AmountOfDirections, Direction = self.ChooseDirection(Position, history, Omit, OmitList)   # Directions in order correspond to NWSE     Choose random direction
                    if self.maze[Position[0]][Position[1]].count(0) > 3:
                        break
                    Omit = None
                    # Break walls ,change position ,add last position to stack
                    if Direction == 0:
                        self.layer[Position[0]][Position[1]][0] = 0
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

                    # Repeats until a route that hasn't been explored is used     (It may go back through the old path over and over until the new path is randomly chosen)
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
                self.OverlapMaze()
                history = Stack.Stack()
                Omit = None
                OmitList = []
                UnvisitableNodesExist, UnvisitedNodes = self.CheckUnvisitedNode()
                if UnvisitableNodesExist == False:      # Because for some reason the retarded program named python doesn't realise it's FALSE WTF
                    break
                Position = random.choice(UnvisitedNodes)
        "self.CreateMatrix()"

    def CreateMatrix(self):
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
        # Created matrix size now to create connections (may be able to connect these two but for now ima do this)
        x = 0
        y = 0
        for row in self.maze:
            for node in row:
                current_index = matrix_map[(y, x)]
                if node[0] == 0:                                        # this may cause a syntax error but the code should never enter the loop if the condition for the error is met
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

    def GetMatrixIndex(self, location):      # location looks like (x,y)
        return self.matrix_map[location]

    def GetMazeLocation(self, index):
        for key, value in self.matrix_map.items():
            if index == value:
                return key

    def GetNeighbours(self, node):
        index = self.GetMatrixIndex(node)
        neighbours = PQ.Heap()
        for finder in range(0, self.width**2):
            if self.matrix[index][finder] != float("inf"):         # only nodes that haven't been visited (yet to be implemented)
                neighbours.push(self.matrix[index][finder], self.GetMazeLocation(finder))
        return neighbours

    def PathFinding(self, source, exit):
        unvisited = PQ.Heap()
        visited = PQ.Heap()
        # create queue filled with unvisited nodes
        for location in self.positions:
            unvisited.push(float("inf"), location)
        unvisited.edit(0, source, None)

        # start the simulation MWhahahahaaahaahahaaha
        while not visited.InQueue(exit) and not unvisited.empty():
            current_node = unvisited.pull()
            print(current_node)
            visited.push(current_node[0], current_node[1][1], current_node[1][0])
            neighbours = self.GetNeighbours(current_node[1][1])
            print(" neighbours of above me dum lol", neighbours.queue)
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
        path.reverse()
        return path, weight


# Change maze generation to make the generator stop once the snake reaches an open node