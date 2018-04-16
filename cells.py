class Cell:
    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self. column = column
        self.location = None
        self.neighbors = []
        self.nextLife = False
        self.livingChar = u"\u2B1B"
        self.longLivingChar = u"\u25C6"
        self.deadChar = u"\u2B1C"
        self.display = 'normal'
        self.timeAlive = 0

    def live(self):
        """Makes the cell alive"""
        self.alive = True
        return self

    def die(self):
        """Makes the cell die"""
        self.alive = False
        return self

    def get_living_neighbors(self):
        """Counts the number of alive neighbors for this cell"""
        living = 0
        for cell in self.neighbors:
            if cell.alive == True:
                living += 1
        return living

    def __repr__(self):
        #
        # Sees if the worlds display is normal or aged and then picks the repr of the cell
        #
        if self.display == 'aged':
            if self.timeAlive > 3:
                living = self.longLivingChar
            else:
                living = self.livingChar
        elif self.display == 'normal':
            living = self.livingChar
        return living if self.alive else self.deadChar
