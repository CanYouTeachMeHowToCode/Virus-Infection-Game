# Virus Infection Game User Interface (UI), using tkinter

from tkinter import *
from board import Board
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
        data.margin = 10 # margin around the board
        data.cellSize = (data.width - data.margin * 2) / data.size
        data.boardWidth  = data.width - 2*data.margin
        data.boardHeight = data.height - 2*data.margin
        data.cellWidth  = data.boardWidth / data.size
        data.cellHeight = data.boardHeight / data.size

        # home page image
        scaleWidth, scaleHeight = 3, 3
        data.homePageImageWidth = data.width
        data.homePageImageHeight = data.height
        data.homePageImage = PhotoImage(file="HomepageBackground.gif")
        data.homePageImage = data.homePageImage.zoom(scaleWidth, scaleHeight)

        # virus win background image
        data.Virus1WinBackgroundImageWidth = data.width
        data.Virus1WinBackgroundImageHeight = data.height
        data.Virus1WinBackgroundImage = PhotoImage(file="Virus1WinBackground.gif")
        data.Virus1WinBackgroundImage = data.Virus1WinBackgroundImage.zoom(scaleWidth, scaleHeight)

        # pills win background image
        data.PillsWinBackgroundImageWidth = data.width
        data.PillsWinBackgroundImageHeight = data.height
        data.PillsWinBackgroundImage = PhotoImage(file="PillsWinBackground.gif")
        data.PillsWinBackgroundImage = data.PillsWinBackgroundImage.zoom(scaleWidth, scaleHeight)

        # pills and viruses image
        data.pillsImage = PhotoImage(file="pills.gif", width=100, height=100)
        data.virus1Image = PhotoImage(file="Virus1.gif", width=100, height=100)
        
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

        # In game selection (TODO: implement moving sequence of players--pills first, virus then, aka 每个棋子一次只能走一步)
        data.selectedPos = -1, -1
        data.putPos = -1, -1
        data.winningPlayer = None

        # time settings
        data.timerDelay = 1000
        data.timeCounter = 0

    def resetGameBoard(self, data):
        self.GameBoard = Board(data.size)
        data.board = self.GameBoard.board
        data.cellSize = (data.width - 2*data.margin) / data.size

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

            # clear mouse position after each manipulation
            event.x, event.y = None, None

        # customize size page
        elif data.customizeMode:
            # press the empty "size button" to enter the board size
            if data.width//2 <= event.x <= data.width*(3/4) and data.height//2 <= event.y <= data.height*(3/5):
                data.selectingBoardSize = True

            ## TODO
            # elif event.x in range(data.width//2, int(data.width*(3/4))) and \
            #    event.y in range(data.height//2, int(data.height*(3/5))):
            #     data.selectingNumPlayers = True

            elif data.width*(3/8) <= event.x <= data.width*(5/8) and data.height*(7/10+1/15) <= event.y <= data.height*(4/5+1/15):
                self.resetGameBoard(data)
                if data.singlePlayerMode: data.levelSelectionMode = True
                else: data.inGame = True
                data.customizeMode = False

            # clear mouse position after each manipulation
            event.x, event.y = None, None

        ## uncomment this part until AI part finished
        # # level selection mode (only applicable for AI mode)
        # if data.levelSelectionMode:
        #     # easy level
        #     if event.x in range(data.width//4, int(data.width*(3/4))) and \
        #         event.y in range(data.height//2, int(data.height*(3/5))):
        #         data.AI = AI(self.GameBoard, 0)
        #         data.levelSelectionMode = False
        #         data.inGame = True
            
        #     # normal level
        #     elif event.x in range(data.width//4, int(data.width*(3/4))) and \
        #         event.y in range(int(data.height*(3/5+1/30)), \
        #                         int(data.height*(7/10+1/30))):
        #         data.AI = AI(self.GameBoard, 1)
        #         data.levelSelectionMode = False
        #         data.inGame = True

        #     # hard level
        #     elif event.x in range(data.width//4, int(data.width*(3/4))) and \
        #         event.y in range(int(data.height*(7/10+1/15)), \
        #                         int(data.height*(4/5+1/15))):
        #         data.AI = AI(self.GameBoard, 2)
        #         data.levelSelectionMode = False
        #         data.inGame = True

        #     # clear mouse position after each manipulation
        #     event.x, event.y = None, None

        elif data.inGame:
            player = data.players[data.playeridx]
            allLegalPos = []
            origPos = None
            row, col = self.getCell(event.x, event.y, data)
            if data.selectedPos == (-1, -1): 
                data.selectedPos = int(row), int(col)
                data.putPos = (-1, -1)
            else: 
                data.selectedPos = (-1, -1)
                data.putPos = int(row), int(col)

            print("data.selectedPos: ", data.selectedPos)
            print("data.putPos: ", data.putPos)
            print("player: ", player)

            if data.selectedPos == (-1, -1) and data.putPos == (-1, -1):
                pass   
            elif data.selectedPos != (-1, -1) and data.putPos == (-1, -1):
                allLegalPos = self.GameBoard.getLegalPos(data.selectedPos)
                print("allLegalPos:", allLegalPos)
                origPos = data.selectedPos
            elif data.selectedPos == (-1, -1) and data.putPos != (-1, -1):
                if data.putPos == origPos: pass # unselect/reselect piece
                elif data.putPos in allLegalPos: 
                    self.GameBoard.step(player, origPos, data.putPos) # move the piece
                    data.playeridx += 1 # switch player
                    data.playeridx %= len(data.players)
                # reset
                allLegalPos = []
                origPos = None
            else: # should not reach here
                print("error")
                assert(False)

            self.GameBoard.printBoard()
            print("\n")
        if data.settingsMode:
            pass # TODO

    def keyPressed(self, event, data):
        # press "shift + b" to return back to home page from anywhere
        if event.keysym == "B": 
            data.startPage = True
            data.singlePlayerMode = False
            data.multiPlayerMode = False
            data.customizeMode = False
            data.selectingBoardSize = False
            data.levelSelectionMode = False
            data.inGame = False

        # customize size mode
        if data.customizeMode:
            if data.selectingBoardSize and (event.keysym in string.digits):
                if int(event.keysym) in range(4, 10):
                    data.size = int(event.keysym)
                elif int(event.keysym) == 1: # enter 1 to represent size = 10
                    data.size = 10
                data.selectingBoardSize = False
            elif data.selectingNumPlayers and (event.keysym in string.digits):
                 if int(event.keysym) in range(2, 4):
                    # data.__ = int(event.keysym) # TODO
                    pass

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
        canvas.create_image(data.width*(7/8), data.height*(1/8), image=data.virus1Image) # TODO: change to exhibit all 4 types of pieces after getting the images
        canvas.create_image(data.width*(1/8), data.height*(3/8), image=data.virus1Image)
        canvas.create_image(data.width*(1/8), data.height*(1/8), image=data.pillsImage)
        canvas.create_image(data.width*(7/8), data.height*(3/8), image=data.pillsImage)

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

        # size (5-10) and number of players (2-4) TODO
        canvas.create_text(data.width//4, data.height*(11/20), text="Board Size(Width):", font="Arial 45")
        if data.selectingBoardSize:
            canvas.create_rectangle(data.width//2, data.height//2, data.width*(3/4), data.height*(3/5), fill="light goldenrod")
        else:
            canvas.create_rectangle(data.width//2, data.height//2, data.width*(3/4), data.height*(3/5), fill="lemon chiffon")
        canvas.create_text(data.width*(5/8), data.height*(11/20), text=str(data.size), font="Arial 35")
        canvas.create_text(data.width*(7/8), data.height*(11/20), text="(5-10)", font="Arial 35")    

        # finish button
        canvas.create_rectangle(data.width*(3/8), data.height*(7/10+1/15), data.width*(5/8), data.height*(4/5+1/15), fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/4+1/15), text = "Finish!", font = "Arial 40")

    # AI mode level selection page
    def drawLevelSelectionPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
        canvas.create_text(data.width//2, data.height//4, text = "Select a Level!", font = "Arial 55 bold", fill = "purple")

        # easy mode
        canvas.create_rectangle(data.width//4, data.height//2, data.width*(3/4), data.height*(3/5), fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(11/20), text = "Easy", font = "Arial 35 bold")

        # normal mode
        canvas.create_rectangle(data.width//4, data.height*(3/5+1/30), data.width*(3/4), data.height*(7/10+1/30), fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(13/20+1/30), text = "Normal", font = "Arial 35 bold")

        # hard mode
        canvas.create_rectangle(data.width//4, data.height*(7/10+1/15), data.width*(3/4), data.height*(4/5+1/15), fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/4+1/15), text = "Hard", font = "Arial 35 bold")

    def drawSettingsPage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
        canvas.create_text(data.width//2, data.height//4, text = "Press the button below \n to start/stop the music", font = "Arial 55 bold", fill = "purple")

        # start button
        canvas.create_rectangle(data.width*(3/8), data.height*(2/5), data.width*(5/8), data.height//2, fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(9/20), text = "Start", font = "Arial 40 bold")

        # stop button
        canvas.create_rectangle(data.width*(3/8), data.height*(11/20), data.width*(5/8), data.height*(13/20), fill = "lemon chiffon")
        canvas.create_text(data.width//2, data.height*(3/5), text = "Stop", font = "Arial 40 bold")
        canvas.create_text(data.width//2, data.height*(3/4), text = "Press 'b' to return back to home page", font = "Arial 40 bold")

    # In game page
    def drawGamePage(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "#EFEBE9")
        self.drawBoard(canvas, data)

        # Game paused
        if data.gamePaused: 
            canvas.create_rectangle(0, data.height/3, data.width, \
                                            data.height*(2/3), fill = "gold")
            canvas.create_text(data.width/2, data.height/2, text = "Game Paused!",\
                                font = "TimesNewRoman 35 bold", fill = "red")

    # helper functions for drawing the game board    
    def pointInBoard(self, x, y, data):
        # return True if (x, y) is inside the board defined by data.
        return data.margin <= x <= data.width-data.margin and data.margin <= y <= data.height-data.margin

    def getCell(self, x, y, data):
        # return (row, col) in which (x, y) occurred or (-1, -1) if the point is outside the board.
        if not self.pointInBoard(x, y, data): return -1, -1
        row = (y - data.margin) // data.cellHeight
        col = (x - data.margin) // data.cellWidth
        return row, col

    def getCellBounds(self, row, col, data):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in board
        columnWidth = data.boardWidth / data.size
        rowHeight = data.boardHeight / data.size
        x0 = data.margin + col * columnWidth
        x1 = data.margin + (col+1) * columnWidth
        y0 = data.margin + row * rowHeight
        y1 = data.margin + (row+1) * rowHeight
        return x0, y0, x1, y1

    def drawBoard(self, canvas, data):
        canvas.create_rectangle(0, 0, data.width, data.height, fill="#C62828")

        # selecting 
        if data.selectedPos != (-1, -1) and data.putPos == (-1, -1):
            allLegalPos = self.GameBoard.getLegalPos(data.selectedPos)
            for row in range(data.size):
                for col in range(data.size):
                    # background 
                    x0, y0, x1, y1 = self.getCellBounds(row, col, data)
                    if (row, col) == data.selectedPos: color = "#9575CD"
                    elif (row, col) in allLegalPos: color = "#76FF03"
                    else: color = "#EF9A9A"
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3) 

                    # pieces (pills or viruses)
                    imageX = col*data.cellWidth + data.cellWidth//2 + data.margin
                    imageY = row*data.cellHeight + data.cellWidth//2 + data.margin
                    if data.board[row][col] == 0: canvas.create_image(imageX, imageY, image=data.pillsImage)
                    elif data.board[row][col] == 1: canvas.create_image(imageX, imageY, image=data.virus1Image)

        # moving
        # elif data.selectedPos == (-1, -1) and data.putPos != (-1, -1):
        else:
            for row in range(data.size):
                for col in range(data.size):
                    # background 
                    x0, y0, x1, y1 = self.getCellBounds(row, col, data)
                    color = "#EF9A9A"
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=3) 

                    # pieces (pills or viruses)
                    imageX = col*data.cellWidth + data.cellWidth//2 + data.margin
                    imageY = row*data.cellHeight + data.cellWidth//2 + data.margin
                    if data.board[row][col] == 0: canvas.create_image(imageX, imageY, image=data.pillsImage)
                    elif data.board[row][col] == 1: canvas.create_image(imageX, imageY, image=data.virus1Image)

        # game over page  
        def drawGameOverPage(self, canvas, data):
            canvas.create_rectangle(0, 0, data.width, data.height, fill="cyan")
            if data.winningPlayer == -1:
                canvas.create_text(data.width//2, data.height*(5/8), text="Tie!", font="Arial 60 bold")
            elif data.winningPlayer == 0:
                canvas.create_image(data.width//2, data.height//2, image=data.PillsWinBackgroundImage)
                canvas.create_text(data.width//2, data.height*(5/8), text="Pills win!", font="Arial 60 bold", fill="#388E3C")
            elif data.winningPlayer == 1:
                canvas.create_image(data.width//2, data.height//2, image=data.Virus1WinBackgroundImage) 
                canvas.create_text(data.width//2, data.height*(5/8), text="Virus 1 win!", font="Arial 60 bold", fill="#388E3C")
            canvas.create_text(data.width//2, data.height*(3/8), text="GAME OVER!", font="Chalkduster 75 bold", fill="#D50000")   
            canvas.create_text(data.width//2, data.height*(7/8), text="Press 'r' to start again", font="Arial 35", fill="#BA68C8") 

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

    ## uncomment this part until AI part finished
    # def AImove(self, data):
    #     print("AI playing")
    #     print("step %d:" % data.AIstep)
    #     data.AI.nextMove()
    #     # update the board after each AI's move
    #     self.GameBoard.board = data.AI.GameBoard.board 
    #     self.GameBoard.printBoard()
    #     data.board = data.AI.GameBoard.board
    #     data.AIstep += 1

    def timerFired(self, data):
        if data.inGame and not data.gameOver and not data.gamePaused:
            data.timeCounter += 1

            if data.singlePlayerMode:
                data.timerDelay = 200
                if not self.GameBoard.GameOver():
                    # move twice in each timer delay period
                    self.AImove(data)
                else:
                    data.inGame = False
                    if self.GameBoard.contains2048(): data.reach2048 = True
                    else: data.cannotMove = True

    def runGame(self, width, height): # tkinter starter code
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill='white', width=0)
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


