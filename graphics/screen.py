import pygame as pg

from game import Game
from sprites.monte_carlo import MonteCarlo

from pygame import Surface


class Screen:
    last = None

    def __init__(self):
        """
        Initialization of font.
        """
        self.my_font = pg.font.SysFont("monospace", 30, bold="true")

    def create_menu(self, surf: Surface) -> None:
        """
        Creates menu, that is displayed at the start of application.
        """
        surf.fill((0, 0, 0))

        self.menu_play = pg.draw.rect(surf, (0, 0, 255), (150, 120, 100, 40))
        label = self.my_font.render("PLAY", 1, (255, 255, 255))
        surf.blit(label, (160, 125, 100, 40))

        self.menu_MCTS = pg.draw.rect(surf, (0, 0, 255), (150, 180, 100, 40))
        label = self.my_font.render("MCTS", 1, (255, 255, 255))
        surf.blit(label, (160, 185, 100, 40))

        self.menu_exit = pg.draw.rect(surf, (255, 0, 0), (150, 240, 100, 40))
        label = self.my_font.render("EXIT", 1, (255, 255, 255))
        surf.blit(label, (160, 245, 100, 40))

    def create_footer(self, surf: Surface) -> None:
        """
        Creates footer, that is visible while player is playing or if the simulation is running.
        """
        self.back_button = pg.draw.rect(surf, (0, 0, 255), (0, 400, 100, 40))
        label = self.my_font.render("BACK", 1, (255, 255, 255))
        surf.blit(label, (10, 405, 100, 40))

        self.footer_reset = pg.draw.rect(surf, (0, 0, 255), (295, 400, 105, 40))
        label = self.my_font.render("RESET", 1, (255, 255, 255))
        surf.blit(label, (295, 405, 100, 40))

    def handle_footer(
        self, x: int, y: int, game: Game, surf: Surface, monte_carlo: MonteCarlo
    ) -> None:
        """
        Handles footer interactions.
        """
        if self.back_button.collidepoint(x, y):
            surf.fill((0, 0, 0))
            game.start = False
            game.screen = False

            monte_carlo.start = False
            monte_carlo.screen = False
            monte_carlo.running = False

            self.create_menu(surf)

        if self.footer_reset.collidepoint(x, y):
            surf.fill((0, 0, 0))
            game.game_over = False
            game.score = 0
            game.is_win = False

            if monte_carlo.screen:
                game.start = False
                monte_carlo.start = True
                monte_carlo.running = True
            else:
                game.start = True
                monte_carlo.running = False

            game.reset_matrix(surf)
            self.create_footer(surf)

    def handle_menu(
        self, x: int, y: int, game: Game, surf: Surface, monte_carlo: MonteCarlo
    ) -> None:
        """
        Handles menu interactions.
        """
        if self.menu_play.collidepoint(x, y):
            surf.fill((0, 0, 0))
            self.create_footer(surf)
            game.start = True
            game.show_game_over = True
            game.screen = True

        elif self.menu_MCTS.collidepoint(x, y):
            self.create_footer(surf)
            monte_carlo.screen = True
            monte_carlo.start = True
            game.start = False
            game.game_over = False
            monte_carlo.running = True
            game.reset_matrix(surf)

        elif self.menu_exit.collidepoint(x, y):
            pg.quit()
            exit()

    def show_game_over(self, surf: Surface) -> None:
        """
        Displays text 'game over' over the window.
        """
        pg.draw.rect(surf, (255, 255, 255), (100, 170, 200, 60))
        label = self.my_font.render("GAME OVER", 1, (0, 0, 255))
        surf.blit(label, (120, 185, 100, 60))

    def update_score_view(self, score: int) -> None:
        """
        Updates score caption with game score.
        """
        score_view = "2048 score: " + str(score)
        pg.display.set_caption(score_view)
