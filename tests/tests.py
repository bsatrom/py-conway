import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(
                   os.path.join(os.path.dirname(__file__), '..')))

from conway.game import Game, GameState  # nopep8


def create_zeros(x, y):
    dim_one = [0 for item in range(x)]
    return [dim_one[:] for item in range(y)]


class TestConway():
    # Create a Game class that takes a numpy array for the seed
    def test_game_init(self):
        test_game = Game(12, 12)
        assert test_game.board_size == (12, 12)

    # Add a beacon with a single cell active
    def test_test_game_init_beacon(self):
        beacon = create_zeros(6, 6)
        beacon[1][1] = 1
        test_game = Game(6, 6, beacon)
        assert test_game.beacon == beacon

    # Test for defaults
    def test_test_game_init_defaults(self):
        test_game = Game()
        assert test_game.board_size == (6, 6)
        assert test_game.beacon == create_zeros(6, 6)

    # Test for default board_size on set beacon
    def test_test_game_init_board_default_beacon(self):
        test_game = Game(12, 12)
        assert test_game.beacon == create_zeros(12, 12)

    # Test that check cell returns a valid value
    def test_test_game_3_x_3_check_cell_with_one_neighbor(self):
        beacon = [[0, 1, 0],
                  [0, 1, 0],
                  [0, 0, 0]]
        test_game = Game(3, 3, beacon)
        assert test_game._num_neighbors(1, 1) == 1

    def test_test_game_3_x_3_check_cell_with_two_neighbors(self):
        beacon = [[0, 1, 0],
                  [0, 1, 0],
                  [0, 0, 0]]
        test_game = Game(3, 3, beacon)
        assert test_game._num_neighbors(1, 2) == 2

    def test_test_game_3_x_3_check_cell_with_three_neighbors(self):
        beacon = [[1, 0, 0],
                  [1, 1, 0],
                  [0, 0, 0]]
        test_game = Game(3, 3, beacon)
        assert test_game._num_neighbors(0, 1) == 3

    # Run on an array of a single column
    def test_single_column_array(self):
        beacon = [[0], [0], [1]]
        test_game = Game(1, 3, beacon)
        assert test_game._num_neighbors(1, 0) == 1

    # Run the test_game for one iteration on a single cell
    def test_3_x_3_single_cell_single_run(self):
        beacon = [[0, 0, 0],
                  [0, 1, 0],
                  [0, 0, 0]]
        test_game = Game(3, 3, beacon)
        test_game.step()
        assert test_game.board == create_zeros(3, 3)

    # Run the test_game for one iteration on three cells
    def test_3_x_3_three_neighbors_single_run(self):
        beacon = [[1, 0, 0],
                  [1, 1, 0],
                  [0, 0, 0]]

        expected_state = [[1, 1, 0],
                          [1, 1, 0],
                          [0, 0, 0]]

        test_game = Game(3, 3, beacon)
        test_game.step()

        assert test_game.board == expected_state

    # Run the test_game for one iteration on four cells
    def test_3_x_3_four_neighbors_single_run(self):
        beacon = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]

        expected_state = [[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]]

        test_game = Game(3, 3, beacon)
        test_game.step()

        assert test_game.board == expected_state

    # Run the test_game for one iteration on four cells
    def test_4_x_3_three_neighbors_single_run(self):
        beacon = [[1, 0, 1, 0],
                  [0, 1, 0, 0],
                  [1, 0, 1, 1]]

        expected_state = [[0, 1, 0, 0],
                          [1, 0, 0, 1],
                          [0, 1, 1, 0]]

        test_game = Game(4, 3, beacon)
        test_game.step()

        assert test_game.board == expected_state

    # Test the number of live cells on an empty beacon
    def test_3_x_3_empty_beacon_no_live_cells(self):
        test_game = Game(3, 3)

        assert test_game.live_cells == 0

    # Test the live cells count on a beacon with 4 lve cells
    def test_3_x_3_beacon_five_live_cells(self):
        beacon = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]

        test_game = Game(3, 3, beacon)

        assert test_game.live_cells == 5

    def test_increment_live_cells_after_update(self):
        beacon = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]

        test_game = Game(3, 3, beacon)
        test_game.step()

        assert test_game.live_cells == 8

    def test_update_steps_after_each_step(self):
        test_game = Game(2, 2, [[1, 0], [0, 1]])

        test_game.step()
        test_game.step()

        assert test_game.num_steps == 2

    # Run the test_game for one iteration on four cells
    def test_3_x_3_four_neighbors_two_runs(self):
        beacon = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]

        expected_state = [[1, 0, 1],
                          [0, 0, 0],
                          [1, 0, 1]]

        test_game = Game(3, 3, beacon)
        test_game.step()
        test_game.step()

        assert test_game.board == expected_state

    def test_default_game_state_ready(self):
        test_game = Game()

        assert test_game.state == GameState.READY

    def test_start_game_changes_state_to_running(self):
        beacon = [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]]

        test_game = Game(3, 3, beacon)
        test_game.state = GameState.READY
        test_game._thread_active = True
        test_game._run()

        assert test_game.state == GameState.FINISHED
        assert test_game.live_cells == 0

    def test_empty_board_run_game_until_no_living_cells_left(self):
        test_game = Game()
        test_game.state = GameState.READY
        test_game._run()

        assert test_game.state == GameState.FINISHED

    def test_ensure_that_width_height_and_beacon_match(self):
        beacon = [[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]]

        with pytest.raises(Exception):
            Game(3, 4, beacon)

    def test_ensure_that_live_cells_count_is_accurate_before_run(self):
        beacon = [[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]]

        test_game = Game(4, 4, beacon)
        test_game.board[0][0] = 1

        test_game.step()

        assert test_game.live_cells == 5

    def test_no_beacon_ensure_live_cells_count_is_accurate_before_run(self):
        test_game = Game(4, 4)
        test_game.board[0][0] = 1
        test_game.board[0][1] = 1
        test_game.board[0][2] = 1

        test_game.step()

        assert test_game.live_cells == 2

    def test_still_life_game_will_continue_to_run(self):
        beacon = [[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]]

        test_game = Game(4, 4, beacon)
        test_game.start()

        assert test_game.state, GameState.RUNNING

    def test_still_life_game_can_be_stopped(self):
        beacon = [[0, 0, 0, 0],
                  [0, 1, 1, 0],
                  [0, 1, 1, 0],
                  [0, 0, 0, 0]]

        test_game = Game(4, 4, beacon)
        test_game.start()

        assert test_game.state, GameState.RUNNING

        test_game.stop()

        assert test_game.state, GameState.FINISHED
