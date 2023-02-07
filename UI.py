import pygame
import os
import rules
import copy
HEIGHT = 800
WIDTH = 800
SCALE = HEIGHT / 8
colors = [pygame.Color("pink"), pygame.Color("white")]
pieceImages = {}


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(pos):
            print("hover")
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("clicked")
                self.clicked == True
                action = True

        return action


def setUp(screen, chess_state):
    pieces = ["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bPawn",
              "wRook", "wKnight", "wBishop", "wQueen", "wKing", "wPawn"]
    for i in pieces:
        pieceImages[i] = pygame.transform.scale(
            pygame.image.load("res/" + i + ".png"), (SCALE-10, SCALE-10))
    draws(screen, chess_state, click=[], turn='w')


def draws(screen, chess_state, click, turn):  # this function is to draw board and hightlight
    for row in range(0, 8):
        for col in range(0, 8):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SCALE, row * SCALE, SCALE, SCALE))
            if "King" in chess_state[row][col]:
                if rules.KingInAttack(chess_state, chess_state[row][col][0]):
                    color = (255, 88, 88)
                    pygame.draw.rect(screen, color, pygame.Rect(
                        col * SCALE, row * SCALE, SCALE, SCALE))
            if chess_state[row][col] == "xx":
                continue
            else:
                screen.blit(pieceImages[chess_state[row][col]], pygame.Rect(
                    col * SCALE+5, row * SCALE+5, SCALE, SCALE))
    if len(click) == 1:
        highlightMove(screen, click, chess_state, turn)


def highlightMove(screen, click, chess_state, turn):
        pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(
            click[0][1] * SCALE, click[0][0] * SCALE, SCALE, SCALE))
        screen.blit(pieceImages[chess_state[click[0][0]][click[0][1]]], pygame.Rect(
            click[0][1] * SCALE+5, click[0][0] * SCALE+5, SCALE, SCALE))
        moveList = rules.moveList(chess_state, click, turn)
        for pos in moveList:
            pygame.draw.rect(screen, pygame.Color(198, 226, 255), pygame.Rect(
                pos[1]*SCALE+1, pos[0]*SCALE+1, SCALE-2, SCALE - 2))
            if chess_state[pos[0]][pos[1]] != "xx":
                screen.blit(pieceImages[chess_state[pos[0]][pos[1]]], pygame.Rect(
                    pos[1] * SCALE+5, pos[0] * SCALE+5, SCALE, SCALE))


def drawText(screen, text):
    font = pygame.font.SysFont("Time new roman", 60, True, False)
    textObject = font.render(text, 0, pygame.Color('Red'))
    textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2,
                                                    HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color('Red'))
    screen.blit(textObject, textLocation.move(2, 2))


def displayTextAt(screen, text, x, y):
    font = pygame.font.SysFont('Time new roman', 30) 
    text = font.render(f"Time:\n {text}", True, (255,255,255))
    screen.blit(text,(x,y)) 

    
    

def animation(click, screen, chess_state, clock,turn):
    
    dR = click[1][0] - click[0][0]
    dC = click[1][1] - click[0][1]
    fps = 10
    fcount = (abs(dR) + abs(dC)) * fps
    for frame in range(fcount + 1):
        r = click[0][0] + dR*frame/fcount
        c = click[0][1] + dC*frame/fcount 
        draws(screen,chess_state, click, turn)

        colore = colors[(click[1][0] + click[1][1]) % 2]
     
        end = pygame.Rect(click[1][1] * SCALE, click[1][0] * SCALE, SCALE,SCALE)
        pygame.draw.rect(screen,colore,end)
       
        
        if chess_state[click[0][0]][click[0][1]] != "xx": #xóa piece on start_node
            temp = chess_state[click[0][0]][click[0][1]]
            chess_state[click[0][0]][click[0][1]] = "xx" 
        
        
        if chess_state[click[1][0]][click[1][1]] != "xx":
            screen.blit(pieceImages[chess_state[click[1][0]][click[1][1]]], end) #vẽ end_node là "xx"
            
              
        screen.blit(pieceImages[temp], pygame.Rect(c*SCALE, r*SCALE, SCALE, SCALE)) # vẽ quân cờ di chuyển
        pygame.display.flip()
        clock.tick(60)    
    chess_state[click[0][1]][click[0][0]] = temp # trả piece về lại start_node để chạy tiếp update bàn cờ

def promoteChoice(screen, sideColor):
    x=40
    y=300
    queen_btn=Button(x, y, pygame.image.load("res/"+sideColor+"Queen.png"))
    rook_btn=Button(x+200, y, pygame.image.load("res/"+sideColor+"Rook.png"))
    knight_btn=Button(x+400,y, pygame.image.load("res/"+sideColor+"Knight.png"))
    bishop_btn=Button(x+600, y, pygame.image.load("res/"+sideColor+"Bishop.png"))
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
