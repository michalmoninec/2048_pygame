import copy
import random

import pygame as pg

from game import Game

dirs = [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]


class MonteCarlo:
    def __init__(self):
        """
        Initialization of simulation with default state.
        """
        self.start = False
        self.running = False
        self.iteration_cnt = 20
        self.matrix_list = []
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]
        self.score_list_all = []
        self.screen = False

    def get_direction(self, game: Game) -> int:
        """
        Chooses direction and then runs simulation until game is over.
        Direction with best acomplished score is selected and returned.
        """
        matrix = game.matrix
        true_score = copy.deepcopy(game.score)
        for _ in range(self.iteration_cnt + 1):
            fixed_dir = dirs[random.randint(0, 3)]
            inner_matrix = copy.deepcopy(matrix)
            while (game.move_in_direction_possible(fixed_dir, inner_matrix)) == False:
                fixed_dir = dirs[random.randint(0, 3)]

            while game.game_possible_movement(inner_matrix) and self.running:
                rand_dir = dirs[random.randint(0, 3)]
                while not game.move_in_direction_possible(rand_dir, inner_matrix):
                    rand_dir = dirs[random.randint(0, 3)]

                game.update_matrix(rand_dir, inner_matrix)
                game.merge_tiles(rand_dir, inner_matrix)
                game.start_random = True
                game.place_random_tile(inner_matrix)

            if fixed_dir == pg.K_UP:
                self.score_up.append(game.score)
            if fixed_dir == pg.K_LEFT:
                self.score_left.append(game.score)
            if fixed_dir == pg.K_DOWN:
                self.score_down.append(game.score)
            if fixed_dir == pg.K_RIGHT:
                self.score_right.append(game.score)

        self.score_list_all.append(sum(self.score_up) / (len(self.score_up)))
        self.score_list_all.append(sum(self.score_left) / (len(self.score_left)))
        self.score_list_all.append(sum(self.score_down) / (len(self.score_down)))
        self.score_list_all.append(sum(self.score_right) / (len(self.score_right)))

        direction = dirs[self.score_list_all.index(max(self.score_list_all))]

        del self.score_list_all[:]
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]
        game.score = true_score
        return direction
