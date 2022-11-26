import os
import pygame
import UI

HEIGHT=800
WIDTH=800
SCALE = HEIGHT / 8
pieceImages = {} #dictionary
turn = True
catle = {"wKR": True, "wQR": True, "bKR": True, "bQR": True}


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
        moveList = checkPawnMove(oldX, oldY, turn, chess_state)

    elif "Rook" in piece:
        moveList = checkRookMove(oldX, oldY, turn, chess_state)

    elif "Bishop" in piece:
        moveList = checkBishopMove(oldX, oldY, turn, chess_state)

    elif "Queen" in piece:
        moveList = checkQueenMove(oldX, oldY, turn, chess_state)
        
    elif "King" in piece:
        moveList = checkKingMove(oldX, oldY, turn, chess_state)

    elif "Knight" in piece:
        moveList = checkKnightMove(oldX, oldY, turn, chess_state)

    return moveList


def moveChess(chess_state, click, turn,screen):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]
    moveList = checkMove(chess_state, click, turn)
    print(f"Available move: (x,y){moveList} ")
    validMove = False
    for pos in moveList:
        if (newX, newY) == pos:
            validMove = True
            break

    if not validMove:
        return False

    # Check ăn chess khác màu
    if chess_state[newY][newX][0] == chess_state[oldY][oldX][0]:
        return False
    checkPawnPromotion(chess_state, click, screen)
    # elif chess_state[oldY][oldX] != "xx":
    #     chess_state[newY][newX] = chess_state[oldY][oldX]
    #     chess_state[oldY][oldX] = "xx"
    return True

def update(chess_state, click):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]
    # Cập nhật lại bàn cờ
    
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
    if "King" in chess_state[oldY][oldX]:
        if newX - oldX == 2:
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
    chess_state[newY][newX] = chess_state[oldY][oldX]
    chess_state[oldY][oldX] = "xx"



#Quang

def promoteChoice(screen, sideColor):
    x=40
    y=300
    queen_btn=UI.Button(x, y, pygame.image.load("res/"+sideColor+"Queen.png"))
    rook_btn=UI.Button(x+200, y, pygame.image.load("res/"+sideColor+"Rook.png"))
    knight_btn=UI.Button(x+400,y, pygame.image.load("res/"+sideColor+"Knight.png"))
    bishop_btn=UI.Button(x+600, y, pygame.image.load("res/"+sideColor+"Bishop.png"))
    pause= True
    piece =''
    while pause:
        queen_btn.draw(screen)
        bishop_btn.draw(screen)
        rook_btn.draw(screen)
        knight_btn.draw(screen) 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:                    
                if queen_btn.draw(screen):
                    piece= sideColor+ "Queen"
                    pause = False
                    return piece
                elif rook_btn.draw(screen):
                    piece =sideColor+"Rook"
                    pause = False
                    return piece
                elif knight_btn.draw(screen):
                    piece =sideColor+"Knight"
                    pause = False
                    return piece
                elif bishop_btn.draw(screen):
                    piece =sideColor+"Bishop"
                    pause = False  
                    return piece       
        pygame.display.update()
                             

def checkPawnPromotion(chess_state, click, screen):
    oldX = click[0][0] 
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]
    if chess_state[0][newX] == 'wPawn':
        chess_state[newY][newX] = chess_state[oldY][oldX]
        chess_state[newY][newX] = promoteChoice(screen,'w')
    if chess_state[7][newX]== 'bPawn':
        chess_state[newY][newX] = chess_state[oldY][oldX]
        chess_state[newY][newX] = promoteChoice(screen,'b')


#End

def checkPawnMove(x, y, turn, chess_state):
    moveList=[]
    if turn == True:
        if chess_state[y - 1][x] == "xx":  # White move ahead 1 step
            pos = (x, y - 1)
            moveList.append(pos)

            if y == 6 and chess_state[y - 2][x] == "xx":  # White move ahead 2 step
                pos = (x, y - 2)
                moveList.append(pos)

        if x - 1 >= 0:
            if chess_state[y - 1][x - 1][0] == 'b':  # Check enemy chess
                pos = (x - 1, y - 1)
                moveList.append(pos)
        if x + 1 <= 7:
            if chess_state[y - 1][x + 1][0] == 'b':
                pos = (x + 1, y - 1)
                moveList.append(pos)
    else:
        if chess_state[y + 1][x] == "xx":  # White move ahead 1 step
            pos = (x, y + 1)
            moveList.append(pos)

            if y == 1 and chess_state[y + 2][x] == "xx":  # White move ahead 2 step
                pos = (x, y + 2)
                moveList.append(pos)

        if x - 1 >= 0:
            if chess_state[y + 1][x - 1][0] == 'w':  # Check enemy chess
                pos = (x - 1, y + 1)
                moveList.append(pos)
        if x + 1 <= 7:
            if chess_state[y + 1][x + 1][0] == 'w':
                pos = (x + 1, y + 1)
                moveList.append(pos)
    return moveList


