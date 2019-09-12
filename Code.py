import random

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
            if history.instack([[current_position[0]], [current_position[1] + 1]]):
                PossibleDirections.remove(direction)
        elif direction == 2:
            if history.instack([[current_position[0] + 1], [current_position[1]]]):
                PossibleDirections.remove(direction)
        elif direction == 3:
            if history.instack([[current_position[0]], [current_position[1] - 1]]):
                PossibleDirections.remove(direction)

    # Return random direction
    if len(PossibleDirections) != 0:
        Direction = PossibleDirections[random.randint(0, len(PossibleDirections)-1)]
        return Direction
    return False

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
        History = Stack()
        Position = [0, 0]
        Exit = [self.width-1, self.length-1]
        Direction = ChooseDirection(self.maze, Position, History)   # Directions in order correspond to NWSE
        print(Direction)
