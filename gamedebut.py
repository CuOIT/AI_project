import pygame
import copy

HEIGHT = 800
WIDTH = 800
SCALE = HEIGHT / 8
pieceImages = {} #dictionary
turn = True
catle = {"wKR": True, "wQR": True, "bKR": True, "bQR": True}

globalCheck = False
globalMate = False
list_chess_state = []

colors = [pygame.Color("pink"), pygame.Color("white")]
def loadImage(pieceImages):
    pieces = ["bBishop", "bKing", "bKnight", "bPawn", "bQueen", "bRook", "wBishop", "wKing", "wPawn", "wQueen", "wRook",
           "wKnight"]
    for i in pieces:
        pieceImages[i] = pygame.transform.scale(pygame.image.load("res/" + i + ".png"), (SCALE-10, SCALE-10))

def draws(screen,chess_state,click,turn):#this function is to draw board and hightlight
    colors = [pygame.Color("pink"), pygame.Color("white")]
    for row in range(0, 8):
        for col in range(0, 8):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col * SCALE, row * SCALE, SCALE, SCALE))     
            if len(click) >= 1:
                highlightMove(screen, click, chess_state, turn)

def drawPieces(screen, pieceImages, chess_state):
    for c in range(0, 8):
        for l in range(0, 8):
            if chess_state[l][c] == "xx":
                continue
            else:
                screen.blit(pieceImages[chess_state[l][c]], pygame.Rect(c * SCALE+5, l * SCALE+5, SCALE, SCALE))

def checkMove(chess_state,click,turn):
    oldX = click[0][0]
    oldY = click[0][1]
    #newX = click[1][0]
    #newY = click[1][1]
    piece = chess_state[oldY][oldX]
    moveList = []  # List of valid moves
    validMove = False

    
    if "Pawn" in piece:
        moveList = checkPawnMove(oldX, oldY, turn, chess_state, True)

    elif "Rook" in piece:
        moveList = checkRookMove(oldX, oldY, turn, chess_state, True)

    elif "Bishop" in piece:
        moveList = checkBishopMove(oldX, oldY, turn, chess_state, True)

    elif "Queen" in piece:
        moveList = checkQueenMove(oldX, oldY, turn, chess_state, True)
        
    elif "King" in piece:
        moveList = checkKingMove(oldX, oldY, turn, chess_state, True)

    elif "Knight" in piece:
        moveList = checkKnightMove(oldX, oldY, turn, chess_state, True)

    return moveList

def moveChess(chess_state, click, turn):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]

    moveList=checkMove(chess_state,click,turn)

    validMove = False
    
    # global list_chess_state
    # list_chess_state.append(chess_state.copy())  
    
    
    for pos in moveList:
        if (newX, newY) == pos:
            validMove = True
            break
        # moveList.append(pos)
    if not validMove:
        return False

    # Check ăn chess khác màu
    if chess_state[newY][newX][0] == chess_state[oldY][oldX][0]:
        return False
    return True

def reset(chess_state):
    chess_state = [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                   ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
                   ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"]
                   ]
    return chess_state #tra ban co ve trang thai ban dau

def update(chess_state, click):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]
    # Cập nhật lại bàn cờ
    chess = copy.deepcopy(chess_state) #copy trang thai ban co
    
    #neu xe di chuyen
    if "Rook" in chess_state[oldY][oldX]:
        if oldY == 7 and oldX == 0:
            catle["wQR"] = False
        elif oldY == 7 and oldX == 7:
            catle["wKR"] = False
        elif oldY == 0 and oldX == 0:
            catle["bQR"] = False
        elif oldX == 7 and oldY == 0:
            catle["bKR"] = False
       
    # neu nhap thanh thi cap nhat lai con xe
    elif "King" in chess_state[oldY][oldX]:
            #neu tuong di chuyen
        if newX - oldX == 1 or oldX - newX == 1 or newY - oldY == 1 or oldY - newY == 1:
            if oldY == 7 and oldX == 4: 
                catle["wKR"] = False
                catle["wQR"] = False
            elif oldY == 0 and oldX == 4:
                catle["bQR"] = False
                catle["bKR"] = False
        
        elif newX - oldX == 2:
            if chess_state[oldY][oldX] == "wKing":
                catle["wKR"] = False
                catle["wQR"] = False
            else:
                catle["bQR"] = False
                catle["bKR"] = False
                
            chess_state[oldY][newX-1] = chess_state[oldY][newX+1] 
            chess_state[oldY][newX+1] = "xx"
            
            if chess_state[oldY][oldX] == "wKing":
                catle["wKR"] = False
                catle["wQR"] = False
            else:
                catle["bQR"] = False
                catle["bKR"] = False
                
        elif oldX - newX == 2:
            if chess_state[oldY][oldX] == "wKing":
                catle["wKR"] = False
                catle["wQR"] = False
            else:
                catle["bQR"] = False
                catle["bKR"] = False
            chess_state[oldY][newX+1] = chess_state[oldY][newX-2]
            chess_state[oldY][newX-2] = "xx"
            
    global list_chess_state
    list_chess_state.append(chess) #day toan bo trang thai ban co vao stack
    
    chess_state[newY][newX] = chess_state[oldY][oldX]
    chess_state[oldY][oldX] = "xx"
 
