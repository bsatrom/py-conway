[![Build Status](https://dev.azure.com/brandon0360/py-conway/_apis/build/status/bsatrom.py-conway?branchName=master)](https://dev.azure.com/brandon0360/py-conway/_build/latest?definitionId=3&branchName=master)
[![codecov](https://codecov.io/gh/bsatrom/py-conway/branch/master/graph/badge.svg)](https://codecov.io/gh/bsatrom/py-conway)
![Pyton Version Support](https://img.shields.io/pypi/pyversions/py-conway)

# py-conway

TDD-style implementation of [Conway's Game of Life](https://www.conwaylife.com/wiki/Conway%27s_Game_of_Life) in Python. Built with zero dependencies in order to be portable to Web, CLI and embedded applications.

[View Project on PyPi](https://pypi.org/project/py-conway/)

## Installation

```bash
pip install py-conway
```

## Usage

To create a game, you'll need to provide dimensions and a starting two-dimensonal list to function as the game board. For example:

```python
from py_conway import Game

seed = [[0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]]

new_game = Game(3, 3, seed)
```

If no seed is provided, the game can either generate a seed of zeroes, or a random starter seed. use the `random=True` positional argument to generate a random seed.

```python
new_game = Game(12, 12, random=True)
```

Once the game board is populated, call the `start()` method. The game values and state will be initialized so you can interact with the board one step at a time. You can also use this method to re-initialize the game:

```python
new_game.start()
```

You can also instruct the game to self-run with the `start_thread()` method. The game will start on a background thread and update the full game board as well as a number of informational instance variables:

```python
new_game.start_thread()

new_game.current_board # hold the complete game state after each step
new_game.live_cells # the count of live cells on the board
new_game.generations # the number of steps elapsed in the current game.

new_game.stop_thread()
```

It's also possible to call the `run_generation()` method and control the game state yourself from one iteration to the next. Make sure you call the `start()` method first:

```python
new_game.run_generation()
```

According to the rules of Conway's Game of Life, the board is meant to be infinite. If you wish to 
emulate this behavior in your own games, you can wrap the board around on itself with the initialization flag `enforce_boundary`, which is true by default.

```python
seed = [[1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0]]

new_game = Game(4, 4, seed=seed, enforce_boundary=False)
```

If the above code is run for a single generation, the board will look like this

```
[[0, 0, 0, 0],
 [1, 1, 0, 1],
 [0, 0, 0, 0],
 [0, 0, 0, 0]]
```

Here's an example that runs the game and plots the game board after intialization and the first generation. You can run this from the [example folder](/example), either in a Jupyter notebook or standalone script:

```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from py-conway import Game

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
```
