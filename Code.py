import random

# (suggestion put this in grid class?)
def ChooseDirection(maze, current_position, history):
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

    # Check for previously visited paths using history Stack
    for direction in PossibleDirections:
        if direction == 0:
            if history.instack([current_position[0] - 1, current_position[1]]):
                PossibleDirections.remove(direction)
        elif direction == 1:
            if history.instack([[current_position[0]], [current_position[1] - 1]]):
                PossibleDirections.remove(direction)
        elif direction == 2:
            if history.instack([[current_position[0] + 1], [current_position[1]]]):
                PossibleDirections.remove(direction)
        elif direction == 3:
            if history.instack([[current_position[0]], [current_position[1] + 1]]):
                PossibleDirections.remove(direction)

    # Return random direction
    if len(PossibleDirections) != 0:
        Direction = PossibleDirections[random.randint(0, len(PossibleDirections)-1)]
        return len(PossibleDirections), Direction
    return len(PossibleDirections), False

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

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.maze = []

    def CreateGrid(self):
        for x in range(0, self.length):
            self.maze.append([[1, 1, 1, 1]] * self.width)  # Need mutable array (fixed size) for this can only get immutable tuple      #In format NWSE(compass)   #indexes in (y,x) format (for graphical output)

    def CreateMaze(self):
        History = Stack()      # Note that data in the History stack should be in [y,x] format
        Position = [0, 0]
        Exit = [self.width-1, self.length-1]    # will adjust to be random later this is for testing purposes
        while [1, 1, 1, 1] in self.maze:
            # First time will make paths to exit (rest will make random exits)

            while Position != Exit:
                AmountOfDirections, Direction = ChooseDirection(self.maze, Position, History)   # Directions in order correspond to NWSE     Choose random direction

                # Break walls ,change position ,add last position to stack
                History.push(Position)
                if Direction == 0:
                    self.maze[Position[0]][Position[1]] = [0 * self.maze[Position[0]][Position[1]][0],          # Done like this to ensure that the maze can overlap walls and gaps
                                                           1 * self.maze[Position[0]][Position[1]][1],
                                                           1 * self.maze[Position[0]][Position[1]][2],
                                                           1 * self.maze[Position[0]][Position[1]][3]]
                    self.maze[Position[0] - 1][Position[1]] = [1 * self.maze[Position[0] - 1][Position[1]][0],
                                                               1 * self.maze[Position[0] - 1][Position[1]][1],
                                                               0 * self.maze[Position[0] - 1][Position[1]][2],
                                                               1 * self.maze[Position[0] - 1][Position[1]][3]]
                    Position = [Position[0] - 1, Position[1]]
                elif Direction == 1:
                    self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                           0 * self.maze[Position[0]][Position[1]][1],
                                                           1 * self.maze[Position[0]][Position[1]][2],
                                                           1 * self.maze[Position[0]][Position[1]][3]]
                    self.maze[Position[0]][Position[1] - 1] = [1 * self.maze[Position[0]][Position[1] - 1][0],
                                                               1 * self.maze[Position[0]][Position[1] - 1][1],
                                                               1 * self.maze[Position[0]][Position[1] - 1][2],
                                                               0 * self.maze[Position[0]][Position[1] - 1][3]]
                    Position = [Position[0], Position[1] - 1]
                elif Direction == 2:
                    self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                           1 * self.maze[Position[0]][Position[1]][1],
                                                           0 * self.maze[Position[0]][Position[1]][2],
                                                           1 * self.maze[Position[0]][Position[1]][3]]
                    self.maze[Position[0] + 1][Position[1]] = [0 * self.maze[Position[0] + 1][Position[1]][0],
                                                               1 * self.maze[Position[0] + 1][Position[1]][1],
                                                               1 * self.maze[Position[0] + 1][Position[1]][2],
                                                               1 * self.maze[Position[0] + 1][Position[1]][3]]
                    Position = [Position[0] + 1, Position[1]]
                elif Direction == 3:
                    self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                           1 * self.maze[Position[0]][Position[1]][1],
                                                           1 * self.maze[Position[0]][Position[1]][2],
                                                           0 * self.maze[Position[0]][Position[1]][3]]
                    self.maze[Position[0]][Position[1] + 1] = [1 * self.maze[Position[0]][Position[1] + 1][0],
                                                               0 * self.maze[Position[0]][Position[1] + 1][1],
                                                               1 * self.maze[Position[0]][Position[1] + 1][2],
                                                               1 * self.maze[Position[0]][Position[1] + 1][3]]
                    Position = [Position[0], Position[1] + 1]

                # Repeats until a route that hasn't been explored is used     (It may go back through the old path over and over until the new path is randomly chosen)
                elif Direction == False:
                    AmountOfDirections = 1
                    while AmountOfDirections <= 1:
                        AmountOfDirections, Direction = ChooseDirection(self.maze, Position, History)

                        LastPosition = History.pop()
                        if LastPosition[0] == Position[0]:
                            if LastPosition[1] == Position[1] + 1:
                                self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                       1 * self.maze[Position[0]][Position[1]][1],
                                                                       1 * self.maze[Position[0]][Position[1]][2],
                                                                       1]
                                self.maze[LastPosition[0]][LastPosition[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                               1,
                                                                               1 * self.maze[Position[0]][Position[1]][2],
                                                                               1 * self.maze[Position[0]][Position[1]][3]]
                            elif LastPosition[1] == Position[1] - 1:
                                self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                       1,
                                                                       1 * self.maze[Position[0]][Position[1]][2],
                                                                       1 * self.maze[Position[0]][Position[1]][3]]
                                self.maze[LastPosition[0]][LastPosition[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                               1 * self.maze[Position[0]][Position[1]][1],
                                                                               1 * self.maze[Position[0]][Position[1]][2],
                                                                               1]
                        elif LastPosition[1] == Position[1]:
                            if LastPosition[0] == Position[0] + 1:
                                self.maze[Position[0]][Position[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                       1 * self.maze[Position[0]][Position[1]][1],
                                                                       1,
                                                                       1 * self.maze[Position[0]][Position[1]][3]]
                                self.maze[LastPosition[0]][LastPosition[1]] = [1,
                                                                               1 * self.maze[Position[0]][Position[1]][1],
                                                                               1 * self.maze[Position[0]][Position[1]][2],
                                                                               1 * self.maze[Position[0]][Position[1]][3]]
                            elif LastPosition[0] == Position[0] - 1:
                                self.maze[Position[0]][Position[1]] = [1,
                                                                       1 * self.maze[Position[0]][Position[1]][1],
                                                                       1 * self.maze[Position[0]][Position[1]][2],
                                                                       1 * self.maze[Position[0]][Position[1]][3]]
                                self.maze[LastPosition[0]][LastPosition[1]] = [1 * self.maze[Position[0]][Position[1]][0],
                                                                               1 * self.maze[Position[0]][Position[1]][1],
                                                                               1,
                                                                               1 * self.maze[Position[0]][Position[1]][3]]
                        Position = LastPosition

        # Create a last direction variable and use it to prevent going back the same direction (hint use len(PossibleDirections) for easier to write code)   (may be solved)

            # Need list of indexes where [1,1,1,1] exists (maybe will do in maze class?)

# BTW the comments aren't purposeful code destruction they are used to allow me to remember my next course of action between code writing seshs and how code works
