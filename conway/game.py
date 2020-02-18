from copy import deepcopy


class Game:
    def __init__(self, width=6, height=6, beacon=None):
        self.board_size = (width, height)
        self.live_cells = 0
        if beacon is None:
            self.beacon = self._create_zeros()
        else:
            self.beacon = beacon
            self.live_cells = self._count_live_cells(self.beacon)

        self.state = deepcopy(self.beacon)

    def _count_live_cells(self, grid_state):
        """
        Count the number of live cells in the game
        """
        return len([col_val
                    for row in grid_state
                    for col_val in row if col_val == 1])

    def _create_zeros(self):
        """
        Initialize the board with all cells off
        """
        cols, rows = self.board_size
        dim_one = [0 for row in range(rows)]
        return [dim_one[:] for col in range(cols)]

    def _num_neighbors(self, row, column):
        neighbors = 0
        num_cols, num_rows = self.board_size

        # each cell has between three and eight potential neighbors, so we'll
        # build up a set of coordinates to check and then iterate over that set
        # to get a count.
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
                if self.state[n_row][n_col] == 1:
                    neighbors += 1

        return neighbors

    def step(self):
        # Enumerate over every element and determine its number of neighbors
        # For each cell, check all eight neighbors and turn on or off
        intermediateState = deepcopy(self.state)
        for row_index, row in enumerate(self.state):
            for col_index in range(len(row)):
                neighbors = self._num_neighbors(row_index, col_index)

                if (neighbors < 2 or neighbors > 3):
                    intermediateState[row_index][col_index] = 0
                elif (neighbors == 3):
                    intermediateState[row_index][col_index] = 1

        self.state = deepcopy(intermediateState)
