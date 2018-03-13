from cells import Cell
from random import *

class World(list):
    def __init__(self, x, y):
        super(World, self).__init__()
        self.rows = x
        self.columns = y
        Values = [True, False]
        for _ in range(y):
            line = []
            for _ in range(x):
                status = Values[randint(0,1)]
                cell = Cell(status)
                line.append(cell)
            self.append(line)

    def __str__(self):
        s = ''
        for row in self:
            s += '| '
            for cell in row:
                s += str(cell)
                s += ' | '
            s += '\n'
        return s