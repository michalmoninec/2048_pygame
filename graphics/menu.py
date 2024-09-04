import pygame


class Menu:
    def start_menu(self, surf):
        myfont = pygame.font.SysFont("monospace", 30, bold="true")
        surf.fill((0, 0, 0))

        self.menu_play = pygame.draw.rect(surf, (0, 0, 255), (150, 120, 100, 40))
        label = myfont.render("PLAY", 1, (255, 255, 255))
        surf.blit(label, (160, 125, 100, 40))

        self.menu_MCTS = pygame.draw.rect(surf, (0, 0, 255), (150, 180, 100, 40))
        label = myfont.render("MCTS", 1, (255, 255, 255))
        surf.blit(label, (160, 185, 100, 40))

        self.menu_exit = pygame.draw.rect(surf, (255, 0, 0), (150, 240, 100, 40))
        label = myfont.render("EXIT", 1, (255, 255, 255))
        surf.blit(label, (160, 245, 100, 40))

        pygame.display.flip()

    def create_footer(self, surf):
        myfont = pygame.font.SysFont("monospace", 30, bold="true")

        self.footer = pygame.draw.rect(surf, (0, 0, 255), (0, 400, 100, 40))
        label = myfont.render("BACK", 1, (255, 255, 255))
        surf.blit(label, (10, 405, 100, 40))

        self.footer_reset = pygame.draw.rect(surf, (0, 0, 255), (295, 400, 105, 40))
        label = myfont.render("RESET", 1, (255, 255, 255))
        surf.blit(label, (295, 405, 100, 40))

        pygame.display.flip()

    def choose_footer(self, x, y, game, surf, monte_carlo):
        if self.footer.collidepoint(x, y):
            # print("You clicked on a Footer")
            game.start = False
            game.game_over = False
            monte_carlo.start = False
            monte_carlo.screen = False
            has_printed = False
            self.start_menu(surf)
        if self.footer_reset.collidepoint(x, y):
            # print("You clicked on Reset")
            game.game_over = False
            game.reset_matrix(surf)
            game.score = 0
            pygame.display.flip()
            game.is_win = False
            if monte_carlo.screen:
                monte_carlo.start = True

    def menu_choose(self, x, y, game, surf, monte_carlo):
        if self.menu_play.collidepoint(x, y):
            # print("You hitted Play")
            self.create_footer(surf)
            game.print_matrix(surf)
            game.start = True
        if self.menu_MCTS.collidepoint(x, y):
            # print("You hitted MCTS")
            self.create_footer(surf)
            monte_carlo.screen = True
            monte_carlo.start = True
            game.start = False
            game.game_over = False
            game.reset_matrix(surf)
        if self.menu_exit.collidepoint(x, y):
            # print("You hitted Exit")
            pygame.quit()
            exit()
