import threading
import pygame as pg
import copy

from pygame import Surface

from game import Game
from graphics.screen import Screen
from simulations.monte_carlo import MonteCarlo


def main() -> None:
    """Initialization setup for pygame, screen, game and mt simultaion classes.
    Runs main loop with initialized classes.
    """
    try:
        pg.init()
    except:
        exit()

    screen = Screen()
    monte_carlo = MonteCarlo()
    surf = surface_setup(screen, 0)
    game = Game(surf)
    game.place_initial_random_tiles()

    main_loop(screen, game, monte_carlo, surf)


def main_loop(screen: Screen, game: Game, monte_carlo: MonteCarlo, surf: Surface):
    """Main loop handles game state, event handling, simulation state."""
    running = True
    while running:
        if game.player_start:
            if screen.last == "simulation":
                screen.last = "game"
                game.reset_matrix()
                # game.print_matrix(surf)
                game.game_over = False
            game.caption_score = game.score
            game.print_matrix()

        if game.game_over and (game.player_screen or monte_carlo.screen):
            screen.show_game_over(surf)

        if monte_carlo.screen and not monte_carlo.sim_running:
            monte_carlo.stop_event.clear()
            monte_carlo.simulation_thread = threading.Thread(
                target=mt_simulation, args=(monte_carlo, game, surf, screen)
            )
            monte_carlo.simulation_thread.start()
            monte_carlo.sim_running = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key in (
                    pg.K_UP,
                    pg.K_DOWN,
                    pg.K_LEFT,
                    pg.K_RIGHT,
                ):
                    game.run_game(event.key)

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if game.player_start or monte_carlo.screen:
                    screen.create_footer(surf)
                    screen.handle_footer(x, y, game, surf, monte_carlo)
                else:
                    screen.handle_menu(x, y, game, surf, monte_carlo)

        screen.update_score_view(game.caption_score)
        pg.display.update()
        pg.display.flip()


def mt_simulation(
    monte_carlo: MonteCarlo, game: Game, surf: Surface, screen: Screen
) -> None:
    """Simulation choose direction based on best score of random movement till game is over.
    Runs as a thread. Manual termination with footer handle.
    """
    screen.last = "simulation"
    while (
        game.game_possible_movement()
        and monte_carlo.running
        and not monte_carlo.stop_event.is_set()
    ):
        score = copy.deepcopy(game.score)
        dir = monte_carlo.get_direction(game)
        game.score = score
        if game.move_in_direction(dir, game.matrix):
            game.place_random_tile()
        game.start_random = True
        game.print_matrix()

        game.caption_score = game.score
        pg.display.update()
        pg.display.flip()
    game.game_over = not game.game_possible_movement()


def surface_setup(screen: Screen, score: int) -> Surface:
    """Setup helper for inital screen creation, window resolution and score cap."""
    pg.display.init()
    score_view = "2048 score: " + str(score)
    pg.display.set_caption(score_view)

    surf = pg.display.set_mode((400, 440))
    screen.create_menu(surf)

    return surf


if __name__ == "__main__":
    main()
