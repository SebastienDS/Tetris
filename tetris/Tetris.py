from typing import List, Tuple
from tetris.color import Color
from tetris.Tetrominoe import Tetrominoe
from tetris import tetrominoes

class Tetris:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[Color]] = [[None for _ in range(width)] for _ in range(height)]
        self.active_piece: Tetrominoe = self.generate_new_piece()
        self.piece_position: Tuple[int, int] = ((self.width - self.active_piece.get_width()) // 2, 0)
        self.stored_piece: Tetrominoe = None
        self.score = 0
        self.is_game_over = False

    def update(self):
        if self.is_game_over:
            print("Game Over")
            return 

        if self.can_piece_go_down():
            self.move_piece_down()
        else:
            self.merge_piece_to_grid()

            completed_rows = self.remove_completed_rows()
            if completed_rows:
                multiplier = 400 if completed_rows >= 4 else 100
                self.add_score(completed_rows * multiplier)
            
            self.init_new_piece()
            self.reset_position()
            self.test_game_over()

    def add_score(self, score: int):
        self.score += score
        print("Score: ", self.score)

    def get_cell(self, x: int, y: int) -> Color:
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, color: Color):
        self.grid[y][x] = color

    def generate_new_piece(self) -> Tetrominoe:
        return tetrominoes.get_random_tetrominoe()

    def init_new_piece(self):
        self.active_piece = self.generate_new_piece()

    def reset_position(self):
        self.piece_position = ((self.width - self.active_piece.get_width()) // 2, 0)

    def remove_completed_rows(self) -> int:
        rows_to_remove = [row for row in range(self.height - 1, -1, -1) if all(self.grid[row])]
        count = len(rows_to_remove)
        
        for row in rows_to_remove:
            self.grid.pop(row)
        for _ in range(count):
            self.grid.insert(0, [None] * self.width)
        return count

    def can_piece_go_down(self) -> bool:
        y = self.piece_position[1]
        height_limit = self.height - self.active_piece.get_height()
        return y < height_limit and self.can_piece_move(0, 1)

    def can_piece_move_left(self) -> bool:
        x = self.piece_position[0]
        wanted_x_position = x - 1
        return wanted_x_position >= 0 and self.can_piece_move(-1, 0)

    def can_piece_move_right(self) -> bool:
        x = self.piece_position[0]
        wanted_x_position = x + 1
        right_piece_position = wanted_x_position + self.active_piece.get_width()
        return right_piece_position <= self.width and self.can_piece_move(1, 0)

    def can_piece_rotate_left(self) -> bool:
        self.active_piece.rotate_left()
        
        x, y = self.piece_position
        right_piece_position = x + self.active_piece.get_width()
        height_limit = self.height - self.active_piece.get_height()
        
        if right_piece_position > self.width or y >= height_limit:
            self.active_piece.rotate_right() # replace piece
            return False

        is_valid_position = self.is_valid_piece_position(x, y)
        self.active_piece.rotate_right() # replace piece
        return is_valid_position
    
    def can_piece_rotate_right(self) -> bool:
        self.active_piece.rotate_right()

        x, y = self.piece_position
        right_piece_position = x + self.active_piece.get_width()
        height_limit = self.height - self.active_piece.get_height()

        if right_piece_position > self.width or y >= height_limit:
            self.active_piece.rotate_left() # replace piece
            return False

        is_valid_position = self.is_valid_piece_position(x, y)
        self.active_piece.rotate_left() # replace piece
        return is_valid_position

    def can_piece_move(self, direction_x: int, direction_y: int) -> bool:
        current_x, current_y = self.piece_position
        final_x = current_x + direction_x
        final_y = current_y + direction_y

        return self.is_valid_piece_position(final_x, final_y)

    def move_piece_down(self):
        assert self.can_piece_go_down()
        x, y = self.piece_position
        self.piece_position = (x, y + 1)
    
    def move_piece_down_max(self):
        while self.can_piece_go_down():
            self.move_piece_down()

    def move_piece_left(self):
        assert self.can_piece_move_left()
        x, y = self.piece_position
        self.piece_position = (x - 1, y)

    def move_piece_right(self):
        assert self.can_piece_move_right()
        x, y = self.piece_position
        self.piece_position = (x + 1, y)

    def rotate_piece_left(self):
        assert self.can_piece_rotate_left()
        self.active_piece.rotate_left()

    def rotate_piece_right(self):
        assert self.can_piece_rotate_right()
        self.active_piece.rotate_right()

    def is_valid_piece_position(self, position_x: int, position_y: int) -> bool:
        width = self.active_piece.get_width()
        height = self.active_piece.get_height()

        for j in range(height):
            for i in range(width):
                if self.active_piece.is_piece_shape(i, j) and self.get_cell(i + position_x, j + position_y) is not None:
                    return False
        return True

    def merge_piece_to_grid(self):
        width = self.active_piece.get_width()
        height = self.active_piece.get_height()
        offset_x, offset_y = self.piece_position

        for j in range(height):
            for i in range(width):
                if self.active_piece.is_piece_shape(i, j):
                    assert self.get_cell(i + offset_x, j + offset_y) is None
                    self.set_cell(i + offset_x, j + offset_y, self.active_piece.color)

    def get_max_piece_position(self) -> Tuple[int, int]:
        current_position = self.piece_position

        self.move_piece_down_max()
        max_piece_position = self.piece_position
        self.piece_position = current_position

        return max_piece_position
    
    def swap_piece(self):
        if self.stored_piece is None:
            self.stored_piece = self.active_piece
            self.init_new_piece()
            self.reset_position()
        else:
            self.active_piece, self.stored_piece = self.stored_piece, self.active_piece
            self.reset_position()
        self.test_game_over()

    def test_game_over(self):
        self.is_game_over = not self.is_valid_piece_position(*self.piece_position)