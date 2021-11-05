import numpy as np
import numpy.typing as npt
from typing import Final

PLATE_POTENTIAL: Final = 10


class Coords:
    """Represents a point in a 3D space, its components can't be negative"""

    def __init__(self, x: int, y: int, z: int) -> None:
        if x < 0 or y < 0 or z < 0:
            raise ValueError("One or more coordinates are negative")
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def as_tuple(self) -> (int, int, int):
        return self.x, self.y, self.z


class Plate:
    pass


class PotentialGrid:
    """Class representing a 3D grid with a capacitor inside.
    The class wraps a few numpy arrays to get the best performances """

    def set_node(self, coords: Coords, value: int = None, lock: bool = False):
        """Allows to set the potential for a specific point of the grid and eventually lock it"""
        if value is not None:
            self.potential[coords.as_tuple()] = value
        self.locked[coords.as_tuple()] = int(lock)

    def average_node(self, coords: Coords):
        x, y, z = coords.as_tuple()
        self.potential[x, y, z] = (self.potential[x + 1, y, z] + self.potential[x - 1, y, z] +
                                   self.potential[x, y + 1, z] + self.potential[x, y - 1, z] +
                                   self.potential[x, y, z + 1] + self.potential[x, y, z - 1]) / 6

    def __init__(self, grid_length: int, distance: int, width: int, height: int):
        self.grid_length: npt.ArrayLike = grid_length
        self.potential: npt.ArrayLike = np.zeros(
            (grid_length * 2, grid_length * 2, grid_length * 2))
        self.locked = np.zeros(
            (grid_length * 2, grid_length * 2, grid_length * 2))
        for z in range(0, 2 * grid_length):
            for x in range(0, 2 * grid_length):
                for y in range(0, 2 * grid_length):
                    node = Coords(x, y, z)
                    # positively charged + blocked potential
                    if x == (grid_length - distance) - 1 and (grid_length - width) <= y <= (
                            grid_length + width) - 1 and (
                            grid_length - height) <= z <= (grid_length + height):
                        self.set_node(node, value=10, lock=True)
                    # negatively charged + blocked potential
                    elif x == (grid_length + distance) and (grid_length - width) <= y <= (
                            grid_length + width) - 1 and (
                            grid_length - height) <= z <= (grid_length + height):
                        self.set_node(node, value=-10, lock=True)
                    # block edges potential
                    elif x == 0 or x == (2 * grid_length) - 1 or y == 0 or y == (
                            2 * grid_length) - 1 or z == 0 or z == (2 * grid_length) - 1:
                        self.set_node(node, lock=True)

    def write_potential(self, file_name: str, output_type: str = "") -> None:
        # TODO write a unique method for all the write methods
        out = open(file_name, "w")

        if len(output_type) == 0 or output_type == "lock":
            def generate_output(coords: (int, int, int), source: npt.ArrayLike) -> str:
                value = source[coords]
                return f"{x} {y} {z} {value}"
        elif output_type == "abs":
            def generate_output(coords: (int, int, int), source: npt.ArrayLike) -> str:
                absolute_potential = abs(source[coords])
                return f"{x} {y} {z} {absolute_potential}"

        for x in range(0, 2 * self.grid_length):
            for y in range(0, 2 * self.grid_length):
                for z in range(0, 2 * self.grid_length):
                    out.write(generate_output((x, y, z), ))
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

    def is_capacitor(self, coords: Coords):
        coords_tuple: (int, int, int) = coords.as_tuple()
        return self.is_locked(coords) and abs(self.potential[coords_tuple] == PLATE_POTENTIAL)

    def is_locked(self, coords: Coords):
        coords: (int, int, int) = coords.as_tuple()
        return self.locked[coords]

    def write_capacitor(self, file_name: str):
        out = open(file_name, "w")

        for x in range(0, 2 * self.grid_length):
            for y in range(0, 2 * self.grid_length):
                for z in range(0, 2 * self.grid_length):
                    if self.is_capacitor(Coords(x, y, z)):
                        out.write(str(x) + " " + str(y) + " " + str(z) + "\n")
            out.write("\n")
        out.close()

    def update(self, iterations: int):
        for i in range(iterations):
            for x in range(2 * self.grid_length):
                for y in range(2 * self.grid_length):
                    for z in range(2 * self.grid_length):
                        coords = Coords(x, y, z)
                        if not self.locked[coords]:
                            self.average_node(coords)
