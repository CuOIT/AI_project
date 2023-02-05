import UI
import copy
import main
def moveList(chess_state,click,turn):
    oldX = click[0][0]
    oldY = click[0][1]
    piece = chess_state[oldX][oldY]
    func=globals()['moveList'+piece[1:]]
    moveList=func(oldX, oldY, turn, chess_state, True)
    return moveList

def availableMove(chess_state, click, turn):
    return click[1] in moveList(chess_state,click,turn)

def update(chess_state, list_chess_state,click):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]
    list_chess_state.append(copy.deepcopy(chess_state))
    # Cập nhật lại bàn cờ
    #neu xe di chuyen
    if "Rook" in chess_state[oldX][oldY]:
        if oldX == 7 and oldY == 0:
            main.castle["wQR"] = False
        elif oldX == 7 and oldY == 7:
            main.castle["wKR"] = False
        elif oldX == 0 and oldY == 0:
            main.castle["bQR"] = False
        elif oldX == 0 and oldY == 7:
            main.castle["bKR"] = False
    
    # neu nhap thanh thi cap nhat lai con xe
    elif "King" in chess_state[oldX][oldY]:
             #neu tuong di chuyen
        if newX - oldX == 1 or oldX - newX == 1 or newY - oldY == 1 or oldY - newY == 1:
            if oldY == 4 and oldX == 7: 
                main.castle["wKR"] = False
                main.castle["wQR"] = False
            elif oldY == 4 and oldX == 0:
                main.castle["bQR"] = False
                main.castle["bKR"] = False
                
        elif newY - oldY == 2:
            if chess_state[oldX][oldY] == "wKing":
                main.castle["wKR"] = False
                main.castle["wQR"] = False
            else:
                main.castle["bQR"] = False
                main.castle["bKR"] = False
            chess_state[newX][newY-1] = chess_state[newX][newY+1] 
            chess_state[newX][newY+1] = "xx"
            
        elif oldY - newY == 2:
            if chess_state[oldX][oldY] == "wKing":
                main.castle["wKR"] = False
                main.castle["wQR"] = False
            else:
                main.castle["bQR"] = False
                main.castle["bKR"] = False
                
            chess_state[newX][newY+1] = chess_state[newX][newY-2]
            chess_state[newX][newY-2] = "xx"
            
    chess_state[newX][newY] = chess_state[oldX][oldY]
    chess_state[oldX][oldY] = "xx"

def checkPawnPromotion(chess_state, click, screen):
    newX = click[1][0]
    newY = click[1][1]
    if chess_state[0][newY] == 'wPawn':
        chess_state[newX][newY] = UI.promoteChoice(screen,'w')
    if chess_state[7][newY]== 'bPawn':
        chess_state[newX][newY] = UI.promoteChoice(screen,'b')

def checkAcceptMove(chess_state, turn, x, y ,newX, newY):
    temp = copy.deepcopy(chess_state) #copy bàn cờ
    piece1 = chess_state[x][y] # lưu lại con cờ ở vị trí sẽ đi
    piece2 = temp[x][y] #lưu lại con cờ ở vị trí con cờ x,y sẽ đi vào

    temp[newX][newY] = piece1 # cập nhật bàn cờ ảo
    temp[x][y] = "xx"
    
    # nếu vua bị tấn công sau khi di chuyển => nước đi không hợp lệ => false
    if KingInAttack(temp, turn) !=False:
        temp[newX][newY] = piece2 # cập nhật lại bàn cờ thật
        temp[x][y] = piece1
        return False

    temp[newX][newY] = piece2 # cập nhật lại bàn cờ thật
    temp[x][y] = piece1
    return True

