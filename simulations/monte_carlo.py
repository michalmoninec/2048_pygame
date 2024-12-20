import copy
import random
import threading
import pygame as pg
from typing import Optional

from game import Game

dirs = [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]


class MonteCarlo:
    def __init__(self, iteration_cnt: int):
        self.iteration_cnt = iteration_cnt
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]
        self.score_all = {}
        self.screen = False
        self.running = False
        self.stop_event = threading.Event()
        self.sim_running = False
        self.simulation_thread = None

    def get_direction(self, game: Game) -> Optional[int]:
        """Chooses a fixed direction and then runs simulation with random directions
        until the game is over. The direction with the best accomplished score is selected and returned.
        """
        self.reset_scores()

        matrix = copy.deepcopy(game.matrix)

        if game.game_possible_movement(game.matrix):
            for _ in range(self.iteration_cnt + 1):
                fixed_dir = self.get_random_direction()
                inner_matrix = copy.deepcopy(matrix)

                while not game.move_in_direction_possible(fixed_dir, inner_matrix):
                    fixed_dir = self.get_random_direction()

                while (
                    game.game_possible_movement(inner_matrix)
                    and self.sim_running
                    and not self.stop_event.is_set()
                ):
                    rand_dir = self.get_random_direction()
                    while not game.move_in_direction_possible(rand_dir, inner_matrix):
                        rand_dir = self.get_random_direction()

                    if game.move_in_direction(rand_dir, inner_matrix):
                        game.place_random_tile(inner_matrix)
                    game.start_random = True

                self.update_scores(fixed_dir, game.score)

            direction = self.get_best_direction()
            self.score_all = {}
            return direction
        else:
            return None

    def reset_scores(self):
        """Resets the scores for each direction."""
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]

    def get_random_direction(self) -> int:
        """Returns a random direction."""
        return random.choice([pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT])

    def update_scores(self, direction: int, score: int):
        """Updates the scores for the given direction."""
        if direction == pg.K_UP:
            self.score_up.append(score)
        elif direction == pg.K_LEFT:
            self.score_left.append(score)
        elif direction == pg.K_DOWN:
            self.score_down.append(score)
        elif direction == pg.K_RIGHT:
            self.score_right.append(score)

    def get_best_direction(self) -> int:
        """Calculates and returns the direction with the highest average score."""
        self.score_all[pg.K_UP] = sum(self.score_up) / len(self.score_up)
        self.score_all[pg.K_LEFT] = sum(self.score_left) / len(self.score_left)
        self.score_all[pg.K_DOWN] = sum(self.score_down) / len(self.score_down)
        self.score_all[pg.K_RIGHT] = sum(self.score_right) / len(self.score_right)

        return max(self.score_all, key=self.score_all.get)
