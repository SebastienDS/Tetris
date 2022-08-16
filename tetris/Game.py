import time, pygame
from tetris.Tetris import Tetris
from tetris.color import Color

pygame.init()


class Game:
    def __init__(self, screen_width: int, screen_height: int, width: int, height: int, cell_size: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.run = True
        self.updating = True
        self.last_update = time.time()
        self.time_for_update = 1
        self.last_input_update = time.time()
        self.time_for_input_update = 0.1

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

        self.cell_size = cell_size
        self.tetris = Tetris(width, height)
    
    def apply_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                elif event.key == pygame.K_SPACE:
                    self.tetris.swap_piece()
                elif event.key == pygame.K_a:
                    if self.tetris.can_piece_rotate_left():
                        self.tetris.rotate_piece_left()
                elif event.key == pygame.K_e:
                    if self.tetris.can_piece_rotate_right():
                        self.tetris.rotate_piece_right()
                elif event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.tetris.move_piece_down_max()
                    self.last_update = 0 # next frame will fix the piece

        self.apply_repeted_inputs()

    def apply_repeted_inputs(self):
        key_pressed = pygame.key.get_pressed()

        if time.time() - self.last_input_update > self.time_for_input_update:
            have_updated = True

            if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_q]:
                if self.tetris.can_piece_move_left():
                    self.tetris.move_piece_left()
            elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
                if self.tetris.can_piece_move_right():
                    self.tetris.move_piece_right()
            elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                if self.tetris.can_piece_go_down():
                    self.tetris.move_piece_down()
                    self.last_update = time.time()
            else:
                have_updated = False
            
            if have_updated:
                self.last_input_update = time.time()

    def draw_grid(self):
        for j in range(self.tetris.height):
            for i in range(self.tetris.width):
                self.draw_cell(i, j, self.tetris.get_cell(i, j))

    def draw_active_piece_max_position(self):
        width = self.tetris.active_piece.get_width()
        height = self.tetris.active_piece.get_height()
        x, y = self.tetris.get_max_piece_position()

        for j in range(height):
            for i in range(width):
                piece = self.tetris.active_piece
                if piece.is_piece_shape(i, j):
                    self.draw_ghost_piece(x + i, y + j, piece.color, 75)

    def draw_ghost_piece(self, x: int, y: int, color: Color, transparency: int):
        surface = pygame.Surface((self.cell_size, self.cell_size))
        surface.set_alpha(transparency)
        surface.fill(color.value)
        self.screen.blit(surface, (x * self.cell_size, y * self.cell_size))

    def draw_active_piece(self):
        width = self.tetris.active_piece.get_width()
        height = self.tetris.active_piece.get_height()
    
        for j in range(height):
            for i in range(width):
                piece = self.tetris.active_piece
                color = piece.color if piece.is_piece_shape(i, j) else None

                x, y = self.tetris.piece_position
                self.draw_cell(x + i, y + j, color)

    def draw_cell(self, x: int, y: int, color: Color):
        rect = (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        if color:
            pygame.draw.rect(self.screen, color.value, rect)
        pygame.draw.rect(self.screen, Color.GRAY.value, rect, 1)

    def update(self):
        if self.tetris.is_game_over: return
        if not self.updating: return

        self.apply_inputs()

        if time.time() - self.last_update > self.time_for_update:
            self.tetris.update()
            self.last_update = time.time()

    def draw(self):
        self.draw_grid()
        self.draw_active_piece_max_position()
        self.draw_active_piece()

    def mainloop(self):
        while self.run:
            self.screen.fill(Color.BLACK.value)
            
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)
