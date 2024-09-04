import pygame, sys, os
import time


from game import Game
from graphics.menu import Menu
from sprites.monte_carlo import MonteCarlo


def main():
    pygame.init()
    menu = Menu()
    game = Game()

    score_view = "2048 score: " + str(game.score)
    pygame.display.set_caption(score_view)

    screen = pygame.display.set_mode((400, 440))
    menu.start_menu(screen)
    clock = pygame.time.Clock()

    monte_carlo = MonteCarlo()
    has_printed = False

    while True:
        if game.start:
            if not has_printed:
                print("Starting game...")
                has_printed = True
                game.place_random_tile(game.matrix)
            game.print_matrix(screen)
            score_view = "2048 score: " + str(game.score)
            pygame.display.set_caption(score_view)
            pygame.display.flip()

        if game.game_over:
            if not has_printed:
                print("Game over")
                has_printed = True
            myfont = pygame.font.SysFont("monospace", 30, bold="true")
            game_over_button = pygame.draw.rect(
                screen, (255, 255, 255), (100, 170, 210, 60)
            )
            label = myfont.render("GAME OVER", 1, (0, 0, 255))
            screen.blit(label, (110, 185, 100, 60))
            pygame.display.flip()

        if monte_carlo.screen:
            if monte_carlo.start:
                if not has_printed:
                    print("Starting MCTS")
                    has_printed = True
                monte_carlo.start = game.check_game(game.matrix)
                while game.check_game(game.matrix):
                    direction = monte_carlo.get_direction(game.matrix, game)
                    game.update_matrix(direction, game.matrix)
                    game.merge_tiles(direction, game.matrix)
                    game.start_random = True
                    game.place_random_tile(game.matrix)
                    game.print_matrix(screen)
                    score_view = "2048 score: " + str(game.score)
                    pygame.display.set_caption(score_view)
                    # game.score = 0
                    pygame.display.flip()
                # game.score = 0

                game.game_over = True

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                ):
                    if game.start:
                        game.run_game(event.key, screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if game.start or game.game_over or monte_carlo.start:
                    menu.create_footer(screen)
                    pygame.display.flip()
                    menu.choose_footer(x, y, game, screen, monte_carlo)
                else:
                    menu.menu_choose(x, y, game, screen, monte_carlo)


if __name__ == "__main__":
    main()
