import pygame


def loadImage(chess):
    img = ["bBishop", "bKing", "bKnight", "bPawn", "bQueen", "bRook", "wBishop", "wKing", "wPawn", "wQueen", "wRook",
           "wKnight"]

    for i in img:
        chess[i] = pygame.transform.scale(pygame.image.load("res/" + i + ".png"), (100, 100))


def draws(scr):
    colors = [pygame.Color("pink"), pygame.Color("white")]
    for r in range(0, 8):
        for c in range(0, 8):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(scr, color, pygame.Rect(c * 100, r * 100, 100, 100))


def drawChess(scr, chess, chess_state):
    for c in range(0, 8):
        for l in range(0, 8):
            if chess_state[l][c] == "xx":
                continue
            else:
                scr.blit(chess[chess_state[l][c]], pygame.Rect(c * 100, l * 100, 100, 100))
    # scr.blit(image, pygame.Rect(x*100, y*100, 100, 100))


def moveChess(chess_state, click, turn):
    oldX = click[0][0]
    oldY = click[0][1]
    newX = click[1][0]
    newY = click[1][1]

    piece = chess_state[oldY][oldX]
    print(piece)
    moveList = []  # List of valid moves
    validMove = False

    if "Pawn" in piece:
        moveList = checkPawnMove(oldX, oldY, moveList, turn, chess_state)

    elif "Rook" in piece:
        moveList = checkRookMove(oldX, oldY, moveList, turn, chess_state)

    elif "Bishop" in piece:
        moveList = checkBishopMove(oldX, oldY, moveList, turn, chess_state)

    elif "Queen" in piece:
        moveList = checkQueenMove(oldX, oldY, moveList, turn, chess_state)

    for pos in moveList:
        if (newX, newY) == pos:
            validMove = True
            break

    if not validMove:
        return False

    # Check ăn chess khác màu
    if chess_state[newY][newX][0] == chess_state[oldY][oldX][0]:
        return False

    # Cập nhật lại bàn cờ
    chess_state[newY][newX] = chess_state[oldY][oldX]
    chess_state[oldY][oldX] = "xx"

    # elif chess_state[oldY][oldX] != "xx":
    #     chess_state[newY][newX] = chess_state[oldY][oldX]
    #     chess_state[oldY][oldX] = "xx"
    return True


def checkPawnMove(x, y, moveList, turn, chess_state):
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


def checkRookMove(x, y, moveList, turn, chess_state):
    direction = ((-1, 0), (1, 0), (0, -1), (0, 1))

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


def checkBishopMove(x, y, moveList, turn, chess_state):
    direction = ((-1, 1), (1, -1), (1, 1), (-1, -1))

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


def checkQueenMove(x, y, moveList, turn, chess_state):
    moveList.append(checkRookMove(x, y, moveList, turn, chess_state))
    moveList.append(checkBishopMove(x, y, moveList, turn, chess_state))

    return moveList


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


def main():
    pygame.init()
    pygame.display.set_caption("Game debut")
    screen = pygame.display.set_mode((800, 800))
    # screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()

    node = pygame.transform.scale(pygame.image.load("res/node_xanh.png"), (100, 100))

    chess_state = [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                   ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "wRook", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
                   ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"]
                   ]
    selected = ()
    click = []
    color = {}
    loadImage(color)
    turn = True
    running = True
    while running:
        draws(screen)
        drawChess(screen, color, chess_state)
        if selected != ():
            screen.blit(node, pygame.Rect(selected[0] * 100, selected[1] * 100, 100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                location = pygame.mouse.get_pos()
                x = int(location[0] / 100)
                y = int(location[1] / 100)
                if selected == (x, y):
                    selected = ()
                    click = []
                else:
                    selected = (x, y)
                    click.append(selected)
                    if len(click) == 2:
                        if moveChess(chess_state, click, turn):
                            turn = not turn
                        click = []
                        selected = ()

                    elif len(click) == 1 and turn_choose(chess_state, (click[0][0], click[0][1]), turn) == False:
                        selected = ()
                        click = []

        clock.tick(15)
        pygame.display.flip()


if __name__ == "__main__":
    main()
