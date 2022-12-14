## Virus Infection Game AI

import random
import copy
import numpy as np
from board import Board

class AI(object):
    def __init__(self, GameBoard, level, player):
        self.GameBoard = GameBoard
        self.level = ["easy", "medium", "hard"][level]  
        self.player = player

    def move(self):
        action = None
        if self.level == "easy": action = self.easyAIMove()
        elif self.level == "medium": action = self.mediumAIMove()
        elif self.level == "hard" : action = self.hardAIMove()
        else: pass
        print("{}'s move: ".format(self.__class__.__name__), end='')
        if action:
            pos, newPos = action
            print(str(pos) + " to " + str(newPos))
            self.GameBoard.step(self.player, pos, newPos)
        else: 
            print("No legal moves now. Skip to next player")

    # evaluation function, may have better version
    def evaluate(self, player): 
        return np.sum(np.array(self.GameBoard.board) == player) - np.sum(np.array(self.GameBoard.board) != player) - np.sum(np.array(self.GameBoard.board) != self.GameBoard.empty)

    # easy level AI: move randomly
    def easyAIMove(self):
        legalMoves = self.GameBoard.getAllLegalMoves(self.player)
        return random.choice(legalMoves) if legalMoves else None

    # medium level AI: move based on greedy algorithm
    def mediumAIMove(self):
        legalMoves = self.GameBoard.getAllLegalMoves(self.player)
        if not legalMoves: return None

        bestScore, bestActions = -float('inf'), []
        for action in legalMoves:
            beforeMoveBoard = copy.deepcopy(self.GameBoard.board)
            pos, newPos = action
            self.GameBoard.step(self.player, pos, newPos, verbose=False)
            score = self.evaluate(self.player)
            self.GameBoard.board = beforeMoveBoard # undo the move

            if score > bestScore:
                bestActions = [action]
                bestScore = score
            elif score == bestScore:
                bestActions.append(action)

        return random.choice(bestActions) if bestActions else random.choice(legalMoves)

     # hard level AI: move based on Minimax algorithm with alpha-beta pruning
    def hardAIMove(self):
        return self.maxieMoveAlphaBeta(depth=4)[1]

    def maxieMoveAlphaBeta(self, depth, alpha=-float('inf'), beta=float('inf')):
        assert(alpha < beta)
        if self.GameBoard.isGameOver(): return (float('inf'), None) if self.GameBoard.winner == self.player or self.GameBoard.winner == -1 else (float('-inf'), None)
        elif not depth: return self.evaluate(self.player), None # depth = 0
        else:
            # get all legal actions for current player and preserve the board
            legalMoves = self.GameBoard.getAllLegalMoves(self.player)
            if not legalMoves: return self.evaluate(self.player), None # no legal actions

            bestScore, bestAction = -float('inf'), None
            for action in legalMoves:
                beforeMoveBoard = copy.deepcopy(self.GameBoard.board)
                pos, newPos = action
                self.GameBoard.step(self.player, pos, newPos, verbose=False)
                minnieScore, _ = self.minnieMoveAlphaBeta(depth-1, alpha, beta)
                self.GameBoard.board = beforeMoveBoard # undo the move

                if minnieScore > bestScore:
                    bestScore = minnieScore
                    bestAction = action
                    alpha = max(alpha, bestScore)
                    if alpha >= beta: return bestScore, bestAction
                # elif minnieScore == bestScore:
                #     bestActions.append(action)
            return bestScore, bestAction
            # return (bestScore, random.choice(bestActions)) if bestActions else (bestScore, random.choice(legalMoves))

    '''
    If there are more than two players (the current player has more than one enemies), we 
    assume all these enemies "integrates" to one enemy that try to prevent current player from
    winning. Therefore, this return back to the miniMax for two players.
    '''

    def minnieMoveAlphaBeta(self, depth, alpha, beta):
        assert(alpha < beta)
        if self.GameBoard.isGameOver(): return (float('-inf'), None) if self.GameBoard.winner != self.player and self.GameBoard.winner != -1 else (float('inf'), None)
        elif not depth: return np.mean([self.evaluate(player) for player in self.GameBoard.players if player != self.player]), None # depth = 0
        else:
            # get all legal actions for all other players and preserve the board
            allLegalMoves = []
            for player in self.GameBoard.players:
                if player == self.player: continue
                legalMoves = self.GameBoard.getAllLegalMoves(player)
                allLegalMoves += legalMoves
            if not allLegalMoves: return np.mean([self.evaluate(player) for player in self.GameBoard.players if player != self.player]), None # no legal actions

            bestScore, bestAction = float('inf'), None
            # get all legal actions for all other players and preserve the board
            for action in allLegalMoves:
                beforeMoveBoard = copy.deepcopy(self.GameBoard.board)
                pos, newPos = action
                player = self.GameBoard.board[pos[0]][pos[1]]
                assert(player != self.player)
                self.GameBoard.step(player, pos, newPos, verbose=False)
                maxieScore, _ = self.maxieMoveAlphaBeta(depth-1, alpha, beta)
                self.GameBoard.board = beforeMoveBoard # undo the move

                if maxieScore < bestScore:
                    bestScore = maxieScore
                    bestAction = action
                    beta = min(beta, bestScore)
                    if alpha >= beta: return bestScore, bestAction

            return bestScore, bestAction

