class Cell:
    def __init__(self, row, column):
        self.alive = False
        self.row = row
        self. column = column
        self.location = None

    def live(self):
        self.alive = True
        return self

    def die(self):
        self.alive = False
        return self

    def __repr__(self):
        return '0' if self.alive else '-'
