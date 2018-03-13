import unittest
from world import World
from cells import Cell


class WorldTestCase(unittest.TestCase):

    def test_constructor(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)
        self.assertEqual(10, world.columns)

    def test_row(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)

    def test_columns(self):
        world = World(10, 5)
        self.assertEqual(5, world.columns)

    def test_string(self):
        world = World(0, 0)
        alive = Cell(True)
        dead = Cell(False)
        world.cells = [[alive, dead], [dead, alive]]
        self.assertEqual(str(world), f'| 0 | - | \n| - | 0 | \n')


if __name__ == '__main__':
    unittest.main()