# test
if __name__ == "__main__":

    # easyPillsAI = AI(testBoard, 0, 0) # easy level AI, AI plays pills
    # mediumPillsAI = AI(testBoard, 1, 0) # medium level AI, AI plays pills
    # hardPillsAI = AI(testBoard, 2, 0) # hard level AI, AI plays pills

    # easyVirus1AI = AI(testBoard, 0, 1) # easy level AI, AI plays virus 0
    # mediumVirus1AI = AI(testBoard, 1, 1) # medium level AI, AI plays virus 1
    # hardVirus1AI = AI(testBoard, 2, 1) # hard level AI, AI plays virus 1

    ########################################################################
    # 2 players
    
    # medium AI vs medium AI
    winners = []
    for _ in range(20):
        testBoard = Board(size=7, numPlayers=2)
        players = testBoard.players
        playerIdx = 0
        mediumPillsAI = AI(testBoard, 1, 0) # medium level AI, AI plays pills
        mediumVirus1AI = AI(testBoard, 1, 1) # medium level AI, AI plays virus 1
        while not testBoard.isGameOver():
            currPlayer = players[playerIdx]
            testBoard.printBoard()
            print("currPlayer: " + str(currPlayer))
            for ai in [mediumPillsAI, mediumVirus1AI]:
                if ai.player == currPlayer: ai.move()
            playerIdx += 1
            playerIdx %= len(players)
        testBoard.printBoard()
        winners.append(testBoard.winner)
    print("winners of medium vs medium 20 times: ", winners)
    print("medium AI (pills) win rate:", winners.count(0)/20)
    print("medium AI (virus 1) win rate:", winners.count(1)/20)
    print("Tie rate:", winners.count(-1)/20)


    # medium AI vs hard AI
    winners = []
    for _ in range(10):
        testBoard = Board(size=7, numPlayers=2)
        players = testBoard.players
        playerIdx = 0
        mediumPillsAI = AI(testBoard, 1, 0) # medium level AI, AI plays pills
        hardVirus1AI = AI(testBoard, 2, 1) # hard level AI, AI plays virus 1
        while not testBoard.isGameOver():
            currPlayer = players[playerIdx]
            testBoard.printBoard()
            print("currPlayer: " + str(currPlayer))
            for ai in [mediumPillsAI, hardVirus1AI]:
                if ai.player == currPlayer: ai.move()
            playerIdx += 1
            playerIdx %= len(players)
        testBoard.printBoard()
        winners.append(testBoard.winner)
    print("winners of medium vs hard 10 times: ", winners)
    print("medium AI (pills) win rate:", winners.count(0)/10)
    print("hard AI (virus 1) win rate:", winners.count(1)/10)
    print("Tie rate:", winners.count(-1)/10)


    # hard AI vs medium AI
    winners = []
    for _ in range(10):
        testBoard = Board(size=7, numPlayers=2)
        players = testBoard.players
        playerIdx = 0
        hardPillsAI = AI(testBoard, 2, 0) # hard level AI, AI plays pills
        mediumVirus1AI = AI(testBoard, 1, 1) # medium level AI, AI plays virus 1
        while not testBoard.isGameOver():
            currPlayer = players[playerIdx]
            testBoard.printBoard()
            print("currPlayer: " + str(currPlayer))
            for ai in [hardPillsAI, mediumVirus1AI]:
                if ai.player == currPlayer: ai.move()
            playerIdx += 1
            playerIdx %= len(players)
        testBoard.printBoard()
        winners.append(testBoard.winner)
    print("winners of hard vs medium 10 times: ", winners)
    print("hard AI (pills) win rate:", winners.count(0)/10)
    print("medium AI (virus 1) win rate:", winners.count(1)/10)
    print("Tie rate:", winners.count(-1)/10)


    #######################################################################
    # # more than 2 players
    # testBoard2 = Board(size=8, numPlayers=4)

    # AIs = []
    # hardPillsAI = AI(testBoard2, 1, 0) # medium level AI, AI plays pills
    # AIs.append(hardPillsAI)
    # easyVirus1AI = AI(testBoard2, 0, 1) # easy level AI, AI plays virus 1
    # AIs.append(easyVirus1AI)
    # mediumVirus2AI = AI(testBoard2, 1, 2) # medium level AI, AI plays virus 2
    # AIs.append(mediumVirus2AI)
    # hardVirus3AI = AI(testBoard2, 2, 3) # hard level AI, AI plays virus 3
    # AIs.append(hardVirus3AI)
    # # mediumVirus3AI = AI(testBoard2, 1, 3) # medium level AI, AI plays virus 3
    # # AIs.append(mediumVirus3AI)

    # players = testBoard2.players
    # playerIdx = 0
    # while not testBoard2.isGameOver():
    #     currPlayer = players[playerIdx]
    #     numPiecesEachPlayer = testBoard2.getNumPiecesEachPlayer()
    #     testBoard2.printBoard()
    #     print("currPlayer: " + str(currPlayer))
    #     for AI in AIs:
    #         if AI.player == currPlayer: 
    #             if numPiecesEachPlayer[currPlayer] == 0: # this player is eliminated, so skip its round
    #                 print("no pieces left, skip player", currPlayer)
    #             elif not testBoard2.getAllLegalMoves(currPlayer): # this player has no legal moves, so skip its round
    #                 print("no legal moves, skip player", currPlayer)
    #             else: AI.move()
    #     playerIdx += 1
    #     playerIdx %= len(players)

    # testBoard2.printBoard()

    ########################################################################

    # # Human vs AI
    # players = testBoard.players
    # playerIdx = 0
    # while not testBoard.isGameOver():
    #     currPlayer = players[playerIdx]
    #     testBoard.printBoard()

    #     if currPlayer == 0:
    #         pos = input("Player's turn. \nPlease select a piece.(such as '23'): ") # '23' represents position (2, 3)
    #         pos = (int(pos[0]), int(pos[1]))
    #         if pos[0] < 0 or pos[0] >= testBoard.size or pos[1] < 0 or pos[1] >= testBoard.size: # out of bounds
    #             pos = input("Invalid piece position. Please select another piece.(such as '23'): ")
    #             pos = (int(pos[0]), int(pos[1]))
    #         elif testBoard.board[pos[0]][pos[1]] != currPlayer or not testBoard.getLegalPos(pos): # not selecting current player's piece
    #             pos = input("You cannot move this piece. Please select another piece.(such as '23'): ")
    #             pos = (int(pos[0]), int(pos[1]))

    #         newPos = input("Please select the point to put your piece.(such as '23'): ")
    #         newPos = (int(newPos[0]), int(newPos[1]))
    #         if newPos[0] < 0 or newPos[0] >= testBoard.size or newPos[1] < 0 or newPos[1] >= testBoard.size: # out of bounds
    #             newPos = input("Invalid piece position. Please select another piece.(such as '23'): ")
    #             newPos = (int(newPos[0]), int(newPos[1]))
    #         elif not testBoard.isLegalMove(pos, newPos) and not testBoard.isLegalJump(pos, newPos): # invalid move
    #             newPos = input("You cannot put your piece here. Please select another piece.(such as '23'): ")
    #             newPos = (int(newPos[0]), int(newPos[1]))

    #         testBoard.step(currPlayer, pos, newPos)

    #     else: 
    #         # easyVirus1AI.move()
    #         mediumVirus1AI.move()

    #     playerIdx += 1
    #     playerIdx %= len(players)

        


