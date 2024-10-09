import pygame as pg
import asyncio


from pygame import Surface

from game import Game
from graphics.screen import Screen
from sprites.monte_carlo import MonteCarlo


def main() -> None:
    """
    Initialization setup for pygame, scren, game and mt simultaion.
    Start of async loop.
    """
    try:
        pg.init()
    except:
        exit()
    screen = Screen()
    game = Game()
    monte_carlo = MonteCarlo()
    surf = surface_setup(screen, game.score)

    asyncio.run(main_loop(screen, game, monte_carlo, surf))


async def main_loop(screen: Screen, game: Game, monte_carlo: MonteCarlo, surf: Surface):
    """
    Main loop handles game state, event handling, simulation state.
    """
    while True:
        if game.start:
            if screen.last == "simulation":
                screen.last = "game"
                game.reset_matrix(surf)
                game.game_over = False
            game.print_matrix(surf)

        if game.game_over and (game.screen or monte_carlo.screen):
            screen.show_game_over(surf)

        if monte_carlo.screen and monte_carlo.start:
            asyncio.create_task(mt_simulation(monte_carlo, game, surf, screen))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key in (
                    pg.K_UP,
                    pg.K_DOWN,
                    pg.K_LEFT,
                    pg.K_RIGHT,
                ):
                    game.run_game(event.key, surf)

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if game.start or monte_carlo.start:
                    screen.create_footer(surf)
                    screen.handle_footer(x, y, game, surf, monte_carlo)
                else:
                    screen.handle_menu(x, y, game, surf, monte_carlo)

        screen.update_score_view(game.score)
        pg.display.update()
        pg.display.flip()

        await asyncio.sleep(0)


async def mt_simulation(
    monte_carlo: MonteCarlo, game: Game, surf: Surface, screen: Screen
) -> None:
    """
    Simulation choose direction based on best score of random movement till game is over.
    """
    screen.last = "simulation"
    while game.game_possible_movement() and monte_carlo.running:
        direction = monte_carlo.get_direction(game)
        game.update_matrix(direction, game.matrix)
        game.merge_tiles(direction, game.matrix)
        game.start_random = True
        game.place_random_tile()
        game.print_matrix(surf)
        # screen.update_score_view(game.score)

        pg.display.update()
        # pg.display.flip()
        await asyncio.sleep(0)
    game.game_over = not game.game_possible_movement()


def surface_setup(screen: Screen, score: int) -> Surface:
    """
    Setup helper for menu creation, window resolution and score cap.
    """
    score_view = "2048 score: " + str(score)
    pg.display.set_caption(score_view)

    surf = pg.display.set_mode((400, 440))
    screen.create_menu(surf)

    return surf


if __name__ == "__main__":
    main()
