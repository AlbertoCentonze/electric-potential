from graphics import *
import numpy as np
import time

class PotentialGrid:
    potential = np.zeros((0, 0))
    locked = np.zeros((0, 0))
    gridLength = 0

    def __init__(self, gridLength, cDistance, cLength):
        self.gridLength = gridLength 
        self.potential = np.zeros((gridLength * 2, gridLength * 2))
        self.locked = np.zeros((gridLength * 2, gridLength * 2))
        for x in range(0, 2 * gridLength):
            for y in range(0, 2 * gridLength):
                if x == (gridLength - cDistance) - 1 and y >= (gridLength - cLength) and y <= (gridLength + cLength) - 1: #condensatore carico positivamente e blocco il potenziale
                    self.potential[x, y] = 10
                    self.locked[x, y] = 1
                elif x == (gridLength + cDistance) and y >= (gridLength - cLength) and y <= (gridLength + cLength) - 1: #condensatore carico negativamente e blocco il potenziale
                    self.potential[x, y] = -10
                    self.locked[x, y] = 1
                elif x == 0 or x == (2 * gridLength) - 1 or y == 0 or y == (2 * gridLength) - 1:  #blocco il potenziale a 0 al bordo della griglia (distanza infinita dalle piastre)
                    self.locked[x, y] = 1


    def Update(self):
        for x in range(0, 2 * self.gridLength):
            for y in range(0, 2 * self.gridLength):
                if self.locked[x, y]:
                    pass
                else:
                    self.potential[x, y] = ( self.potential[x + 1, y] + self.potential[x - 1, y] + self.potential[x, y + 1] + self.potential[x, y - 1] ) * .25
        


gridSideLength = 25
ourGrid = PotentialGrid(gridSideLength, 8, 5)

winX, winY = 1000, 1000
win = GraphWin("Ponteziale elettrico", winX, winY)
win.setBackground("black")
win.setCoords(-5, -5, (gridSideLength * 2) + 5, (gridSideLength * 2) + 5)


i = 0
while i < 10000:
    ourGrid.Update()
    i += 1
    print("iteration n. " + str(i))
    if i > 9000:

        for x in range(0, 2 * ourGrid.gridLength):
                for y in range(0, 2 * ourGrid.gridLength):
                    c = Circle(Point(x, y), .3)
                    c.setOutline("white")
                    c.draw(win)
                    if ourGrid.potential[x, y] > 0:
                        c.setFill("orange")
                    if ourGrid.potential[x, y] > 2:
                        c.setFill("red")
                    if ourGrid.potential[x, y] < 0:
                        c.setFill("cyan")
                    if ourGrid.potential[x, y] < -2:
                        c.setFill("blue")
                    if ourGrid.locked[x, y]:
                        c.setFill("white")

while True:
    time.sleep(5)