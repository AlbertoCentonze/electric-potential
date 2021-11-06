from dataclasses import dataclass
from pydantic import validator
from potential import Grid


@dataclass
class Coords:
    """Represents a point in a 3D space, its components can't be negative"""

    x: int
    y: int
    z: int

    @classmethod
    @validator("*")
    def validate_coordinate(cls, value):
        print(value)
        if value < 0:
            raise ValueError("Coordinates can't be negative")


def iter_3d(func, width: int, height: int, depth: int):
    for x in range(width):
        for y in range(height):
            for z in range(depth):
                c = Coords(x, y, z)
                func(c)


def save_grid(grid: Grid, file_name: str) -> None:
    # TODO
    out = open(file_name, "w")


def load_grid(file_name: str) -> Grid:
    # TODO
    file = open(file_name, "r")
