from game import Game
import matplotlib.pyplot as plt
from pprint import pprint


def create_zeros(x, y):
    dim_one = [0 for item in range(x)]
    return [dim_one[:] for item in range(y)]


beacon = create_zeros(12, 12)

beacon[0][1] = 1
beacon[1][2] = 1
beacon[2][3] = 1
game = Game(12, 12, beacon)

pprint(beacon)

plt.imshow(game.beacon, cmap='binary')
plt.show()
