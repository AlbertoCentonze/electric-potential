from abc import ABC, abstractmethod
from dataclasses import dataclass

from utils import Coords


class ElementIncompatibleError(Exception):
    pass  # TODO


class GridElement(ABC):
    """Abstract class to define elements with a fixed potential to insert in the grid"""

    @abstractmethod
    def is_compatible(self, width: int, height: int, depth: int) -> bool:
        return True

    @abstractmethod
    def update_cell(self, c: Coords) -> (int, bool):
        """Returns the potential of the cell (int) and if it should be locked (bool)"""
        pass


@dataclass
class Plate(GridElement):
    bottom_left: (int, int)
    top_right: (int, int)
    charge: int

    def update_cell(self, c: Coords) -> (int, bool):
        return 0, True  # TODO

    def is_compatible(self, width: int, height: int, depth: int) -> bool:
        return True  # TODO


class Capacitor(GridElement):
    """Representation of a capacitor in a grid. Made out of two plates with opposite charges"""

    def __init__(self, charge: int, center: (int, int), size: (int, int), distance: int) -> None:
        # TODO
        self.positive_plate = Plate(0, 0, charge)
        self.negative_plate = Plate(0, 0, -charge)

    def update_cell(self, c: Coords) -> (int, bool):
        pos_charge, pos_lock = self.positive_plate.update_cell(c)
        neg_charge, neg_lock = self.negative_plate.update_cell(c)
        cell_charge = pos_charge if abs(pos_charge) > abs(neg_charge) else neg_charge
        cell_lock = pos_lock or neg_lock
        return cell_charge, cell_lock

    def is_compatible(self, width: int, height: int, depth: int) -> bool:
        pos_comp = self.positive_plate.is_compatible(width, height, depth)
        neg_comp = self.negative_plate.is_compatible(width, height, depth)
        return pos_comp and neg_comp