def undoMove(chess_state):
    global list_chess_state
    if len(list_chess_state) != 0:
        chess_state = list_chess_state.pop() #trang thai ban co duoc lay ra tu stack
    return chess_state
    
def checkPawnMove(x, y, turn, chess_state, realState):
    moveList=[]
    if turn == True:
        if chess_state[y - 1][x] == "xx":  # White move ahead 1 step
            pos = (x, y - 1)
            if realState == True:
                if checkAcceptMove(chess_state, turn,x, y, x, y-1):
                    moveList.append(pos)
            else:        
                moveList.append(pos)

            if y == 6 and chess_state[y - 2][x] == "xx":  # White move ahead 2 step
                pos = (x, y - 2)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x, y-2):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)

        if x - 1 >= 0:
            if chess_state[y - 1][x - 1][0] == 'b':  # Check enemy chess
                pos = (x - 1, y - 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x-1, y-1):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
        if x + 1 <= 7:
            if chess_state[y - 1][x + 1][0] == 'b':
                pos = (x + 1, y - 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x+1, y-1):
                        moveList.append(pos)
                else:            
                    moveList.append(pos)
    else:
        if chess_state[y + 1][x] == "xx":  # White move ahead 1 step
            pos = (x, y + 1)
            if realState == True:
                if checkAcceptMove(chess_state, turn,x, y, x, y+1):
                    moveList.append(pos)
            else:        
                moveList.append(pos)

            if y == 1 and chess_state[y + 2][x] == "xx":  # White move ahead 2 step
                pos = (x, y + 2)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x, y+2):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)

        if x - 1 >= 0:
            if chess_state[y + 1][x - 1][0] == 'w':  # Check enemy chess
                pos = (x - 1, y + 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x-1, y+1):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
        if x + 1 <= 7:
            if chess_state[y + 1][x + 1][0] == 'w':
                pos = (x + 1, y + 1)
                if realState == True:
                    if checkAcceptMove(chess_state, turn,x, y, x, y-1):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)

    # # nếu vua đang bị chiếu
    # if realState == True:
    #     if KingInAttack(chess_state, turn) == True:
    #         return acceptMove(chess_state, turn, x, y, moveList)
    
    return moveList


def checkRookMove(x, y, turn, chess_state, realState):
    global globalCheck
    direction = ((-1, 0), (1, 0), (0, -1), (0, 1))
    moveList=[]
    if turn == True:
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        for i in range(1, 8):
            newX = x + d[0] * i
            newY = y + d[1] * i

            if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the board
                if chess_state[newY][newX] == "xx":
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:        
                        moveList.append(pos)

                elif chess_state[newY][newX][0] == enemyColor:
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:        
                        moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the board
                break
    # if realState== True:        
    #     if KingInAttack(chess_state, turn) == True:
    #         return acceptMove(chess_state, turn, x, y, moveList)        
            
    return moveList

def checkAcceptMove(chess_state, turn, x, y ,newX, newY):
    temp = chess_state.copy() #copy bàn cờ
    piece1 = chess_state[y][x] # lưu lại con cờ ở vị trí sẽ đi
    piece2 = temp[newY][newX] #lưu lại con cờ ở vị trí con cờ x,y sẽ đi vào
        
    temp[newY][newX] = piece1 # cập nhật bàn cờ ảo     
    temp[y][x] = "xx"
    
    if KingInAttack(temp, turn) == True:
        temp[newY][newX] = piece2 # cập nhật lại bàn cờ thật
        temp[y][x] = piece1
        return False
    
    temp[newY][newX] = piece2 # cập nhật lại bàn cờ thật
    temp[y][x] = piece1
    return True
    

