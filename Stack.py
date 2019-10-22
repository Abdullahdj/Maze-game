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