def moveListPawn(x, y, turn, chess_state, realState):
    moveList=[]
    if turn == 'w':
        if chess_state[x-1][y] == "xx":  # White move ahead 1 step
            pos = (x-1,y)
            if realState == True:
                if checkAcceptMove(chess_state, turn,x, y, x-1,y):
                    moveList.append(pos)
            else:
                moveList.append(pos)

            if x==6 and chess_state[x-2][y] == "xx":  # White move ahead 2 step
                pos = (x-2, y)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x-2,y):
                        moveList.append(pos)
                else:
                    moveList.append(pos)

        if y - 1 >= 0:
            if chess_state[x - 1][y - 1][0] == 'b':  # Check enemy chess
                pos = (x - 1, y - 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x-1, y-1):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
        if y + 1 <= 7:
            if chess_state[x - 1][y + 1][0] == 'b':
                pos = (x - 1, y + 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x-1, y+1):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
    else:
        if chess_state[x + 1][y] == "xx":  # White move ahead 1 step
            pos = (x+1, y)
            if realState == True:
                if checkAcceptMove(chess_state, turn,x, y, x+1,y):
                    moveList.append(pos)
            else:
                moveList.append(pos)

            if x == 1 and chess_state[x + 2][y] == "xx":  # White move ahead 2 step
                pos = (x+2, y)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x+2, y):
                        moveList.append(pos)
                else:
                    moveList.append(pos)

        if y - 1 >= 0:
            if chess_state[x + 1][y - 1][0] == 'w':  # Check enemy chess
                pos = (x + 1, y -1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x+1, y-1):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
        if y + 1 <= 7:
            if chess_state[x + 1][y + 1][0] == 'w':
                pos = (x + 1, y + 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x+1, y+1):
                        moveList.append(pos)
                else:
                    moveList.append(pos)

    
    return moveList

def moveListRook(x, y, turn, chess_state, realState):
    direction = ((-1, 0), (1, 0), (0, -1), (0, 1))
    moveList=[]
    if turn == 'w':
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        for i in range(1, 8):
            newX = x + d[0] * i
            newY = y + d[1] * i
            if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the chess_state
                if chess_state[newX][newY] == "xx":
                    pos = (newX, newY)
                    # nếu bàn cờ là thật => check nước đi hợp lệ
                    #nếu bàn cờ là ảo (tức đã đi 1 nước ảo để check xem nước đó có hợp lệ ko) => ko cần check nước hợp lệ
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:
                        moveList.append(pos)

                elif chess_state[newX][newY][0] == enemyColor:
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:
                        moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the chess_state
                break
    # if realState== True:
    #     if KingInAttack(chess_state, wturn) == True:
    #         return acceptMove(chess_state, wturn, x, y, moveList)

    return moveList

def moveListBishop(x, y, turn, chess_state, realState):
    direction = ((-1, 1), (1, -1), (1, 1), (-1, -1))
    moveList=[]
    if turn == 'w':
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        for i in range(1, 8):
            newX = x + d[0] * i
            newY = y + d[1] * i

            if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the chess_state
                if chess_state[newX][newY] == "xx":
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:
                        moveList.append(pos)

                elif chess_state[newX][newY][0] == enemyColor:
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:
                        moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the chess_state
                break
    return moveList

def moveListQueen(x, y, turn, chess_state, realState):
    moveList=[]
    move1 = moveListRook(x, y, turn, chess_state, realState)
    move2 = moveListBishop(x, y,turn, chess_state, realState)
    if move1:
        for pos in move1:
            moveList.append(pos)
    if move2:
        for pos in move2:
            moveList.append(pos)
    return moveList

def moveListKing(x, y, turn, chess_state, realState):
    moveList = []
    direction = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
    if turn == 'w':
        enemyColor = "b"
    else:
        enemyColor = "w"

    if realState == True:
        if (turn == 'w'):
            if main.castle["wKR"] == True and currentCastleRightKing(chess_state, turn, 5) == True:
                moveList.append((7,6))
            if main.castle["wQR"] == True and currentCastleRightKing(chess_state, turn, 1) == True:
                moveList.append((7,2))
        else:
            if main.castle["bKR"] == True and currentCastleRightKing(chess_state, turn, 5) == True:
                moveList.append((0,6))
            if main.castle["bQR"] == True and currentCastleRightKing(chess_state, turn, 1) == True:
                moveList.append((0,2))
    for i in range(8):
        newX = x + direction[i][0]
        newY = y + direction[i][1]
        if 0 <= newX < 8 and 0 <= newY < 8:
            if chess_state[newX][newY] == "xx":
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
            elif chess_state[newX][newY][0] == enemyColor:
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
    return moveList

