import numpy as np
import copy


class Game:
    def __init__(self, width=6, height=6, beacon=None):
        self.board_size = (width, height)
        if beacon is None:
            self.beacon = np.zeros(self.board_size)
        else:
            self.beacon = beacon
        self.state = self.beacon

    def _numNeighbors(self, x, y):
        startX = 0
        startY = 0
        neighbors = 0
        endX = self.board_size[0]
        endY = self.board_size[1]

        if (x > 0):
            startX = -1
        if (y > 0):
            startY = -1

        if y < endY:
            endY = 1
        if x < endX:
            endX = 1

        for checkX in range(startX, endX):
            for checkY in range(startY, endY):
                if not (checkX == 0 and checkY == 0):
                    if (self.state[x + checkX][y + checkY] == 1):
                        neighbors += 1

        return neighbors

    def step(self):
        # Enumerate over every element and determine its number of neighbors
        # For each cell, check all eight neighbors and turn on or off
        processingState = copy(self.state)
        for x, y in np.ndenumerate(self.state):
            if (self._numNeighbors(x, y) < 2):
                processingState[x, y] = 0

        self.state = processingState
