from typing import Any
import pygame
import pytest
import threading


from game import Game
from graphics.screen import Screen
from main import surface_setup
from simulations.monte_carlo import MonteCarlo


def copy_matrix(matrix):
    return [row[:] for row in matrix]


def empty_matrix():
    return [[0 for _ in range(4)] for _ in range(4)]


def end_matrix():
    return [[i + j for i in range(1, 5)] for j in range(0, 16, 4)]


def non_zero_cells(matrix):
    return sum(1 for row in matrix for cell in row if cell != 0)


@pytest.fixture(scope="session", autouse=True)
def pygame_init_and_teardown():
    """
    Pygame initialization decorator.
    """
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game(mock_surface):
    """
    Prepares and returns Game.
    """
    return Game(mock_surface)


@pytest.fixture
def mock_game(mock_surface):
    """
    Prepares and returns Game initialized with mocked surface.
    """
    return Game(mock_surface)


@pytest.fixture
def screen():
    """
    Prepares and returns Screen.
    """
    return Screen()


@pytest.fixture
def surface(screen):
    """
    Prepares and return Surface.
    """
    return surface_setup(screen, 0)


@pytest.fixture
def mock_surface(screen, mock_method):
    """
    Prepares and return mocked Surface.
    Functions that render window are mocked for the tests.
    """
    mock_method(pygame.display, "set_mode")
    mock_method(Screen, "create_menu")

    return surface_setup(screen, 0)


@pytest.fixture
def mock_graphics(mock_method):
    mock_method(pygame.display, "update")
    mock_method(pygame.display, "flip")
    mock_method(Game, "print_matrix")
    mock_method(Game, "print_win_label")


@pytest.fixture
def mcarlo():
    return MonteCarlo()


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

    suspec_matrix = empty_matrix()
    suspec_matrix[0][0] = 2
    suspec_matrix[0][1] = 4
    suspec_matrix[0][2] = 8
    suspec_matrix[0][3] = 16

    crit_below = empty_matrix()
    crit_above = empty_matrix()
    crit_above[0][0] = 4096
    crit_exac = empty_matrix()
    crit_exac[0][0] = 2048

    mc_valid_move_left_and_right = end_matrix()
    mc_valid_move_left_and_right[0][0] = mc_valid_move_left_and_right[0][1] = 2048

    mc_valid_move_up_and_down = end_matrix()
    mc_valid_move_up_and_down[0][0] = mc_valid_move_up_and_down[1][0] = 2048

    last_valid_left = end_matrix()
    last_valid_left[3][3] = last_valid_left[3][2] = 1024

    last_valid_up = end_matrix()
    last_valid_up[3][3] = last_valid_up[2][3] = 1024

    return {
        "empty_matrix": empty_matrix(),
        "end_matrix": end_matrix(),
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
            "suspect_matrix": suspec_matrix,
        },
        "win_crit": {
            "above": crit_above,
            "below": crit_below,
            "exac": crit_exac,
        },
        "mc_valid": {
            "mc_valid_left_and_right": mc_valid_move_left_and_right,
            "mc_valid_up_and_down": mc_valid_move_up_and_down,
        },
        "last_valid": {
            pygame.K_UP: last_valid_up,
            pygame.K_LEFT: last_valid_left,
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


@pytest.fixture
def mock_method(mocker, request):
    def mock_wrapper(obj, class_method, return_value=None, side_effect=None):
        mock_method = mocker.patch.object(
            obj, class_method, return_value=return_value, side_effect=side_effect
        )
        request.addfinalizer(lambda: mocker.stop(mock_method))
        return mock_method

    return mock_wrapper
