import random

# (suggestion put this in grid class?)
def ChooseDirection(maze, current_position, history, omit, omitlist):
    PossibleDirections = [0, 1, 2, 3]
    if (current_position[0] - 1) < 0:
        PossibleDirections.remove(0)
    if (current_position[1] - 1) < 0:
        PossibleDirections.remove(1)

    try:
        maze[current_position[0] + 1][current_position[1]]
    except IndexError:
        PossibleDirections.remove(2)
    try:
        maze[current_position[0]][current_position[1] + 1]
    except IndexError:
        PossibleDirections.remove(3)

    # So far enough to omit impossible directions however stack needs to be implemented first before proceeding to remove visited directions
    #My code was broken because python is a bad bad language
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
        Direction = PossibleDirections[random.randint(0, len(PossibleDirections)-1)]
        return len(PossibleDirections), Direction
    return len(PossibleDirections), 4

class Stack:
    def __init__(self):
        self.stack = []

    def isempty(self):
        if len(self.stack) == 0:
            return True
        return False

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if not self.isempty():
            top = self.stack.pop(len(self.stack)-1)
            return top
        else:
            raise IndexError("Stack empty")

    def peek(self):
        return self.stack[len(self.stack) - 1]

    def instack(self, value):
        if value in self.stack:
            return True
        return False


class Grid:

    def __init__(self, width):
        self.width = width
        self.maze = []

    def CreateGrid(self):
        for x in range(0, self.width):
            self.maze.append([[1, 1, 1, 1]] * self.width)  # Need mutable array (fixed size) for this can only get immutable tuple      #In format NWSE(compass)   #indexes in (y,x) format (for graphical output)

    def CheckUnvisitedNode(self):
        Coordinates = []
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[y])):
                if self.maze[y][x] == [1, 1, 1, 1]:
                    Coordinates.append([y, x])
        return Coordinates

    def CreateMaze(self):
        History = Stack()      # Note that data in the History stack should be in [y,x] format
        Omit = None
        OmitList = []
        Position = [int(self.width/2), int(self.width/2)]
        Exit = [self.width-1, self.width-1]    # will adjust to be random later this is for testing purposes
        while Position != Exit:
            AmountOfDirections, Direction = ChooseDirection(self.maze, Position, History, Omit, OmitList)   # Directions in order correspond to NWSE     Choose random direction
            Omit = None
            # Break walls ,change position ,add last position to stack
            if Direction == 0:
                self.maze[Position[0]][Position[1]] = [0,                                           # Done like this to ensure that the maze can overlap walls and gaps
                                                       self.maze[Position[0]][Position[1]][1],
                                                       self.maze[Position[0]][Position[1]][2],
                                                       self.maze[Position[0]][Position[1]][3]]
                self.maze[Position[0] - 1][Position[1]] = [self.maze[Position[0] - 1][Position[1]][0],
                                                           self.maze[Position[0] - 1][Position[1]][1],
                                                           0,
                                                           self.maze[Position[0] - 1][Position[1]][3]]
                History.push(Position)
                Position = [Position[0] - 1, Position[1]]
            elif Direction == 1:
                self.maze[Position[0]][Position[1]] = [self.maze[Position[0]][Position[1]][0],
                                                       0,
                                                       self.maze[Position[0]][Position[1]][2],
                                                       self.maze[Position[0]][Position[1]][3]]
                self.maze[Position[0]][Position[1] - 1] = [self.maze[Position[0]][Position[1] - 1][0],
                                                           self.maze[Position[0]][Position[1] - 1][1],
                                                           self.maze[Position[0]][Position[1] - 1][2],
                                                           0]
                History.push(Position)
                Position = [Position[0], Position[1] - 1]
            elif Direction == 2:
                self.maze[Position[0]][Position[1]] = [self.maze[Position[0]][Position[1]][0],
                                                       self.maze[Position[0]][Position[1]][1],
                                                       0,
                                                       self.maze[Position[0]][Position[1]][3]]
                self.maze[Position[0] + 1][Position[1]] = [0,
                                                           self.maze[Position[0] + 1][Position[1]][1],
                                                           self.maze[Position[0] + 1][Position[1]][2],
                                                           self.maze[Position[0] + 1][Position[1]][3]]
                History.push(Position)
                Position = [Position[0] + 1, Position[1]]
            elif Direction == 3:
                self.maze[Position[0]][Position[1]] = [self.maze[Position[0]][Position[1]][0],
                                                       self.maze[Position[0]][Position[1]][1],
                                                       self.maze[Position[0]][Position[1]][2],
                                                       0]
                self.maze[Position[0]][Position[1] + 1] = [self.maze[Position[0]][Position[1] + 1][0],
                                                           0,
                                                           self.maze[Position[0]][Position[1] + 1][2],
                                                           self.maze[Position[0]][Position[1] + 1][3]]
                History.push(Position)
                Position = [Position[0], Position[1] + 1]

            # Repeats until a route that hasn't been explored is used     (It may go back through the old path over and over until the new path is randomly chosen)
            elif Direction == 4:
                while AmountOfDirections == 0:
                    AmountOfDirections, Direction = ChooseDirection(self.maze, Position, History, Omit, OmitList)
                    Omit = None
                    try:
                        LastPosition = History.pop()
                        if LastPosition[0] == Position[0]:
                            if LastPosition[1] == Position[1] + 1:
                                #East
                                self.maze[Position[0]][Position[1]][3] = 1
                                self.maze[LastPosition[0]][LastPosition[1]][1] = 1
                                Omit = 1
                            #West
                            elif LastPosition[1] == Position[1] - 1:
                                self.maze[Position[0]][Position[1]][1] = 1
                                self.maze[LastPosition[0]][LastPosition[1]][3] = 1
                                Omit = 3
                        elif LastPosition[1] == Position[1]:
                            #South
                            if LastPosition[0] == Position[0] + 1:
                                self.maze[Position[0]][Position[1]][2] = 1
                                self.maze[LastPosition[0]][LastPosition[1]][0] = 1
                                Omit = 0
                            #North
                            elif LastPosition[0] == Position[0] - 1:
                                self.maze[Position[0]][Position[1]][0] = 1
                                self.maze[LastPosition[0]][LastPosition[1]][2] = 1
                                Omit = 2
                        PositionToOmit = Position
                        Position = LastPosition
                    except:
                        OmitList = []
                        AmountOfDirections = 4
                OmitList.append(PositionToOmit)


x = Grid(100)
x.CreateGrid()
x.CreateMaze()

# BTW the comments aren't purposeful code destruction they are used to allow me to remember my next course of action between code writing seshs and how code works

                                                                          # ____
# Problem the code may get permanently stuck if it blocks the path to exit !      like this (maybe not?)
# Instead of replacing the walls i tell it to replace it replaces all walls
# Massive legend here: Big problem due to maths.  Though it is random there is a high probability that the maze snake will go down down down down down down down right right right emd (for example)(solution start in mid for first pass through)
# Can be resolved by fixing the probabilities of each direction being chosen but that's kinda long ngl and no-one is really gonna notice (solved by placing start point at the centre)
