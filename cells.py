class Cell:
    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self. column = column
        self.location = None
        self.neighbors = 0
        self.nextLife = False

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
        return u"\u25A0" if self.alive else u"\u25A1"