def checkRookMove(x, y, turn, chess_state):
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
                    moveList.append(pos)

                elif chess_state[newY][newX][0] == enemyColor:
                    pos = (newX, newY)
                    moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the board
                break
    return moveList


def checkBishopMove(x, y, turn, chess_state):
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
                    moveList.append(pos)

                elif chess_state[newY][newX][0] == enemyColor:
                    pos = (newX, newY)
                    moveList.append(pos)
                    break  # Can not move piece behind chess

                else:  # frendly chess
                    break
            else:  # Out of the board
                break
    return moveList


def checkQueenMove(x, y, turn, chess_state):
    moveList=[]
    if checkRookMove(x, y, turn, chess_state):
        for pos in checkRookMove(x, y, turn, chess_state):
            moveList.append(pos)
    if checkBishopMove(x, y,turn, chess_state):
        for pos in checkBishopMove(x, y, turn, chess_state):
            moveList.append(pos)
    # print(moveList)
    return moveList

def checkKingMove(x, y, turn, board):
    moveList = []
    direction = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
    if turn == True:
        enemyColor = "b"
    else:
        enemyColor = "w"
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
                moveList.append(pos)
            elif board[newY][newX][0] == enemyColor:
                pos = (newX, newY)
                moveList.append(pos)
    return moveList

def checkKnightMove(x, y, turn, board):
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
                moveList.append(pos)
            elif board[newY][newX][0] == enemyColor:
                pos = (newX, newY)
                moveList.append(pos)
    return moveList

def currentCastleRightKing(chess_state, turn, c):
    if turn == True:
        r = 7
    else:
        r = 0
    if chess_state[r][c] == "xx" and chess_state[r][c+1] == "xx" and chess_state[r][c+2] == "xx" and "Rook" in chess_state[r][c-1] :
        return True
    if chess_state[r][c] == "xx" and chess_state[r][c+1] == "xx" and "Rook" in chess_state[r][c+2]:
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

def highlightMove(screen,click, chess_state, turn):
        pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(click[0][0] * SCALE, click[0][1] * SCALE, SCALE, SCALE))
        moveList=checkMove(chess_state,click,turn)
        for i in moveList:
            pygame.draw.rect(screen,pygame.Color(198,226,255),pygame.Rect(i[0]*SCALE+1,i[1]*SCALE+1, SCALE-2 ,SCALE - 2))


# vẽ animation
def animation(click, screen, chess_state, clock):
    
    dR = click[1][1] - click[0][1]
    dC = click[1][0] - click[0][0]
    fps = 3
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
    selected = () #tuples
    click = []
    
    
    loadImage(pieceImages)
    running = True

    while running:
        draws(screen,chess_state,click,turn)
        #draws(screen,selected)
        drawPieces(screen, pieceImages, chess_state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                location = pygame.mouse.get_pos()
                x = int(location[0] / SCALE)
                y = int(location[1] / SCALE)
                print((y,x))
                print(chess_state[y][x])
                print(currentCastleRightKing(chess_state, turn, 1))
                if selected == (x, y):
                    selected = ()
                    click = []
                else:
                    selected = (x, y)
                    click.append(selected)
                    if len(click) == 2:
                        if moveChess(chess_state, click, turn,screen):
                            turn = not turn
                            animation(click, screen, chess_state, clock)
                            
                            update(chess_state, click)
                        #quang
                        checkPawnPromotion(chess_state, click, screen)
                        #end
                        click = []
                        selected = ()

                    elif len(click) == 1 and turn_choose(chess_state, (click[0][0], click[0][1]), turn) == False:
                        selected = ()
                        click = []
        clock.tick(15)
        pygame.display.flip()


if __name__ == "__main__":
    print(os.getcwd())
    main()

