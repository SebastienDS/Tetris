import numpy as np
from typing import List

from tetris.color import Color


class Tetrominoe:

    def __init__(self, shape: List[List[bool]], color: Color):
        self.shape = np.array(shape)
        self.color = color

    def __eq__(self, other: object) -> bool:
        if self.shape.shape != other.shape.shape: return False

        equal_matrix = self.shape == other.shape
        return not (False in equal_matrix)

    def rotate_right(self):
        self.shape = np.rot90(self.shape, 3)

    def rotate_left(self):
        self.shape = np.rot90(self.shape)

    def get_width(self) -> int:
        _, width = self.shape.shape
        return width

    def get_height(self) -> int:
        height, _ = self.shape.shape
        return height

    def is_piece_shape(self, x: int, y: int) -> bool:
        return self.shape[y, x]