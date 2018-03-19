import unittest
from world import World
from cells import Cell


class WorldTestCase(unittest.TestCase):

    def test_constructor(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)
        self.assertEqual(10, world.columns)
        for row in range(world.rows):
            for column in range(world.columns):
                self.assertFalse(world.cells[row][column].alive)
                self.assertEqual(world.cells[row][column].row, row)
                self.assertEqual(world.cells[row][column].column, column)

    def test_row(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)

    def test_columns(self):
        world = World(10, 5)
        self.assertEqual(5, world.columns)

    def test_str(self):
        world = World(0, 0)
        alive = Cell(0, 0)
        alive.live()
        dead = Cell(0, 1)
        world.cells = [[alive, dead], [dead, alive]]
        self.assertEqual(str(world), f'| 0 | - | \n| - | 0 | \n')

    def test_populate(self):
        rows = 10
        columns = 10
        w = World(rows, columns)
        w.populate_cells(0)
        self.assertEqual(w.count_living(), 0)
        w.populate_cells(50)
        self.assertEqual(w.count_living(), 50)
        w.populate_cells(100)
        self.assertEqual(w.count_living(), 100)


    def test_count_living(self):
        w = World(10, 10)
        living = 30
        w.populate_cells(living)
        self.assertEqual(living, w.count_living())



if __name__ == '__main__':
    unittest.main()
