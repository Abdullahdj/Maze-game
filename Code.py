class Grid:

    def __init__(self,width,length):
        self.width = width
        self.length = length
        self.grid = []

    def CreateGrid(self):
        for x in range(0,self.length):
            self.grid.append([0]*self.width)