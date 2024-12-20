from typing import Any, List
import pygame as pg

from game import Game
from simulations.monte_carlo import MonteCarlo
from tests.conftest import copy_matrix


def test_get_direction_invalid_all_movement(
    mock_game: Game, matrices: dict[str, Any], mcarlo: MonteCarlo
):
    """Tests, that for matrix, that has no valid movement return
    value of direction is None.
    """
    mock_game.matrix = copy_matrix(matrices["empty_matrix"])

    assert mock_game.game_possible_movement() == False
    dir = mcarlo.get_direction(mock_game)
    assert dir is None


def test_get_direction_valid_movement(
    mock_game: Game, matrices: dict[str, Any], mcarlo: MonteCarlo
):
    """Tests, that for matrix, that has some valid movement return
    value of direction is not None.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])

    assert mock_game.game_possible_movement() == True
    dir = mcarlo.get_direction(mock_game)
    assert dir is not None


def test_get_direction_valid_left_or_right(
    mock_game: Game, matrices: dict[str, Any], mcarlo: MonteCarlo
):
    """Tests, that direction for provided matrix is either left or right."""
    mock_game.matrix = copy_matrix(matrices["mc_valid"]["mc_valid_left_and_right"])
    assert mock_game.game_possible_movement() == True
    dir = mcarlo.get_direction(mock_game)
    assert dir in [pg.K_LEFT, pg.K_RIGHT]


def test_get_direction_valid_up_or_down(
    mock_game: Game, matrices: dict[str, Any], mcarlo: MonteCarlo
):
    """Tests, that direction for provided matrix is either left or right."""
    mock_game.matrix = copy_matrix(matrices["mc_valid"]["mc_valid_up_and_down"])
    assert mock_game.game_possible_movement() == True
    dir = mcarlo.get_direction(mock_game)
    assert dir in [pg.K_UP, pg.K_DOWN]


def test_get_direction_long(mock_game: Game, dirs: List[int], mcarlo: MonteCarlo):
    """Tests, that for starting matrix with twoo tiles, there is no
    error and direction is valid.
    """
    mock_game.place_initial_random_tiles()
    assert mock_game.game_possible_movement() == True
    dir = mcarlo.get_direction(mock_game)
    assert dir in dirs
