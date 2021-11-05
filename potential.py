import numpy as np
import numpy.typing as npt


class Plate:
    pass


class PotentialGrid:
    """Class representing a 3D grid with a capacitor  inside"""

    def set_cell(self, x: int, y: int, z: int, value: int = None, lock: bool = False):
        """Allows to set the potential for a specific point of the grid and eventually lock it"""
        if x < 0 or y < 0 or z < 0:
            raise ValueError("One or more coordinates are negative")
        if value is not None:
            self.potential[x, y, z] = value
        self.locked[x, y, z] = int(lock)

    def __init__(self, grid_length: int, distance: int, width: int, height: int):
        self.grid_length: npt.ArrayLike = grid_length
        self.potential: npt.ArrayLike = np.zeros(
            (grid_length * 2, grid_length * 2, grid_length * 2))
        self.locked = np.zeros(
            (grid_length * 2, grid_length * 2, grid_length * 2))
        for z in range(0, 2 * grid_length):
            for x in range(0, 2 * grid_length):
                for y in range(0, 2 * grid_length):
                    # positively charged + blocked potential
                    if x == (grid_length - distance) - 1 and (grid_length - width) <= y <= (
                            grid_length + width) - 1 and (
                            grid_length - height) <= z <= (grid_length + height):
                        self.set_cell(x, y, z, value=10, lock=True)
                    # negatively charged + blocked potential
                    elif x == (grid_length + distance) and (grid_length - width) <= y <= (
                            grid_length + width) - 1 and (
                            grid_length - height) <= z <= (grid_length + height):
                        self.set_cell(x, y, z, value=-10, lock=True)
                    # block edges potential
                    elif x == 0 or x == (2 * grid_length) - 1 or y == 0 or y == (
                            2 * grid_length) - 1 or z == 0 or z == (2 * grid_length) - 1:
                        self.set_cell(x, y, z, lock=True)

    def write_potential(self, file_name: str, absolute: bool = False):

        out = open(file_name, "w")

        for x in range(0, 2 * self.grid_length):
            for y in range(0, 2 * self.grid_length):
                for z in range(0, 2 * self.grid_length):
                    potential = abs(self.potential[x, y, z]) if absolute else self.potential[x, y, z]
                    out.write(f"{x} {y} {z} {potential} \n")
            out.write("\n")
        out.close()

    def write_locked(self, file_name: str):
        out = open(file_name, "w")

        for x in range(0, 2 * self.grid_length):
            for y in range(0, 2 * self.grid_length):
                for z in range(0, 2 * self.grid_length):
                    if self.locked[x, y, z]:
                        out.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            out.write("\n")
        out.close()

    def write_capacitor(self, file_name: str):
        out = open(file_name, "w")

        for x in range(0, 2 * self.grid_length):
            for y in range(0, 2 * self.grid_length):
                for z in range(0, 2 * self.grid_length):
                    if self.locked[x, y, z] and abs(self.potential[x, y, z]) == 10:
                        out.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            out.write("\n")
        out.close()

    def update(self, iterations: int):
        for i in range(iterations):
            for x in range(2 * self.grid_length):
                for y in range(2 * self.grid_length):
                    for z in range(2 * self.grid_length):
                        if self.locked[x, y, z]:
                            pass
                        else:
                            self.potential[x, y, z] = (self.potential[x + 1, y, z] + self.potential[x - 1, y, z] +
                                                       self.potential[x, y + 1, z] + self.potential[x, y - 1, z] +
                                                       self.potential[x, y, z + 1] + self.potential[x, y, z - 1]) / 6


if __name__ == "__main__":
    ourGrid = PotentialGrid(10, 2, 4, 5)
    ourGrid.update(700)
    ourGrid.write_potential("potential.fas")
    ourGrid.write_potential("abs-potential.fas", absolute=True)
    ourGrid.write_capacitor("capacitor.fas")
    ourGrid.write_locked("locked.fas")
