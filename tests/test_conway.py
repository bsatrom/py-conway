import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(
                   os.path.join(os.path.dirname(__file__), '..')))

from conway.game import Game, GameState, InitError  # nopep8


def create_zeros(x, y):
    dim_one = [0 for item in range(x)]
    return [dim_one[:] for item in range(y)]


# Create a Game class that takes a numpy array for the seed
def test_game_init():
    test_game = Game(12, 12)
    assert test_game.board_size == (12, 12)


# Add a seed with a single cell active
def test_test_game_init_seed():
    seed = create_zeros(6, 6)
    seed[1][1] = 1
    test_game = Game(6, 6, seed)
    assert test_game.seed == seed


# Test for defaults
def test_test_game_init_defaults():
    test_game = Game()
    assert test_game.board_size == (6, 6)
    assert test_game.seed == create_zeros(6, 6)


# Test for default board_size on set seed
def test_test_game_init_board_default_seed():
    test_game = Game(12, 12)
    assert test_game.seed == create_zeros(12, 12)


# Test that check cell returns a valid value
def test_test_game_3_x_3_check_cell_with_one_neighbor():
    seed = [[0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]]

    test_game = Game(3, 3, seed)
    assert test_game._num_neighbors(1, 1) == 1


def test_test_game_3_x_3_check_cell_with_two_neighbors():
    seed = [[0, 1, 0],
            [0, 1, 0],
            [0, 0, 0]]

    test_game = Game(3, 3, seed)
    assert test_game._num_neighbors(1, 2) == 2


def test_test_game_3_x_3_check_cell_with_three_neighbors():
    seed = [[1, 0, 0],
            [1, 1, 0],
            [0, 0, 0]]

    test_game = Game(3, 3, seed)
    assert test_game._num_neighbors(0, 1) == 3


# Run on an array of a single column
def test_single_column_array():
    seed = [[0], [0], [1]]
    test_game = Game(1, 3, seed)
    assert test_game._num_neighbors(1, 0) == 1


# Run the test_game for one iteration on a single cell
def test_3_x_3_single_cell_single_run():
    seed = [[0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]]

    test_game = Game(3, 3, seed)
    test_game.run_generation()
    assert test_game.current_board == create_zeros(3, 3)


# Run the test_game for one iteration on three cells
def test_3_x_3_three_neighbors_single_run():
    seed = [[1, 0, 0],
            [1, 1, 0],
            [0, 0, 0]]

    expected_state = [[1, 1, 0],
                      [1, 1, 0],
                      [0, 0, 0]]

    test_game = Game(3, 3, seed)
    test_game.run_generation()

    assert test_game.current_board == expected_state


# Run the test_game for one iteration on four cells
def test_3_x_3_four_neighbors_single_run():
    seed = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    expected_state = [[1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]]

    test_game = Game(3, 3, seed)
    test_game.run_generation()

    assert test_game.current_board == expected_state


# Run the test_game for one iteration on four cells
def test_4_x_3_three_neighbors_single_run():
    seed = [[1, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 1, 1]]

    expected_state = [[0, 1, 0, 0],
                      [1, 0, 0, 1],
                      [0, 1, 1, 0]]

    test_game = Game(4, 3, seed)
    test_game.run_generation()

    assert test_game.current_board == expected_state


# Test the number of live cells on an empty seed
def test_3_x_3_empty_seed_no_live_cells():
    test_game = Game(3, 3)

    assert test_game.live_cells == 0


# Test the live cells count on a seed with 4 lve cells
def test_3_x_3_seed_five_live_cells():
    seed = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    test_game = Game(3, 3, seed)

    assert test_game.live_cells == 5


def test_increment_live_cells_after_update():
    seed = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    test_game = Game(3, 3, seed)
    test_game.run_generation()

    assert test_game.live_cells == 8


def test_update_generations_count_after_each_generation():
    test_game = Game(2, 2, [[1, 0], [0, 1]])

    test_game.run_generation()
    test_game.run_generation()

    assert test_game.generations == 2


# Run the test_game for one iteration on four cells
def test_3_x_3_four_neighbors_two_runs():
    seed = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    expected_state = [[1, 0, 1],
                      [0, 0, 0],
                      [1, 0, 1]]

    test_game = Game(3, 3, seed)
    test_game.run_generation()
    test_game.run_generation()

    assert test_game.current_board == expected_state


def test_default_game_state_ready():
    test_game = Game()

    assert test_game.state == GameState.READY


def test_start_game_changes_state_to_running():
    seed = [[0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]]

    test_game = Game(3, 3, seed)
    test_game.state = GameState.READY
    test_game._thread_active = True
    test_game._run()

    assert test_game.state == GameState.FINISHED
    assert test_game.live_cells == 0


def test_empty_board_run_game_until_no_living_cells_left():
    test_game = Game()
    test_game.state = GameState.READY
    test_game._run()

    assert test_game.state == GameState.FINISHED


def test_ensure_that_width_height_and_seed_match():
    seed = [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]]

    with pytest.raises(InitError):
        Game(3, 4, seed)


def test_ensure_that_live_cells_count_is_accurate_before_run():
    seed = [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]]

    test_game = Game(4, 4, seed)
    test_game.current_board[0][0] = 1

    test_game.run_generation()

    assert test_game.live_cells == 5


def test_no_seed_ensure_live_cells_count_is_accurate_before_run():
    test_game = Game(4, 4)
    test_game.current_board[0][0] = 1
    test_game.current_board[0][1] = 1
    test_game.current_board[0][2] = 1

    test_game.run_generation()

    assert test_game.live_cells == 2


def test_still_life_game_will_continue_to_run():
    seed = [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]]

    test_game = Game(4, 4, seed)
    test_game.start()

    assert test_game.state, GameState.RUNNING


def test_still_life_game_can_be_stopped():
    seed = [[0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]]

    test_game = Game(4, 4, seed)
    test_game.start()

    assert test_game.state, GameState.RUNNING

    test_game.stop()

    assert test_game.state, GameState.FINISHED


def test_ensure_that_seed_includes_valid_data():
    seed = [['a', 0, 0, 0],
            [0, 2, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, -1]]

    with pytest.raises(InitError):
        Game(4, 4, seed)

    seed = [[0, 0, 0, 0],
            [0, 2, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, -1]]

    with pytest.raises(InitError):
        Game(4, 4, seed)

    seed = [[0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, -1]]

    with pytest.raises(InitError):
        Game(4, 4, seed)


def test_generate_random_seed_generates_random_seed():
    test_game = Game(12, 12, random=True)

    assert test_game.live_cells > 0
