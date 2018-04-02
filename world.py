from cells import Cell
from random import *


class World(list):
    def __init__(self, x, y, geometry='dish'):
        super(World, self).__init__()
        self.rows = x
        self.columns = y
        self.cells = self.create_cells()
        self.generation = 1
        #
        # Geometry can either be a dish or a donut
        #
        self.geometry = geometry
        self.name = 'N/A'

    def __str__(self):
        s = ''
        s += f'Living cells: {self.count_living()}\n'
        for row in self.cells:
            for cell in row:
                s += str(cell)
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

    def count_neighbors_donut(self):
        for row in self.cells:
            for cell in row:
                neighbors = [(-1, -1), (-1, 0), (-1, 1),
                             (0, -1),           (0, 1),
                             (1, -1),  (1, 0),  (1, 1)]
                cell.neighbors = []
                for neighbor in neighbors:
                    try:
                        x = (cell.row + neighbor[0])
                        y = (cell.column + neighbor[1])
                        cell.neighbors.append(self.cells[x][y])
                    except:
                        x = (cell.row + neighbor[0]) % self.rows
                        y = (cell.column + neighbor[1]) % self.columns
                        cell.neighbors.append(self.cells[x][y])

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
                neighbors = cell.get_living_neighbors()
                cell.nextLife = False
                if cell.alive:
                    if neighbors in [2, 3]:
                        cell.nextLife = True
                else:
                    if neighbors in [3]:
                        cell.nextLife = True

    def create_next_world(self):
        for row in self.cells:
            for cell in row:
                if cell.nextLife:
                    cell.live()
                else:
                    cell.die()
        self.generation += 1

    def from_file(self, file):
        world = []
        rows = 0
        columns = 0
        with open(r'/Users/jacobglines/Desktop/Programming/gameOfLife/{}'.format(file), 'r') as savedWorld:
            for line in savedWorld:
                row = []
                cells = line.split(',')
                for char in cells:
                    if char == '1':
                        cell = Cell(rows, columns).live()
                        row.append(cell)
                    elif char == '0':
                        cell = Cell(rows, columns)
                        row.append(cell)
                    elif char == '\n':
                        pass
                    columns += 1
                world.append(row)
                rows += 1
                finalcolumns = columns - 1
                columns = 0
        newWorld = World(rows, finalcolumns)
        newWorld.cells = world
        newWorld.name = file
        return newWorld