def acceptMove(chess_state, turn, x, y, moveList):
    temp = chess_state.copy() #copy bàn cờ
    piece1 = chess_state[y][x] # lưu lại con cờ ở vị trí sẽ đi
    
    acceptMove = []
    for pos in moveList: #duyệt list di chuyển của con cờ tại x,y
           
        newX = pos[1]
        newY = pos[0]
        
        piece2 = temp[newX][newY] #lưu lại con cờ ở vị trí con cờ x,y sẽ đi vào
        temp[newX][newY] = piece1 # cập nhật bàn cờ ảo
               
        temp[y][x] = "xx"
        
        if KingInAttack(temp, turn) == False: # check KingInAttack trong bàn cờ ảo
            acceptMove.append(pos)
            
        temp[newX][newY] = piece2 # cập nhật lại bàn cờ thật
        temp[y][x] = piece1
   
    return acceptMove    
def checkBishopMove(x, y, turn, chess_state, realState):
    direction = ((-1, 1), (1, -1), (1, 1), (-1, -1))
    moveList=[]
    if turn == True:
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        for i in range(1, 8):
            newX = x + d[0] * i
            newY = y + d[1] * i

            if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the board
                if chess_state[newY][newX] == "xx":
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:        
                        moveList.append(pos)

                elif chess_state[newY][newX][0] == enemyColor:
                    pos = (newX, newY)
                    if realState == True:
                        if checkAcceptMove(chess_state, turn,x, y, newX, newY):
                            moveList.append(pos)
                    else:        
                        moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the board
                break
            
    # if realState == True:        
    #     if KingInAttack(chess_state, turn) == True:
    #         return acceptMove(chess_state, turn, x, y, moveList)         
    return moveList


def checkQueenMove(x, y, turn, chess_state, realState):
    moveList=[]
    move1 = checkRookMove(x, y, turn, chess_state, realState)
    move2 = checkBishopMove(x, y,turn, chess_state, realState)
    if move1:
        for pos in move1:
            moveList.append(pos)
    if move2:
        for pos in move2:
            moveList.append(pos)
  
    return moveList

