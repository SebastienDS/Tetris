import unittest
from tetris.Tetrominoe import Tetrominoe
import tetris.tetrominoes as tetrominoes

class TestTetrominoe(unittest.TestCase):

    def test_equal(self):
        T = Tetrominoe([
            [True, True, True],
            [False, True, False]
        ], None)
        O = Tetrominoe([
            [True, True],
            [True, True]
        ], None)

        self.assertEqual(tetrominoes.get_T(), T)
        self.assertNotEqual(tetrominoes.get_T(), O)

    def test_left_rotation(self):
        T = tetrominoes.get_T()
        I = tetrominoes.get_I()

        T.rotate_left()
        I.rotate_left()

        self.assertEqual(T, Tetrominoe([
            [True, False],
            [True, True],
            [True, False]
        ], None))
        self.assertEqual(I, Tetrominoe([
            [True, True, True, True]
        ], None))

    def test_right_rotation(self):
        T = tetrominoes.get_T()
        I = tetrominoes.get_I()

        T.rotate_right()
        I.rotate_right()

        self.assertEqual(T, Tetrominoe([
            [False, True],
            [True, True],
            [False, True]
        ], None))
        self.assertEqual(I, Tetrominoe([
            [True, True, True, True]
        ], None))

    def test_get_width(self):
        I = tetrominoes.get_I()
        O = tetrominoes.get_O()
        T = tetrominoes.get_T()

        self.assertEqual(I.get_width(), 1)
        self.assertEqual(O.get_width(), 2)
        self.assertEqual(T.get_width(), 3)

    def test_get_height(self):
        I = tetrominoes.get_I()
        O = tetrominoes.get_O()
        T = tetrominoes.get_T()

        self.assertEqual(I.get_height(), 4)
        self.assertEqual(O.get_height(), 2)
        self.assertEqual(T.get_height(), 2)

    def test_is_piece_shape(self):
        O = tetrominoes.get_O()
        T = tetrominoes.get_T()

        for j in range(O.get_height()):
            for i in range(O.get_width()):
                self.assertTrue(O.is_piece_shape(i, j))

        self.assertTrue(T.is_piece_shape(0, 0))
        self.assertTrue(T.is_piece_shape(1, 0))
        self.assertTrue(T.is_piece_shape(2, 0))
        self.assertFalse(T.is_piece_shape(0, 1))
        self.assertTrue(T.is_piece_shape(1, 1))
        self.assertFalse(T.is_piece_shape(2, 1))