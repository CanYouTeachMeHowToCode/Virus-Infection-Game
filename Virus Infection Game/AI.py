## Basic A.I. part
import random
import copy
#basic A.I. level 1 (Easy Mode):
#--> with a random pick of virus list and the random possible step
# in a 8*8 board
def easyChoosingVirus1(data):
    data.virus1Lst = []
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == 1:
                #to check that if the virus 1 have empty units to move
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        if 0 <= row+drow <= data.rows-1 and \
                            0 <= col+dcol <= data.cols-1 and \
                            data.board[row+drow][col+dcol] == 0:
                            data.virus1Lst.append((row,col))
                        else:
                            continue
    #remove repetitive positions for efficiency
    data.virus1Lst = list(set(data.virus1Lst))
    print("data.virus1Lst:", data.virus1Lst)
    chosenVirus1 = random.choice(data.virus1Lst)
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if data.board[chosenVirus1[0]+drow][chosenVirus1[1]+dcol] == 0:
                data.chosenVirus1 = chosenVirus1
            else:
                break
    if data.chosenVirus1 == None:
        data.chosenVirus1 = random.choice(data.virus1Lst)

def easyMovingVirus1(data):
    board = copy.deepcopy(data.board)
    availablePosition1 = []
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if 0 <= data.chosenVirus1[0]+drow <= data.rows-1 and \
                0 <= data.chosenVirus1[1]+dcol <= data.cols-1 and \
                board[data.chosenVirus1[0]+drow][data.chosenVirus1[1]+dcol] == 0:
                availablePosition1.append((data.chosenVirus1[0]+drow,\
                                            data.chosenVirus1[1]+dcol))
            else:
                continue
    availablePosition2 = []
    for drow in [-2, 0, 2]:
        for dcol in [-2, 0, 2]:
            if 0 <= data.chosenVirus1[0]+drow <= data.rows-1 and \
                0 <= data.chosenVirus1[1]+dcol <= data.cols-1 and \
                board[data.chosenVirus1[0]+drow][data.chosenVirus1[1]+dcol] == 0:
                availablePosition2.append((data.chosenVirus1[0]+drow,\
                                            data.chosenVirus1[1]+dcol))
            else:
                continue
    print(availablePosition1, availablePosition2)
    availablePosition = availablePosition1 + availablePosition2
    data.movingPosition = random.choice(availablePosition)
    print(data.movingPosition)
    if data.movingPosition in availablePosition2:
        board[data.chosenVirus1[0]][data.chosenVirus1[1]] = 0
    board[data.movingPosition[0]][data.movingPosition[1]] = 1
    data.board = board

def easyAIMove(data):
    if data.beginEasyAIMode == True and data.AIMove == True and  \
        data.AIDoMove == True:
        print("easy")
        print("virus1 list: ", end = "")
        print(data.virus1Lst)
        easyChoosingVirus1(data)
        print(data.chosenVirus1)
        easyMovingVirus1(data)
        AIInvade(data)
        AIisGameOver(data)
        data.AIMove = False
        data.AIDoMove = False

#basic A.I. level 2 (Medium Mode):
#--> with a random pick of virus list and the most optimistic step
# (choosing the step that can invade most pieces)
# in a 8*8 board

def mediumChoosingVirus1(data):
    data.virus1Lst = []
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == 1:
                #to check that if the virus 1 have empty units to move or jump
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        if 0 <= row+drow <= data.rows-1 and \
                            0 <= col+dcol <= data.cols-1 and \
                            data.board[row+drow][col+dcol] == 0:
                            data.virus1Lst.append((row,col))
                        else:
                            continue
                for drow in [-2, 0, 2]:
                    for dcol in [-2, 0, 2]:
                        if 0 <= row+drow <= data.rows-2 and \
                            0 <= col+dcol <= data.cols-2 and \
                            data.board[row+drow][col+dcol] == 0:
                            data.virus1Lst.append((row,col))
                        else:
                            continue
    #remove repetitive positions for efficiency
    data.virus1Lst = list(set(data.virus1Lst))
    print("data.virus1Lst:", data.virus1Lst)
    if data.virus1Lst == []:
        data.winningPieceType = "Pills"
        data.GameOver = True
    chosenVirus1 = random.choice(data.virus1Lst)
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if 0 <= chosenVirus1[0]+drow <= data.rows-1 and \
                0 <= chosenVirus1[1]+dcol <= data.cols-1 and \
                data.board[chosenVirus1[0]+drow][chosenVirus1[1]+dcol] == 0:
                data.chosenVirus1 = chosenVirus1
            else:
                break
    if data.chosenVirus1 == None:
        data.chosenVirus1 = random.choice(data.virus1Lst)

