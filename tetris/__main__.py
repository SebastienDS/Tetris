from tetris.Game import Game
from tetris.color import Color

width = 10
height = 20
cell_size = 35


game = Game(width * cell_size, height * cell_size, width, height, cell_size)
game.mainloop()