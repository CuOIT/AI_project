import rules
import AI
import UI
import pygame
import time

castle = {"wKR": True, "wQR": True, "bKR": True, "bQR": True}


def main():
    list_chess_state = []
    turn = 'w'
    checkMate = False
    chess_state = [["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
                   ["bPawn", "bPawn", "bPawn", "bPawn",
                       "bPawn", "bPawn", "bPawn", "bPawn"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
                   ["wPawn", "wPawn", "wPawn", "wPawn",
                       "wPawn", "wPawn", "wPawn", "wPawn"],
                   ["wRook", "wKnight", "wBishop", "wQueen",
                       "wKing", "wBishop", "wKnight", "wRook"]
                   ]
    pygame.init()
    pygame.display.set_caption("Game Chess")
    screen = pygame.display.set_mode((1000, UI.WIDTH))
    clock = pygame.time.Clock()
    selected = ()  # tuples
    click = []
    UI.setUp(screen, chess_state)
    running = True
    tbT = 0
    UI.displayDepth(screen, (str)(AI._DEPTH), 840, 80)

    while running:
        UI.draws(screen, chess_state, click, turn)
        if checkMate == True:
            if turn == 'w':
                UI.drawText(screen, "White win!")
            elif turn == 'b':
                UI.drawText(screen, "Black win!")
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_r:
                        checkMate = False
                        chess_state = rules.reset_Board(chess_state)
                        turn = 'w'
                        list_chess_state.clear()
            
            # UI.drawText(screen,"Black win" if turn=='w' else "White win")
        else:
            if turn =='w':
                checkMate = rules.checkNoMove(chess_state, turn)
                if checkMate:
                    turn=rules.switchTurn(turn)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        location = pygame.mouse.get_pos()
                        x = int(location[1] / UI.SCALE)
                        y = int(location[0] / UI.SCALE)
                        if selected == (x, y):
                            selected = ()
                            click = []
                        else:
                            selected = (x, y)
                            click.append(selected)
                            if len(click) == 2:
                                if rules.availableMove(chess_state, click, turn):
                                    rules.update(chess_state,list_chess_state, click)
                                    rules.checkPawnPromotion(chess_state, click, screen)
                                    turn=rules.switchTurn(turn)
                                click = []
                                selected = ()

                            elif len(click) == 1:
                                if chess_state[selected[0]][selected[1]][0] != turn:
                                    selected = ()
                                    click = []
                    elif event.type == pygame.KEYDOWN:
                        global castle
                        if event.key == pygame.K_LCTRL and len(list_chess_state) != 0:
                            print("stack co: ", len(list_chess_state))
    
                            chess_state = list_chess_state.pop()
                            turn = 'w'
                            castle = rules.check_castle(chess_state)

                        elif event.key == pygame.K_r:
                            chess_state = rules.reset_Board(chess_state)
                            turn = 'w'
            else:
                # chess_state=AI.miniMax(chess_state)
                startTime = time.time()
                chess_state = AI.alpha_beta_Search(chess_state)
                checkMate = rules.checkNoMove(chess_state, turn)
                endTime = time.time()

                totalTime = endTime-startTime
                print("Time: ", (str)(totalTime))
                print("Tong so nuoc di: ", (str)(len(list_chess_state)))
                numOfMove = len(list_chess_state)
                tbT = tbT+(totalTime-tbT) / numOfMove
                tbTdisplay = round(tbT, 3)
                print("Thoi gian trung binh: ", (str)(tbT))
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(840, 100, 120, 30))
                UI.displayTextAt(screen, (str)(tbTdisplay), 840, 100)
                pygame.display.update()
                turn = rules.switchTurn(turn)

            UI.draws(screen,chess_state,click,turn)

        clock.tick(15)


        pygame.display.flip()


if __name__ == "__main__":
    main()
# Het chuong trinh
