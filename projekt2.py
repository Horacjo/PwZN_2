import argparse
import math
import random
import time
import numpy as np
import rich.traceback
from rich.console import Console
from rich.progress import track
from PIL import Image, ImageDraw


#Sekcja parametrów skryptu
parser = argparse.ArgumentParser(description="Opis:")
parser.add_argument('number', help = "Użytkowniku podaj rozmiar siatki", type = int, default=5)
parser.add_argument('j', help = "Użytkowniku podaj wartość J", type = float)
parser.add_argument('b', help = "Użytkowniku podaj wartość parametru b", type = float)
parser.add_argument('H', help = "Użytkowniku podaj wartość pola H", type = float)
parser.add_argument('steps', help = "Użytkowniku podaj liczbę kroków symulacji jaką chcesz wykonać", type = int, default=10)
parser.add_argument('-d','--density', help = "Użytkowniku podaj początkową gęstość spinów", type = float, default=1.0)
parser.add_argument('-f', '-file',help = "Użytkowniku podaj nazwę pliku z obrazkiem", type = str, default='step')
args = parser.parse_args()

print(f'Grid size: {args.number}')
print(f'J value: {args.j}')
print(f'B value: {args.b}')
print(f'Hamiltonian value: {args.H}')
print(f'Number of steps: {args.steps}')
print(f'Spin density: {args.density}')
print(f'FILE name: {args.f}')

def do_some_work():
    time.sleep(0.1)

#Klasa symulacja
class simulation:
    def __init__(self,size,jVal,BVal,hVal,spinDensity, file) -> None:
        self.state = np.random.choice([-spinDensity, spinDensity], size=(size, size))
        self.size = size
        self.jVal = jVal
        self.BVal = BVal
        self.hVal = hVal
        self.file = file
        self.index = 0
    
    def energy(self):
        h_influence = 0
        h_spin = 0

        for x in range(self.size):
            for y in range(self.size):
                h_influence += -self.jVal * self.state[x, y] * ((self.state[x][y-1] if y-1 >= 0 else 0) + 
                                                                 (self.state[x][y+1] if y+1 < self.size else 0) +
                                                                 (self.state[x-1][y] if x-1 >= 0 else 0) +
                                                                 (self.state[x+1][y] if x+1 < self.size else 0))
                h_spin += -(self.hVal * self.state[x, y])

        print(f'{h_influence = }, {h_spin = }, {h_spin + h_influence = }') 
        return h_influence + h_spin

    def step(self):
        e1 = sim.energy()
        x = random.randint(0,len(self.state)-1)
        y = random.randint(0,len(self.state)-1)
    
        self.state[x,y] = -self.state[x,y]
        e2 = sim.energy()
    
        dE = e2 - e1
        if dE > 0:
            pr = random.random()
            if pr < math.e ** (-dE*self.BVal):
                self.__pictureGenerator__()
                self.index +=1 
            else:
                self.state[x,y] = -self.state[x,y]
        else:
            self.__pictureGenerator__()
            self.index +=1 

    def __pictureGenerator__(self):
        self.image = Image.fromarray(np.uint8(self.state), mode = 'L')
        self.image.save(self.file + str(self.index)+'.jpg')

console = Console()
console.clear()

#sim = simulation(100, 1, 1, 1, 1.0)
sim = simulation(args.number, args.j, args.b, args.H, args.density, args.f)
print(sim.state)

for i in track(range(args.steps)):
    sim.step()
    do_some_work()
sim.image.show()
