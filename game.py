import pygame, time
import random

from pygame import Surface
from assets.colours import colour_dict, get_colour


class Game:
    def __init__(self):
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.board_size = 4
        self.myfont = pygame.font.SysFont("monospace", 30, bold="true")
        self.tile_size = 100
        self.start_random = True
        self.start = False
        self.game_over = False
        self.score = 0
        self.is_win = False
        self.screen = False

        self.place_random_tile()

    def print_matrix(self, surf: Surface) -> None:
        for col in range(self.board_size):
            for row in range(self.board_size):
                pygame.draw.rect(
                    surf,
                    colour_dict[self.matrix[col][row]],
                    (
                        row * self.tile_size,
                        col * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                )
                if self.matrix[col][row] != 0:
                    label = self.myfont.render(str(self.matrix[col][row]), 1, (0, 0, 0))
                    label_width, label_height = label.get_size()
                    surf.blit(
                        label,
                        (
                            row * (400 / self.board_size)
                            + (400 / self.board_size - label_width) / 2,
                            col * (400 / self.board_size)
                            + (400 / self.board_size - label_height) / 2,
                        ),
                    )

    def run_game(self, dir: int, surf: Surface) -> None:
        if self.start:
            if self.game_possible_movement() and not self.game_over:
                if self.move_in_direction_possible(dir, self.matrix):
                    self.update_matrix(dir, self.matrix)
                    self.merge_tiles(dir, self.matrix)
                    self.place_random_tile()
                    self.print_matrix(surf)

                    if self.is_score():
                        pygame.draw.rect(surf, (255, 255, 255), (100, 170, 210, 60))
                        label = self.my_font.render("YOU WON", 1, (0, 0, 255))
                        surf.blit(label, (110, 185, 100, 60))
                        time.sleep(2)
            else:
                self.game_over = True

    def place_random_tile(self, matrix=None):
        if matrix is None:
            matrix = self.matrix
        self.start_random = True
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

    def transpose(self, matrix):
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    def game_possible_movement(self, matrix=None) -> bool:
        if matrix is None:
            matrix = self.matrix
        can_move_up = False
        can_move_left = False
        can_move_down = False
        can_move_right = False
        for k in range(4):
            if k == 0:
                self.transpose(matrix)
                for i in range(0, self.board_size):
                    for j in range(0, self.board_size - 1):
                        if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                        ):
                            can_move_up = True
                self.transpose(matrix)

            elif k == 1:
                for i in range(0, self.board_size):
                    for j in range(0, self.board_size - 1):
                        if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                        ):
                            can_move_left = True

            elif k == 2:
                self.transpose(matrix)
                for i in range(0, self.board_size):
                    for j in range(self.board_size - 1, 0, -1):
                        if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                            matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                        ):
                            can_move_down = True
                self.transpose(matrix)

            elif k == 3:
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
            return False
        return True

    def move_in_direction_possible(self, dir: int, matrix):

        if dir == pygame.K_UP:
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

        elif dir == pygame.K_LEFT:
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if (matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][j:]) > 0
                    ):
                        return True
            return False

        elif dir == pygame.K_DOWN:
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

        elif dir == pygame.K_RIGHT:
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, 0, -1):
                    if (matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0) or (
                        matrix[i][j] == 0 and sum(matrix[i][:j]) > 0
                    ):
                        return True
            return False

    def update_matrix(self, dir: int, matrix):

        if dir == pygame.K_UP:
            self.transpose(matrix)
            for i in range(0, 4):
                for j in range(0, 3):
                    while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
                        for dir in range(j, 3):
                            matrix[i][dir] = matrix[i][dir + 1]
                        matrix[i][3] = 0
            self.transpose(matrix)

        elif dir == pygame.K_LEFT:
            for i in range(0, 4):
                for j in range(0, 3):
                    while matrix[i][j] == 0 and sum(matrix[i][j:]) > 0:
                        for dir in range(j, 3):
                            matrix[i][dir] = matrix[i][dir + 1]
                        matrix[i][3] = 0

        elif dir == pygame.K_DOWN:
            self.transpose(matrix)
            for i in range(0, 4):
                for j in range(3, -1, -1):
                    while matrix[i][j] == 0 and sum(matrix[i][:j]) > 0:
                        for dir in range(j, -1, -1):
                            matrix[i][dir] = matrix[i][dir - 1]
                        matrix[i][0] = 0
            self.transpose(matrix)

        elif dir == pygame.K_RIGHT:
            for i in range(0, 4):
                for j in range(3, 0, -1):
                    while matrix[i][j] == 0 and sum(matrix[i][:j]) > 0:
                        for dir in range(j, -1, -1):
                            matrix[i][dir] = matrix[i][dir - 1]
                        matrix[i][0] = 0

    def merge_tiles(self, k, matrix):
        if k == pygame.K_UP:
            self.transpose(matrix)
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                        matrix[i][j] = matrix[i][j] * 2
                        matrix[i][j + 1] = 0
                        self.score += matrix[i][j]
            self.transpose(matrix)
            self.update_matrix(k, matrix)
        if k == pygame.K_LEFT:
            for i in range(0, self.board_size):
                for j in range(0, self.board_size - 1):
                    if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                        matrix[i][j] = matrix[i][j] * 2
                        matrix[i][j + 1] = 0
                        self.score += matrix[i][j]
            self.update_matrix(k, matrix)
        if k == pygame.K_DOWN:
            self.transpose(matrix)
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, -1, -1):
                    if matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0:
                        matrix[i][j] = matrix[i][j] * 2
                        matrix[i][j - 1] = 0
                        self.score += matrix[i][j]
            self.transpose(matrix)
            self.update_matrix(k, matrix)
        if k == pygame.K_RIGHT:
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, -1, -1):
                    if matrix[i][j] == matrix[i][j - 1] and matrix[i][j] != 0:
                        matrix[i][j] = matrix[i][j] * 2
                        matrix[i][j - 1] = 0
                        self.score += matrix[i][j]
            self.update_matrix(k, matrix)

    def reset_matrix(self, surf):
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.start_random = True
        self.place_random_tile()
        self.print_matrix(surf)

    def is_score(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if not self.is_win:
                    if self.matrix[i][j] == 2048:
                        self.is_win = True
                        return True
        return False
