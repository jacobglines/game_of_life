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
        self.assertEqual(str(world), u'\u25A0 \u25A1 \n\u25A1 \u25A0 \n')

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

    def test_neighbors(self):
        rows = 3
        columns = 3
        w = World(rows, columns)
        w.populate_cells(100)
        w.count_neighbors()
        cell = w.cells[0][0]
        self.assertEqual(len(cell.neighbors), 3)
        cell2 = w.cells[0][1]
        self.assertEqual(len(cell2.neighbors), 5)
        cell3 = w.cells[1][1]
        self.assertEqual(len(cell3.neighbors), 8)

    def test_next_life(self):
        rows = 3
        columns = 3
        w = World(rows, columns)
        w.populate_cells(100)
        w.count_neighbors()
        w.next_cell_status()
        cell = w.cells[0][0]
        self.assertEqual(cell.nextLife, True)
        cell2 = w.cells[1][1]
        self.assertEqual(cell2.nextLife, False)

    def test_next_worlds(self):
        rows = 3
        columns = 3
        w = World(rows, columns)
        w.populate_cells(100)
        w.count_neighbors()
        w.next_cell_status()
        w.create_next_world()
        self.assertEqual(str(w), u"\u25A0 \u25A1 \u25A0 \n"
                                 u"\u25A1 \u25A1 \u25A1 \n"
                                 u"\u25A0 \u25A1 \u25A0 \n")
        w.next_cell_status()
        w.create_next_world()
        self.assertEqual(str(w), u"\u25A1 \u25A1 \u25A1 \n"
                                 u"\u25A1 \u25A1 \u25A1 \n"
                                 u"\u25A1 \u25A1 \u25A1 \n")


if __name__ == '__main__':
    unittest.main()
