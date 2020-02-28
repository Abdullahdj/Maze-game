# stack to store the maze generations snake history while moving through the maze and creating a path
class Stack:
    def __init__(self):
        self.stack = []

    # checks if stack is empty
    def isempty(self):
        return len(self.stack) == 0

    # pushes an item onto the stack
    def push(self, value):
        self.stack.append(value)

    # removes an item and returns it from the stack
    def pop(self):
        if not self.isempty():
            top = self.stack.pop(len(self.stack)-1)
            return top
        else:
            raise IndexError("Stack empty")

    # returns the top item of the stack without removing it
    def peek(self):
        return self.stack[len(self.stack) - 1]

    # checks if a value is in the stack
    def instack(self, value):
        if value in self.stack:
            return True
        return False
