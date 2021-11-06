from __future__ import annotations
import numpy as np
import numpy.typing as npt

from elements import GridElement
from constants import MAX_CHARGE, NO_CHARGE
from utils import Coords, iter_3d
from dataclasses import astuple


class Grid:
    """Class representing a 3D grid with a capacitor inside.
    For performance reason the class is built as a wrapper around two np.arrays"""
    def set_cell(self, c: Coords, value: int = None, lock: bool = None) -> None:
        """Setter for the electric potential in a specific point of the grid"""
        c = astuple(c)
        # TODO check syntax for None
        if value is None and lock is None:
            raise Exception("The method is not doing anything, you should check the code")
        if lock is not None:
            self.locked[c] = int(lock)

        locked = self.locked[c]
        if value is not None:
            if locked:
                raise Exception("Trying to change the value of a locked cell, you should unlock it first")
            else:
                self.potential[c] = value

    def __average_cell(self, c: Coords) -> None:
        """Sets the potential of a cell in the grid as the mean potential of its neighbours"""
        x, y, z = astuple(c)
        neighbours = (self.potential[x + 1, y, z], self.potential[x - 1, y, z],
                      self.potential[x, y + 1, z], self.potential[x, y - 1, z],
                      self.potential[x, y, z + 1], self.potential[x, y, z - 1])
        self.set_cell(c, value=np.mean(neighbours))

    def add_element(self, element: GridElement) -> None:
        """Adds an element to the grid, consequently setting the cells as described by the element itself"""
        if not element.is_compatible(self.width, self.height, self.depth):
            raise Exception
        # TODO
        pass

    def __init__(self, size: Coords):
        size_tuple = astuple(size)
        self.width, self.height, self.depth = size_tuple
        self.potential: npt.ArrayLike = np.zeros(size_tuple)
        self.locked: npt.ArrayLike = np.zeros(size_tuple)
        self.add_capacitor_manually(self.width, 5, 2, 2)

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

    def update_node(self, c: Coords):
        """Set a cell potential as the average of its neighbours only if it's not locked"""
        if not self.locked[c]:
            self.__average_cell(c)

    def update_grid(self, iterations: int):
        """Updates all the cells in the grid for a certain amount of iterations"""
        for i in range(iterations):
            iter_3d(self.update_node, self.width, self.height, self.depth)
