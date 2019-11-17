import random
import Stack


class Grid:

    def __init__(self, width):
        if type(width) != int and width != 0:
            self.width = 1
        else:
            self.width = width
        self.walls = None
        self.maze = []
        self.layer = []

    def OverlapMaze(self):
        for y in range(0, self.width):
            for x in range(0, self.width):
                for nwse in range(0, 4):
                    if self.layer[y][x][nwse] == 0:
                        self.maze[y][x][nwse] = 0

    def CreateGrid(self):
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
            Exit = [self.width-1, self.width-1]    # will adjust to be random later this is for testing purposes
            while UnvisitableNodesExist:
                self.CreateGridCopy()
                while Position != Exit:
                    AmountOfDirections, Direction = self.ChooseDirection(Position, history, Omit, OmitList)   # Directions in order correspond to NWSE     Choose random direction
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
