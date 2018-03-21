from world import World
import time


class Simulation(object):
    def __init__(self, name=False):
        self.world = None
        self.name = name
        self.size = []

    def add_world(self, x, y):
        self.world = World(x, y)
        self.size.append(x)
        self.size.append(y)


def test():
    sim = Simulation()
    sim.add_world(10, 10)
    sim.world.populate_cells(40)
    sim.world.count_neighbors()
    while sim.world.count_living() > 0:
        print(sim.world)
        sim.world.next_cell_status()
        sim.world.create_next_world()
        time.sleep(0.2)
    print(sim.world)


test()
