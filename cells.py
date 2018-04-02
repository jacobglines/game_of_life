class Cell:
    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self. column = column
        self.location = None
        self.neighbors = []
        self.nextLife = False
        self.livingChar = u"\u2B1B"
        self.deadChar = u"\u2B1C"

    def live(self):
        self.alive = True
        return self

    def die(self):
        self.alive = False
        return self

    def get_living_neighbors(self):
        living = 0
        for cell in self.neighbors:
            if cell.alive == True:
                living += 1
        return living

    def __repr__(self):
        return self.livingChar if self.alive else self.deadChar
