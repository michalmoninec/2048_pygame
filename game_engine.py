import pygame, sys, time
# from colours import *
from pygame.locals import *
import random
import keyboard
# import copy

tileMatrix = matice([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
tileSize = 100
mapwidth = 4
mapheight = 4
BOARD_SIZE = 4


def restore():
    global canMoveUP,canMoveDOWN,canMoveRIGHT,canMoveLEFT
    canMoveUP = False
    canMoveDOWN = False
    canMoveRIGHT = False
    canMoveLEFT = False

def printMatrix():
    for column in range(0,mapwidth):
        for row in range(0,mapheight):
            pygame.draw.rect(DISPLAYSURF,colour_dict[tileMatrix.matrix[column][row]],(row*tileSize,column*tileSize,tileSize,tileSize))
            if tileMatrix.matrix[column][row] != 0:
                myfont = pygame.font.SysFont("monospace", 30, bold = 'true')
                label = myfont.render(str(tileMatrix.matrix[column][row]), 1, (255,255,255))
                DISPLAYSURF.blit(label, (row*(400/mapwidth) + 10, column*(400/mapheight) + 10))
    pygame.display.update()

def gameMovement(k):
    if event.type == KEYDOWN:
        return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)
    #get arrows and output is direction

def getRotations(k):
	if k == pygame.K_UP:
		return 0
	elif k == pygame.K_DOWN:
		return 2
	elif k == pygame.K_LEFT:
		return 1
	elif k == pygame.K_RIGHT:
		return 3

def transpose(A):
    N = 4
    for i in range(N):
        for j in range(i+1, N):
            A[i][j], A[j][i] = A[j][i], A[i][j]

def placeRandomTile(matice_):
    global getRandomTile
    # print('random se aspon zapne')
    i = random.randint(0,3)
    j = random.randint(0,3)
    if matice_[i][j] == 0:
        rand = random.randint(0,100)
        if rand>10:
            matice_[i][j] = 2
            # getRandomTile = False
        else:
            matice_[i][j] = 4
            # getRandomTile = False

def mergeTiles(direction,matice_,matice):
    k = direction
    if k == 0: #nahoru
        transpose(matice_)
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE -1):
                if matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j+1] = 0
                        matice.hodnota += matice_[i][j]
        transpose(matice_)
        updateMatrix(k,matice_)
    if k == 1: #doleva
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE -1):
                if matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j+1] = 0
                        matice.hodnota += matice_[i][j]
        updateMatrix(k,matice_)
    if k == 2: #dolu
        transpose(matice_)
        for i in range(0, BOARD_SIZE):
            for j in range(BOARD_SIZE - 1,-1,-1):
                if matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0:
                        matice_[i][j] = matice_[i][j] * 2
                        matice_[i][j-1] = 0
                        matice.hodnota += matice_[i][j]
        transpose(matice_)
        updateMatrix(k,matice_)
    if k == 3: #doprava
        for i in range(0, BOARD_SIZE):
            for j in range(BOARD_SIZE - 1,-1,-1):
                if matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0:
                            matice_[i][j] = matice_[i][j] * 2
                            matice_[i][j-1] = 0
                            matice.hodnota += matice_[i][j]
        updateMatrix(k,matice_)

def updateMatrix(k,matice_):

        if k ==0: #nahoru
            transpose(matice_)
            for i in range (0,4):
                for j in range (0,3):
                    while matice_[i][j]==0 and sum(matice_[i][j:])>0:
                        for k in range(j,3):
                            matice_[i][k] = matice_[i][k+1]
                        matice_[i][3]=0
            transpose(matice_)
        elif k==1: #doleva
            for i in range (0,4):
                for j in range (0,3):
                    while matice_[i][j]==0 and sum(matice_[i][j:])>0:
                        for k in range(j,3):
                            matice_[i][k] = matice_[i][k+1]
                        matice_[i][3]=0


        elif k==2: #dolu
            transpose(matice_)
            for i in range (0,4):
                for j in range (3,-1,-1):
                    while matice_[i][j]==0 and sum(matice_[i][:j])>0:
                        for k in range(j,-1,-1):
                            matice_[i][k] = matice_[i][k-1]
                        matice_[i][0]=0
            transpose(matice_)

        elif k==3: #vpravo
            for i in range (0,4):
                for j in range (3,0,-1):
                    while matice_[i][j]==0 and sum(matice_[i][:j])>0:
                        for k in range(j,-1,-1):
                            matice_[i][k] = matice_[i][k-1]
                        matice_[i][0]=0