def moveListKnight(x, y, turn, chess_state, realState):
    moveList = []
    direction = ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
    if turn == 'w':
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        newX = x + d[0]
        newY = y + d[1]
        if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the chess_state
            if chess_state[newX][newY] == "xx":
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
            elif chess_state[newX][newY][0] == enemyColor:
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:
                    moveList.append(pos)
    return moveList

def squareInAttack(x,y,turn,chess_state): 
    for piece in ["Bishop","Knight","Rook","Queen","King","Pawn"]:
        func=globals()["moveList"+piece]
        moveList=func(x,y,turn,chess_state,False)
        for pos in moveList:
            if piece in chess_state[pos[0]][pos[1]]:
                return True
    return False

def findPiece(chess_state, piece):
    for i in range(0,8):
        for j in range(0,8):
            if chess_state[i][j] == piece:
                return (i,j)
    return None

def KingInAttack(chess_state,turn):
    pos = findPiece(chess_state, turn+"King")
    if pos==None:
        return True
    x = pos[0]
    y = pos[1]
    if squareInAttack(x,y,turn,chess_state) == True:
        return turn+"King"
    return False

def checkNoMove(chess_state, turn):
    #return True if turn have no move
    moveList = []
    for j in range(0,8):
        for i in range(0,8):
            piece = chess_state[i][j]
            if piece == "xx":
                continue
            else:
                if piece[0]==turn:
                    func=globals()['moveList'+piece[1:]]
                    if len(func(i, j, turn, chess_state, True)) != 0:
                        return False
                    else:
                        moveList=moveList+func(i, j, turn, chess_state, True)
    if len(moveList)!=0:
        return False
    return True

def checkMate(chess_state, turn):
    return checkNoMove(chess_state,turn) and KingInAttack(chess_state,turn)

def currentCastleRightKing(chess_state, turn, c):
    # if wturn == True => white move => row = 7 else row = 0
    if turn == 'w':
        r = 7
    else:
        r = 0
    # if king under attack => not castling = > false
    if KingInAttack(chess_state, turn) == (turn+"King"):
        return False
    # check square from left rook to King, if square under attack or any piece on the square => return false
    if chess_state[r][c] == "xx" \
        and chess_state[r][c+1] == "xx"\
            and chess_state[r][c+2] == "xx" \
            and "Rook" in chess_state[r][c-1] :
                for i in range(c,c+3):
                    if squareInAttack(r,c,turn,chess_state) == True:
                        return False
                return True
    # check square from right Rook to King 
    if chess_state[r][c] == "xx" and chess_state[r][c+1] == "xx" and "Rook" in chess_state[r][c+2]:
        for i in range(c,c+2):
            if squareInAttack(r,c, turn, chess_state) == True:
                return False
        return True
    return False

def switchTurn(turn):
    if turn == 'w':
        return 'b'
    else:
        return 'w'
    
def reset_Board(chess_state):
    chess_state = [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                    ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                    ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
                    ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"]
                    ]
    main.castle = {"wKR": True, "wQR": True, "bKR": True, "bQR": True}                      
    return chess_state

def check_castle(chess_state):
    if chess_state[0][4] == "bKing":
        if chess_state[0][0] == "bRook":
            main.castle["bQR"] = True
        if chess_state[0][7] =="bRook":
            main.castle["bKR"] = True
    if chess_state[7][4] == "wKing":
        if chess_state[7][0] == "wRook":
            main.castle["wQR"] = True
        if chess_state[7][7] == "wRook":
            main.castle["wKR"] = True
    return main.castle

    
