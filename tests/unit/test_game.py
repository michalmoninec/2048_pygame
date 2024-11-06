from typing import Any
import pygame
import pytest
import copy

from functools import wraps

from game import Game
from graphics.screen import Screen
from main import surface_setup


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def empty_matrix():
    return [[0 for _ in range(4)] for _ in range(4)]


def test_class_init(matrices: dict[str, list[list[int]]]):
    """
    Tests initialization of Game class.
    """
    game = Game()
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
    game: Game, matrices: dict[str, list[list[int]]]
):
    """
    Tests empty matrix at initialization.
    Then placing random tiles.
    Then tests that matrix is not empty.
    Then tests that count of non empty cell is two.
    """
    assert game.matrix == matrices["empty_matrix"]
    tile1, tile2 = game.place_initial_random_tiles()
    assert game.matrix != matrices["empty_matrix"]

    assert sum(sum(sub_matrix) for sub_matrix in game.matrix) != 0

    i, j, k = tile1
    assert game.matrix[i][j] == k
    i, j, k = tile2
    assert game.matrix[i][j] == k


def test_transpose(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests transposition of matrix.
    """
    empty_matrix = matrices["empty_matrix"]
    assert game.matrix == game.transpose(game.matrix)

    game.matrix[0][0] = 2
    game.matrix[1][1] = 2
    game.matrix[2][2] = 2
    game.matrix[3][3] = 2

    assert game.matrix == game.transpose(game.matrix)

    game.matrix = empty_matrix
    for i in range(len(game.matrix)):
        game.matrix[0][i] = 2
        game.transpose(game.matrix)
        assert game.matrix[i][0] == 2


def test_game_possible_movement(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests if there is any possible movement.
    """

    assert game.game_possible_movement() == False
    game.matrix[0][0] = 2
    assert game.game_possible_movement() == True

    end_matrix = matrices["end_matrix"]
    assert game.game_possible_movement(end_matrix) == False

    game.matrix = copy_matrix(matrices["end_matrix"])
    game.matrix[0][0] = 99
    game.matrix[0][1] = 99
    assert game.game_possible_movement(game.matrix) == True

    game.matrix = copy_matrix(matrices["end_matrix"])
    game.matrix[0][0] = 99
    game.matrix[1][0] = 99
    assert game.game_possible_movement(game.matrix) == True

    game.matrix = matrices["empty_matrix"]
    for i in range(len(game.matrix) - 1):
        for j in range(len(game.matrix[i]) - 1):
            game.matrix = copy_matrix(matrices["empty_matrix"])
            assert game.game_possible_movement(game.matrix) == False
            game.matrix[i][j] = game.matrix[i + 1][j] = 99
            assert game.game_possible_movement(game.matrix) == True


def test_compress(game: Game):
    """
    Tests compression, which should move all numbers to the left in a list.
    """
    input_row = [1, 0, 1, 0]
    output_row = [1, 1, 0, 0]

    assert game.compress(input_row) == output_row
    assert game.compress([]) == []


def test_merge(game: Game):
    """
    Tests that same neighbour merge together and creates zero value behind merge.
    """
    assert game.merge([]) == []
    assert game.merge([2, 2, 2, 2]) == [4, 0, 4, 0]
    assert game.merge([2, 0, 2, 2]) == [2, 0, 4, 0]
    assert game.merge([2, 4, 8, 16]) == ([2, 4, 8, 16])


def test_move_left(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests if elements in matrix move to the left correctly.
    """
    game.matrix = copy_matrix(matrices["empty_matrix"])
    assert game.move_left(game.matrix) == matrices["empty_matrix"]

    game.matrix = copy_matrix(matrices["valid_template"])
    assert game.move_left(game.matrix) == matrices["valid_matrices"][pygame.K_LEFT]


def test_move_up(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests if elements in matrix move up correctly.
    """
    game.matrix = copy_matrix(matrices["empty_matrix"])
    assert game.move_up(game.matrix) == matrices["empty_matrix"]

    game.matrix = copy_matrix(matrices["valid_template"])
    assert game.move_up(game.matrix) == matrices["valid_matrices"][pygame.K_UP]


def test_move_right(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests if elements in matrix move up correctly.
    """
    game.matrix = copy_matrix(matrices["empty_matrix"])
    assert game.move_right(game.matrix) == matrices["empty_matrix"]

    game.matrix = copy_matrix(matrices["valid_template"])
    assert game.move_right(game.matrix) == matrices["valid_matrices"][pygame.K_RIGHT]


def test_move_down(game: Game, matrices: dict[str, list[list[int]]]):
    """
    Tests if elements in matrix move up correctly.
    """
    game.matrix = copy_matrix(matrices["empty_matrix"])
    assert game.move_down(game.matrix) == matrices["empty_matrix"]

    game.matrix = copy_matrix(matrices["valid_template"])
    assert game.move_down(game.matrix) == matrices["valid_matrices"][pygame.K_DOWN]


def test_move_in_direction(
    game: Game, matrices: dict[str, list[list[int]]], dirs: list[int]
):
    for dir in dirs:
        game.matrix = copy_matrix(matrices["empty_matrix"])
        assert game.move_in_direction(dir, game.matrix) == None

    for dir in dirs:
        game.matrix = copy_matrix(matrices["valid_template"])
        assert (
            game.move_in_direction(dir, game.matrix) == matrices["valid_matrices"][dir]
        )


def test_move_in_direction_possible(
    game: Game, matrices: dict[str, list[list[int]]], dirs: list[int]
):
    """
    Tests invalid movement with empty matrix.
    Tests valid movement for each direction with two same values in corresponding direction.
    """
    for dir in dirs:
        assert game.move_in_direction_possible(dir, game.matrix) == False

    game.matrix = copy_matrix(matrices["valid_template"])
    for dir in dirs:
        assert game.move_in_direction_possible(dir, game.matrix) == True


def test_reset_matrix(game: Game, matrices: dict[str, Any], surface):
    """
    Tests that reseting matrix is correct.
    """
    game.matrix = copy_matrix(matrices["end_matrix"])
    game.reset_matrix()
    assert game.matrix != matrices["end_matrix"]


def test_score_reached_criterium(game: Game, matrices):
    """
    Tests that while reaching value 2048, function returns True.
    """
    game.matrix = copy_matrix(matrices["crit"]["above"])
    assert game.score_reached_criterium() == False

    game.matrix = copy_matrix(matrices["crit"]["below"])
    assert game.score_reached_criterium() == False

    game.matrix = copy_matrix(matrices["crit"]["exac"])
    assert game.score_reached_criterium() == True
