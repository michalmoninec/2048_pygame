import pygame, sys, os
import pygameMenu
from game import *
from monte_carlo import *
import time


#play, mcts, you vs. stupid mcts

class Menu():
    def startMenu(self, surf):
        myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
        surf.fill((0,0,0))


        self.menuPlay = pygame.draw.rect(surf,(0,0,255),(150,120, 100, 40))
        label = myfont.render("PLAY", 1, (255,255,255))
        surf.blit(label, (160,125, 100, 40))

        self.menuMCTS = pygame.draw.rect(surf,(0,0,255),(150,180, 100, 40))
        label = myfont.render("MCTS", 1, (255,255,255))
        surf.blit(label, (160,185, 100, 40))

        self.menuExit = pygame.draw.rect(surf,(255,0,0),(150,240, 100, 40))
        label = myfont.render("EXIT", 1, (255,255,255))
        surf.blit(label, (160,245, 100, 40))

        pygame.display.flip()

    def createFooter(self, surf):
        myfont = pygame.font.SysFont("monospace", 30, bold = 'true')

        self.footer = pygame.draw.rect(surf, (0,0,255), (0,400, 100, 40))
        label = myfont.render("BACK", 1, (255,255,255))
        surf.blit(label, (10,405, 100, 40))
        
        self.footerReset = pygame.draw.rect(surf, (0,0,255), (295,400, 105, 40))
        label = myfont.render("RESET", 1, (255,255,255))
        surf.blit(label, (295,405, 100, 40))

        #TODO: dodelat scoreview
        pygame.display.flip()

    def chooseFooter(self,x,y,game, surf, monteCarlo):
        if self.footer.collidepoint(x,y):
            print('You clicked on a Footer')
            game.start = False
            game.gameOver = False
            monteCarlo.start = False
            monteCarlo.screen = False
            hasPrinted = False
            self.startMenu(surf)
        if self.footerReset.collidepoint(x,y):
            print('You clicked on Reset')
            game.gameOver = False
            game.resetMatrix(surf)
            game.score = 0
            pygame.display.flip()
            if monteCarlo.screen:
                monteCarlo.start = True
            
        

    def menuChoose(self,x,y,game,surf,monteCarlo):
        if self.menuPlay.collidepoint(x,y):
            print('You hitted Play')
            self.createFooter(surf)
            game.printMatrix(surf)
            game.start = True
        if self.menuMCTS.collidepoint(x,y):
            print('You hitted MCTS')
            self.createFooter(surf)
            monteCarlo.screen = True
            monteCarlo.start = True
            game.start = False
            game.gameOver = False
            game.resetMatrix(surf)
        if self.menuExit.collidepoint(x,y):
            print('You hitted Exit')
            pygame.quit()
            exit()




def main():
    menu = Menu()
    pygame.init()
    pygame.display.set_caption("2048")
    screen = pygame.display.set_mode((400,440))
    menu.startMenu(screen)
    clock = pygame.time.Clock()
    game = Game()
    monteCarlo = MonteCarlo()
    hasPrinted = False

    while True:
        if game.start:
            if not hasPrinted:
                print('Starting game...')
                hasPrinted = True
                game.placeRandomTile(game.matrix)
            game.printMatrix(screen)
            pygame.display.flip()
            
        if game.gameOver:
            if not hasPrinted:
                print('Game over')
                hasPrinted = True
            myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
            gameOverButton = pygame.draw.rect(screen,(255,255,255),(100,170, 210, 60))
            label = myfont.render("GAME OVER", 1, (0,0,255))
            screen.blit(label,(110, 185, 100, 60))
            pygame.display.flip()

        if monteCarlo.screen:
            if monteCarlo.start:
                if not hasPrinted:
                    print("Starting MCTS")
                    hasPrinted = True
                monteCarlo.start = game.checkGame(game.matrix)
                while game.checkGame(game.matrix):
                    direction = monteCarlo.getDirection(game.matrix, game)
                    game.updateMatrix(direction,game.matrix)
                    game.mergeTiles(direction,game.matrix)
                    game.startRandom = True
                    game.placeRandomTile(game.matrix)
                    game.printMatrix(screen)
                    pygame.display.flip()
                game.score = 0
                game.gameOver = True

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if game.start:
                        game.run(event.key,screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    
                    if game.start or game.gameOver or monteCarlo.start:
                        menu.createFooter(screen)
                        pygame.display.flip()
                        menu.chooseFooter(x,y,game, screen, monteCarlo)
                    else:
                        menu.menuChoose(x,y,game,screen, monteCarlo)


if __name__ == "__main__":
    main()
