import pygame

from graphics.screen import Screen


def test_init(pygame_font_type: pygame.font.Font):
    """Tests init method of Screen class.
    Checks last attribute match and my_font attribute type check.
    """
    screen = Screen()

    assert screen.last == None
    assert type(screen.my_font) == pygame_font_type
