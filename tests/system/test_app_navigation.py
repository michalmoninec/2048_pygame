import pygame, pytest

from typing import List

from graphics.screen import Screen
from tests.conftest import copy_matrix
from main import main_loop


def post_mouse_down() -> None:
    """Returns pygame MOUSEBUTTONDOWN event."""
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(100, 100))


def event_seq() -> List[pygame.event.Event]:
    """Returns sequence of pygame mousebuttondown events, terminated
    with pygame QUIT event.
    """
    return [
        post_mouse_down(),
        pygame.event.Event(pygame.QUIT),
    ]


def test_mousebuttondown_menu_trigger(
    mock_game,
    mock_graphics,
    mock_method,
    matrices,
    screen,
    mcarlo,
    mock_surface,
):
    """Tests, that after mousebutton event, application reacts correctly.
    In this test, only handle_menu should be triggered.
    Simulates app navigation at main screen.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_method(pygame.event, "get", side_effect=event_seq)
    mock_footer_handler = mock_method(Screen, "handle_footer")
    mock_menu_handler = mock_method(Screen, "handle_menu")

    assert mock_game.player_start == False
    assert mcarlo.screen == False
    with pytest.raises(SystemExit):
        main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.font.init()

    assert mock_menu_handler.call_count == 1
    assert mock_footer_handler.call_count == 0


def test_mousebuttondown_footer_trigger_player(
    mock_game,
    mock_graphics,
    mock_method,
    matrices,
    screen,
    mcarlo,
    mock_surface,
):
    """Tests, that after mousebutton event, application reacts correctly.
    In this test, only handle_footer should be triggered.
    Simulatece app navigation with player mode screen.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mock_game.player_start = True

    mock_method(pygame.event, "get", side_effect=event_seq)
    mock_method(Screen, "create_footer")
    mock_footer_handler = mock_method(Screen, "handle_footer")
    mock_menu_handler = mock_method(Screen, "handle_menu")

    assert mcarlo.screen == False
    with pytest.raises(SystemExit):
        main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.init()

    assert mock_menu_handler.call_count == 0
    assert mock_footer_handler.call_count == 1


def test_mousebuttondown_footer_trigger_mcarlo(
    mock_game,
    mock_graphics,
    mock_method,
    matrices,
    screen,
    mcarlo,
    mock_surface,
):
    """Tests, that after mousebutton event, application reacts correctly.
    In this test, only handle_footer should be triggered.
    Simulates app navigation with monte carlo screen active.
    """
    mock_game.matrix = copy_matrix(matrices["valid_template"])
    mcarlo.screen = True

    mock_method(pygame.event, "get", side_effect=event_seq)
    mock_method(Screen, "create_footer")
    mock_footer_handler = mock_method(Screen, "handle_footer")
    mock_menu_handler = mock_method(Screen, "handle_menu")

    assert mock_game.player_start == False
    with pytest.raises(SystemExit):
        main_loop(screen, mock_game, mcarlo, mock_surface)
    pygame.init()

    assert mock_menu_handler.call_count == 0
    assert mock_footer_handler.call_count == 1
