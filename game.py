import pygame, time
import random
import copy

from pygame import Surface
from typing import List

from assets.colours import colour_dict


class Game:
    def __init__(self):
        """
        Initializes empty matrix, and game parameters.
        """
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
        self.place_random_tile()

    def run_game(self, dir: int, surf: Surface) -> None:
        """
        Updates game state with provided direction.
        """
        if self.start:
            if self.game_possible_movement() and not self.game_over:
                self.move_in_direction(dir, self.matrix)

                if self.is_score():
                    pygame.draw.rect(surf, (255, 255, 255), (100, 170, 210, 60))
                    label = self.my_font.render("YOU WON", 1, (0, 0, 255))
                    surf.blit(label, (110, 185, 100, 60))
                    time.sleep(2)
            else:
                self.game_over = True

    def print_matrix(self, surf: Surface) -> None:
        """
        Print game matrix with corresponding numbers inside cells.
        Each number has it's own colour.
        """
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

    def place_random_tile(self, matrix: List[List[int]] = None) -> None:
        """
        Places random tile into game matrix.
        With probability of 90 percent it is number 2, otherwise number 4.
        """
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

    def transpose(self, matrix: List[List[int]]) -> None:
        """
        Switches columns for rows and vice versa.
        """
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    def game_possible_movement(self, matrix: List[List[int]] = None) -> bool:
        """
        Checks if there is any free space or if there are any tiles with same value.
        """
        if matrix is None:
            matrix = self.matrix

        for row in matrix:
            if 0 in row:
                return True

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if j < len(matrix[i]) - 1 and matrix[i][j] == matrix[i][j + 1]:
                    return True
                if i < len(matrix) - 1 and matrix[i][j] == matrix[i + 1][j]:
                    return True
        return False

    def compress(self, row: List[int]) -> List[int]:
        """
        Takes only non zero values and move them to the left.
        Rest of length of row is filled with zeros.
        """
        new_row = [i for i in row if i != 0]
        new_row += [0] * (len(row) - len(new_row))
        return new_row

    def merge(self, row: List[int]) -> List[int]:
        """
        Merges same values together and creates empty after merge.
        """
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move_left(self, matrix: List[List[int]]) -> None:
        """
        Handles move left.
        Native move function, that compress row, merge it and then compress it again.
        Resulting in having merged items on the left side.
        All other direction are derivates of this function.
        """
        for i in range(0, self.board_size):
            matrix[i] = self.compress(matrix[i])
            matrix[i] = self.merge(matrix[i])
            matrix[i] = self.compress(matrix[i])

    def move_up(self, matrix: List[List[int]]) -> None:
        """
        Handles movement up.
        Movement up is the same as movement left, only with matrix transposition added.
        """
        self.transpose(matrix)
        self.move_left(matrix)
        self.transpose(matrix)

    def move_right(self, matrix: List[List[int]]) -> None:
        """
        Handles move right.
        Reverses matrix, then do the same as movement left.
        Movement right is the same as movement left, with reversed order of matrix.
        """
        for i in range(0, self.board_size):
            matrix[i] = matrix[i][::-1]
            matrix[i] = self.compress(matrix[i])
            matrix[i] = self.merge(matrix[i])
            matrix[i] = self.compress(matrix[i])
            matrix[i] = matrix[i][::-1]

    def move_down(self, matrix: List[List[int]]) -> None:
        """
        Handles movement down.
        Movement down is the same as movement right, only with matrix transpotion added.
        """
        self.transpose(matrix)
        self.move_right(matrix)
        self.transpose(matrix)

    def move_in_direction(self, dir: int, matrix: List[List[int]]) -> bool:
        """
        Moves in provided direction.
        If the original matrix is not the same as the updated, move is valid.
        If the move is valid, there is new value placed on a random tile.
        Validity of move is returned.
        """
        original_matrix = copy.deepcopy(matrix)
        if dir == pygame.K_UP:
            self.move_up(matrix)
        elif dir == pygame.K_LEFT:
            self.move_left(matrix)
        elif dir == pygame.K_DOWN:
            self.move_down(matrix)
        elif dir == pygame.K_RIGHT:
            self.move_right(matrix)

        if original_matrix != matrix:
            self.place_random_tile(matrix)
            return True
        return False

    def move_in_direction_possible(self, dir: int, matrix: List[List[int]]) -> bool:
        """
        Checks if movement in provided direction is possible.
        """
        dummy = copy.deepcopy(matrix)
        return self.move_in_direction(dir, dummy)

    def reset_matrix(self, surf: Surface):
        """
        Resets matrix to default state with one random tile.
        """
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.start_random = True
        self.place_random_tile()
        self.place_random_tile()
        self.print_matrix(surf)

    def is_score(self) -> bool:
        """
        Checks if score 2048 was acomplished somewhere in matrix.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if not self.is_win:
                    if self.matrix[i][j] == 2048:
                        self.is_win = True
                        return True
        return False
