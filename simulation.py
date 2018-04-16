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
        """Adds a world to the simulation"""
        self.world = World(x, y)
        self.size.append(x)
        self.size.append(y)

    def clear_world(self, name = False):
        """Clears the simualtions world"""
        self.world = None
        self.name = name
        self.size = []

    def intro(self):
        """Intro to the program"""
        print("""
 ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ███████╗    ██╗     ██╗███████╗███████╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██╔════╝    ██║     ██║██╔════╝██╔════╝
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║█████╗      ██║     ██║█████╗  █████╗  
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██╔══╝      ██║     ██║██╔══╝  ██╔══╝  
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝██║         ███████╗██║██║     ███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝ ╚═╝         ╚══════╝╚═╝╚═╝     ╚══════╝
""")
        time.sleep(1.5)

    def menu(self):
        """Prints the main menu"""
        menu = """[C]reate | [S]im | S[K]ip | [P]opulate | C[R]eations | [M]ore | [H]elp | [Q]uit"""
        print(menu)

    def more_menu(self):
        """Prints the secondary menu"""
        menu = '[S]ave | [L]oad | S[P]eed | [G]eometry | [D]isplay | [R]ules | [B]ack'
        print(menu)

    def play(self):
        """Takes an input to play the program"""
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
            #
            # Parameters skip the next step of their choice
            # Parameters expect the input to always be correct
            #
            if len(choice) > 1:
                parameter = choice[1:].strip()
            choice = choice[0].lower()
        print('')
        return choice, parameter

    def create_world(self, parameter):
        """Creates a new world"""
        if parameter != None:
            sizes = parameter.split(' ')
            rows = sizes[0]
            columns = sizes[1]
        else:
            rows = get_integer_between("How many rows do you want? ", 1, 250, 0)
            columns = get_integer_between("How many columns do you want? ", 1, 1001, 0)
        self.clear_world()
        self.add_world(int(rows), int(columns))
        self.world.create_cells()
        if self.world.geometry == 'dish':
            self.world.count_neighbors()
        elif self.world.geometry == 'donut':
            self.world.count_neighbors_donut()
        print('')

    def sim(self, parameter):
        """Simulates throught generations of the current world"""
        if self.world == None:
            print("You haven't made a world yet\n")
        elif self.world.count_living() == 0:
            print('All your cells are dead, please populate your world\n')
        else:
            if parameter!= None:
                generations = parameter
            else:
                generations = get_integer("How many generations do you want to move forward? ")
            counter = 0
            self.world.state = 'alive'
            while int(generations) > counter and self.world.count_living() > 0:
                self.world.next_cell_status()
                self.world.create_next_world()
                counter += 1
                #
                # Remove the time sleep when running speed test
                #
                time.sleep(self.speed)
                print(self.world)
            if self.world.count_living() == 0:
                print('Your cells all died at generation ', self.world.generation)
            elif self.world.state == 'stale':
                print('Your world will not change in its current state\n')
            elif self.world.state == 'blinker':
                print('All you have left is blinkers')

    def skip(self, parameter):
        """Skips a number of generations of the current world"""
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
        """Populates the world based on the users input"""
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
        """Menu to load pre-made worlds"""
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
        """Saves the current generation of the world"""
        if parameter != None:
            worldFileName = parameter
            if worldFileName[-5:] == '.life':
                pass
            else:
                worldFileName += '.life'
        else:
            #
            # There is always a world_one.life so this should trigger the next while statement
            #
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
                    #
                    # A way to write the world so that when reading, it's easy to make a cell alive or dead
                    #
                    if cell.alive == True:
                        byte = '1'
                    else:
                        byte = '0'
                    fileline += byte + ','
                fileline += '\n'
            newWorld.write(fileline)

    def load(self, worldFileName):
        """Loads previously saved worlds"""
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
        """Prints help screen"""
        print("""
This is the game of life. Each character represents a cell. You create a world
and the program will show you the generation. Cycling through generations will
kill come cells and have some come to life. Here are the rules:
        
        Living Cells                    Dead Cells
        
        0-1 living neighbors: Dead      0-2 living neighbors = Dead
        2-3 living neighbors: Alive     3 living neighbors = Alive
        4-8 living neighbors: Dead      4-8 living neighbors = Dead
        
Command Menu
To use the command menu, type in the letter in the brackets and press enter.

c : Creates a new world
s : Simulates the world and moves through generations
k : Skip through generations without displaying them
p : Populate your world with living cells
r : Pre-made worlds that come with cool designs
m : Displays a menu full of more commands
    s : Save your world
    l : Load an already saved world
    p : Change the speed of the simulation
    g : Change the geometry of the world to either dish or torus
    d : Change the displays of the world
        l : Change the living cells appearance
        d : Change the dead cells appearance
        a : Change from normal display or aged display
    b : Goes back to the main menu
q : Quits the program

""")

    def show_worlds(self):
        """Prints the names of files already saved"""
        worlds = os.listdir(path='/Users/jacobglines/Desktop/Programming/gameOfLife')
        for file in worlds:
            if file[-5:] == '.life':
                print(file)

    def geometry(self):
        """Changes the geometry of the world"""
        choice = 'x'
        while choice not in ['dish', 'donut']:
            choice = input('Dish or Donut? ').lower()
        self.world.geometry = choice
        if self.world.geometry == 'dish':
            self.world.count_neighbors()
        elif self.world.geometry == 'donut':
            self.world.count_neighbors_donut()

    def status_bar(self):
        """Status bar of the world generation"""
        s = f'Size: {self.world.rows}x{self.world.columns} | Gen: {self.world.generation} | ' \
            f'Name: {self.world.name} | Alive: {self.get_percent():0.0f}% | ' \
            f'Geometry: {self.world.geometry} | Speed: {self.speed}\n'
        print(s)

    def play_menu(self):
        """Secondary play menu that gets inputs to run the program"""
        parameter = None
        plays = {'s': '[S]ave',
                 'l': '[L]oad',
                 'p': 'S[P]eed',
                 'g': '[G]eometry',
                 'd': '[D]isplay',
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
        """Secondary commands loop"""
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
        elif choice == 'd':
            self.change_display()
        elif choice == 'r':
            self.change_rules()

    def change_display(self):
        """Changes the displays cell appearances"""
        print('[L]iving | [D]ead | [A]ge')
        choice = 'x'
        choiceInputs = ['l', 'd', 'a']
        while choice not in choiceInputs:
            choice = input().lower()
        if choice == 'l':
            self.change_living()
        elif choice == 'd':
            self.change_dead()
        elif choice == 'a':
            self.change_age()

    def change_living(self):
        """Changes the living cells appearance"""
        alive = input('What do you want the living character to be? ')
        for row in self.world.cells:
            for cell in row:
                cell.livingChar = alive

    def change_dead(self):
        """Changes the dead cells appearance"""
        dead = input('What do you want the dead character to be? ')
        for row in self.world.cells:
            for cell in row:
                cell.deadChar = dead

    def change_age(self):
        """Changes the way the cells look based on age of the cells"""
        choice = get_yes_no("Would you like to switch the display?")
        if choice == 'yes':
            if self.world.cells[0][0].display == 'normal':
                for row in self.world.cells:
                    for cell in row:
                        cell.display = 'aged'
            elif self.world.cells[0][0].display == 'aged':
                for row in self.world.cells:
                    for cell in row:
                        cell.display = 'normal'

    def change_rules(self):
        """Changes the rules for alive and dead cells"""
        aliveNeighbors = []
        deadNeighbors = []
        print('Please enter numbers 0-7 for how many living neighbors an alive cells needs to stay alive'
              '\n[When done, type: done]')
        number = 'x'
        while number != 'done':
            number = input()
            #
            # If entered number is an integer, it will append it
            # otherwise it just passes and does nothing
            #
            try:
                numb = int(number)
                aliveNeighbors.append(numb)
            except:
                pass
        print('Please enter numbers 0-7 for how many living neighbors an dead cells needs to come alive'
              '\n[When done, type: done]')
        number = 'x'
        while number != 'done':
            number = input()
            try:
                numb = int(number)
                deadNeighbors.append(numb)
            except:
                pass
        self.world.aliveToAlive = aliveNeighbors
        self.world.deadToAlive = deadNeighbors

    def set_speed(self, parameter):
        """Changes the speed of simulation"""
        if parameter != None:
            self.speed = int(parameter)
        else:
            number = False
            while not number:
                speed = input('How fast do you want to simulate? (lower is faster. Default is 0.25) ')
                number = is_number(speed)
            self.speed = float(speed)

    def get_percent(self):
        """Gets percent of alive cells for the generation"""
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
    """Tests the speed of the program"""
    sim = Simulation()
    sim.create_world('200 900')
    print('hello')
    sim.world.count_neighbors_donut()
    print('hello')
    sim.populate_world(50)
    print(sim.world)

main()
#speed_test()
#
# When running speed_test, paste this in terminal, python3 -m cProfile simulation.py
#