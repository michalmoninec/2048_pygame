import pygame, pytest

from game import Game
from graphics.screen import Screen
from main import main_loop
from tests.conftest import copy_matrix


def post_quit() -> None:
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def post_key(key: pygame.key) -> None:
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))


def test_main_loop_quit_game(mock_game, mcarlo, mock_surface, mock_method, screen):
    """
    Tests, that QUIT pygame event raises SystemExit.
    """
    mock_update = mock_method(pygame.display, "update")
    mock_flip = mock_method(pygame.display, "flip")

    post_quit()

    assert mock_game.player_start == False

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_update.call_count == 0
    assert mock_flip.call_count == 0


def test_main_loop_valid_move_up(
    mock_game, mock_method, matrices, screen, mcarlo, mock_surface, mock_graphics
):
    """
    Tests, that with provided valid movement, run_game method runs.
    update_score_view method of Screen class is patched to raise SystemExit and leave while loop.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.player_start = True

    mock_run_game = mock_method(
        Screen,
        "update_score_view",
        side_effect=SystemExit,
    )

    post_key(pygame.K_UP)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_game.matrix[0][0] == 4
    assert mock_game.matrix[0][1] == 2

    assert mock_run_game.call_count == 1


def test_main_loop_valid_move_down(
    mock_game, mock_method, matrices, screen, mcarlo, mock_surface, mock_graphics
):
    """
    Tests, that with provided valid movement, run_game method runs.
    update_score_view method of Screen class is patched to raise SystemExit and leave while loop.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.player_start = True

    mock_run_game = mock_method(
        Screen,
        "update_score_view",
        side_effect=SystemExit,
    )

    post_key(pygame.K_DOWN)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_game.matrix[3][0] == 4
    assert mock_game.matrix[3][1] == 2

    assert mock_run_game.call_count == 1


def test_main_loop_valid_move_left(
    mock_game, mock_method, matrices, screen, mcarlo, mock_surface, mock_graphics
):
    """
    Tests, that with provided valid movement, run_game method runs.
    update_score_view method of Screen class is patched to raise SystemExit and leave while loop.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.player_start = True

    mock_run_game = mock_method(
        Screen,
        "update_score_view",
        side_effect=SystemExit,
    )

    post_key(pygame.K_LEFT)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_game.matrix[0][0] == 4
    assert mock_game.matrix[1][0] == 2

    assert mock_run_game.call_count == 1


def test_main_loop_valid_move_right(
    mock_game, mock_method, matrices, screen, mcarlo, mock_surface, mock_graphics
):
    """
    Tests, that with provided valid movement, run_game method runs.
    update_score_view method of Screen class is patched to raise SystemExit and leave while loop.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.player_start = True

    mock_update_score = mock_method(
        Screen,
        "update_score_view",
        side_effect=SystemExit,
    )

    post_key(pygame.K_RIGHT)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_game.matrix[0][3] == 4
    assert mock_game.matrix[1][3] == 2

    assert mock_update_score.call_count == 1


def test_main_loop_end_move_left(
    mock_game, matrices, mock_method, mock_graphics, mcarlo, screen, mock_surface
):
    """
    Tests, that with provided end matrix, movement is possible, but afterwards game over occurs.
    """
    mock_game.matrix = copy_matrix(matrices["last_valid"][pygame.K_LEFT])
    mock_game.player_start = True
    mock_game.player_screen = True

    mock_show_game_over = mock_method(
        Screen,
        "show_game_over",
        side_effect=SystemExit,
    )

    post_key(pygame.K_LEFT)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()


def test_main_loop_end_move_right(
    mock_game, matrices, mock_method, mock_graphics, mcarlo, screen, mock_surface
):
    """
    Tests, that with provided end matrix, movement is possible, but afterwards game over occurs.
    """
    mock_game.matrix = copy_matrix(matrices["last_valid"][pygame.K_LEFT])
    mock_game.player_start = True
    mock_game.player_screen = True

    mock_show_game_over = mock_method(
        Screen,
        "show_game_over",
        side_effect=SystemExit,
    )

    post_key(pygame.K_RIGHT)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()


def test_main_loop_end_move_up(
    mock_game, matrices, mock_method, mock_graphics, mcarlo, screen, mock_surface
):
    """
    Tests, that with provided end matrix, movement is possible, but afterwards game over occurs.
    """
    mock_game.matrix = copy_matrix(matrices["last_valid"][pygame.K_UP])
    mock_game.player_start = True
    mock_game.player_screen = True

    mock_show_game_over = mock_method(
        Screen,
        "show_game_over",
        side_effect=SystemExit,
    )

    post_key(pygame.K_UP)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()


def test_main_loop_end_move_down(
    mock_game, matrices, mock_method, mock_graphics, mcarlo, screen, mock_surface
):
    """
    Tests, that with provided end matrix, movement is possible, but afterwards game over occurs.
    """
    mock_game.matrix = copy_matrix(matrices["last_valid"][pygame.K_UP])
    mock_game.player_start = True
    mock_game.player_screen = True

    mock_show_game_over = mock_method(
        Screen,
        "show_game_over",
        side_effect=SystemExit,
    )

    post_key(pygame.K_DOWN)

    with pytest.raises(SystemExit):
        assert main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()


# def test_main_loop_simulation_till_game_over(
#     mock_game, mock_method, matrices, screen, mcarlo, mock_surface, mock_graphics
# ):
#     """
#     Tests that simulation loop is running correctly.
#     Simulation ends with game_over attribute with True value.
#     """
#     mock_game.matrix = copy_matrix(matrices["valid_template"])
#     mcarlo.screen = True
#     mcarlo.running = True

#     mock_show_game_over = mock_method(
#         Screen,
#         "show_game_over",
#         side_effect=SystemExit,
#     )

#     with pytest.raises(SystemExit):
#         assert main_loop(screen, mock_game, mcarlo, mock_surface)
#     pygame.font.init()

#     assert mock_game.game_over == True
