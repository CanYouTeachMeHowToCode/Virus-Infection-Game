#################################################################
# Fall 2018 Term Project--Virus Infection Game
# Your Name: Yilun Wu
# Your Andrew ID: yilunw
# Your Section: F
# Collaborators: yilunw
#################################################################
import string
import copy
import random
import sys

from image_util import *
from tkinter import *
from BasicAI import *
from Audio import *

##init part

def init(data):
    #initialize the first empty normal game board with a 8*8 size and two roles.
    data.boardSize = 8
    data.rows = data.boardSize
    data.cols = data.boardSize
    data.board = [[0 for col in range(data.cols)]for row in range(data.rows)]
    marginWidth = 10
    data.margin = marginWidth # margin around the board
    data.boardWidth  = data.width - 2*data.margin
    data.boardHeight = data.height - 2*data.margin
    data.cellWidth  = data.boardWidth / data.cols
    data.cellHeight = data.boardHeight / data.rows
    
    scaleWidth = 3
    scaleHeight = 3
    #import home page image
    data.homePageImageWidth = data.width
    data.homePageImageHeight = data.height
    data.homePageImage = PhotoImage(file="HomepageBackground.gif")
    data.homePageImage = data.homePageImage.zoom(scaleWidth, scaleHeight)
    
    #import virus win background image
    data.Virus1WinBackgroundImageWidth = data.width
    data.Virus1WinBackgroundImageHeight = data.height
    data.Virus1WinBackgroundImage = PhotoImage(file="Virus1WinBackground.gif")
    data.Virus1WinBackgroundImage = \
        data.Virus1WinBackgroundImage.zoom(scaleWidth, scaleHeight)
    
    #import pills win background image
    data.PillsWinBackgroundImageWidth = data.width
    data.PillsWinBackgroundImageHeight = data.height
    data.PillsWinBackgroundImage = PhotoImage(file="PillsWinBackground.gif")
    data.PillsWinBackgroundImage = \
        data.PillsWinBackgroundImage.zoom(scaleWidth, scaleHeight)
        
    #all pills and viruses on the board appears as the same size
    data.imageWidth = 100
    data.imageHeight = 100
    #import virus 1 image
    data.virus1Image = PhotoImage(file="Virus1.gif", \
                width = int(data.imageWidth), height = int(data.imageHeight))
    #the coordinates of the virus1 
    #(initially at the left-top corner in the board)
    data.firstVirus1X, data.firstVirus1Y = 0, 0
    #the virus 1 appears on the board as the number 1
    data.board[data.firstVirus1Y][data.firstVirus1X] = 1
    
    #import virus 2 image
    data.virus2Image = PhotoImage(file="Virus2.gif", \
                width = 70, height = 70)
    data.virus2Image = data.virus2Image.zoom(scaleWidth, scaleHeight)
    data.virus2Image = data.virus2Image.subsample(2, 2)
    #the coordinates of the virus2 
    #(initially at the right-top corner in the board)
    data.firstVirus2X, data.firstVirus2Y = 0, data.cols-1
    #the virus 2 appears on the board as the number 2
    data.board[data.firstVirus2Y][data.firstVirus2X] = 2
    
    #import pills image
    data.pillsImage = PhotoImage(file="pills.gif", \
                width = int(data.imageWidth), height = int(data.imageHeight))
    #the coordinates of the pills 
    #(initially at the left-bottom corner in the board)                                                 
    data.firstPillX, data.firstPillY = 0, data.cols-1
    #the pill appears on the board as the lowercase letter "p"
    data.board[data.firstPillY][data.firstPillX] = "p"
    
    data.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    data.lastSelection = (-1, -1)
    data.selectedPiece = (-1, -1)
    data.selectingPills = False
    data.selectingVirus1 = False
    data.selectingVirus2 = False
    
    data.levelSelection = False
    data.customizeMode = False
    data.settings = False
    data.selectingBoardSize = False
    data.GameBegin = False
    data.GameOver = False
    data.winningPieceType = None
    
    data.beginEasyAIMode = False
    data.beginMediumAIMode = False
    data.beginHardAIMode = False
    data.AIMove = False
    data.timer = 0
    data.AIDoMove = False
    data.chosenVirus1 = None

    #below are for A.I. initial datas
    data.virus1Lst = []
    data.boardScore = 0
    
    #below are for audio initial datas
    data.isPlaying = False
    data.mythread = None

