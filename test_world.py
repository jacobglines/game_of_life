import unittest
from world import World
from cells import Cell

class WorldTestCase(unittest.TestCase):
    def test_constructor(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)
        self.assertEqual(10, world.columns)

    def test_rows(self):
        world = World(5, 10)
        self.assertEqual(5, world.rows)

    def test_columns(self):
        world = World(10, 5)
        self.assertEqual(5, world.columns)

if __name__ == '__main__':
    unittest.main()
