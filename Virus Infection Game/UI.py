# Virus Infection Game User Interface (UI), using tkinter
from tkinter import *
from board import Board
from AI import AI

import string
import sys

class UI(object):
    def __init__(self):
        self.GameBoard = Board() # default board size is 8, number of players is 2

    def init(self, data):
        # board size settings
        data.size = self.GameBoard.size
        data.players = self.GameBoard.players
        data.playeridx = 0 
        data.board = self.GameBoard.board
        data.margin = 20 # margin around the board
        data.boardSize = data.width - 2*data.margin
        data.cellSize = data.boardSize / data.size

        # home page image
        scaleWidth, scaleHeight = 3, 3
        data.homePageImageWidth = data.width
        data.homePageImageHeight = data.height
        data.homePageImage = PhotoImage(file="Images/HomepageBackground.gif")
        data.homePageImage = data.homePageImage.zoom(scaleWidth, scaleHeight)

        # virus win background image
        data.VirusWinBackgroundImageWidth = data.width
        data.VirusWinBackgroundImageHeight = data.height
        data.VirusWinBackgroundImage = PhotoImage(file="Images/VirusWinBackground.gif") 
        data.VirusWinBackgroundImage = data.VirusWinBackgroundImage.zoom(scaleWidth, scaleHeight)

        # pills win background image
        data.PillsWinBackgroundImageWidth = data.width
        data.PillsWinBackgroundImageHeight = data.height
        data.PillsWinBackgroundImage = PhotoImage(file="Images/PillsWinBackground.gif")
        data.PillsWinBackgroundImage = data.PillsWinBackgroundImage.zoom(scaleWidth, scaleHeight)

        # pills and viruses image

        # pills image reference: https://favpng.com/png_view/medicine-pill-medicine-cartoon-png/r3xWQfBP
        data.pillsImage = PhotoImage(file="Images/Pill.gif") # TODO: try rescale the image size based on cell size (can be done later)
        
        # viruses image reference: https://www.biopharma-reporter.com/Article/2020/10/15/Virus-strain-change-should-not-affect-COVID-19-vaccines-study
        data.virus1Image = PhotoImage(file="Images/Virus1.gif")
        data.virus2Image = PhotoImage(file="Images/Virus2.gif")
        data.virus3Image = PhotoImage(file="Images/Virus3.gif")

        # start page
        data.startPage = True
        data.singlePlayerMode = False
        data.multiPlayerMode = False
        data.settingsMode = False

        # size, # of player(s), level selection page (only applicable for single player mode)
        data.customizeMode = False
        data.selectingBoardSize = False
        data.selectingNumPlayers = False

        data.levelSelectionMode = False 

        # game page modes
        data.inGame = False

        # game state settings (Game Over, Game Paused)
        data.gameOver = False
        data.gamePaused = False

        # In game selection
        data.selectedPos = -1, -1
        data.putPos = -1, -1
        data.winner = None
        data.origPos = None

        # time settings
        data.timerDelay = 1000
        data.timeCounter = 0

        # AI settings
        data.AIs = [None, None, None, None] # all AI player object
        data.AIPlayers = [False, False, False, False] # is AI player or not

    def resetGameBoard(self, data):
        self.GameBoard = Board(size=data.size, numPlayers=len(data.players))
        for ai in data.AIs: 
            if ai: ai.GameBoard = self.GameBoard
        data.board = self.GameBoard.board
        data.boardSize = data.width - 2*data.margin
        data.cellSize = data.boardSize / data.size
        data.playeridx = 0 # also reset player turns
        data.gameOver = False
        data.gamePaused = False
        data.selectedPos = -1, -1
        data.putPos = -1, -1
        data.winner = None
        data.origPos = None

