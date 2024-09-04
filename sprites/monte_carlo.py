import copy
import random


class MonteCarlo:
    def __init__(self):
        self.start = False
        self.iteration_cnt = 20
        self.matrix_list = []
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]
        self.score_list_all = []
        self.screen = False

    def get_direction(self, matrix, game):

        true_score = copy.deepcopy(game.score)
        for i in range(self.iteration_cnt + 1):
            k = random.randint(0, 3)  # smer, kterym se ma hra posunout
            inner_matrix = copy.deepcopy(matrix)
            # print("score is: ", trueScore)
            while (
                game.check_if_can_move(k, inner_matrix)
            ) == False:  # pokud vyberu smer, kterym nemuzu, vyberu jiny smer
                k = random.randint(0, 3)

            while game.check_game(inner_matrix):  # hraju dokud muzu random postupem
                a = random.randint(0, 3)
                while not game.check_if_can_move(a, inner_matrix):
                    a = random.randint(0, 3)

                game.update_matrix(a, inner_matrix)
                game.merge_tiles(a, inner_matrix)
                game.start_random = True
                game.place_random_tile(inner_matrix)

            if k == 0:
                self.score_up.append(game.score)
            if k == 1:
                self.score_left.append(game.score)
            if k == 2:
                self.score_down.append(game.score)
            if k == 3:
                self.score_right.append(game.score)

        self.score_list_all.append(sum(self.score_up) / (len(self.score_up)))
        self.score_list_all.append(sum(self.score_left) / (len(self.score_left)))
        self.score_list_all.append(sum(self.score_down) / (len(self.score_down)))
        self.score_list_all.append(sum(self.score_right) / (len(self.score_right)))

        direction = self.score_list_all.index(max(self.score_list_all))

        del self.score_list_all[:]
        self.score_up = [0]
        self.score_down = [0]
        self.score_left = [0]
        self.score_right = [0]
        game.score = true_score
        return direction