def checkIfCanMove(direction,matice_):
    k = direction

    if k == 0: #nahoru
        transpose(matice_)
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE -1):
                if (matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][j:])>0):
                    transpose(matice_)
                    return True
                    canMoveUP = True
        transpose(matice_)


    elif k == 1: #doleva
        for i in range(0, BOARD_SIZE):
            for j in range(0, BOARD_SIZE -1):
                if (matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][j:])>0):
                    return True
                    canMoveLEFT = True


    elif k == 2: #dolu
        transpose(matice_)
        for i in range(0, BOARD_SIZE):
            for j in range(BOARD_SIZE - 1,0,-1):
                if (matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][:j])>0):
                    transpose(matice_)
                    return True
                    canMoveDOWN = True
        transpose(matice_)


    elif k == 3: #doprava
        for i in range(0, BOARD_SIZE):
            for j in range(BOARD_SIZE - 1,0,-1):
                if (matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][:j])>0):
                    return True
                    canMoveRIGHT = True

    else:
        return False

def checkGame(matice_):
    canMove0 = False
    canMove1 = False
    canMove2 = False
    canMove3 = False
    for k in range (4):
        if k == 0: #nahoru
            transpose(matice_)
            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE -1):
                    if (matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][j:])>0):
                        #return True
                        canMove0 = True
            transpose(matice_)


        elif k == 1: #doleva
            for i in range(0, BOARD_SIZE):
                for j in range(0, BOARD_SIZE -1):
                    if (matice_[i][j] == matice_[i][j+1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][j:])>0):
                        canMove1 = True


        elif k == 2: #dolu
            transpose(matice_)
            for i in range(0, BOARD_SIZE):
                for j in range(BOARD_SIZE - 1,0,-1):
                    if (matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][:j])>0):
                        canMove2 = True
            transpose(matice_)


        elif k == 3: #doprava
            for i in range(0, BOARD_SIZE):
                for j in range(BOARD_SIZE - 1,0,-1):
                    if (matice_[i][j] == matice_[i][j-1] and matice_[i][j]!=0) or (matice_[i][j]==0 and sum(matice_[i][:j])>0):
                        canMove3 = True
    if (canMove0 == False and canMove1 == False and canMove2 == False and canMove3 == False):
        return False
    else:
        return True

    global directionOut
    global getRandomTile
    global bestScore
    global bestScoreTemp


    #temp1 = bestScore


def placeDefault():
    getRandomTile = True
    placeRandomTile(tileMatrix.matrix)
    getRandomTile = True
    placeRandomTile(tileMatrix.matrix)
    printMatrix()
    scoreView(tileMatrix.hodnota,myfont,DISPLAYSURF)
# while True:
#     for event in pygame.event.get():
#         if event.type ==QUIT:
#             #pygame.exit()
#             sys.exit()
#         if event.type == KEYDOWN:
#             if gameMovement(event.key):
#                 global direction
#                 print('zmacknuto')
#                 direction = getRotations(event.key)
#                 print('smer: ',direction)
#                 if checkGame(tileMatrix.matrix):
#                     print('hra ma pokracovani')
#                     if checkIfCanMove(direction,tileMatrix.matrix):
#                         print('muzu se pohnout timto smerem')
#                         updateMatrix(direction,tileMatrix.matrix)
#                         mergeTiles(direction,tileMatrix.matrix,tileMatrix)
#                         getRandomTile = True
#                         placeRandomTile(tileMatrix.matrix)
                        
#                         scoreView(tileMatrix.hodnota,myfont,DISPLAYSURF)
#                         printMatrix()
                        
#                         print('score: ',tileMatrix)
#                         print('---------')
#                     else:
#                                 #DISPLAYSURF.fill(BLACK)
#                         score2 = f"invalid move"
#                         label2 = myfont.render(score2, 1, (0,0,0))
#                         pygame.draw.rect(DISPLAYSURF,(255,255,255),(0,400,400,200))
#                         scoreView(tileMatrix.hodnota,myfont,DISPLAYSURF)
#                         DISPLAYSURF.blit(label2,(0,500))
#                         pygame.display.update()
#                 else:
#                     score2 = f"game over"

#                     label2 = myfont.render(score2, 1, (0,0,0))
#                     pygame.draw.rect(DISPLAYSURF,(255,255,255),(0,400,400,200))
#                     scoreView(tileMatrix,myfont,DISPLAYSURF)
#                     DISPLAYSURF.blit(label2,(0,500))
#                     pygame.display.update()
