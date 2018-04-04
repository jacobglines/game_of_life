from world import World
import time
import os
from toolbox import get_integer, get_integer_between, is_number, get_yes_no


class Simulation(object):
    def __init__(self, name=False):
        self.world = None
        self.name = name
        self.size = []
        self.speed = 0.25

    def add_world(self, x, y):
        self.world = World(x, y)
        self.size.append(x)
        self.size.append(y)

    def clear_world(self, name = False):
        self.world = None
        self.name = name
        self.size = []

    def intro(self):
        print("""
 ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗    ██╗     ██╗███████╗███████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██╔════╝    ██║     ██║██╔════╝██╔════╝
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║█████╗      ██║     ██║█████╗  █████╗  
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝      ██║     ██║██╔══╝  ██╔══╝  
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║         ███████╗██║██║     ███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝         ╚══════╝╚═╝╚═╝     ╚══════╝
""")
        time.sleep(2)

    def menu(self):
        menu = """[C]reate | [S]im | S[K]ip | [P]opulate | C[R]eations | [M]ore | [H]elp | [Q]uit"""
        print(menu)

    def more_menu(self):
        menu = '[S]ave | [L]oad | S[P]eed | [G]eometry | [C]haracters | [B]ack'
        print(menu)

    def play(self):
        parameter = None
        plays = {'c': '[C]reate',
               's': '[S]im',
               'k': 'S[K]ip',
               'p': '[P]opulate',
               'r': 'C[R]eations',
               'm': '[M]ore',
               'h': '[H]elp',
               'q': '[Q]uit'}
        self.menu()
        menuChoices = plays.keys()
        choice = 'x'
        while choice not in menuChoices:
            choice = input()
            if len(choice) > 1:
                parameter = choice[1:].strip()
            choice = choice[0].lower()
        print('')
        return choice, parameter

    def create_world(self, parameter):
        if parameter != None:
            sizes = parameter.split(' ')
            rows = sizes[0]
            columns = sizes[1]
        else:
            rows = get_integer_between("How many rows do you want? ", 1, 100, 0)
            columns = get_integer_between("How many columns do you want? ", 1, 100, 0)
        self.clear_world()
        self.add_world(int(rows), int(columns))
        self.world.create_cells()
        if self.world.geometry == 'dish':
            self.world.count_neighbors()
        elif self.world.geometry == 'donut':
            self.world.count_neighbors_donut()
        print('')

    def sim(self, parameter):
        if self.world == None:
            print("You haven't made a world yet\n")
        elif self.world.count_living() == 0:
            print('All your cells are dead, please populate your world\n')
        else:
            if parameter != None:
                generations = parameter
            else:
                generations = get_integer("How many generations do you want to move forward? ")
            counter = 0
            while int(generations) > counter and self.world.count_living() > 0:
                self.world.next_cell_status()
                self.world.create_next_world()
                counter += 1
                #
                # Remove the time sleep when running speed test
                #
                # time.sleep(self.speed)
                # print(self.world)
            if self.world.count_living() == 0:
                print('Your cells all died at generation ', self.world.generation)

    def skip(self, parameter):
        if self.world == None:
            print("You haven't made a world yet")
        elif self.world.count_living() == 0:
            print('All your cells are dead, please populate your world')
        else:
            if parameter != None:
                generations = parameter
            else:
                generations = get_integer("How many generations do you want to skip? ")
            counter = 0
            while int(generations) > counter and self.world.count_living() > 0:
                self.world.next_cell_status()
                self.world.create_next_world()
                counter += 1
            if self.world.count_living() == 0:
                print('Your cells all died at generation ', self.world.generation)

    def populate_world(self, parameter):
        if self.world == None:
            print("You haven't made a world yet")
        else:
            if parameter != None:
                percent = parameter
            else:
                percent = get_integer_between("What percentage do you want to be alive? ", 0, 100, 101)
            for row in self.world.cells:
                for cell in row:
                    cell.die()
            self.world.populate_cells(int(percent))

    def load_pattern(self):
        print('[L]etter L | [G]lider | [S]paceship | [P]entadecatalon | P[U]lsar\n')
        choices = ['l', 'g', 's', 'p', 'u']
        choice = 'x'
        while choice not in choices:
            choice = input('Which patter would you like to load? ').lower()
        if choice == 'l':
            pattern = 'Creations/letter_l.life'
        elif choice == 'g':
            pattern = 'Creations/glider.life'
        elif choice == 's':
            pattern = 'Creations/spaceship.life'
        elif choice == 'p':
            pattern = 'Creations/pentadecathalon.life'
        elif choice == 'u':
            pattern = 'Creations/pulsar.life'
        self.load(pattern)

    def save_world(self, parameter):
        if parameter != None:
            worldFileName = parameter
            if worldFileName[-5:] == '.life':
                pass
            else:
                worldFileName += '.life'
        else:
            worldFileName = 'world_one.life'
        fileNames = os.listdir(path='/Users/jacobglines/Desktop/Programming/gameOfLife')
        while worldFileName in fileNames:
            worldFileName = input("What would you like to save this world as? ")
            if worldFileName[-5:] == '.life':
                pass
            else:
                worldFileName += '.life'
        with open(r'/Users/jacobglines/Desktop/Programming/gameOfLife/{}'.format(worldFileName), 'w+') as newWorld:
            fileline = ''
            for line in self.world.cells:
                for cell in line:
                    if cell.alive == True:
                        byte = '1'
                    else:
                        byte = '0'
                    fileline += byte + ','
                fileline += '\n'
            newWorld.write(fileline)

    def load(self, worldFileName):
        #
        # To add more creations, comment out the requirements for it to be a .life file
        #
        if worldFileName[-5:] == '.life':
            pass
        else:
            worldFileName += '.life'
        self.clear_world()
        world = World.from_file(self, worldFileName)
        self.world = world
        if self.world.geometry == 'dish':
            self.world.count_neighbors()
        elif self.world.geometry == 'donut':
            self.world.count_neighbors_donut()

    def help_screen(self):
        print("""
This game of life program is deigned based on the idea of the life of cells. If a dead cell has 3 alive neighbors,
it too becomes alive. If an alive cell has 2 or 3 alive cells next to it, it will stay alive. But if an live cell
has 0-1 or 4-8 alive neighbors, it dies from either overpopulation or not enough. In this program you are able to
create a new world, adjusting rows, columns, and the population. You can also move forward generations.
You can import interesting premade shapes, and if you so choose, you can save and load in different worlds.
""")

    def show_worlds(self):
        worlds = os.listdir(path='/Users/jacobglines/Desktop/Programming/gameOfLife')
        for file in worlds:
            if file[-5:] == '.life':
                print(file)

    def geometry(self):
        choice = 'x'
        while choice not in ['dish', 'donut']:
            choice = input('Dish or Donut? ').lower()
        self.world.geometry = choice
        if self.world.geometry == 'dish':
            self.world.count_neighbors()
        elif self.world.geometry == 'donut':
            self.world.count_neighbors_donut()

    def status_bar(self):
        s = f'Size: {self.world.rows}x{self.world.columns} | Gen: {self.world.generation} | ' \
            f'Name: {self.world.name} | Alive: {self.get_percent():0.0f}% | ' \
            f'Geometry: {self.world.geometry} | Speed: {self.speed}\n'
        print(s)

    def play_menu(self):
        parameter = None
        plays = {'s': '[S]ave',
                 'l': '[L]oad',
                 'p': 'S[P]eed',
                 'g': '[G]eometry',
                 'c': '[C]haracters',
                 'r': '[R]ules',
                 'b': '[B]ack'}
        self.more_menu()
        menuChoices = plays.keys()
        choice = 'x'
        while choice not in menuChoices:
            choice = input()
            if len(choice) > 1:
                parameter = choice[1:].strip()
            else:
                parameter = None
            choice = choice[0].lower()
        print('')
        return choice, parameter

    def more_menu_play(self):
        print(self.world)
        self.status_bar()
        choice, parameter = self.play_menu()
        if choice == 's':
            self.save_world(parameter)
        elif choice == 'l':
            if parameter != None:
                worldFileName = parameter
            else:
                self.show_worlds()
                worldFileName = input('Which file would you like to open? ')
            self.load(worldFileName)
        elif choice == 'g':
            self.geometry()
        elif choice == 'p':
            self.set_speed(parameter)
        elif choice == 'c':
            self.change_character()
        elif choice == 'r':
            self.change_rules()

    def change_rules(self):
        choice = get_yes_no('Do you want to see the current rules? ')
        if choice == 'yes':
            pass
            #
            # TODO create a rules help menu .txt and print it
            #


    def change_character(self):
        alive = input('What do you want the living character to be? ')
        dead = input('What do you want the dead character to be? ')
        for row in self.world.cells:
            for cell in row:
                cell.deadChar = dead
                cell.livingChar = alive

    def set_speed(self, parameter):
        if parameter != None:
            self.speed = int(parameter)
        else:
            number = False
            while not number:
                speed = input('How fast do you want to simulate? (lower is faster. Default is 0.25) ')
                number = is_number(speed)
            self.speed = float(speed)

    def get_percent(self):
        cellLocations = [(row, column) for row in range(self.world.rows) for column in range(self.world.columns)]
        living = 0
        for row in self.world.cells:
            for cell in row:
                if cell.alive:
                    living += 1
        percent = 100 * (living / len(cellLocations))
        return percent

