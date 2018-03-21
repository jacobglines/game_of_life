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
            for cell in row:
                s += str(cell)
                s += ' '
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
        for row in self.cells:
            for cell in row:
                row = cell.row
                column = cell.column
                neighborList = []
                cellLocations = {'topLeft': [row - 1, column - 1],
                                 'topMiddle': [row - 1, column],
                                 'topRight': [row -1, column + 1],
                                 'right': [row, column + 1],
                                 'bottomRight': [row + 1, column + 1],
                                 'bottomMiddle': [row + 1, column],
                                 'bottomLeft': [row + 1, column - 1],
                                 'left': [row, column - 1]}
                for location, coordinates in cellLocations.items():
                    valid = self.coordinate_checker(coordinates)
                    if valid == True:
                        x = coordinates[0]
                        y = coordinates[1]
                        neighborList.append(self.cells[x][y])
                cell.neighbors = neighborList

    def coordinate_checker(self, coordinates):
        valid = True
        x = coordinates[0]
        y = coordinates[1]
        if x < 0 or x > self.rows - 1:
            valid = False
        if y < 0 or y > self.columns - 1:
            valid = False
        return valid

    def next_cell_status(self):
        for row in self.cells:
            for cell in row:
                if cell.get_living_neighbors() <= 1 and cell.alive == True:
                    cell.nextLife = False
                elif cell.get_living_neighbors() in [2,3] and cell.alive == True:
                    cell.nextLife = True
                elif cell.get_living_neighbors() in [4,5,6,7,8] and cell.alive == True:
                    cell.nextLife = False
                elif cell.get_living_neighbors() == 3 and cell.alive == False:
                    cell.nextLife = True
                else:
                    cell.nextLife = False

    def create_next_world(self):
        for row in self.cells:
            for cell in row:
                if cell.nextLife:
                    cell.live()
                else:
                    cell.die()
