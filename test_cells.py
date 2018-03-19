import unittest
from cells import Cell


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
        self.assertEqual('0', str(cell))
        cell.die()
        self.assertEqual('-', str(cell))


if __name__ == '__main__':
    unittest.main()
