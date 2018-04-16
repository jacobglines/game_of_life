from cells import Cell
from random import *
import random


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
        self.aliveToAlive = [2, 3]
        self.deadToAlive = [3]
        self.name = 'N/A'
        self.state = 'alive'

    def __str__(self):
        s = '\n'
        for row in self.cells:
            for cell in row:
                s += str(cell)
            s += '\n'
        return s

    def create_cells(self):
        """Creates empty cells for the world"""
        #
        # The world is a list of lists
        #
        cells = []
        for row in range(self.rows):
            line = []
            for column in range(self.columns):
                cell = Cell(row, column)
                line.append(cell)
            cells.append(line)
        return cells

    def populate_cells(self, percentAlive):
        """Turns a certain percentage of cells alive"""
        cellLocations = [(row, column) for row in range(self.rows) for column in range(self.columns)]
        availableCells = cellLocations
        #
        # Instead of getting a random location every time, it is faster to shuffle
        # the list of cells and take the first cell then remove it every time
        #
        random.shuffle(availableCells)
        percent = (percentAlive / 100) * len(cellLocations)
        alive = 0
        while alive < percent:
            location = availableCells[0]
            cell = self.cells[location[0]][location[1]]
            cell.live()
            availableCells.remove(location)
            alive += 1
        return self

    def count_living(self):
        """Counts the living cells in the world"""
        living = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].alive:
                    living += 1
        return living

    def count_neighbors(self):
        """[Dish] Makes a list of neighbors for every cell in the world"""
        for row in self.cells:
            for cell in row:
                row = cell.row
                column = cell.column
                neighborList = []
                #
                # Creates the 8 possible locations for neighbors
                #
                cellLocations = {'topLeft': [row - 1, column - 1],
                                 'topMiddle': [row - 1, column],
                                 'topRight': [row -1, column + 1],
                                 'right': [row, column + 1],
                                 'bottomRight': [row + 1, column + 1],
                                 'bottomMiddle': [row + 1, column],
                                 'bottomLeft': [row + 1, column - 1],
                                 'left': [row, column - 1]}
                for location, coordinates in cellLocations.items():
                    #
                    # Checks to see if the coordinates are valid
                    # If not, the location is not added to the neighbors list
                    #
                    valid = self.coordinate_checker(coordinates)
                    if valid == True:
                        x = coordinates[0]
                        y = coordinates[1]
                        neighborList.append(self.cells[x][y])
                cell.neighbors = neighborList

    def count_neighbors_donut(self):
        """[Donut] Makes a list of neighbors for every cell in the world"""
        for row in self.cells:
            for cell in row:
                #
                # Creates a list of locations for possible neighbors
                #
                neighbors = [(-1, -1), (-1, 0), (-1, 1),
                             (0, -1),           (0, 1),
                             (1, -1),  (1, 0),  (1, 1)]
                cell.neighbors = []
                for neighbor in neighbors:
                    #
                    # Sees if location is a normal neighbor
                    # If not it wraps around, like a torus/donut, and creates a neighbor from there
                    #
                    try:
                        x = (cell.row + neighbor[0])
                        y = (cell.column + neighbor[1])
                        cell.neighbors.append(self.cells[x][y])
                    except:
                        x = (cell.row + neighbor[0]) % self.rows
                        y = (cell.column + neighbor[1]) % self.columns
                        cell.neighbors.append(self.cells[x][y])

    def coordinate_checker(self, coordinates):
        """[Dish] Sees if a location is able to be a valid neighbor"""
        valid = True
        x = coordinates[0]
        y = coordinates[1]
        #
        # If the x/y is greater or less than the number of rows/columns
        # It is not a valid location
        #
        if x < 0 or x > self.rows - 1:
            valid = False
        if y < 0 or y > self.columns - 1:
            valid = False
        return valid

    def next_cell_status(self):
        """Changes the next cells status based on the number of neighbors"""
        for row in self.cells:
            for cell in row:
                neighbors = cell.get_living_neighbors()
                cell.nextLife = False
                if cell.alive:
                    if neighbors in self.aliveToAlive:
                        cell.nextLife = True
                        #
                        # If the display is set to 'aged' this will change the repr of the cell
                        #
                        cell.timeAlive += 1
                    else:
                        cell.timeAlive = 0
                else:
                    if neighbors in self.deadToAlive:
                        cell.nextLife = True
                        cell.timeAlive += 1
                    else:
                        cell.timeAlive = 0

    def create_next_world(self):
        """Officially uses the cells next status as current status and makes a new generation"""
        for row in self.cells:
            for cell in row:
                if cell.nextLife:
                    cell.live()
                else:
                    cell.die()
        self.generation += 1

    def from_file(self, file):
        """Opens up a saved file"""
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
