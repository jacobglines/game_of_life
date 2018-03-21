import unittest
from cells import Cell
from world import World


class CellTestCase(unittest.TestCase):

    def test_create_cell(self):
        row = 1
        column = 2
        cell = Cell(row, column)
        self.assertEqual(cell.alive, False)
        self.assertEqual(cell.row, row)
        self.assertEqual(cell.column, column)

    def test_dead_cells(self):
        cell = Cell(0, 0)
        cell.die()
        self.assertFalse(cell.alive)

    def test_live_cells(self):
        cell = Cell(0, 0)
        cell.live()
        self.assertTrue(cell.alive)

    def test_str(self):
        cell = Cell(0, 0)
        cell.live()
        self.assertEqual(u'\u25A0', str(cell))
        cell.die()
        self.assertEqual(u'\u25A1', str(cell))

    def test_living_neighbors(self):
        rows = 3
        columns = 3
        w = World(rows, columns)
        w.populate_cells(100)
        w.count_neighbors()
        w.next_cell_status()
        w.create_next_world()
        cell = w.cells[0][0]
        living = cell.get_living_neighbors()
        self.assertEqual(living, 0)
        cell2 = w.cells[1][1]
        living2 = cell2.get_living_neighbors()
        self.assertEqual(living2, 4)


if __name__ == '__main__':
    unittest.main()
