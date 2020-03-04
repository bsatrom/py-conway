"""Threaded Game module for py-conway.

This module contains the core functionality for running Conway's Game
of Life on a background thread. Unlike the main game, which must be
advanced manually, a threaded game will run automatically until
stopped.
"""
from . import Game, GameState
from threading import Thread


class ThreadedGame(Game):
    """Threaded module class.

    Class for running a game of Conway's Game of Life on a virtual
    two-dimensional board of any size on a background thread.
    """

    def __init__(self, width: int = 0, height: int = 0,
                 seed: list = None, random: bool = False,
                 enforce_boundary: bool = True):
        """
        Intialize the game based on provided board size values and a seed.

        Args:
            width (int): the width (in columns) of the game board
            height (int): the height (in rows) of the game board
            seed (int): A two-dimensional list with 1 and 0 values that
                    should be set to the initial game state.
            random (bool): Boolean indicating whether a random seed should
                    be created. Ignored if a seed is provided.
            enforce_boundary (bool): Boolean indicating whether cells on
                    the edge of the board should wrap around to the other
                    side.
        """
        self._thread_active = False
        super().__init__(width, height, seed, random, enforce_boundary)

    def _run(self):
        """Target method for running a game on a thread."""
        if (self.state == GameState.READY):
            self.state = GameState.RUNNING
            while True:
                if (self.live_cells == 0 or not self._thread_active):
                    self.state = GameState.FINISHED
                    break
                self.run_generation()

    def start_thread(self):
        """Run the game automatically on a background thread."""
        thread = Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()
        self._thread_active = True

    def stop_thread(self):
        """Stop a game currently running on a background thread."""
        self._thread_active = False
