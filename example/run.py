import matplotlib.pyplot as plt
from pprint import pprint

import os
import sys
sys.path.insert(0, os.path.abspath(
                   os.path.join(os.path.dirname(__file__), '..')))

from py_conway.game import Game  # nopep8


def create_zeros(x, y):
    dim_one = [0 for item in range(x)]
    return [dim_one[:] for item in range(y)]


seed = create_zeros(12, 12)

seed[0][1] = 1
seed[1][2] = 1
seed[2][3] = 1
game = Game(12, 12, seed)

plt.imshow(game.current_board, cmap='binary')
plt.show()

game.run_generation()

plt.imshow(game.current_board, cmap='binary')
plt.show()
