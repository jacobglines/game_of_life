from world import World

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
    sim.add_world(5, 10)
    print(str(sim.world))

test()