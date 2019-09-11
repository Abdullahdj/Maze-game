import random

def ChooseDirection(maze, current_position):
    PossibleDirections = []
    Direction = 1
    while Direction < 4:
        try:
            if Direction == 1:
                maze[current_position[0] - 1][current_position[1]]
            elif Direction == 2:
                maze[current_position[0]][current_position[1] + 1]
            elif Direction == 3:
                maze[current_position[0] + 1][current_position[1]]
            elif Direction == 4:
                maze[current_position[0]][current_position[1] - 1]
            else:
                raise ArithmeticError("Bad programmer you get -rep")
            PossibleDirections.append(Direction)
            Direction += 1
        except IndexError:
            Direction += 1

    #So far enough to omit impossible directions however stack needs to be implemented first before proceeding

    Direction = PossibleDirections[randint(0,len(PossibleDirections)-1)]


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
        Exit = [self.width-1,self.length-1]
        Direction = ChooseDirection(self.maze,Position)   # Directions in order correspond to NWSE
