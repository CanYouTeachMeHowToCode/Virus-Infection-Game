# Virus Infection Game Board

import string
import copy
import random
import sys

class Board(object):
    def __init__(self, size=8, numPlayers=2):
        # size default set to 8, but can be customized (from 5 to 10)
        # number of players default set to 2 (one pill and one virus), but can be customized (from 2 to 4)

        # -1 represents empty grid, 0 represents pill (player), 1 to (numPlayers-1) represents enemies (virus or other pills)
        self.empty = -1 
        self.board = [[self.empty for _ in range(size)] for _ in range(size)]
        self.size = size

        # at most 1 pills, 3 enemies 
        self.players = list(range(numPlayers))
        startPos = [[self.size-1, 0], [0, 0], [0, self.size-1], [self.size-1, self.size-1]]
        for i in range(numPlayers): # initialize
            self.board[startPos[i][0]][startPos[i][1]] = self.players[i]

        self.winner = None

    def printBoard(self):
        print("current board:")
        for i in range(self.size): print(self.board[i], "\n")
        print("----------------------------------------------------------------")

    def isLegalMove(self, pos, newPos):
        if self.board[newPos[0]][newPos[1]] != -1: return False
        else:
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if 0 <= pos[0]+drow < self.size and pos[0]+drow == newPos[0] \
                        and 0 <= pos[1]+dcol < self.size and pos[1]+dcol == newPos[1]: return True
            return False

    def isLegalJump(self, pos, newPos):
        if self.board[newPos[0]][newPos[1]] != -1: return False
        else:
            for drow in [-2, 0, 2]:
                for dcol in [-2, 0, 2]:
                    if 0 <= pos[0]+drow < self.size and pos[0]+drow == newPos[0] \
                        and 0 <= pos[1]+dcol < self.size and pos[1]+dcol == newPos[1]: return True
            return False

    def getLegalPos(self, pos): # may be useful later in UI to (click->show legal position)
        legalPos = []
        for i in range(max(pos[0]-2, 0), min(pos[0]+3, self.size-1)):
            for j in range(max(pos[0]-2, 0), min(pos[0]+3, self.size-1)):
                newPos = (i, j)
                if self.isLegalMove(pos, newPos) or self.isLegalJump(pos, newPos): legalPos.append(newPos)
        return legalPos

    def invade(self, player, currPos):
        '''
        Once a moving step is completed, the virus/pill on that unit can invade the area 1 unit surrounding it. 
        That is, to "eaten up" all units that are not empty and not the same species.
        (i.e. pills eaten up viruses or viruses eaten up pills.)

        Note: different species of viruses can also invade each other.
        '''
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if drow == dcol == 0: continue
                else:
                    invadePos = (currPos[0]+drow, currPos[1]+dcol)
                    if 0 <= invadePos[0] < self.size and 0 <= invadePos[1] < self.size \
                        and self.board[invadePos[0]][invadePos[1]] != self.empty \
                        and self.board[invadePos[0]][invadePos[1]] != player:
                        self.board[invadePos[0]][invadePos[1]] = player


    def step(self, player, pos, newPos):
        assert(self.board[pos[0]][pos[1]] == player) # current player is only allowed to move his/her own pieces
        if self.isLegalMove(pos, newPos):
            self.board[newPos[0]][newPos[1]] = player
            self.invade(player, newPos)
            if self.isGameOver():
                print("Game Over")
                if self.winner == -1: print("Tie!")
                else: print("winner is %d" % self.winner)

        elif self.isLegalJump(pos, newPos):
            self.board[pos[0]][pos[1]] = self.empty
            self.board[newPos[0]][newPos[1]] = player
            self.invade(player, newPos)
            if self.isGameOver():
                print("Game Over")
                if self.winner == -1: print("Tie!")
                else: print("winner is %d" % self.winner)

    def isGameOver(self):
        '''
        If the board has no empty tiles left, or only one type of pieces left on board, or every pieces does not have legal moves, 
        then the game is over.
        Note: One piece that does not have legal moves left does not mean game over--the other piece(s) may move until the board is full
        '''
        numEmptyTiles = 0
        numPiecesEachPlayer = [0]*len(self.players) # length equals to number of players
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.empty: numEmptyTiles += 1
                else: numPiecesEachPlayer[self.board[i][j]] += 1

        winnerPieces, winner = -1, -1
        if numEmptyTiles == 0: # no empty tiles
            if all(num == numPiecesEachPlayer[0] for num in numPiecesEachPlayer): self.winner = winner # tie
            else:
                for p in self.players:
                    if (numPiecesEachPlayer[p] > winnerPieces):
                        winnerPieces = numPiecesEachPlayer[p]
                        winner = p
                self.winner = winner
            return True
        else: 
            # only one piece left
            for p in self.players:
                if numPiecesEachPlayer[p] == sum(numPiecesEachPlayer): 
                    self.winner = p
                    return True

            # does not have legal moves
            allPosEachPiece = []
            for _ in self.players: allPosEachPiece.append([])
            for i in range(self.size):
                for j in range(self.size):
                    allPosEachPiece[self.board[i][j]].append((i, j))
            for allPos in allPosEachPiece: # if any piece have legal moves, then game is still not over
                for pos in allPos:
                    if self.getLegalPos(pos) != []: return False

            if all(num == numPiecesEachPlayer[0] for num in numPiecesEachPlayer): self.winner = winner # tie
            else:
                for p in self.players:
                    if (numPiecesEachPlayer[p] > winnerPieces):
                        winnerPieces = numPiecesEachPlayer[p]
                        winner = p
                self.winner = winner
            return True 

# test
if __name__ == "__main__":
    board = Board(size=5, numPlayers=2) # 5×5 board, one pill, one virus
    board.printBoard() 
    board.step(0, (4, 0), (4, 1))
    board.printBoard() 
    # board.step(1, (4, 1), (4, 2)) # should raise assertion error here
    board.step(1, (0, 0), (1, 1))
    board.printBoard() 
    board.step(0, (4, 0), (3, 1))
    board.printBoard() 
    board.step(1, (1, 1), (1, 2))
    board.printBoard() 
    board.step(0, (4, 0), (2, 0))
    board.printBoard() 
    board.step(1, (1, 2), (2, 1))
    board.printBoard() 
    board.step(0, (4, 1), (4, 0))
    board.printBoard() 
    board.step(1, (2, 1), (3, 0)) # kills all pills pieces and virus 1 win
    board.printBoard() 

