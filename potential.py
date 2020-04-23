from graphics import *
import numpy as np
import time


class PotentialGrid:
    potential = np.zeros((0, 0, 0))
    locked = np.zeros((0, 0, 0))
    gridLength = 0

    def __init__(self, gridLength, cDistance, cLength, cHeight):
        self.gridLength = gridLength
        self.potential = np.zeros(
            (gridLength * 2, gridLength * 2, gridLength * 2))
        self.locked = np.zeros(
            (gridLength * 2, gridLength * 2, gridLength * 2))
        for z in range(0, 2 * gridLength):
            for x in range(0, 2 * gridLength):
                for y in range(0, 2 * gridLength):
                    # condensatore carico positivamente e blocco il potenziale
                    if x == (gridLength - cDistance) - 1 and y >= (gridLength - cLength) and y <= (gridLength + cLength) - 1 and z >= (gridLength - cHeight) and z <= (gridLength + cHeight):
                        self.potential[x, y, z] = 10
                        self.locked[x, y, z] = 1
                    # condensatore carico negativamente e blocco il potenziale
                    elif x == (gridLength + cDistance) and y >= (gridLength - cLength) and y <= (gridLength + cLength) - 1 and z >= (gridLength - cHeight) and z <= (gridLength + cHeight):
                        self.potential[x, y, z] = -10
                        self.locked[x, y, z] = 1
                    # blocco il potenziale a 0 al bordo della griglia (distanza infinita dalle piastre)
                    elif x == 0 or x == (2 * gridLength) - 1 or y == 0 or y == (2 * gridLength) - 1 or z == 0 or z == (2 * gridLength) - 1:
                        self.locked[x, y, z] = 1

    def writePotential(self, fileName, absolute = False):

        out = open(fileName, "w")

        for x in range(0, 2 * self.gridLength):
            for y in range(0, 2 * self.gridLength):
                for z in range(0, 2 * self.gridLength):
                    potential = str(abs(self.potential[x, y, z])) if absolute else str(self.potential[x, y, z])
                    out.write(str(x) + " " + str(y) + " " + str(z) + " " +
                              potential + "\n")
            out.write("\n")
        out.close()
    
    def writeLocked(self, fileName):
        out = open(fileName, "w")

        for x in range(0, 2 * self.gridLength):
            for y in range(0, 2 * self.gridLength):
                for z in range(0, 2 * self.gridLength):
                    if self.locked[x, y, z]:
                        out.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            out.write("\n")
        out.close()

    def writeCapacitor(self, fileName):
        out = open(fileName, "w")

        for x in range(0, 2 * self.gridLength):
            for y in range(0, 2 * self.gridLength):
                for z in range(0, 2 * self.gridLength):
                    if self.locked[x, y, z] and abs(self.potential[x, y, z]) == 10:
                        out.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            out.write("\n")
        out.close()


    def update(self, iterationsNumber):
        iteration = 0
        while iteration < iterationsNumber:
            for x in range(0, 2 * self.gridLength):
                for y in range(0, 2 * self.gridLength):
                    for z in range(0, 2 * self.gridLength):
                        if self.locked[x, y, z]:
                            pass
                        else:
                            self.potential[x, y, z] = (self.potential[x + 1, y, z] + self.potential[x - 1, y, z] +
                                                       self.potential[x, y + 1, z] + self.potential[x, y - 1, z] + self.potential[x, y, z + 1] + self.potential[x, y, z - 1]) / 6
            iteration += 1

    def showGraph2D(self, z): # z è l'altezza a cui viene sezionato il piano tridimensionale
        winX, winY = 1000, 1000
        win = GraphWin("Ponteziale elettrico", winX, winY)
        win.setBackground("black")
        win.setCoords(-5, -5, (self.gridLength * 2) +
                      5, (self.gridLength * 2) + 5)

        for x in range(0, 2 * self.gridLength):
            for y in range(0, 2 * self.gridLength):
                c = Circle(Point(x, y), .3)
                c.setOutline("white")
                c.draw(win)
                if self.potential[x, y, z] > 0:
                    c.setFill("orange")
                if self.potential[x, y, z] > 2:
                    c.setFill("red")
                if self.potential[x, y, z] < 0:
                    c.setFill("cyan")
                if self.potential[x, y, z] < -2:
                    c.setFill("blue")
                if self.locked[x, y, z]:
                    c.setFill("white")

        while True:
            time.sleep(5)


ourGrid = PotentialGrid(10, 2, 4, 5)
ourGrid.update(700)
ourGrid.writePotential("potential.fas") # la vecchia funzione che aveva scritto lei
ourGrid.writePotential("abs-potential.fas", True) # stessa cosa ma coi valori assoluti (utile per grafico)
ourGrid.writeCapacitor("capacitor.fas") # grafico del condensatore nello spazio (senza potenziale)
ourGrid.writeLocked("locked.fas") # grafico dei punti bloccati nello spazio
ourGrid.showGraph2D(10) # sezione a metà del cubo per vedere il potenziale in 2d e non buttare del "buon" codice