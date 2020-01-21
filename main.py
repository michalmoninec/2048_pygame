import pygame, sys, os
import pygameMenu
from game import *

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
        #label + blit back a dodelat i reset blit + bile pozadi dole na liste
        
        #TODO: footerReset: resetuje hru

        pygame.display.flip()

    def chooseFooter(self,x,y,game, surf):
        if self.footer.collidepoint(x,y):
            print('You clicked on a Footer')
            game.start = False
            game.gameOver = False
            hasPrinted = False
            self.startMenu(surf)
        #TODO: reset pri kliknuti na tlacitko
        #reset
        #vykresleni

    def menuChoose(self,x,y,game,surf):
        if self.menuPlay.collidepoint(x,y):
            print('You hitted Play')
            self.createFooter(surf)
            game.printMatrix(surf)
            game.start = True
            #play mode
        if self.menuMCTS.collidepoint(x,y):
            print('You hitted MCTS')
            #AI mode
        if self.menuExit.collidepoint(x,y):
            print('You hitted Exit')
            #exit
            pygame.quit()
            exit()




def main():
    menu = Menu()
    pygame.init()
    pygame.display.set_caption("2048")
    screen = pygame.display.set_mode((400,440))
    menu.startMenu(screen)
    clock = pygame.time.Clock()
    print()
    
    

    game = Game()
    hasPrinted = False
     

    while True:
        #menu:
        # game.placeRandomTile()
        # game.printMatrix(screen)
        # pygame.draw.rect(screen,(255,255,255),(0,0, 20, 20))
        # pygame.display.flip()
        # print('another cycle')
        if game.start:
            if not hasPrinted:
                print('Starting game...')
                hasPrinted = True
                # screen.fill((0,0,0))
                game.placeRandomTile()
                game.printMatrix(screen)
                pygame.display.flip()
        elif game.gameOver:
            print('Game over')
            myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
            gameOverButton = pygame.draw.rect(screen,(255,255,255),(100,170, 210, 60))
            label = myfont.render("GAME OVER", 1, (0,0,255))
            screen.blit(label,(110, 185, 100, 60))
            pygame.display.flip()

            #zobrazit tlacitko na ukonceni a nastaveni game.reset = True
        elif game.reset:
            menu.startMenu(screen)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    if game.start:
                        # game.move(event.key)
                        game.run(event.key,screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    
                    if game.start:
                        menu.createFooter(screen)
                        pygame.display.flip()
                        menu.chooseFooter(x,y,game, screen)
                    else:
                        menu.menuChoose(x,y,game,screen)
        clock.tick(20)


if __name__ == "__main__":
    main()