def mediumMovingVirus1(data):
    board = copy.deepcopy(data.board)
    availablePosition1 = []
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if 0 <= data.chosenVirus1[0]+drow <= data.rows-1 and \
                0 <= data.chosenVirus1[1]+dcol <= data.cols-1 and \
                board[data.chosenVirus1[0]+drow][data.chosenVirus1[1]+dcol] == 0:
                availablePosition1.append((data.chosenVirus1[0]+drow,\
                                            data.chosenVirus1[1]+dcol))
            else:
                continue
    availablePosition2 = []
    for drow in [-2, 0, 2]:
        for dcol in [-2, 0, 2]:
            if 0 <= data.chosenVirus1[0]+drow <= data.rows-1 and \
                0 <= data.chosenVirus1[1]+dcol <= data.cols-1 and \
                board[data.chosenVirus1[0]+drow][data.chosenVirus1[1]+dcol] == 0:
                availablePosition2.append((data.chosenVirus1[0]+drow,\
                                            data.chosenVirus1[1]+dcol))
            else:
                continue
    print(availablePosition1, availablePosition2)
    availablePosition = availablePosition1 + availablePosition2
    data.movingPosition = random.choice(availablePosition)
    print(data.movingPosition)
    if data.movingPosition in availablePosition2:
        board[data.chosenVirus1[0]][data.chosenVirus1[1]] = 0
    board[data.movingPosition[0]][data.movingPosition[1]] = 1
    data.board = board

def mediumAIMove(data):
    if data.beginMediumAIMode == True and data.AIMove == True and \
        data.AIDoMove == True:
        print("medium")
        mediumChoosingVirus1(data)
        print(data.chosenVirus1)
        mediumMovingVirus1(data)
        AIInvade(data)
        AIisGameOver(data)
        data.AIMove = False
        data.AIDoMove = False

#basic A.I. level 3 (Hard Mode):
#--> with the most optimistic pick of virus list and the most optimistic step
# in a 8*8 board

def getAvailablePosition(data):
    availablePositionList1 = []
    availablePositionList2 = []
    board = copy.deepcopy(data.board)
    # first fint every empty place on the board that viruses are leagl 
    # to move there
    for row in range(data.rows):
        for col in range(data.cols):
            if board[row][col] == 0:
                for drow in [-1, 0, 1]:
                    for dcol in [-1, 0, 1]:
                        if 0 <= row+drow <= data.rows-1 and \
                            0 <= col+dcol <= data.cols-1 and \
                            board[row+drow][col+dcol] == 1:
                            availablePositionList1.append((row, col))
                for drow in [-2, 0, 2]:
                    for dcol in [-2, 0, 2]:
                        if 0 <= row+drow <= data.rows-2 and \
                            0 <= col+dcol <= data.cols-2 and \
                            board[row+drow][col+dcol] == 1:
                            availablePositionList2.append((row, col))
            else:
                continue
    print(availablePositionList1, availablePositionList2)
    return availablePositionList1, availablePositionList2
    
## Citation: below code is partially written by Eric Clinch(112 TA)
def maxieMoveCount(data):
    board = copy.deepcopy(data.board)
    countPills = 0
    maxCount1 = 0
    maxPosition1 = None
    if getAvailablePosition(data)[0] == []:
        return 0, None
    for availablePosition1 in getAvailablePosition(data)[0]:
        row, col = availablePosition1[0], availablePosition1[1]
        print((row, col))
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if 0 <= row+drow <= data.rows-1 and \
                    0 <= col+dcol <= data.cols-1 and \
                    board[row+drow][col+dcol] == "p":
                    print("find pills!")
                    countPills += 1
        print("countPills:", countPills)
        if countPills > maxCount1:
            maxCount1 = countPills
            maxPosition1 = availablePosition1
        print("maxCount1:", maxCount1)
        countPills = 0
    return maxCount1, maxPosition1

