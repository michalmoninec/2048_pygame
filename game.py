import pygame, sys, time
from pygame.locals import *
import random
import keyboard
from assets.colours import colour_dict, get_colour
import random


class Game:
    def __init__(self):
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.board_size = 4
        self.myfont = pygame.font.SysFont("monospace", 30, bold="true")
        self.tile_size = 100
        self.start_random = True
        self.start = False
        self.game_over = False
        self.reset = False
        self.score = 0
        self.is_win = False

    def print_matrix(self, surf):
        for c in range(0, self.board_size):
            for r in range(0, self.board_size):
                pygame.draw.rect(
                    surf,
                    colour_dict[self.matrix[c][r]],
                    (
                        r * self.tile_size,
                        c * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                )
                if self.matrix[c][r] != 0:
                    label = self.myfont.render(str(self.matrix[c][r]), 1, (0, 0, 0))
                    surf.blit(
                        label,
                        (
                            r * (400 / self.board_size) + 10,
                            c * (400 / self.board_size) + 10,
                        ),
                    )
        pygame.display.update()

    def is_there_space(self):
        count = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.matrix[i][j] == 0:
                    return True
        return False

    def place_random_tile(self, matrix):
        while self.start_random == True:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
            if matrix[i][j] == 0:
                rand = random.randint(0, 100)
                if rand > 10:
                    matrix[i][j] = 2
                    self.start_random = False
                    break
                else:
                    matrix[i][j] = 4
                    self.start_random = False
                    break

    def move(self, dir):
        if dir == pygame.K_UP:
            self.start_random = True
            return 0
        if dir == pygame.K_DOWN:
            self.start_random = True
            return 2
        if dir == pygame.K_RIGHT:
            self.start_random = True
            return 3
        if dir == pygame.K_LEFT:
            self.start_random = True
            return 1

    def transpose(self, A):
        N = 4
        for i in range(N):
            for j in range(i + 1, N):
                A[i][j], A[j][i] = A[j][i], A[i][j]

    def check_game(self, matrix):
        can_move_up = False
        can_move_left = False
        can_move_down = False
        can_move_right = False
        for k in range(4):
            if k == 0:  # up
                self.transpose(matrix)
                for i in range(0, self.board_size):
                    for j in range(0, self.board_size - 1):
                        if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                        ):
                            # return True
                            can_move_up = True
                self.transpose(matrix)

            elif k == 1:  # left
                for i in range(0, self.board_size):
                    for j in range(0, self.board_size - 1):
                        if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                        ):
                            can_move_left = True

            elif k == 2:  # down
                self.transpose(matrix)
                for i in range(0, self.board_size):
                    for j in range(self.board_size - 1, 0, -1):
                        if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                        ):
                            can_move_down = True
                self.transpose(matrix)

            elif k == 3:  # right
                for i in range(0, self.board_size):
                    for j in range(self.board_size - 1, 0, -1):
                        if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                        ):
                            can_move_right = True
        if (
            can_move_up == False
            and can_move_left == False
            and can_move_down == False
            and can_move_right == False
        ):
            # self.gameOver = True
            return False
        else:
            return True

    def check_if_can_move(self, direction, matrix):
        k = direction

        if k == 0:  # up
            self.transpose(matrix)
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                    ):
                        self.transpose(matrix)
                        return True

            self.transpose(matrix)
            return False

        elif k == 1:  # left
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                    ):
                        return True
            return False

        elif k == 2:  # down
            self.transpose(matrix)
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, 0, -1):
                    if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                    ):
                        self.transpose(matrix)
                        return True
            self.transpose(matrix)
            return False

        elif k == 3:  # right
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, 0, -1):
                    if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                    ):
                        return True
            return False

    def update_matrix(self, dir, matrix):

        if dir == 0:  # up
            self.transpose(matrix)
            for i in range(0, 4):
                for j in range(0, 3):
                    while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
                        for dir in range(j, 3):
                            matrix[i][dir] = matrix[i][dir + 1]
                        matrix[i][3] = 0
            self.transpose(matrix)

        elif dir == 1:  # left
            for i in range(0, 4):
                for j in range(0, 3):
                    while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
                        for dir in range(j, 3):
                            matrix[i][dir] = matrix[i][dir + 1]
                        matrix[i][3] = 0

        elif dir == 2:  # down
            self.transpose(matrix)
            for i in range(0, 4):
                for j in range(3, -1, -1):
                    while matrix[i][j] == 0 and sum(matrix[i][:j]) > 0:
                        for dir in range(j, -1, -1):
                            matrix[i][dir] = matrix[i][dir - 1]
                        matrix[i][0] = 0
            self.transpose(matrix)

        elif dir == 3:  # right
            for i in range(0, 4):
                for j in range(3, 0, -1):
                    while matrix[i][j] == 0 and sum(matrix[i][:j]) > 0:
                        for dir in range(j, -1, -1):
                            matrix[i][dir] = matrix[i][dir - 1]
                        matrix[i][0] = 0

    def merge_tiles(self, k, matice_):
        if k == 0:  # up
            self.transpose(matice_)
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if matice_[i][j] == matice_[i][j + 1] and matice_[i][j] != 0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j + 1] = 0
                        self.score += matice_[i][j]
            self.transpose(matice_)
            self.update_matrix(k, matice_)
        if k == 1:  # left
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if matice_[i][j] == matice_[i][j + 1] and matice_[i][j] != 0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j + 1] = 0
                        self.score += matice_[i][j]
            self.update_matrix(k, matice_)
        if k == 2:  # down
            self.transpose(matice_)
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, -1, -1):
                    if matice_[i][j] == matice_[i][j - 1] and matice_[i][j] != 0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j - 1] = 0
                        self.score += matice_[i][j]
            self.transpose(matice_)
            self.update_matrix(k, matice_)
        if k == 3:  # right
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, -1, -1):
                    if matice_[i][j] == matice_[i][j - 1] and matice_[i][j] != 0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j - 1] = 0
                        self.score += matice_[i][j]
            self.update_matrix(k, matice_)

    def reset_matrix(self, surf):
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.start_random = True
        self.place_random_tile(self.matrix)
        self.print_matrix(surf)

    def is_score(self, surf):
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if not self.is_win:
                    if self.matrix[i][j] == 8:
                        print("Dosahnul jsi 8")
                        self.is_win = True
                        return True

    def run_game(self, dir, surf):
        if self.check_game(self.matrix) and not self.game_over:
            # print(self.move(dir))
            if self.check_if_can_move(self.move(dir), self.matrix):
                self.update_matrix(self.move(dir), self.matrix)
                self.merge_tiles(self.move(dir), self.matrix)
                self.place_random_tile(self.matrix)
                self.print_matrix(surf)

                # print("Score is: ", self.score)

                if self.is_score(surf):
                    my_font = pygame.font.SysFont("monospace", 30, bold="true")
                    game_over_button = pygame.draw.rect(
                        surf, (255, 255, 255), (100, 170, 210, 60)
                    )
                    label = my_font.render("YOU WIN", 1, (0, 0, 255))
                    surf.blit(label, (110, 185, 100, 60))
                    pygame.display.flip()
                    time.sleep(2)
        else:
            self.start = False
            self.game_over = True
