import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pprint import pprint

import os
import sys
sys.path.insert(0, os.path.abspath(
                   os.path.join(os.path.dirname(__file__), '..')))

from py_conway import Game  # nopep8

my_game = Game(12, 12, random=True, enforce_boundary=False)
my_game.start()

board, ax = plt.subplots()
plt.title("Conway's Game of Life")

ylim, xlim = my_game.board_size

ax.set_xlim(0, xlim)
ax.set_ylim(0, ylim)

image = plt.imshow(my_game.current_board, animated=True, cmap='binary')


def update(*args, **kwargs):
    my_game.run_generation()
    plt.xlabel(f"Generation: {my_game.generations} |\
                Population: {my_game.live_cells}")
    image.set_array(my_game.current_board)
    return image,


conway_animation = FuncAnimation(board, update, interval=50, blit=True)
plt.show()
