import unittest
import numpy as np
from game import Game


class TestConway(unittest.TestCase):
    # Create a Game class that takes a numpy array for the seed
    def test_game_init(self):
        game = Game(12, 12)
        self.assertEqual(game.board_size, (12, 12))

    # Add a beacon with a single cell active
    def test_game_init_beacon(self):
        beacon = np.zeros((6, 6))
        beacon[1, 1] = 1
        game = Game(6, 6, beacon)
        self.assertTrue(np.array_equal(game.beacon, beacon))

    # Test for defaults
    def test_game_init_defaults(self):
        game = Game()
        self.assertEqual(game.board_size, (6, 6))
        self.assertTrue(np.array_equal(game.beacon, np.zeros((6, 6))))

    # Test for default board_size on set beacon
    def test_game_init_board_default_beacon(self):
        game = Game(12, 12)
        self.assertTrue(np.array_equal(game.beacon, np.zeros((12, 12))))

    # Test that check cell returns a valid value
    def test_game_check_cell_with_one_neighbor(self):
        beacon = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
        game = Game(3, 3, beacon)
        self.assertEqual(game._numNeighbors(1, 1), 1)

    def test_game_check_cell_with_two_neighbors(self):
        beacon = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
        game = Game(3, 3, beacon)
        self.assertEqual(game._numNeighbors(1, 2), 2)

    #def test_single_column_array(self):
    #    beacon = [[0], [0], [1]]
    #    game = Game(1, 1, beacon)
    #    self.assertEqual(game._numNeighbors(0, 2), 0)

    # Run the game for one iteration on a single cell


if __name__ == '__main__':
    unittest.main()
