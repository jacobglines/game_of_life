import unittest
from cells import Cell

class CellTestCase(unittest.TestCase):
    def test_constructor(self):
        cell = Cell(True)
        self.assertTrue(cell.living)

    def test_string(self):
        cell = Cell(True)
        self.assertEqual('0', str(cell))
        cell.living = False
        self.assertEqual('x', str(cell))

if __name__ == '__main__':
    unittest.main()