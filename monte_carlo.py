import copy
import random


class MonteCarlo():
    def __init__(self):
        self.start = False
        self.pocetIteraci = 20
        self.matrixList = []
        self.scoreUp = [0]
        self.scoreDown = [0]
        self.scoreLeft = [0]
        self.scoreRight = [0]
        self.scoreListAll = []
        self.screen = False
        

    def getDirection(self,matrix,game):
        for i  in range (self.pocetIteraci+1):
            k = random.randint(0,3) #smer, kterym se ma hra posunout
            interMatrix = copy.deepcopy(matrix)
            while (game.checkIfCanMove(k,interMatrix)) == False: #pokud vyberu smer, kterym nemuzu, vyberu jiny smer
                k = random.randint(0,3)

            while game.checkGame(interMatrix): #hraju dokud muzu random postupem
                a = random.randint(0,3)
                while not game.checkIfCanMove(a,interMatrix): 
                    a = random.randint(0,3)

                game.updateMatrix(a,interMatrix)
                game.mergeTiles(a,interMatrix)
                game.startRandom = True
                game.placeRandomTile(interMatrix)

            if k == 0:
                self.scoreUp.append(game.score)
            if k == 1:
                self.scoreLeft.append(game.score)
            if k == 2:
                self.scoreDown.append(game.score)
            if k == 3:
                self.scoreRight.append(game.score)

        self.scoreListAll.append(sum(self.scoreUp)/(len(self.scoreUp)))
        self.scoreListAll.append(sum(self.scoreLeft)/(len(self.scoreLeft)))
        self.scoreListAll.append(sum(self.scoreDown)/(len(self.scoreDown)))
        self.scoreListAll.append(sum(self.scoreRight)/(len(self.scoreRight)))

        direction = self.scoreListAll.index(max(self.scoreListAll))
        
        del self.scoreListAll[:]
        self.scoreUp = [0]
        self.scoreDown = [0]
        self.scoreLeft = [0]
        self.scoreRight = [0]
        return direction

