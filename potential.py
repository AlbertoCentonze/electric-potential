from __future__ import annotations
import numpy as np
import numpy.typing as npt

from elements import GridElement
from constants import MAX_CHARGE, NO_CHARGE
from utils import Coords, iter_3d
from dataclasses import astuple


class Grid:
    """Class representing a 3D grid with a capacitor inside.
    The class wraps a few numpy arrays to get the best performances """

    def set_cell(self, coords: Coords, value: int = None, lock: bool = False) -> None:
        """Allows to set the potential for a specific point of the grid and eventually lock it"""
        coords = astuple(coords)
        if value is not None:
            self.potential[coords] = value
        self.locked[coords] = int(lock)

    def average_cell(self, coords: Coords) -> None:
        x, y, z = astuple(coords)
        self.potential[x, y, z] = (self.potential[x + 1, y, z] + self.potential[x - 1, y, z] +
                                   self.potential[x, y + 1, z] + self.potential[x, y - 1, z] +
                                   self.potential[x, y, z + 1] + self.potential[x, y, z - 1]) / 6

    def add_element(self, element: GridElement) -> None:
        # TODO
        pass

    def __init__(self, grid_length: int, distance: int, width: int, height: int):
        self.grid_length: npt.ArrayLike = grid_length
        double_length = grid_length * 2
        self.potential: npt.ArrayLike = np.zeros((double_length, double_length, double_length))
        self.locked = np.zeros((double_length, double_length, double_length))
        self.add_capacitor_manually(grid_length, distance, width, height)

    def add_capacitor_manually(self, grid_length, distance, width, height):
        double_length = 2 * grid_length
        double_edge = double_length - 1
        for z in range(double_length):
            for x in range(double_length):
                for y in range(double_length):
                    common_capacitors = (grid_length - width) <= y <= (grid_length + width) - 1 and (
                            grid_length - height) <= z <= (grid_length + height)
                    node = Coords(x, y, z)
                    # positively charged + blocked potential
                    if x == (grid_length - distance) - 1 and common_capacitors:
                        self.set_cell(node, value=MAX_CHARGE, lock=True)
                    # negatively charged + blocked potential
                    elif x == (grid_length + distance) and common_capacitors:
                        self.set_cell(node, value=-MAX_CHARGE, lock=True)
                    # block edges potential
                    elif x == 0 or x == double_edge or y == 0 or y == double_edge or z == 0 or z == double_edge:
                        self.set_cell(node, value=NO_CHARGE, lock=True)

    def is_capacitor(self, coords: Coords):
        coords_tuple: (int, int, int) = astuple(coords)
        return self.is_locked(coords) and abs(self.potential[coords_tuple] == MAX_CHARGE)

    def is_locked(self, coords: Coords):
        coords: (int, int, int) = astuple(coords)
        return self.locked[coords]

    def update_node(self, c: Coords):
        if not self.locked[c]:
            self.average_cell(c)

    def update(self, iterations: int):
        for i in range(iterations):
            length = 2 * self.grid_length
            iter_3d(self.update_node, length, length, length)
