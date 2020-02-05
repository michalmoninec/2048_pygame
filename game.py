import pygame, sys, time
from pygame.locals import *
import random
import keyboard
from colours import *
import random


class Game:
    def __init__(self):
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.boardSize = 4
        self.myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
        self.tileSize = 100
        self.startRandom = True
        self.start = False
        self.gameOver = False
        self.reset = False
        self.score = 0
        self.isWin = False

    def printMatrix(self,surf):
        for c in range(0,self.boardSize):
            for r in range (0, self.boardSize):
              pygame.draw.rect(surf,colour_dict[self.matrix[c][r]],(r*self.tileSize,c*self.tileSize,self.tileSize,self.tileSize))
              if self.matrix[c][r] != 0:
                label = self.myfont.render(str(self.matrix[c][r]), 1, (0,0,0))
                surf.blit(label, (r*(400/self.boardSize) + 10, c*(400/self.boardSize) + 10))  
        pygame.display.update()

    def isThereSpace(self):
        count = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.matrix[i][j] == 0:
                    return True
        print('Matice uz je plna!')
        return False
        
    def placeRandomTile(self, matrix):
        # if self.isThereSpace():
        while self.startRandom == True:
            i = random.randint(0,3)
            j = random.randint(0,3)
            if matrix[i][j] == 0:
                rand = random.randint(0,100)
                if rand>10:
                    matrix[i][j] = 2
                    self.startRandom = False
                    break
                else:
                    matrix[i][j] = 4
                    self.startRandom = False
                    break

    def move(self, dir):
        if dir == pygame.K_UP:
            # print('Nahoru')
            self.startRandom = True
            return 0
        if dir == pygame.K_DOWN:
            # print('Dolu')
            self.startRandom = True
            return 2
        if dir == pygame.K_RIGHT:
            # print('Doprava')
            self.startRandom = True
            return 3
        if dir == pygame.K_LEFT:
            # print('Doleva')
            self.startRandom = True
            return 1

    def transpose(self,A):
        N = 4
        for i in range(N):
            for j in range(i+1, N):
                A[i][j], A[j][i] = A[j][i], A[i][j]

    def checkGame(self,matrix):
        canMove0 = False
        canMove1 = False
        canMove2 = False
        canMove3 = False
        for k in range (4):
            if k == 0: #nahoru
                self.transpose(matrix)
                for i in range(0, self.boardSize):
                    for j in range(0, self.boardSize -1):
                        if (matrix[i][j] == matrix[i][j+1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][j:])>0):
                            #return True
                            canMove0 = True
                self.transpose(matrix)


            elif k == 1: #doleva
                for i in range(0, self.boardSize):
                    for j in range(0, self.boardSize -1):
                        if (matrix[i][j] == matrix[i][j+1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][j:])>0):
                            canMove1 = True


            elif k == 2: #dolu
                self.transpose(matrix)
                for i in range(0, self.boardSize):
                    for j in range(self.boardSize - 1,0,-1):
                        if (matrix[i][j] == matrix[i][j-1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][:j])>0):
                            canMove2 = True
                self.transpose(matrix)


            elif k == 3: #doprava
                for i in range(0, self.boardSize):
                    for j in range(self.boardSize - 1,0,-1):
                        if (matrix[i][j] == matrix[i][j-1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][:j])>0):
                            canMove3 = True
        if (canMove0 == False and canMove1 == False and canMove2 == False and canMove3 == False):
            # self.gameOver = True
            return False
        else:
            return True

    def checkIfCanMove(self,direction,matrix):
        k = direction

        if k == 0: #nahoru
            self.transpose(matrix)
            for i in range(0, self.boardSize):
                for j in range(0, self.boardSize -1):
                    if (matrix[i][j] == matrix[i][j+1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][j:])>0):
                        self.transpose(matrix)
                        return True
                        canMoveUP = True
            self.transpose(matrix)
            return False
            


        elif k == 1: #doleva
            for i in range(0, self.boardSize):
                for j in range(0, self.boardSize -1):
                    if (matrix[i][j] == matrix[i][j+1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][j:])>0):
                        return True
                        canMoveLEFT = True
            return False


        elif k == 2: #dolu
            self.transpose(matrix)
            for i in range(0, self.boardSize):
                for j in range(self.boardSize - 1,0,-1):
                    if (matrix[i][j] == matrix[i][j-1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][:j])>0):
                        self.transpose(matrix)
                        return True
                        canMoveDOWN = True
            self.transpose(matrix)
            return False


        elif k == 3: #doprava
            for i in range(0, self.boardSize):
                for j in range(self.boardSize - 1,0,-1):
                    if (matrix[i][j] == matrix[i][j-1] and matrix[i][j]!=0) or (matrix[i][j]==0 and sum(matrix[i][:j])>0):
                        return True
                        canMoveRIGHT = True
            return False

        

    def updateMatrix(self,k,matice_):

        if k == 0: #nahoru
            self.transpose(matice_)
            for i in range (0,4):
                for j in range (0,3):
                    while matice_[i][j]==0 and sum(matice_[i][j:])>0:
                        for k in range(j,3):
                            matice_[i][k] = matice_[i][k+1]
                        matice_[i][3]=0
            self.transpose(matice_)

        elif k==1: #doleva
            for i in range (0,4):
                for j in range (0,3):
                    while matice_[i][j]==0 and sum(matice_[i][j:])>0:
                        for k in range(j,3):
                            matice_[i][k] = matice_[i][k+1]
                        matice_[i][3]=0


        elif k==2: #dolu
            self.transpose(matice_)
            for i in range (0,4):
                for j in range (3,-1,-1):
                    while matice_[i][j]==0 and sum(matice_[i][:j])>0:
                        for k in range(j,-1,-1):
                            matice_[i][k] = matice_[i][k-1]
                        matice_[i][0]=0
            self.transpose(matice_)

        elif k==3: #vpravo
            for i in range (0,4):
                for j in range (3,0,-1):
                    while matice_[i][j]==0 and sum(matice_[i][:j])>0:
                        for k in range(j,-1,-1):
                            matice_[i][k] = matice_[i][k-1]
                        matice_[i][0]=0

    def mergeTiles(self,k,matice_):
        if k == 0: #nahoru
            self.transpose(matice_)
            for i in range(0, self.boardSize):
                for j in range(0, self.boardSize -1):
                    if matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0:
                            matice_[i][j] = matice_[i][j] * 2
                            matice_[i][j+1] = 0
                            self.score += matice_[i][j]
                            # matice.hodnota += matice_[i][j]
            self.transpose(matice_)
            self.updateMatrix(k,matice_)
        if k == 1: #doleva
            for i in range(0, self.boardSize):
                for j in range(0, self.boardSize -1):
                    if matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0:
                            matice_[i][j] = matice_[i][j] * 2
                            matice_[i][j+1] = 0
                            self.score += matice_[i][j]
                            # matice.hodnota += matice_[i][j]
            self.updateMatrix(k,matice_)
        if k == 2: #dolu
            self.transpose(matice_)
            for i in range(0, self.boardSize):
                for j in range(self.boardSize - 1,-1,-1):
                    if matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0:
                            matice_[i][j] = matice_[i][j] * 2
                            matice_[i][j-1] = 0
                            self.score += matice_[i][j]
                            # matice.hodnota += matice_[i][j]
            self.transpose(matice_)
            self.updateMatrix(k,matice_)
        if k == 3: #doprava
            for i in range(0, self.boardSize):
                for j in range(self.boardSize - 1,-1,-1):
                    if matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0:
                                matice_[i][j] = matice_[i][j] * 2
                                matice_[i][j-1] = 0
                                self.score += matice_[i][j]
                                # matice.hodnota += matice_[i][j]
            self.updateMatrix(k,matice_)

    def resetMatrix(self, surf):
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.startRandom = True
        self.placeRandomTile(self.matrix)
        self.printMatrix(surf)

    def isScore(self,surf):
        for i in range(0, self.boardSize):
            for j in range(0,self.boardSize):
                if not self.isWin:
                    if self.matrix[i][j] == 8:
                        print("Dosahnul jsi 8")
                        self.isWin = True
                        return True
                    


    def run(self,dir,surf):
        if self.checkGame(self.matrix) and not self.gameOver:
        # print(self.move(dir))
            if self.checkIfCanMove(self.move(dir),self.matrix):
                self.updateMatrix(self.move(dir),self.matrix)
                self.mergeTiles(self.move(dir),self.matrix)
                self.placeRandomTile(self.matrix)
                self.printMatrix(surf)
                
                print("Score is: ", self.score)
                
                if self.isScore(surf):
                    myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
                    gameOverButton = pygame.draw.rect(surf,(255,255,255),(100,170, 210, 60))
                    label = myfont.render("YOU WIN", 1, (0,0,255))
                    surf.blit(label,(110, 185, 100, 60))
                    pygame.display.flip()
                    time.sleep(2)
        else:
            self.start = False
            self.gameOver = True
        
        

