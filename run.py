from game import Game
import numpy as np
import matplotlib.pyplot as plt

beacon = np.zeros((12, 12))
beacon[1, 1] = 1
beacon[2, 2] = 1
beacon[3, 3] = 1
game = Game(12, 12, beacon)

plt.imshow(game.beacon, cmap='binary')
plt.show()