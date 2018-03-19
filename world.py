from cells import Cell
from random import *


class World(list):
    def __init__(self, x, y):
        super(World, self).__init__()
        self.rows = x
        self.columns = y
        self.cells = self.create_cells()

    def __str__(self):
        s = ''
        for row in self.cells:
            s += '| '
            for cell in row:
                s += str(cell)
                s += ' | '
            s += '\n'
        return s

    def create_cells(self):
        cells = []
        for row in range(self.rows):
            line = []
            for column in range(self.columns):
                cell = Cell(row, column)
                line.append(cell)
            cells.append(line)
        return cells

    def create_location(self):
        cellLocations = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        availableCells = cellLocations
        counter = 0
        for location in availableCells:
            cell = self.cells[location[0]][location[1]]
            counter += 1
            if location == (0, 0):
                cell.location = 'topLeftCorner'
            elif location == (0, (self.columns - 1)):
                cell.location = 'topRightCorner'
            elif location == ((self.rows - 1), 0):
                cell.location = 'bottomLeftCorner'
            elif location == ((self.rows - 1), (self.columns - 1)):
                cell.location = 'bottomRightCorner'
            elif location[0] == 0:
                cell.location = 'top'
            elif location[0] == (self.rows - 1):
                cell.location = 'bottom'
            elif location[1] == 0:
                cell.location = 'left'
            elif location[1] == (self.columns - 1):
                cell.location = 'right'
            else:
                cell.location = 'middle'
            print(cell.location)

    def populate_cells(self, percentAlive):
        cellLocations = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        availableCells = cellLocations
        percent = (percentAlive / 100) * len(cellLocations)
        alive = 0
        while alive < percent:
            location = availableCells[randint(0, (len(availableCells) - 1))]
            cell = self.cells[location[0]][location[1]]
            cell.live()
            availableCells.remove(location)
            alive += 1
        return self

    def count_living(self):
        living = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].alive:
                    living += 1
        return living

    def count_neighbors(self):
        newWorld = self
        for row in self.cells:
            for cell in row:
                neighbors = 0
                if cell.location == 'topLeftCorner':
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                    print(neighbors)
                elif cell.location == 'topRightCorner':
                    if self.cells[cell.row + 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'bottomLeftCorner':
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'bottomRightCorner':
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'top':
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'bottom':
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'left':
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'right':
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                elif cell.location == 'middle':
                    if self.cells[cell.row - 1][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column].alive:
                        neighbors += 1
                    if self.cells[cell.row - 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row][cell.column - 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column + 1].alive:
                        neighbors += 1
                    if self.cells[cell.row + 1][cell.column - 1].alive:
                        neighbors += 1
                if neighbors == 2 or neighbors == 3:
                    newWorld.cells[cell.row][cell.column].live()
                else:
                    newWorld.cells[cell.row][cell.column].die()
        return newWorld

w = World(10, 10)
w.populate_cells(45)
w.create_location()
print(w)
newWorld = w.count_neighbors()
print(newWorld)