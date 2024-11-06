import pytest

from game import Game
from tests.conftest import copy_matrix


def test_run_game_value_error(game):
    """
    Tests that None direction raises ValueError.
    """
    with pytest.raises(ValueError):
        assert game.run_game(None)


def test_run_not_start(game, dirs, mock_method):
    """
    Tests that when attribute 'player_start' is False function returns False, but wont affect attribute 'game_over'.
    """
    for dir in dirs:
        assert game.run_game(dir) == False
        assert game.game_over == False


def test_run_game_all_invalid_moves(game, dirs):
    """
    Tests that for True value of atribute 'player_start' function evaluates movement in provided direction.
    Based on matrix with no possible movement function should return False and mutate 'game_over' to False value.
    """
    game.player_start = True
    for dir in dirs:
        assert game.run_game(dir) == False
        assert game.game_over == True


def test_run_game_all_valid_moves(game, dirs, matrices, mock_method):
    """
    Tests that for True value of atribute 'player_start' function evaluates movement in provided direction.
    Based od matrix with possible movement in all directions function should:
    - Call method 'move_in_direction every time:
    -- If it returns True, then call method 'place_random_tile' if it is possible to move in that direction:
    -- (For this example it should call it every time).
    - Call method 'score_reached_criterium' every time.
    -- If it returns True, then call method 'print_win_label'.
    -- (For this ecample it should not call any time).
    """
    mocked_tiles = mock_method(Game, "place_random_tile")
    mocked_crit = mock_method(Game, "score_reached_criterium")
    mocked_print_label = mock_method(Game, "print_win_label")

    game.player_start = True
    for dir in dirs:
        game.matrix = copy_matrix(matrices["valid_template"])
        assert game.run_game(dir) == True
        assert game.game_over == False

    assert mocked_tiles.call_count == len(dirs)
    assert mocked_crit.call_count == len(dirs)
    assert mocked_print_label.call_count == 0


def test_run_game_all_valid_print_win(game, dirs, matrices, mock_method):
    """
    Tests that for True value of atribute 'player_start' function evaluates movement in provided direction.
    Based od matrix with possible movement in all directions function should:
    - Call method 'move_in_direction every time:
    -- If it returns True, then call method 'place_random_tile' if it is possible to move in that direction:
    -- (For this example it should call it every time).
    - Call method 'score_reached_criterium' every time.
    -- If it returns True, then call method 'print_win_label'.
    -- (For this ecample it should call every time).
    """
    mocked_print_label = mock_method(Game, "print_win_label")
    mocked_crit = mock_method(Game, "score_reached_criterium", return_value=True)

    game.player_start = True

    for dir in dirs:
        game.matrix = copy_matrix(matrices["valid_template"])
        assert game.run_game(dir) == True

    assert mocked_print_label.call_count == len(dirs)
    assert mocked_crit.call_count == len(dirs)