def maxieJumpCount(data):
    board = copy.deepcopy(data.board)
    countPills = 0
    maxCount2 = 0
    maxPosition2 = None
    if getAvailablePosition(data)[1] == []:
        return 0, None
    for availablePosition2 in getAvailablePosition(data)[1]:
        row, col = availablePosition2[0], availablePosition2[1]
        print((row, col))
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                if 0 <= row+drow <= data.rows-1 and \
                    0 <= col+dcol <= data.cols-1 and \
                    board[row+drow][col+dcol] == "p":
                    print("find pills!")
                    countPills += 1
        print("countPills:", countPills)
        if countPills > maxCount2:
            maxCount2 = countPills
            maxPosition2 = availablePosition2
        print("maxCount2:", maxCount2)
        countPills = 0
    return maxCount2, maxPosition2 
##citation over

def hardAIMaxieMove(data):
    board = copy.deepcopy(data.board)
    # then figure out every position's profit (the number of pills that 
    # can be invaded or eaten up) and then find out the largest profit place 
    print(data.board)
    maxCount, maxPosition = (0, None)
    if maxieJumpCount(data)[0] - 1 > maxieMoveCount(data)[0]:
        maxCount = maxieJumpCount(data)[0]
        maxPosition = maxieJumpCount(data)[1]
    else:
        maxCount = maxieMoveCount(data)[0]
        maxPosition = maxieMoveCount(data)[1]
    print("maxCount, maxPosition", end= " ")
    print(maxCount, maxPosition)        
    
    if maxPosition == None:
        print("xian fa yu")
        # if there is too few viruses, propagate first.
        mediumChoosingVirus1(data)
        data.movingPosition = random.choice(getAvailablePosition(data)[0])
        print(data.movingPosition)
        data.board[data.movingPosition[0]][data.movingPosition[1]] = 1
    else:
        # and finally find out the possible original virus that can reach that place
        # and do move.
        chosenVirusList = []
        if maxPosition in getAvailablePosition(data)[0]:
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if 0 <= maxPosition[0]+drow <= data.rows-1 and \
                        0 <= maxPosition[1]+dcol <= data.cols-1 and \
                        board[maxPosition[0]+drow][maxPosition[1]+dcol] == 1:
                        chosenVirusList.append((maxPosition[0]+drow,\
                                                maxPosition[1]+dcol))
            chosenVirus = random.choice(chosenVirusList)
        elif maxPosition in getAvailablePosition(data)[1]:
            for drow in [-2, 0, 2]:
                for dcol in [-2, 0, 2]:
                    if 0 <= maxPosition[0]+drow <= data.rows-1 and \
                        0 <= maxPosition[1]+dcol <= data.cols-1 and \
                        board[maxPosition[0]+drow][maxPosition[1]+dcol] == 1:
                        chosenVirusList.append((maxPosition[0]+drow,\
                                                maxPosition[1]+dcol))
            chosenVirus = random.choice(chosenVirusList)
            board[chosenVirus[0]][chosenVirus[1]] = 0
        board[maxPosition[0]][maxPosition[1]] = 1
        data.board = board
        data.movingPosition = maxPosition
        
def hardAIMove(data):
    if data.beginHardAIMode == True and data.AIMove == True and  \
        data.AIDoMove == True:
        print("hard")
        hardAIMaxieMove(data)
        AIInvade(data)
        AIisGameOver(data)
        data.AIMove = False
        data.AIDoMove = False

def AIInvade(data):
    #the invade function for A.I.'s move
    print("invade")
    print(data.movingPosition)
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if 0 <= data.movingPosition[0]+drow <= data.rows-1 and \
                0 <= data.movingPosition[1]+dcol <= data.cols-1 and \
                data.board[data.movingPosition[0]+drow] \
                        [data.movingPosition[1]+dcol] == "p":
                data.board[data.movingPosition[0]+drow] \
                        [data.movingPosition[1]+dcol] = 1

def AIisGameOver(data):
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