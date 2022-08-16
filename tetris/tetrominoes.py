import random
from tetris.Tetrominoe import Tetrominoe
from tetris.color import Color


def get_I() -> Tetrominoe:
    return Tetrominoe([
        [True],
        [True],
        [True],
        [True]
    ], Color.CYAN)

def get_J() -> Tetrominoe:
    return Tetrominoe([
        [False, True],
        [False, True],
        [True, True]
    ], Color.BLUE)

def get_L() -> Tetrominoe:
    return Tetrominoe([
        [True, False],
        [True, False],
        [True, True]
    ], Color.ORANGE)

def get_O() -> Tetrominoe:
    return Tetrominoe([
        [True, True],
        [True, True]
    ], Color.YELLOW)

def get_S() -> Tetrominoe:
    return Tetrominoe([
        [False, True, True],
        [True, True, False]
    ], Color.GREEN)

def get_T() -> Tetrominoe:
    return Tetrominoe([
        [True, True, True],
        [False, True, False]
    ], Color.MAGENTA)

def get_Z() -> Tetrominoe:
    return Tetrominoe([
        [True, True, False],
        [False, True, True]
    ], Color.RED)

constructors = [get_I, get_J, get_L, get_O, get_S, get_T, get_Z]

def get_random_tetrominoe() -> Tetrominoe:
    tetrominoe_constructor = random.choice(constructors)
    return tetrominoe_constructor()