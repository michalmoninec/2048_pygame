import pygame

from typing import Any, List

from game import Game


def copy_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """Copies matrix and returns it."""
    return [row[:] for row in matrix]


def empty_matrix() -> List[List[int]]:
    """Returns empty matrix."""
    return [[0 for _ in range(4)] for _ in range(4)]


def test_class_init(mock_surface: pygame.Surface, matrices: dict[str, list[list[int]]]):
    """Tests initialization of Game class."""
    game = Game(mock_surface)
    assert game.matrix == matrices["empty_matrix"]
    assert game.board_size == 4
    assert type(game.myfont) == type(pygame.font.SysFont("monospace", 30, bold="true"))
    assert game.tile_size == 100
    assert game.start_random == True
    assert game.player_start == False
    assert game.game_over == False
    assert game.score == 0
    assert game.is_win == False
    assert game.player_screen == False
    assert game.caption_score == None


def test_initial_random_tiles_placement(
    mock_game: Game, matrices: dict[str, list[list[int]]]
):
    """Tests empty matrix at initialization.
    Then placing random tiles.
    Then tests that matrix is not empty.
    Then tests that count of non empty cell is two.
    """
    assert mock_game.matrix == matrices["empty_matrix"]
    tile1, tile2 = mock_game.place_initial_random_tiles()
    assert mock_game.matrix != matrices["empty_matrix"]

    assert sum(sum(sub_matrix) for sub_matrix in mock_game.matrix) != 0

    i, j, k = tile1
    assert mock_game.matrix[i][j] == k
    i, j, k = tile2
    assert mock_game.matrix[i][j] == k


