from copy import deepcopy
from enum import Enum
from threading import Thread


class GameState(Enum):
    READY = 1
    RUNNING = 2
    FINISHED = 3


class Game:
    """
    Class for running a game of Conway's Game of Life on a virtual
    two-dimensional board of any size.
    """
    def __init__(self, width: int = 6, height: int = 6, beacon: list = None):
        """
        Intialize the game based on provided board size values and a
        starter beacon.

        Keyword Arguments:
        width -- the width (in columns) of the game board
        height -- the height (in rows) of the game board
        beacon -- A two-dimensional list with 1 and 0 values that
                  should be set to the initial game state.
        """
        self.board_size = (width, height)
        self.live_cells = 0
        self.num_steps = 0
        if beacon is None:
            self.beacon = self._create_zeros()
        else:
            if len(beacon) != height or len(beacon[0]) != width:
                raise Exception("Please make sure that the beacon matches \
                                 the provided width and height values.")

            self.beacon = beacon
            self.live_cells = self._count_live_cells(self.beacon)

        self.board = deepcopy(self.beacon)
        self.state = GameState.READY

    def _count_live_cells(self, grid_state: list) -> int:
        """
        Count the number of live cells in a provided X by Y grid.

        Positional arguments:
        grid_state -- An X by Y two-dimensional list with 1 and 0 values.
        """
        return len([col_val
                    for row in grid_state
                    for col_val in row if col_val == 1])

    def _create_zeros(self) -> list:
        """
        Initialize the board with all cells "dead" or off. Based on the
        provided board_size, returns a two-dimensional list of zeros.
        """
        cols, rows = self.board_size
        dim_one = [0 for row in range(rows)]
        return [dim_one[:] for col in range(cols)]

    def _num_neighbors(self, row: int, column: int) -> int:
        """
        Determine the number of neighbors to a given cell that
        are "alive" or on. each cell has between three and eight
        potential neighbors.

        Positional arguments:
        row -- The row of the current cell
        col -- The column of the current cell
        """
        neighbors = 0
        num_cols, num_rows = self.board_size

        # Build up a set of possible coordinates to check
        # and then iterate over that set to get a count,
        # ignoring those values that exist outside of the grid
        neighbor_set = {(row - 1, column - 1),
                        (row - 1, column),
                        (row - 1, column + 1),
                        (row, column - 1),
                        (row, column + 1),
                        (row + 1, column - 1),
                        (row + 1, column),
                        (row + 1, column + 1)}
        for n_row, n_col in neighbor_set:
            # if row == 0, don't check the row above
            # if col == 0, don't check the column before
            if n_row < 0 or n_col < 0:
                continue
            # if row + 1 == num_rows, don't check the row after
            # if col + 1 == num_cols, don't check the col after
            elif n_row == num_rows or n_col == num_cols:
                continue
            else:
                if self.board[n_row][n_col] == 1:
                    neighbors += 1

        return neighbors

    def _run(self):
        """Target method for running a game on a thread."""
        if (self.state == GameState.READY):
            self.state = GameState.RUNNING
            while True:
                if (self.live_cells == 0):
                    self.state = GameState.FINISHED
                    break
                self.step()

    def start(self):
        """Run the game automatically on a background thread."""
        thread = Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()

    def step(self):
        """
        Enumerate over every element and determine its number of neighbors
        For each cell, check all eight neighbors and turn on or off.
        Once every cell has been checked against Conway's three rules,
        the entire state grid is updated at once.
        """
        # Get a deep copy of the state to track cells that will need
        # to change without affecting the outcome for other cells in-step
        intermediate_state = deepcopy(self.board)
        upcoming_live_cells = self._count_live_cells(self.board)

        for row_index, row in enumerate(self.board):
            for col_index in range(len(row)):
                neighbors = self._num_neighbors(row_index, col_index)

                if (neighbors < 2 or neighbors > 3):
                    if (self.board[row_index][col_index] == 1):
                        upcoming_live_cells -= 1
                    intermediate_state[row_index][col_index] = 0
                elif (neighbors == 3):
                    if (self.board[row_index][col_index] == 0):
                        upcoming_live_cells += 1
                    intermediate_state[row_index][col_index] = 1

        self.board = deepcopy(intermediate_state)
        self.num_steps += 1
        self.live_cells = upcoming_live_cells
