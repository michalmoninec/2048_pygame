from typing import Any
import pygame
import pytest
import threading


from game import Game
from graphics.screen import Screen
from main import surface_setup


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def empty_matrix():
    return [[0 for _ in range(4)] for _ in range(4)]


@pytest.fixture(scope="session", autouse=True)
def pygame_init_and_teardown():
    """
    Pygame initialization decorator.
    """
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game():
    """
    Prepares and returns Game.
    """
    return Game()


@pytest.fixture
def screen():
    """
    Prepares and returns Screen.
    """
    return Screen()


@pytest.fixture
def surface(screen: Screen):
    """
    Prepares and return Surface.
    """

    return surface_setup(screen, 0)


@pytest.fixture
def matrices():
    valid_matrix = empty_matrix()
    valid_matrix[0][0] = valid_matrix[0][1] = valid_matrix[1][0] = 2

    valid_left = empty_matrix()
    valid_left[0][0] = 4
    valid_left[1][0] = 2

    valid_right = empty_matrix()
    valid_right[0][3] = 4
    valid_right[1][3] = 2

    valid_up = empty_matrix()
    valid_up[0][0] = 4
    valid_up[0][1] = 2

    valid_down = empty_matrix()
    valid_down[3][0] = 4
    valid_down[3][1] = 2

    invalid_left = empty_matrix()
    invalid_left[0][0] = 4

    invalid_right = empty_matrix()
    invalid_right[0][3] = 4

    invalid_up = empty_matrix()
    invalid_up[0][0] = 4

    invalid_down = empty_matrix()
    invalid_down[3][0] = 4

    crit_below = empty_matrix()
    crit_above = empty_matrix()
    crit_above[0][0] = 4096
    crit_exac = empty_matrix()
    crit_exac[0][0] = 2048

    return {
        "empty_matrix": empty_matrix(),
        "end_matrix": [[i + j for i in range(1, 5)] for j in range(0, 16, 4)],
        "valid_template": valid_matrix,
        "valid_matrices": {
            pygame.K_UP: valid_up,
            pygame.K_DOWN: valid_down,
            pygame.K_LEFT: valid_left,
            pygame.K_RIGHT: valid_right,
        },
        "invalid_matrices": {
            pygame.K_UP: invalid_up,
            pygame.K_DOWN: invalid_down,
            pygame.K_LEFT: invalid_left,
            pygame.K_RIGHT: invalid_right,
        },
        "crit": {
            "above": crit_above,
            "below": crit_below,
            "exac": crit_exac,
        },
    }


@pytest.fixture
def dirs():
    return [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


@pytest.fixture
def mc_init_attrs():
    return {
        "values": {
            "start": False,
            "running": False,
            "iteration_cnt": 20,
            "matrix_list": [],
            "score_up": [0],
            "score_down": [0],
            "score_left": [0],
            "score_right": [0],
            "score_list_all": [],
            "screen": False,
            "sim_running": False,
            "simulation_thread": None,
        },
        "types": {
            "stop_event": type(threading.Event()),
        },
    }


@pytest.fixture
def pygame_font_type():
    return type(pygame.font.SysFont("monospace", 30, bold="true"))