def test_transpose(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests transposition of matrix."""
    empty_matrix = matrices["empty_matrix"]
    assert mock_game.matrix == mock_game.transpose(mock_game.matrix)

    mock_game.matrix[0][0] = 2
    mock_game.matrix[1][1] = 2
    mock_game.matrix[2][2] = 2
    mock_game.matrix[3][3] = 2

    assert mock_game.matrix == mock_game.transpose(mock_game.matrix)

    mock_game.matrix = empty_matrix
    for i in range(len(mock_game.matrix)):
        mock_game.matrix[0][i] = 2
        mock_game.transpose(mock_game.matrix)
        assert mock_game.matrix[i][0] == 2


def test_game_possible_movement(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests if there is any possible movement."""

    assert mock_game.game_possible_movement() == False
    mock_game.matrix[0][0] = 2
    assert mock_game.game_possible_movement() == True

    end_matrix = matrices["end_matrix"]
    assert mock_game.game_possible_movement(end_matrix) == False

    mock_game.matrix = copy_matrix(matrices["end_matrix"])
    mock_game.matrix[0][0] = 99
    mock_game.matrix[0][1] = 99
    assert mock_game.game_possible_movement(mock_game.matrix) == True

    mock_game.matrix = copy_matrix(matrices["end_matrix"])
    mock_game.matrix[0][0] = 99
    mock_game.matrix[1][0] = 99
    assert mock_game.game_possible_movement(mock_game.matrix) == True

    mock_game.matrix = matrices["empty_matrix"]
    for i in range(len(mock_game.matrix) - 1):
        for j in range(len(mock_game.matrix[i]) - 1):
            mock_game.matrix = copy_matrix(matrices["empty_matrix"])
            assert mock_game.game_possible_movement(mock_game.matrix) == False
            mock_game.matrix[i][j] = mock_game.matrix[i + 1][j] = 99
            assert mock_game.game_possible_movement(mock_game.matrix) == True


def test_compress(mock_game: Game):
    """Tests compression, which should move all numbers to the left in a list."""
    input_row = [1, 0, 1, 0]
    output_row = [1, 1, 0, 0]

    assert mock_game.compress(input_row) == output_row
    assert mock_game.compress([]) == []


def test_merge(mock_game: Game):
    """Tests that same neighbour merge together and creates zero value behind merge."""
    assert mock_game.merge([]) == []
    assert mock_game.merge([2, 2, 2, 2]) == [4, 0, 4, 0]
    assert mock_game.merge([2, 0, 2, 2]) == [2, 0, 4, 0]
    assert mock_game.merge([2, 4, 8, 16]) == ([2, 4, 8, 16])


def test_move_left(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests if elements in matrix move to the left correctly."""
    mock_game.matrix = copy_matrix(matrices["empty_matrix"])
    assert mock_game.move_left(mock_game.matrix) == matrices["empty_matrix"]

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    assert (
        mock_game.move_left(mock_game.matrix)
        == matrices["valid_matrices"][pygame.K_LEFT]
    )


def test_move_up(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests if elements in matrix move up correctly."""
    mock_game.matrix = copy_matrix(matrices["empty_matrix"])
    assert mock_game.move_up(mock_game.matrix) == matrices["empty_matrix"]

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    assert (
        mock_game.move_up(mock_game.matrix) == matrices["valid_matrices"][pygame.K_UP]
    )


def test_move_right(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests if elements in matrix move up correctly."""
    mock_game.matrix = copy_matrix(matrices["empty_matrix"])
    assert mock_game.move_right(mock_game.matrix) == matrices["empty_matrix"]

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    assert (
        mock_game.move_right(mock_game.matrix)
        == matrices["valid_matrices"][pygame.K_RIGHT]
    )


def test_move_down(mock_game: Game, matrices: dict[str, list[list[int]]]):
    """Tests if elements in matrix move up correctly."""
    mock_game.matrix = copy_matrix(matrices["empty_matrix"])
    assert mock_game.move_down(mock_game.matrix) == matrices["empty_matrix"]

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    assert (
        mock_game.move_down(mock_game.matrix)
        == matrices["valid_matrices"][pygame.K_DOWN]
    )


def test_move_in_direction(
    mock_game: Game, matrices: dict[str, list[list[int]]], dirs: list[int]
):
    """Tests, that for direction move is evaluated correctly."""
    for dir in dirs:
        mock_game.matrix = copy_matrix(matrices["empty_matrix"])
        assert mock_game.move_in_direction(dir, mock_game.matrix) == None

    for dir in dirs:
        mock_game.matrix = copy_matrix(matrices["valid_template"])
        assert (
            mock_game.move_in_direction(dir, mock_game.matrix)
            == matrices["valid_matrices"][dir]
        )


def test_move_in_direction_possible(
    mock_game: Game, matrices: dict[str, list[list[int]]], dirs: list[int]
):
    """Tests invalid movement with empty matrix.
    Tests valid movement for each direction with two same values in corresponding direction.
    """
    for dir in dirs:
        assert mock_game.move_in_direction_possible(dir, mock_game.matrix) == False

    mock_game.matrix = copy_matrix(matrices["valid_template"])
    for dir in dirs:
        assert mock_game.move_in_direction_possible(dir, mock_game.matrix) == True


def test_reset_matrix(
    mock_game: Game, matrices: dict[str, Any], mock_surface: pygame.Surface
):
    """Tests that reseting matrix is correct."""
    mock_game.matrix = copy_matrix(matrices["end_matrix"])
    mock_game.reset_matrix()
    assert mock_game.matrix != matrices["end_matrix"]


def test_score_reached_criterium(mock_game: Game, matrices: dict[str, Any]):
    """Tests that while reaching value 2048, function returns True."""
    mock_game.matrix = copy_matrix(matrices["win_crit"]["above"])
    assert mock_game.score_reached_criterium() == False

    mock_game.matrix = copy_matrix(matrices["win_crit"]["below"])
    assert mock_game.score_reached_criterium() == False

    mock_game.matrix = copy_matrix(matrices["win_crit"]["exac"])
    assert mock_game.score_reached_criterium() == True


def test_game_possible_suspect(mock_game: Game, matrices: dict[str, Any]):
    """Test for one example that occured while manual testing."""
    mock_game.matrix = copy_matrix(matrices["invalid_matrices"]["suspect_matrix"])
    assert mock_game.game_possible_movement() == True
