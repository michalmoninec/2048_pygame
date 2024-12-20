from typing import Any, Callable, List
import pytest

from game import Game

from tests.conftest import copy_matrix, mock_wrapper, non_zero_cells


def test_run_game_value_error(mock_game: Game):
    """Tests that None direction raises ValueError."""
    with pytest.raises(ValueError):
        assert mock_game.run_game(None)


def test_run_not_start(mock_game: Game, dirs: List[int]):
    """Tests that when attribute 'player_start' is False function returns False,
    but wont affect attribute 'game_over'.
    """
    for dir in dirs:
        assert mock_game.run_game(dir) == False
        assert mock_game.game_over == False


def test_run_game_all_invalid_moves(mock_game: Game, dirs: List[int]):
    """Tests that for True value of atribute 'player_start' function
    evaluates movement in provided direction.
    Based on matrix with no possible movement function should return False
    and mutate 'game_over' to False value.
    """
    mock_game.player_start = True
    for dir in dirs:
        assert mock_game.run_game(dir) == False
        assert mock_game.game_over == True


def test_run_game_all_valid_moves(
    mock_game: Game,
    dirs: List[int],
    matrices: dict[str, Any],
    mock_method: Callable[..., Any],
):
    """Tests that for True value of atribute 'player_start' function
    evaluates movement in provided direction.
    Based od matrix with possible movement in all directions function should:
    - Call method 'move_in_direction every time:
    -- If it returns True, then call method 'place_random_tile' if it is
    possible to move in that direction:
    -- (For this example it should call it every time).
    - Call method 'score_reached_criterium' every time.
    -- If it returns True, then call method 'print_win_label'.
    -- (For this ecample it should not call any time).
    """
    mocked_tiles = mock_method(Game, "place_random_tile")
    mocked_crit = mock_method(Game, "score_reached_criterium")
    mocked_print_label = mock_method(Game, "print_win_label")

    mock_game.player_start = True
    assert mock_game.game_over == False
    for dir in dirs:
        mock_game.matrix = copy_matrix(matrices["valid_template"])
        assert mock_game.run_game(dir) == True
        assert mock_game.game_over == False

    assert mocked_tiles.call_count == len(dirs)
    assert mocked_crit.call_count == len(dirs)
    assert mocked_print_label.call_count == 0


def test_run_game_all_valid_print_win(
    mock_game: Game,
    dirs: List[int],
    matrices: dict[str, Any],
    mock_method: Callable[..., Any],
):
    """Tests that for True value of atribute 'player_start' function evaluates
    movement in provided direction.
    Based od matrix with possible movement in all directions function should:
    - Call method 'move_in_direction every time:
    -- If it returns True, then call method 'place_random_tile' if it is
    possible to move in that direction:
    -- (For this example it should call it every time).
    - Call method 'score_reached_criterium' every time.
    -- If it returns True, then call method 'print_win_label'.
    -- (For this ecample it should call every time).
    """
    mocked_print_label = mock_method(Game, "print_win_label")
    mocked_crit = mock_method(Game, "score_reached_criterium", return_value=True)

    mock_game.player_start = True
    assert mock_game.game_over == False
    for dir in dirs:
        mock_game.matrix = copy_matrix(matrices["valid_template"])
        assert mock_game.run_game(dir) == True

    assert mocked_print_label.call_count == len(dirs)
    assert mocked_crit.call_count == len(dirs)


def test_print_matrix_no_values(mock_game: Game, mock_method: Callable[..., Any]):
    """Tests, that with provided empty matrix, 'draw_rect' method
    would be called for all cells.
    'fill_playground' would be called for non zero cells, therefore
    for an empty matrix, zero times.
    """
    mock_draw_rect = mock_method(Game, "draw_rect")
    mock_fill_playground = mock_method(Game, "fill_playground")

    mock_game.print_matrix()

    assert mock_draw_rect.call_count == len(mock_game.matrix) ** 2
    assert mock_fill_playground.call_count == 0


def test_print_matrix_valid_values(
    mock_game: Game, matrices: dict[str, Any], mock_method: Callable[..., Any]
):
    """Tests, that with provided empty matrix, 'draw_rect' method
    would be called for all cells.
    'fill_playground' would be called for non zero cells, therefore
    for a non empty matrix,
    number of calls would be equal to the number of non zero cells.
    """
    mock_draw_rect = mock_method(Game, "draw_rect")
    mock_fill_playground = mock_method(Game, "fill_playground")

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.print_matrix()

    assert mock_draw_rect.call_count == len(mock_game.matrix) ** 2
    assert mock_fill_playground.call_count == non_zero_cells(mock_game.matrix)
