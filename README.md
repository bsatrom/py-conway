[![Build Status](https://dev.azure.com/brandon0360/py-conway/_apis/build/status/bsatrom.py-conway?branchName=master)](https://dev.azure.com/brandon0360/py-conway/_build/latest?definitionId=3&branchName=master)

# py-conway

TDD-style implementation of [Conway's Game of Life](https://www.conwaylife.com/wiki/Conway%27s_Game_of_Life) in Python. Built with zero dependencies in order to be portable to Web, CLI and embedded applications.

[View Project on PyPi](https://pypi.org/project/py-conway/0.0.1/)

## Installation

```bash
pip install py-conway
```

## Usage

To create a game, you'll need to provide dimensions and a starting two-dimensonal list to function as the game board. For example:

```python
from conway.game import Game

beacon = [[0, 1, 0],
          [1, 1, 1],
          [0, 1, 0]]

new_game = Game(3, 3, beacon)
```

Once the game board is populated, call the `start()` method. The game will start on a background thread and update the full game board as well as a number of informational instance variables:

```python
new_game.start()

new_game.board # hold the complete game state after each step
new_game.live_cells # the count of live cells on the board
new_game.num_steps # the number of steps elapsed in the current game.
```

It's also possible to call the `step()` method and control the game state yourself from one iteration to the next:

```python
new_game.step()
```

Here's an example that runs the game and plots the game board after intialization and the first step:

```python
import matplotlib.pyplot as plt
from py-conway import Game

def create_zeros(x, y):
    dim_one = [0 for item in range(x)]
    return [dim_one[:] for item in range(y)]

beacon = create_zeros(12, 12)

beacon[0][1] = 1
beacon[1][2] = 1
beacon[2][3] = 1
game = Game(12, 12, beacon)

plt.imshow(game.beacon, cmap='binary')
plt.show()

game.step()

plt.imshow(game.beacon, cmap='binary')
plt.show()
```
