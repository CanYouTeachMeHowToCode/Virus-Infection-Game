## Virus Infection Game AI

import random
import copy
from board import Board

class AI(object):
    def __init__(self, GameBoard, level, player):
        self.GameBoard = GameBoard
        self.level = ["easy", "normal", "hard"][level]  
        self.player = player

    def move(self):
        pos, newPos = None, None
        if self.level == "easy": pos, newPos = self.easyAIMove()
        elif self.level == "normal": pos, newPos = self.mediumAIMove()
        elif self.level == "hard" : pos, newPos = self.hardAIMove()
        else: pass
        print("{}'s move: ".format(self.__class__.__name__), end='')
        print(str(pos) + " to " + str(newPos))
        self.GameBoard.step(self.player, pos, newPos)

    def getAllLegalMoves(self): # None -> list[tuple(tuple(int, int))]
        legalMoves = []
        for row in range(self.GameBoard.size):
            for col in range(self.GameBoard.size):
                pos = (row, col)
                if self.GameBoard.board[row][col] == self.player:
                    allLegalPos = self.GameBoard.getLegalPos(pos)
                    for newPos in allLegalPos: legalMoves.append((pos, newPos))
        return legalMoves

    # easy level AI: move randomly
    def easyAIMove(self):
        legalMoves = self.getAllLegalMoves()
        pos, newPos = random.choice(legalMoves)
        return pos, newPos

    # medium level AI: move based on Minimax algorithm
    def mediumAIMove(self):
        pass

    # hard level AI: move based on Minimax algorithm with alpha-beta pruning
    def hardAIMove(self):
        pass

# test
if __name__ == "__main__":
    testBoard = Board(size=5, numPlayers=2) # size = 5, two players
    easyVirus1AI = AI(testBoard, 0, 1) # easy level AI, AI players virus 1
    players = testBoard.players
    playerIdx = 0
    while not testBoard.isGameOver():
        currPlayer = players[playerIdx]
        testBoard.printBoard()

        if currPlayer == 0:
            pos = input("Player's turn. \nPlease select a piece.(such as '23'): ") # '23' represents position (2, 3)
            pos = (int(pos[0]), int(pos[1]))
            if pos[0] < 0 or pos[0] >= testBoard.size or pos[1] < 0 or pos[1] >= testBoard.size: # out of bounds
                pos = input("Invalid piece position. Please select another piece.(such as '23'): ")
                pos = (int(pos[0]), int(pos[1]))
            elif testBoard.board[pos[0]][pos[1]] != currPlayer or not testBoard.getLegalPos(pos): # not selecting current player's piece
                pos = input("You cannot move this piece. Please select another piece.(such as '23'): ")
                pos = (int(pos[0]), int(pos[1]))

            newPos = input("Please select the point to put your piece.(such as '23'): ")
            newPos = (int(newPos[0]), int(newPos[1]))
            if newPos[0] < 0 or newPos[0] >= testBoard.size or newPos[1] < 0 or newPos[1] >= testBoard.size: # out of bounds
                newPos = input("Invalid piece position. Please select another piece.(such as '23'): ")
                newPos = (int(newPos[0]), int(newPos[1]))
            elif not testBoard.isLegalMove(pos, newPos) and not testBoard.isLegalJump(pos, newPos): # invalid move
                newPos = input("You cannot put your piece here. Please select another piece.(such as '23'): ")
                newPos = (int(newPos[0]), int(newPos[1]))

            testBoard.step(currPlayer, pos, newPos)

        else: 
            easyVirus1AI.move()

        playerIdx += 1
        playerIdx %= len(players)



        