def startBoard(data):
    # initialize an empty board with certain length and width \
    # according to different levels
    data.board = [[0 for col in range(data.cols)]for row in range(data.rows)]
    data.board[0][0] = 1
    data.board[data.rows-1][0] = "p"
    
    imageProportion = data.boardSize/8
    data.margin = imageProportion*data.margin # margin around the board
    data.boardWidth  = data.width - 2*data.margin
    data.boardHeight = data.height - 2*data.margin
    data.cellWidth  = data.boardWidth / data.cols
    data.cellHeight = data.boardHeight / data.rows

##Controller Part

def mousePressed(event, data):
    if data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == False and \
        data.settings == False:
        # enter the sigle player level selection mode
        if event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(data.height//2, \
                            int(data.height*(3/5))):
            data.levelSelection = True
        
        # enter the multiplayer customize mode
        elif event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(int(data.height*(3/5+1/30)), \
                            int(data.height*(7/10+1/30))):
            data.customizeMode = True
        
        # enter the settings
        elif event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(int(data.height*(7/10+1/15)), \
                            int(data.height*(4/5+1/15))):
            data.settings = True
            
        # enter the exit button to exit
        elif event.x in range(int(data.width*(5/6)), int(data.width*(29/30))) \
            and event.y in range(int(data.height*(9/10)), \
                            int(data.height*(29/30))):
            sys.exit()
    
    elif data.levelSelection == True and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == False:
        # enter one of the different levels to start the game state
        # enter the Easy mode
        if event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(data.height//2, int(data.height*(3/5))):
            data.GameBegin = True
            data.levelSelection = False
            data.beginEasyAIMode = True
        
        # enter the Medium mode
        elif event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(int(data.height*(3/5+1/30)), \
                            int(data.height*(7/10+1/30))):
            data.GameBegin = True
            data.levelSelection = False
            data.beginMediumAIMode = True
        
        # enter the Hard mode
        elif event.x in range(data.width//4, int(data.width*(3/4))) and \
            event.y in range(int(data.height*(7/10+1/15)), \
                            int(data.height*(4/5+1/15))):
            data.GameBegin = True
            data.levelSelection = False
            data.beginHardAIMode = True
    
    elif data.levelSelection == False and data.customizeMode == True and \
        data.GameBegin == False and data.GameOver == False:
        # press the empty "size button" to enter the board size
        if event.x in range(data.width//2, int(data.width*(3/4)))and \
            event.y in range(data.height//2, int(data.height*(3/5))):
            data.selectingBoardSize = True
        # press the finish button to enter the game state
        elif event.x in range(int(data.width*(3/8)), int(data.width*(5/8)))and \
            event.y in range(int(data.height*(7/10+1/15)), \
                            int(data.height*(4/5+1/15))):
            data.GameBegin = True
            data.customizeMode = False
    
    elif data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == True and data.GameOver == False:
        (row, col) = getCell(event.x, event.y, data)
        # select this (row, col) unless it is selected
        if (data.selection == (row, col)):
            data.selection = (-1, -1)
        else:
            data.selection = (row, col)
   
    elif data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == True:
        pass
    
    if data.settings == True:
        if event.x in range(int(data.width*(3/8)), int(data.width*(5/8))) \
            and event.y in range(int(data.height*(2/5)), data.height//2):
                print("playing")
                data.isPlaying = True
                pressPlayButton(data)
        elif event.x in range(int(data.width*(3/8)), int(data.width*(5/8))) \
            and event.y in range(int(data.height*(11/20)),\
                                int(data.height*(13/20))):
                print("stop!")
                pressStopButton(data)

def keyPressed(event, data):
    if data.settings == True and event.keysym == "b":
        data.settings = False
        data.levelSelection = False
        data.customizeMode = False
        data.GameBegin = False 
        data.GameOver = False
    #press "shift + b" to return back to home page
    if event.keysym == "B":
        data.levelSelection = False
        data.customizeMode = False
        data.GameBegin = False 
        data.GameOver = False
    elif data.levelSelection == False and data.customizeMode == True and \
        data.GameBegin == False and data.GameOver == False:
        if event.keysym in string.digits and data.selectingBoardSize:
            if int(event.keysym) in range(5,10):
                data.boardSize = int(event.keysym)
            elif int(event.keysym) == 1:
                data.boardSize = 10
            data.rows = data.boardSize
            data.cols = data.boardSize
            data.selectingBoardSize = False
        startBoard(data)
    elif data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == True:
        if event.keysym == "r":
            init(data)

def timerFired(data):
    #the A.I. will pause for 1 second and then move its step
    if data.AIMove:
        data.timer += 1
        print(data.timer)
        if data.timer%2 == 0:
            print("move")
            data.AIDoMove = True
            data.timer = 0

##Main game mechanisms(algorithms) below

def isLegalMove(data):
    if data.board[int(data.selection[0])][int(data.selection[1])] != 0:
        return False
    else:
        drow = [-1, 0, 1]
        dcol = [-1, 0, 1]
        if int(data.selection[0]) - int(data.lastSelection[0])in drow and \
            int(data.selection[1]) - int(data.lastSelection[1]) in dcol:
                return True
        else:
            return False

def isLegalJump(data):
    if data.board[int(data.selection[0])][int(data.selection[1])] != 0:
        return False
    else:
        drow = [-2, 0, 2]
        dcol = [-2, 0, 2]
        if int(data.selection[0]) - int(data.lastSelection[0])in drow and \
            int(data.selection[1]) - int(data.lastSelection[1]) in dcol:
                return True
        else:
            return False

def movePills(data):
    #first ensure that every first selection should be a virus or a pill
    if (data.selectingPills, data.selectingVirus1) == (False, False) \
        and data.board[int(data.selection[0])][int(data.selection[1])] == 0:
        data.selection = (-1, -1)
    elif data.board[int(data.selection[0])][int(data.selection[1])] == "p": 
        #first select a pill
        data.selectingPills = True
        #to ensure that players cannot select pills and viruses at the same time
        if data.selectingPills == True and data.selectingVirus1 == True:
            data.selectingVirus1 = False
            print("1")
            data.selection = (-1, -1)
        else:
            data.lastSelection = (data.selection)
    #print(data.lastSelection, data.selection)
    if data.selectingPills == True and data.selectingVirus1 == False \
        and data.selection != (-1, -1):
        #then move the pill if the movement is legal
        #print(data.lastSelection, data.selection)
        if isLegalMove(data):
            data.board[int(data.selection[0])][int(data.selection[1])] = "p"
            invade(data)
            isGameOver(data)
            #renew all settings for the next move
            data.selection = (-1, -1) 
            data.selectingPills = False
            if data.beginEasyAIMode == True or data.beginMediumAIMode == True \
                or data.beginHardAIMode == True:
                print("AI's turn!")
                data.AIMove = True
        elif isLegalJump(data):
            data.board[int(data.lastSelection[0])][int(data.lastSelection[1])] = 0
            data.board[int(data.selection[0])][int(data.selection[1])] = "p"
            invade(data)
            isGameOver(data)
            #renew all settings for the next move
            data.selection = (-1, -1)   
            data.selectingPills = False
            if data.beginEasyAIMode == True or data.beginMediumAIMode == True \
                or data.beginHardAIMode == True:
                print("AI's turn!")
                data.AIMove = True

def moveVirus1(data):
    #first ensure that every first selection should be a virus or a pill
    if (data.selectingPills, data.selectingVirus1) == (False, False) \
        and data.board[int(data.selection[0])][int(data.selection[1])] == 0:
        data.selection = (-1, -1)
    #if enters the single player mode, the user can only move pills
    elif data.beginEasyAIMode == True or data.beginMediumAIMode == True or \
        data.beginHardAIMode == True:
        data.selection = (-1, -1)
    elif data.board[int(data.selection[0])][int(data.selection[1])] == 1: 
        #first select a virus 1
        data.selectingVirus1 = True
        #to ensure that players cannot select pills and viruses at the same time
        if data.selectingPills == True and data.selectingVirus1 == True:
            data.selectingPills = False
            print("2")
            data.selection = (-1, -1)
        else:
            data.lastSelection = (data.selection)
    #print(data.lastSelection, data.selection)
    if data.selectingVirus1 == True and data.selectingPills == False \
        and data.selection != (-1, -1):
        #then move the virus 1 if the movement is legal
        if isLegalMove(data):
            print("yes")
            data.board[int(data.selection[0])][int(data.selection[1])] = 1
            invade(data)
            isGameOver(data)
            #renew all settings for the next move
            data.selection = (-1, -1)  
            data.selectingVirus1 = False
        elif isLegalJump(data):
            data.board[int(data.lastSelection[0])][int(data.lastSelection[1])] = 0
            data.board[int(data.selection[0])][int(data.selection[1])] = 1
            invade(data)
            isGameOver(data)
            #renew all settings for the next move
            data.selection = (-1, -1)   
            data.selectingVirus1 = False
            
def invade(data):
    #once a moving step is completed, the virus/pill on that unit can \
    #invade the area 1 unit surrounding it. That is, to "eaten up" all units \
    #that are not empty and not the same species. (i.e. pills eaten up viruses \
    #or viruses eaten up pills.)
    # (note: different species of viruses can also invade each other.)
    data.selectedPiece = (data.selection)
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if drow == dcol == 0:
                continue
            elif 0 <= int(data.selection[0])+drow <= data.rows-1 and \
                0 <= int(data.selection[1])+dcol <= data.cols-1 and \
                data.board[int(data.selectedPiece[0])]\
                [int(data.selectedPiece[1])] != 0:
                # to ensure that the movement is in the board
                if data.board[int(data.selection[0])+drow]\
                    [int(data.selection[1])+dcol] != \
                    data.board[int(data.selection[0])][int(data.selection[1])] \
                    and data.board[int(data.selection[0])+drow]\
                    [int(data.selection[1])+dcol] != 0 :
                    #to check not the same species and not empty
                    # then "eaten up" all other species.
                    data.board[int(data.selection[0])+drow]\
                    [int(data.selection[1])+dcol] = data.board\
                    [int(data.selectedPiece[0])][int(data.selectedPiece[1])]

def isGameOver(data):
    if data.GameBegin == True and data.GameOver == False:
        print(data.board)
        countZeros = 0
        countVirus1 = 0
        countPills = 0
        for row in range(data.rows):
            for col in range(data.cols):
                if data.board[row][col] == 0:
                    countZeros += 1
                elif data.board[row][col] == 1:
                    countVirus1 += 1
                elif data.board[row][col] == "p":
                    countPills += 1
        #if there is no empty space left, or there is only Pills or Viruses 
        #left, or there is no legal moves for a certain piece, then game over.
        if countZeros == 0:
            if countVirus1 > countPills:
                data.winningPieceType = "Virus1"
            elif countVirus1 < countPills:
                data.winningPieceType = "Pills"
            else:
                data.winningPieceType = "Tie!"
            data.GameBegin = False
            data.GameOver = True
        elif countVirus1 == 0: 
            data.winningPieceType = "Pills"
            data.GameBegin = False
            data.GameOver = True
        elif countPills == 0:  
            data.winningPieceType = "Virus1"
            data.GameBegin = False
            data.GameOver = True
        else:
            pillsList = []
            virus1List = []
            # to check if every pill cannot have any legal move at all
            checkIsOver = True
            for row in range(data.rows):
                for col in range(data.cols):
                    if data.board[row][col] == "p":
                        pillsList.append((row, col))
                    elif data.board[row][col] == 1:
                        virus1List.append((row, col))
            for pills in pillsList:
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        if 0 <= pills[0]+drow <= data.rows-1 and \
                            0 <= pills[1]+dcol <= data.cols-1 and \
                            data.board[pills[0]+drow][pills[1]+dcol] == 0:
                            checkIsOver = False
                            break
                        else:
                            continue
                    if checkIsOver == False:
                        break
                    else:
                        continue
                if checkIsOver == False:
                    break
                
                for drow in [-2, 0, 2]:
                    for dcol in [-2, 0, 2]:
                        if 0 <= pills[0]+drow <= data.rows-1 and \
                            0 <= pills[1]+dcol <= data.cols-1 and \
                            data.board[pills[0]+drow][pills[1]+dcol] == 0:
                            checkIsOver = False
                            break
                        else:
                            continue
                    if checkIsOver == False:
                        break
                    else:
                        continue
                if checkIsOver == False:
                    break
            
            if checkIsOver:
                data.winningPieceType = "Virus1"
                data.GameBegin = False
                data.GameOver = True
            
            # to check if every virus cannot have any legal move at all
            checkIsOver = True   
            for virus1 in virus1List:
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        if 0 <= virus1[0]+drow <= data.rows-1 and \
                            0 <= virus1[1]+dcol <= data.cols-1 and \
                            data.board[virus1[0]+drow][virus1[1]+dcol] == 0:
                            checkIsOver = False
                            break
                        else:
                            continue
                    if checkIsOver == False:
                        break
                    else:
                        continue
                if checkIsOver == False:
                    break
                
                for drow in [-2, 0, 2]:
                    for dcol in [-2, 0, 2]:
                        if 0 <= virus1[0]+drow <= data.rows-1 and \
                            0 <= virus1[1]+dcol <= data.cols-1 and \
                            data.board[virus1[0]+drow][virus1[1]+dcol] == 0:
                            checkIsOver = False
                            break
                        else:
                            continue
                    if checkIsOver == False:
                        break
                    else:
                        continue
                if checkIsOver == False:
                    break
                    
            if checkIsOver:
                data.winningPieceType = "Pills"
                data.GameBegin = False
                data.GameOver = True
  
##Graphic drawing functions below

def drawStartState(canvas, data):
    #draw home page
    #draw background
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "VioletRed1")
    canvas.create_image(data.width//2, data.height//2, \
                        image = data.homePageImage)
    
    #draw buttons and icons
    canvas.create_text(data.width//2, data.height//8, text = "VIRUS", \
                        fill = "#64DD17", font = "Chalkduster 75 bold" )
    canvas.create_text(data.width//2, data.height//4, text = "INFECTION", \
                        fill = "light coral", font = "Chalkduster 75 bold" )    
    canvas.create_text(data.width//2, 3*(data.height//8), text = "GAME", \
                        fill = "green yellow", font = "Chalkduster 75 bold" )                                        
    canvas.create_image(data.width*(7/8), data.height*(1/8), \
                        image = data.virus1Image)
    canvas.create_image(data.width*(1/8), data.height*(3/8), \
                        image = data.virus1Image)
    canvas.create_image(data.width*(1/8), data.height*(1/8), \
                        image = data.pillsImage)
    canvas.create_image(data.width*(7/8), data.height*(3/8), \
                        image = data.pillsImage)
    #single player mode button
    canvas.create_rectangle(data.width//4, data.height//2, \
                            data.width*(3/4), data.height*(3/5), 
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(11/20), \
                            text = "Single Player", font = "Arial 40 bold")
    #multi-player mode button
    canvas.create_rectangle(data.width//4, data.height*(3/5+1/30), \
                            data.width*(3/4), data.height*(7/10+1/30), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(13/20+1/30), \
                            text = "MultiPlayer", font = "Arial 40 bold")
    #settings button
    canvas.create_rectangle(data.width//4, data.height*(7/10+1/15), \
                            data.width*(3/4), data.height*(4/5+1/15), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(3/4+1/15), \
                            text = "Settings", font = "Arial 40 bold")
    #quit button
    canvas.create_rectangle(data.width*(5/6), data.height*(9/10), \
                            data.width*(29/30), data.height*(29/30),
                            fill = "light grey")
    canvas.create_text(data.width*(9/10), data.height*(14/15), \
                            text = "Quit", font = "Arial 30 bold")

def drawSinglePlayerLevelSelectionState(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
    canvas.create_text(data.width//2, data.height//4, text = "Select a Level!", \
                        font = "Arial 55 bold", fill = "purple")
    #level 1 (Easy mode)
    canvas.create_rectangle(data.width//4, data.height//2, \
                            data.width*(3/4), data.height*(3/5), 
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(11/20), text = "Easy", \
                        font = "Arial 35 bold")
    #level 2 (Medium mode)
    canvas.create_rectangle(data.width//4, data.height*(3/5+1/30), \
                            data.width*(3/4), data.height*(7/10+1/30), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(13/20+1/30), \
                        text = "Medium", font = "Arial 35 bold")
    #level 3 (Hard mode)
    canvas.create_rectangle(data.width//4, data.height*(7/10+1/15), \
                            data.width*(3/4), data.height*(4/5+1/15), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(3/4+1/15), 
                        text = "Hard", font = "Arial 35 bold")
    
def drawMultiplayerCustomizeSizeState(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
    canvas.create_text(data.width//2, data.height//4, \
                        text = "Select Your Size Here!", \
                        font = "Arial 50 bold", fill = "purple")
    #Sizes (5-10)
    canvas.create_text(data.width//4, data.height*(11/20), \
                        text = "Board Size(Width):", font = "Arial 45")
    if data.selectingBoardSize:
        canvas.create_rectangle(data.width//2, data.height//2, \
                            data.width*(3/4), data.height*(3/5), \
                            fill = "light goldenrod")
    else:
        canvas.create_rectangle(data.width//2, data.height//2, \
                            data.width*(3/4), data.height*(3/5), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width*(5/8), data.height*(11/20), \
                        text = data.boardSize, font = "Arial 35")
    canvas.create_text(data.width*(7/8), data.height*(11/20), \
                        text = "(5-10)", font = "Arial 35")                    
    # finish button
    canvas.create_rectangle(data.width*(3/8), data.height*(7/10+1/15), \
                            data.width*(5/8), data.height*(4/5+1/15), \
                            fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(3/4+1/15), 
                        text = "Finish!", font = "Arial 40")

def drawSettingsState(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
    canvas.create_text(data.width//2, data.height//4, \
                        text = "Press the button below \n to start/stop the music", \
                        font = "Arial 55 bold", fill = "purple")
    # start button
    canvas.create_rectangle(data.width*(3/8), data.height*(2/5), \
                data.width*(5/8), data.height//2, fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(9/20), \
                        text = "Start", \
                        font = "Arial 40 bold")
    # stop button
    canvas.create_rectangle(data.width*(3/8), data.height*(11/20), \
                data.width*(5/8), data.height*(13/20), fill = "lemon chiffon")
    canvas.create_text(data.width//2, data.height*(3/5), \
                        text = "Stop", font = "Arial 40 bold")

    canvas.create_text(data.width//2, data.height*(3/4), \
                        text = "Press 'b' to return back to home page", \
                        font = "Arial 40 bold")

# helper functions for drawing the game board    
def pointInBoard(x, y, data):
    # return True if (x, y) is inside the board defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    #return (row, col) in which (x, y) occurred \
    #or (-1, -1) if the point is outside the board.
    if (not pointInBoard(x, y, data)):
        return (-1, -1)
    row = (y - data.margin) // data.cellHeight
    col = (x - data.margin) // data.cellWidth
    return (row, col)

def getCellBounds(row, col, data):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in board
    columnWidth = data.boardWidth / data.cols
    rowHeight = data.boardHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

def drawBoard(canvas,data):
    #drawing backgrounds
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "#C62828")
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            if (data.selection == (row, col)) and \
                (isLegalMove(data) or isLegalJump(data)):
                color = "#76FF03"
            elif (data.selection == (row, col)) and \
                data.board[row][col] in ["p", 1]:
                color = "#9575CD"
            elif (data.selection == (row, col)) and not \
                (isLegalMove(data) or isLegalJump(data)):
                color = "#ECEFF1"
            else:
                color = "#EF9A9A"
            everyCellWidth = 3
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, \
                                    width = everyCellWidth)

def drawVirus1(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == 1:
                imageX = col*data.cellWidth + data.cellWidth//2 + data.margin
                imageY = row*data.cellHeight + data.cellWidth//2 + data.margin
                canvas.create_image(imageX, imageY, image = data.virus1Image)

def drawPills(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == "p":
                imageX = col*data.cellWidth + data.cellWidth//2 + data.margin
                imageY = row*data.cellHeight + data.cellWidth//2 + data.margin
                canvas.create_image(imageX, imageY, image = data.pillsImage)

def drawGameState(canvas, data):
    drawBoard(canvas, data)
    drawPills(canvas, data)
    drawVirus1(canvas, data)
    movePills(data)
    moveVirus1(data)
    easyAIMove(data)
    mediumAIMove(data)
    hardAIMove(data)

def drawGameOverState(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "cyan")
    if data.winningPieceType == "Tie!":
        canvas.create_text(data.width//2, data.height*(5/8), \
                        text = str(data.winningPieceType) + "Nobody wins!", \
                        font = "Arial 60 bold")
    else:
        if data.winningPieceType == "Virus1":
            canvas.create_image(data.width//2, data.height//2, \
                            image = data.Virus1WinBackgroundImage)
        elif data.winningPieceType == "Pills":
            canvas.create_image(data.width//2, data.height//2, \
                            image = data.PillsWinBackgroundImage)
        canvas.create_text(data.width//2, data.height*(5/8), \
                        text = str(data.winningPieceType) + " win!", \
                        font = "Arial 60 bold", fill = "#388E3C")
    canvas.create_text(data.width//2, data.height*(3/8), \
                    text = "GAME OVER!", font = "Chalkduster 75 bold", \
                                        fill = "#D50000")   
    canvas.create_text(data.width//2, data.height*(7/8), \
                    text = "Press 'r' to start again", \
                    font = "Arial 35", fill = "#BA68C8") 

def redrawAll(canvas, data):
    if data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == False:
        drawStartState(canvas, data)
        if data.settings == True:
           drawSettingsState(canvas, data)
    
    elif data.levelSelection == True and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == False:
        drawSinglePlayerLevelSelectionState(canvas, data)
    
    elif data.levelSelection == False and data.customizeMode == True and \
        data.GameBegin == False and data.GameOver == False:
        drawMultiplayerCustomizeSizeState(canvas, data)
    
    elif data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == True and data.GameOver == False:
        drawGameState(canvas, data)
    
    elif data.levelSelection == False and data.customizeMode == False and \
        data.GameBegin == False and data.GameOver == True:
        drawGameOverState(canvas, data)

##Citation : tkinter start code from \
##           https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def runVirusInfectionGame(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
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
    init(data)
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
    print("bye!")

runVirusInfectionGame(800, 800)