def checkKingMove(x, y, turn, board, realState):
    moveList = []
    direction = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
    if turn == True:
        enemyColor = "b"
    else:
        enemyColor = "w"
        
    if realState == True:
        if (turn == True):
            if catle["wKR"] == True and currentCastleRightKing(board, True, 5) == True:
                moveList.append((6,7))
            if catle["wQR"] == True and currentCastleRightKing(board, True, 1) == True:
                moveList.append((2,7))
        else:
            if catle["bKR"] == True and currentCastleRightKing(board, False, 5) == True:  
                moveList.append((6,0))
            if catle["bQR"] == True and currentCastleRightKing(board, False, 1) == True:
                moveList.append((2,0))
    for i in range(8):
        newX = x + direction[i][0]
        newY = y + direction[i][1]
        if 0 <= newX < 8 and 0 <= newY < 8:
            if board[newY][newX] == "xx":
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(board, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
            elif board[newY][newX][0] == enemyColor:
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(board, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
    
    # if realState == True:
    #     if KingInAttack(board, turn):
    #         return acceptMove(board, turn, x, y, moveList)             
    return moveList

def checkKnightMove(x, y, turn, board, realState):
    moveList = []
    direction = ((-2, -1), (-2, 1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
    if turn == True:
        enemyColor = "b"
    else:
        enemyColor = "w"

    for d in direction:
        newX = x + d[0]
        newY = y + d[1]
        if 0 <= newX < 8 and 0 <= newY < 8:  # Position on the board
            if board[newY][newX] == "xx":
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(board, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
            elif board[newY][newX][0] == enemyColor:
                pos = (newX, newY)
                if realState == True:
                    if checkAcceptMove(board, turn,x, y, newX, newY):
                        moveList.append(pos)
                else:        
                    moveList.append(pos)
    # if realState == True:        
    #     if KingInAttack(board, turn) == True:
    #         return acceptMove(board, turn, x, y, moveList)   
    return moveList

def pieceInMove(piece, moveList, chess_state):
    for pos in moveList:
        x = pos[0]
        y = pos[1]
        if piece in chess_state[y][x]:
            return True
    return False    

def squareInAttack(x,y,turn,chess_state):
    moveList = checkBishopMove(x,y,turn, chess_state, False)
    # print(moveList)
    if pieceInMove("Bishop", moveList, chess_state) == True:
        return True
    moveList = checkKnightMove(x,y,turn, chess_state, False)
    # print(moveList)
    if pieceInMove("Knight", moveList, chess_state) == True:
        return True
    
    moveList = checkRookMove(x,y,turn,chess_state, False)
    # print(moveList)
    if pieceInMove("Rook", moveList, chess_state) == True:
        return True
    
    moveList = checkQueenMove(x,y,turn,chess_state, False)
    # print(moveList)
    if pieceInMove("Queen", moveList, chess_state) == True:
        return True
    
    moveList = checkPawnMove(x,y,turn,chess_state, False)
    # print(moveList)
    if pieceInMove("Pawn", moveList, chess_state) == True:
        return True
    
    moveList = checkKingMove(x,y,turn,chess_state,False)
    if pieceInMove("King", moveList, chess_state) == True:
        return True
    
    return False

def findPiece(chess_state, piece):
    for i in range(0,8):
        for j in range(0,8):
            if chess_state[i][j] == piece:
                return (i,j)

def KingInAttack(chess_state, turn):
    if turn == True:
        king = "wKing"
    else:
        king = "bKing"
    pos = findPiece(chess_state, king)
    x = pos[0]
    y = pos[1]
    if squareInAttack(y,x,turn,chess_state) == True:
        return True
    return False
         
def getAllMove(chess_state, turn):
    moveList = []
    if turn == True:
        color = "w"
    else:
        color = "b"
    for j in range(0,8):
        for i in range(0,8):
            piece = chess_state[j][i]
            if piece == "xx":
                continue
            elif "Pawn" in piece and color in piece:
                moveList = moveList + checkPawnMove(i, j, turn, chess_state, True)

            elif "Rook" in piece and color in piece:
                moveList =  moveList + checkRookMove(i, j, turn, chess_state, True)

            elif "Bishop" in piece and color in piece:
                moveList =  moveList + checkBishopMove(i, j, turn, chess_state, True)

            elif "Queen" in piece and color in piece:
                moveList =  moveList + checkQueenMove(i, j, turn, chess_state, True)
                
            elif "King" in piece and color in piece:
                moveList =  moveList + checkKingMove(i, j, turn, chess_state, True)

            elif "Knight" in piece and color in piece:
                moveList = moveList +  checkKnightMove(i, j, turn, chess_state, True)        
    return moveList

def checkMate(chess_state, turn):
    moveList = getAllMove(chess_state, turn)
    if len(moveList) <= 0:
        return True
    return False
def currentCastleRightKing(chess_state, turn, c):
    if turn == True:
        r = 7
    else:
        r = 0
    if KingInAttack(chess_state, turn) == True:
        return False
    if chess_state[r][c] == "xx" \
        and chess_state[r][c+1] == "xx"\
            and chess_state[r][c+2] == "xx" \
            and "Rook" in chess_state[r][c-1] :
                for i in range(c,c+3):
                    if squareInAttack(i,r,turn,chess_state) == True:
                        return False
                return True
    if chess_state[r][c] == "xx" and chess_state[r][c+1] == "xx" and "Rook" in chess_state[r][c+2]:
        for i in range(c,c+2):
            if squareInAttack(i,r, turn, chess_state) == True:
                return False
        return True
    return False

def turn_choose(chess_state, selected, turn):
    if turn == True:
        if chess_state[selected[1]][selected[0]][0] == "w":
            return True
        else:
            return False
    elif turn == False:
        if chess_state[selected[1]][selected[0]][0] == "b":
            return True
        else:
            return False
    return False

def drawText(screen, text):
    font = pygame.font.SysFont("Time new roman", 60, True, False)
    textObject = font.render(text, 0, pygame.Color('Red'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color('Red'))
    screen.blit(textObject, textLocation.move(2, 2))


def highlightMove(screen,click, chess_state, turn):
        pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(click[0][0] * SCALE, click[0][1] * SCALE, SCALE, SCALE))
        moveList=checkMove(chess_state,click,turn)
        for i in moveList:
            pygame.draw.rect(screen,pygame.Color(198,226,255),pygame.Rect(i[0]*SCALE+1,i[1]*SCALE+1, SCALE-2 ,SCALE - 2))


# vẽ animation
def animation(click, screen, chess_state, clock):
    
    dR = click[1][1] - click[0][1]
    dC = click[1][0] - click[0][0]
    fps = 1
    fcount = (abs(dR) + abs(dC)) * fps
    for frame in range(fcount + 1):
        r = click[0][1] + dR*frame/fcount
        c = click[0][0] + dC*frame/fcount 
        draws(screen,chess_state, click, turn)
        drawPieces(screen, pieceImages, chess_state)

        
        colore = colors[(click[1][1] + click[1][0]) % 2]
     
        end = pygame.Rect(click[1][0] * SCALE, click[1][1] * SCALE, SCALE,SCALE)
        pygame.draw.rect(screen,colore,end)
       
        
        if chess_state[click[0][1]][click[0][0]] != "xx": #xóa piece on start_node
            temp = chess_state[click[0][1]][click[0][0]]
            chess_state[click[0][1]][click[0][0]] = "xx" 
        
        
        if chess_state[click[1][1]][click[1][0]] != "xx":
            screen.blit(pieceImages[chess_state[click[1][1]][click[1][0]]], end) #vẽ end_node là "xx"
            
              
        screen.blit(pieceImages[temp], pygame.Rect(c*SCALE, r*SCALE, SCALE, SCALE)) # vẽ quân cờ di chuyển
        pygame.display.flip()
        clock.tick(60)    
    chess_state[click[0][1]][click[0][0]] = temp # trả piece về lại start_node để chạy tiếp update bàn cờ   

def main():
    global turn
    global pieceImages
    global globalCheck
    global globalMate
    global list_chess_state
    pygame.init()
    pygame.display.set_caption("Game debut")
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    clock = pygame.time.Clock()

    #node = pygame.transform.scale(pygame.image.load("res/node_xanh.png"), (100, 100))

    chess_state = [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                   ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
                   ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"]
                   ]
    # list_chess_state.append(chess_state)
    selected = () #tuples
    click = []
    
    
    loadImage(pieceImages)
    running = True
    while running:
            
                
        draws(screen,chess_state,click,turn)
       
        drawPieces(screen, pieceImages, chess_state)
        if globalMate == True:
            if turn == True:
                drawText(screen, "Black win")
            else:
                drawText(screen, "White win")
        else:
            if globalCheck == True:
                drawText(screen, "Check rui hoho")
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                location = pygame.mouse.get_pos()
                x = int(location[0] / SCALE)
                y = int(location[1] / SCALE)
                

                if selected == (x, y):
                    selected = ()
                    click = []
                else:
                    selected = (x, y)
                    click.append(selected)
                    if len(click) == 2:
                        if moveChess(chess_state, click, turn):
                            
                            turn = not turn

                            animation(click, screen, chess_state, clock) 
                            update(chess_state, click)
                            
                            globalCheck = KingInAttack(chess_state, turn)
                            globalMate = checkMate(chess_state, turn)
                            
                        click = []
                        selected = ()

                    elif len(click) == 1 and turn_choose(chess_state, (click[0][0], click[0][1]), turn) == False:
                        selected = ()
                        click = []
            elif event.type == pygame.KEYDOWN:
                global catle
                if event.key == pygame.K_LCTRL: #bam ctrl trai de goi ham undo
                    chess_state = undoMove(chess_state) 
                    turn = not turn
                    
                    if chess_state == [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                                    ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
                                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                                    ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                                    ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
                                    ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"]
                                    ]:
                        turn = True
                    if chess_state[0][4] == "bKing":
                        if chess_state[0][0] == "bRook":
                            catle["bQR"] = True
                        if chess_state[0][7] =="bRook":
                            catle["bKR"] = True
                    if chess_state[7][4] == "wKing":
                        if chess_state[7][0] == "wRook":
                            catle["wQR"] = True
                        if chess_state[7][7] == "wRook":
                            catle["wKR"] = True
                     
                elif event.key == pygame.K_r: #bam r de reset ban co
                    global list_chess_state
                    while(len(list_chess_state) != 0):
                        list_chess_state.pop()
                    drawText(screen, "You're just restart this game!")
                    chess_state = reset(chess_state) 
                    turn = True
                    catle = {"wKR": True, "wQR": True, "bKR": True, "bQR": True}
        clock.tick(15)
        pygame.display.flip()


if __name__ == "__main__":
    main()