def main():
    sim = Simulation()
    sim.intro()
    sim.add_world(30, 70)
    sim.world.populate_cells(35)
    sim.world.count_neighbors()
    play = True
    while play == True:
        print(sim.world)
        sim.status_bar()
        choice, parameter = sim.play()
        if choice == 'c':
            sim.create_world(parameter)
        elif choice == 's':
            sim.sim(parameter)
        elif choice == 'k':
            sim.skip(parameter)
        elif choice == 'p':
            sim.populate_world(parameter)
        elif choice == 'r':
            sim.load_pattern()
        elif choice == 'a':
            sim.save_world(parameter)
        elif choice == 'l':
            if parameter != None:
                worldFileName = parameter
            else:
                sim.show_worlds()
                worldFileName = input('Which file would you like to open? ')
            sim.load(worldFileName)
        elif choice == 'm':
            sim.more_menu_play()
        elif choice == 'h':
            sim.help_screen()
        elif choice == 'q':
            play = False

def speed_test():
    sim = Simulation()
    sim.create_world('200 900')
    print('hello')
    sim.world.count_neighbors_donut()
    print('hello')
    sim.populate_world(50)
    print(sim.world)

#main()
speed_test()
#
# TODO get help on 1.7 (confirmation)
#
# TODO how do I convert a string of a unicode character to actual unicode (in change_character())
#
# TODO update help page(s)
#