## Controller functions below
    def mousePressed(self, event, data):
        # three buttons in the start page
        if data.startPage:
            # enter the single player mode
            if data.width//4 <= event.x <= data.width*(3/4) and data.height//2 <= event.y <= data.height*(3/5):
                data.singlePlayerMode = True
                data.customizeMode = True
                data.startPage = False

            # enter the multi player mode
            elif data.width//4 <= event.x <= data.width*(3/4) and data.height*(3/5+1/30) <= event.y <= data.height*(7/10+1/30):
                data.multiPlayerMode = True
                data.customizeMode = True
                data.startPage = False

            # exit button
            elif data.width*(5/6) <= event.x <= data.width*(29/30) and data.height*(9/10) <= event.y <= data.height*(29/30):
                sys.exit()

        # customize size page
        elif data.customizeMode: # can only customize one of them at a time
            # press the "size button" to customize the board size
            if data.width//2 <= event.x <= data.width*(3/4) and data.height*(2/5) <= event.y <= data.height*(1/2):
                data.selectingBoardSize = True
                data.selectingNumPlayers = False

            # press the "num of players button" to customize the number of players
            elif data.width//2 <= event.x <= data.width*(3/4) and data.height*(11/20) <= event.y <= data.height*(13/20):
                data.selectingBoardSize = False
                data.selectingNumPlayers = True  

            elif data.width*(3/8) <= event.x <= data.width*(5/8) and data.height*(7/10+1/15) <= event.y <= data.height*(4/5+1/15):
                self.resetGameBoard(data)
                if data.singlePlayerMode: data.levelSelectionMode = True
                else: data.inGame = True
                data.customizeMode = False

        # level selection mode (only applicable for single player (AI) mode)
        elif data.levelSelectionMode:
            if len(data.players) == 2:
                # easy level
                if data.width//4 <= event.x <= data.width*(3/4) and data.height//2 <= event.y <= data.height*(3/5):
                    easyAI = AI(self.GameBoard, 0, 1)
                    data.AIs[1] = easyAI
                    data.levelSelectionMode = False
                    data.inGame = True
            
                # normal level
                elif data.width//4 <= event.x <= data.width*(3/4) and data.height*(3/5+1/30) <= event.y <= data.height*(7/10+1/30):
                    mediumAI = AI(self.GameBoard, 1, 1)
                    data.AIs[1] = mediumAI
                    data.levelSelectionMode = False
                    data.inGame = True

                # hard level
                elif data.width//4 <= event.x <= data.width*(3/4) and data.height*(7/10+1/15) <= event.y <= data.height*(4/5+1/15):
                    hardAI = AI(self.GameBoard, 2, 1)
                    data.AIs[1] = hardAI
                    data.levelSelectionMode = False
                    data.inGame = True

                data.AIPlayers[1] = True

            elif len(data.players) == 3: pass

            elif len(data.players) == 4: pass

        elif data.inGame:
            print("data.players:", data.players)
            print("data.playeridx: ", data.playeridx)
            print("data.AIs", data.AIs)
            print("data.AIPlayers", data.AIPlayers)
            player = data.players[data.playeridx]
            numPiecesEachPlayer = self.GameBoard.getNumPiecesEachPlayer()
            if (numPiecesEachPlayer[player] == 0 or not self.GameBoard.getAllLegalMoves(player)) and not self.GameBoard.isGameOver(): # this player is eliminated, so skip its round
                print("skip player", player)
                data.playeridx += 1 # switch player
                data.playeridx %= len(data.players)
            else:
                print("player: ", player)
                if data.AIPlayers[player]: 
                    print("AI's turn")
                    ai = data.AIs[player]                       
                    ai.move()
                    if self.GameBoard.isGameOver(): 
                        data.gameOver = True
                        data.inGame = False
                        data.winner = self.GameBoard.winner
                    data.playeridx += 1 # switch player
                    data.playeridx %= len(data.players)

                else:
                    row, col = self.getCell(event.x, event.y, data)
                    if data.selectedPos == (-1, -1): 
                        data.selectedPos = int(row), int(col)
                        data.putPos = (-1, -1)
                    else: 
                        data.selectedPos = (-1, -1)
                        data.putPos = int(row), int(col)

                    print("data.selectedPos: ", data.selectedPos)
                    print("data.putPos: ", data.putPos)
                    if data.selectedPos == (-1, -1) and data.putPos == (-1, -1):
                        pass   
                    elif data.selectedPos != (-1, -1) and data.putPos == (-1, -1):
                        if (data.board[data.selectedPos[0]][data.selectedPos[1]] == player): # current player is only allowed to move his/her own pieces
                            data.origPos = data.selectedPos
                        else: data.selectedPos = (-1, -1) # not the player's turn, redo the selection
                    elif data.selectedPos == (-1, -1) and data.putPos != (-1, -1):
                        allLegalPos = self.GameBoard.getLegalPos(data.origPos)
                        print("data.allLegalPos:", allLegalPos)
                        if data.putPos in allLegalPos: # each move must be a legal move, otherwise the selection is also cancelled
                            print("step")
                            self.GameBoard.step(player, data.origPos, data.putPos) # move the piece
                            if self.GameBoard.isGameOver(): 
                                data.gameOver = True
                                data.inGame = False
                                data.winner = self.GameBoard.winner
                            data.playeridx += 1 # switch player
                            data.playeridx %= len(data.players)
                            # reset
                            data.origPos = None
                    else: # should not reach here
                        print("error")
                        assert(False)

            self.GameBoard.printBoard()
            data.board = self.GameBoard.board
            print("\n")

        if data.settingsMode:
            pass # TODO

        # clear mouse position after each manipulation
        event.x, event.y = None, None

    def keyPressed(self, event, data):
        # press "shift + b" to return back to home page from anywhere
        if event.keysym == "B": 
            data.startPage = True
            data.singlePlayerMode = False
            data.multiPlayerMode = False
            data.customizeMode = False
            data.selectingBoardSize = False
            data.selectingNumPlayers = False
            data.levelSelectionMode = False
            data.inGame = False

        # customize size mode
        if data.customizeMode:
            if data.selectingBoardSize and (event.keysym in string.digits):
                if int(event.keysym) in range(5, 10):
                    data.size = int(event.keysym)
                elif int(event.keysym) == 1: # enter 1 to represent size = 10
                    data.size = 10
                data.selectingBoardSize = False
            elif data.selectingNumPlayers and (event.keysym in string.digits):
                if int(event.keysym) in range(2, 5):
                    data.players = list(range(int(event.keysym)))
                data.selectingNumPlayers = False

        # in game mode
        if data.inGame:
            # pause the game (can be retrieved)
            if event.keysym == "p":
                data.gamePaused = not data.gamePaused 

        else:
            assert(not data.inGame)
            # restart the game only when the current game is over
            if event.keysym == "r":
                data.inGame = True
                data.gameOver = False
                self.resetGameBoard(data)

            # press "b" to return back to the home page after game is over
            if event.keysym == "b": self.init(data) 

## Graphic drawing functions below
    # home page
    def drawStartPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="VioletRed1")
        canvas.create_image(data.width//2, data.height//2, image=data.homePageImage)
        
        # draw buttons and icons
        canvas.create_text(data.width//2, data.height//8, text="VIRUS", fill="#64DD17", font="Chalkduster 75 bold" )
        canvas.create_text(data.width//2, data.height//4, text="INFECTION", fill="light coral", font="Chalkduster 75 bold")    
        canvas.create_text(data.width//2, 3*(data.height//8), text="GAME", fill="green yellow", font="Chalkduster 75 bold")                                        
        canvas.create_image(data.width*(7/8), data.height*(1/8), image=data.virus1Image)
        canvas.create_image(data.width*(1/8), data.height*(3/8), image=data.pillsImage)
        canvas.create_image(data.width*(1/8), data.height*(1/8), image=data.virus2Image)
        canvas.create_image(data.width*(7/8), data.height*(3/8), image=data.virus3Image)

        # single player mode button
        canvas.create_rectangle(data.width//4, data.height//2, data.width*(3/4), data.height*(3/5), fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(11/20), text="Single Player", font="Arial 40 bold")

        # multi-player mode button
        canvas.create_rectangle(data.width//4, data.height*(3/5+1/30), data.width*(3/4), data.height*(7/10+1/30), fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(13/20+1/30), text="MultiPlayer", font="Arial 40 bold")

        # settings button
        canvas.create_rectangle(data.width//4, data.height*(7/10+1/15), data.width*(3/4), data.height*(4/5+1/15), fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/4+1/15), text="Settings", font="Arial 40 bold")

        # quit button
        canvas.create_rectangle(data.width*(5/6), data.height*(9/10), data.width*(29/30), data.height*(29/30), fill="light grey")
        canvas.create_text(data.width*(9/10), data.height*(14/15), text="Quit", font="Arial 30 bold")

    # customize size/player page
    def drawCustomizePage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan")
        canvas.create_text(data.width//2, data.height//4, text="Select Your Size/# of Players Here!", font="Arial 45 bold", fill="purple")

        # size
        canvas.create_text(data.width//4, data.height*(9/20), text="Board Size:", font="Arial 45")
        if data.selectingBoardSize:
            canvas.create_rectangle(data.width//2, data.height*(2/5), data.width*(3/4), data.height*(1/2), fill="light goldenrod")
        else:
            canvas.create_rectangle(data.width//2, data.height*(2/5), data.width*(3/4), data.height*(1/2), fill="lemon chiffon")
        canvas.create_text(data.width*(5/8), data.height*(9/20), text=str(data.size), font="Arial 35")
        canvas.create_text(data.width*(7/8), data.height*(9/20), text="(5-10)", font="Arial 35")    

        # number of players
        canvas.create_text(data.width//4, data.height*(3/5), text="Num of Players:", font="Arial 45")
        if data.selectingNumPlayers:
            canvas.create_rectangle(data.width//2, data.height*(11/20), data.width*(3/4), data.height*(13/20), fill="light goldenrod")
        else:
            canvas.create_rectangle(data.width//2, data.height*(11/20), data.width*(3/4), data.height*(13/20), fill="lemon chiffon")
        canvas.create_text(data.width*(5/8), data.height*(3/5), text=str(len(data.players)), font="Arial 35")
        canvas.create_text(data.width*(7/8), data.height*(3/5), text="(2-4)", font="Arial 35")    

        # finish button
        canvas.create_rectangle(data.width*(3/8), data.height*(7/10+1/15), data.width*(5/8), data.height*(4/5+1/15), fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/4+1/15), text="Finish!", font="Arial 40")

    # AI mode level selection page
    def drawLevelSelectionPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
        canvas.create_text(data.width//2, data.height//4, text = "Select a Level!", font = "Arial 55 bold", fill="purple")

        # one virus
        if len(data.players) == 2:
            # virus 1
            canvas.create_image(data.width//2, data.height*(2/5), image=data.virus1Image)

            # easy mode
            canvas.create_rectangle(data.width//4, data.height//2, data.width*(3/4), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width//4, data.height*(3/5+1/30), data.width*(3/4), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width//4, data.height*(7/10+1/15), data.width*(3/4), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

        # two viruses
        elif len(data.players) == 3:
            # virus 1
            canvas.create_image(data.width*(3/10), data.height*(2/5), image=data.virus1Image)

            # easy mode
            canvas.create_rectangle(data.width*(3/20), data.height//2, data.width*(9/20), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width*(3/10), data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width*(3/20), data.height*(3/5+1/30), data.width*(9/20), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width*(3/10), data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width*(3/20), data.height*(7/10+1/15), data.width*(9/20), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width*(3/10), data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

            # virus 2
            canvas.create_image(data.width*(7/10), data.height*(2/5), image=data.virus2Image)

            # easy mode
            canvas.create_rectangle(data.width*(11/20), data.height//2, data.width*(17/20), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width*(7/10), data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width*(11/20), data.height*(3/5+1/30), data.width*(17/20), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width*(7/10), data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width*(11/20), data.height*(7/10+1/15), data.width*(17/20), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width*(7/10), data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

        # three viruses
        elif len(data.players) == 4:
            # virus 1
            canvas.create_image(data.width//4, data.height*(2/5), image=data.virus1Image)

            # easy mode
            canvas.create_rectangle(data.width*(1/4-1/10), data.height//2, data.width*(1/4+1/10), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width//4, data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width*(1/4-1/10), data.height*(3/5+1/30), data.width*(1/4+1/10), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width//4, data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width*(1/4-1/10), data.height*(7/10+1/15), data.width*(1/4+1/10), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width//4, data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

            # virus 2
            canvas.create_image(data.width//2, data.height*(2/5), image=data.virus2Image)

            # easy mode
            canvas.create_rectangle(data.width*(1/2-1/10), data.height//2, data.width*(1/2+1/10), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width*(1/2-1/10), data.height*(3/5+1/30), data.width*(1/2+1/10), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width*(1/2-1/10), data.height*(7/10+1/15), data.width*(1/2+1/10), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width//2, data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

            # virus 3
            canvas.create_image(data.width*(3/4), data.height*(2/5), image=data.virus3Image)

            # easy mode
            canvas.create_rectangle(data.width*(3/4-1/10), data.height//2, data.width*(3/4+1/10), data.height*(3/5), fill="lemon chiffon")
            canvas.create_text(data.width*(3/4), data.height*(11/20), text="Easy", font="Arial 35 bold")

            # normal mode
            canvas.create_rectangle(data.width*(3/4-1/10), data.height*(3/5+1/30), data.width*(3/4+1/10), data.height*(7/10+1/30), fill="lemon chiffon")
            canvas.create_text(data.width*(3/4), data.height*(13/20+1/30), text="Normal", font="Arial 35 bold")

            # hard mode
            canvas.create_rectangle(data.width*(3/4-1/10), data.height*(7/10+1/15), data.width*(3/4+1/10), data.height*(4/5+1/15), fill="lemon chiffon")
            canvas.create_text(data.width*(3/4), data.height*(3/4+1/15), text="Hard", font="Arial 35 bold")

    def drawSettingsPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan")
        canvas.create_text(data.width//2, data.height//4, text="Press the button below \n to start/stop the music", font="Arial 55 bold", fill="purple")

        # start button
        canvas.create_rectangle(data.width*(3/8), data.height*(2/5), data.width*(5/8), data.height//2, fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(9/20), text="Start", font="Arial 40 bold")

        # stop button
        canvas.create_rectangle(data.width*(3/8), data.height*(11/20), data.width*(5/8), data.height*(13/20), fill="lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/5), text="Stop", font="Arial 40 bold")
        canvas.create_text(data.width//2, data.height*(3/4), text="Press 'b' to return back to home page", font="Arial 40 bold")

    # In game page
    def drawGamePage(self, canvas, data):
        numPiecesEachPlayer = self.GameBoard.getNumPiecesEachPlayer()
        del numPiecesEachPlayer[-1]
        if all(numPiecesEachPlayer[p] == numPiecesEachPlayer[0] for p in numPiecesEachPlayer): # tie
            canvas.create_rectangle(0, 0, data.width, data.height, fill="#EFEBE9")
        elif max(numPiecesEachPlayer, key=numPiecesEachPlayer.get) == 0: # pills ahead
            canvas.create_rectangle(0, 0, data.width, data.height, fill="#B2FF59")
        else: # viruses ahead
            canvas.create_rectangle(0, 0, data.width, data.height, fill="#E64A19")
        self.drawBoard(canvas, data)

        # Game paused
        if data.gamePaused: 
            canvas.create_rectangle(0, data.height/3, data.width, data.height*(2/3), fill="gold")
            canvas.create_text(data.width/2, data.height/2, text="Game Paused!", font="TimesNewRoman 35 bold", fill="red")

    # helper functions for drawing the game board    
    def pointInBoard(self, x, y, data):
        # return True if (x, y) is inside the board defined by data.
        return data.margin <= x <= data.width-data.margin and data.margin <= y <= data.height-data.margin

    def getCell(self, x, y, data):
        # return (row, col) in which (x, y) occurred or (-1, -1) if the point is outside the board.
        if not self.pointInBoard(x, y, data): return -1, -1
        row = (y - data.margin) // data.cellSize
        col = (x - data.margin) // data.cellSize
        return row, col

    def getCellBounds(self, row, col, data):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in board
        x0 = data.margin + col * data.cellSize
        x1 = data.margin + (col+1) * data.cellSize
        y0 = data.margin + row * data.cellSize
        y1 = data.margin + (row+1) * data.cellSize
        return x0, y0, x1, y1

    def drawBoard(self, canvas, data):
        # selecting 
        if data.selectedPos != (-1, -1) and data.putPos == (-1, -1):
            isThisPlayerTurn = data.board[data.selectedPos[0]][data.selectedPos[1]] == data.players[data.playeridx]
            allLegalPos = self.GameBoard.getLegalPos(data.selectedPos)
            for row in range(data.size):
                for col in range(data.size):
                    # background 
                    x0, y0, x1, y1 = self.getCellBounds(row, col, data)
                    color = "#EF9A9A"
                    if isThisPlayerTurn:
                        if (row, col) == data.selectedPos: color = "#9575CD"
                        elif (row, col) in allLegalPos: color = "#FFEB3B"
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3, outline='#C62828') 

                    # pieces (pills or viruses)
                    imageX = col*data.cellSize + data.cellSize//2 + data.margin
                    imageY = row*data.cellSize + data.cellSize//2 + data.margin
                    if data.board[row][col] == 0: canvas.create_image(imageX, imageY, image=data.pillsImage)
                    elif data.board[row][col] == 1: canvas.create_image(imageX, imageY, image=data.virus1Image)
                    elif data.board[row][col] == 2: canvas.create_image(imageX, imageY, image=data.virus2Image)
                    elif data.board[row][col] == 3: canvas.create_image(imageX, imageY, image=data.virus3Image)

        # moving
        else:
            for row in range(data.size):
                for col in range(data.size):
                    # background 
                    x0, y0, x1, y1 = self.getCellBounds(row, col, data)
                    color = "#EF9A9A"
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3, outline='#C62828') 

                    # pieces (pills or viruses)
                    imageX = col*data.cellSize + data.cellSize//2 + data.margin
                    imageY = row*data.cellSize + data.cellSize//2 + data.margin
                    if data.board[row][col] == 0: canvas.create_image(imageX, imageY, image=data.pillsImage)
                    elif data.board[row][col] == 1: canvas.create_image(imageX, imageY, image=data.virus1Image)
                    elif data.board[row][col] == 2: canvas.create_image(imageX, imageY, image=data.virus2Image)
                    elif data.board[row][col] == 3: canvas.create_image(imageX, imageY, image=data.virus3Image)

    # game over page  
    def drawGameOverPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan")
        if data.winner == -1: # tie
            canvas.create_text(data.width//2, data.height*(5/8), text="Tie!", font="Arial 60 bold")
        elif data.winner == 0: # winner is pill
            canvas.create_image(data.width//2, data.height//2, image=data.PillsWinBackgroundImage)
            canvas.create_text(data.width//2, data.height*(5/8), text="Pills Win!", font="Arial 60 bold", fill="#388E3C")
        else: # winner is virus (can have different type)
            canvas.create_image(data.width//2, data.height//2, image=data.VirusWinBackgroundImage) 
            canvas.create_text(data.width//2, data.height*(5/8), text="Virus " + str(data.winner) + " Win!", font="Arial 60 bold", fill="#388E3C")
        canvas.create_text(data.width//2, data.height*(3/8), text="GAME OVER!", font="Chalkduster 75 bold", fill="#D50000")   
        canvas.create_text(data.width//2, data.height*(13/16), text="Press 'r' to start again", font="Arial 35", fill="#BA68C8") 
        canvas.create_text(data.width//2, data.height*(7/8), text="Press 'b' to back to home page", font="Arial 35", fill="#BA68C8") 

    def redrawAll(self, canvas, data):
        # start page
        if data.startPage: self.drawStartPage(canvas, data)

        # customize size page
        elif data.customizeMode: self.drawCustomizePage(canvas, data)

        # AI mode level selection page
        elif data.levelSelectionMode: 
            assert(data.singlePlayerMode and not data.multiPlayerMode and not data.customizeMode)
            self.drawLevelSelectionPage(canvas, data)

        # in game page
        elif data.inGame: self.drawGamePage(canvas, data)

        # game over page
        elif data.gameOver: self.drawGameOverPage(canvas, data)

    def timerFired(self, data):
        pass
    #     if data.inGame and not data.gameOver and not data.gamePaused:
    #         data.timeCounter += 1

    #         if data.singlePlayerMode:
    #             data.timerDelay = 200
    #             if not self.GameBoard.GameOver():
    #                 # move twice in each timer delay period
    #                 self.AImove(data)
    #             else:
    #                 data.inGame = False
    #                 if self.GameBoard.contains2048(): data.reach2048 = True
    #                 else: data.cannotMove = True

    def runGame(self, width, height): # tkinter starter code
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height, fill='white', width=0)
            self.redrawAll(canvas, data)
            canvas.update()    

        def mousePressedWrapper(event, canvas, data):
            self.mousePressed(event, data)
            redrawAllWrapper(canvas, data)

        def keyPressedWrapper(event, canvas, data):
            self.keyPressed(event, data)
            redrawAllWrapper(canvas, data)

        def timerFiredWrapper(canvas, data):
            self.timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 500 # milliseconds
        root = Tk()
        root.title("Virus Infection Game")
        root.resizable(width=False, height=False) # prevents resizing window
        self.init(data)
        # create the root and the canvas
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed


