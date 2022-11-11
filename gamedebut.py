import pygame, sys



def loadImage(colors):
    img = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wp", "wQ","wR", "wN"]
    
    for i in img:
        colors[i] = pygame.transform.scale(pygame.image.load("image/"+i + ".png"), (100,100))
    
    
def draws(scr):
    colors= [pygame.Color("pink"), pygame.Color("white")]
    for r in range(0,8):
        for c in range(0,8):
            color = colors[((r+c) %2)]
            pygame.draw.rect(scr, color, pygame.Rect(c*100,r*100, 100, 100))

def draw_co(scr,colors, chess_state):
    
    for c in range(0,8):
        for l in range(0,8):
            if(chess_state[l][c] == "xx"):
                continue
            else:
                scr.blit(colors[chess_state[l][c]], pygame.Rect(c*100, l*100, 100,100))    
    # scr.blit(image, pygame.Rect(x*100, y*100, 100, 100))

def move_co(chess_state, click):
    if chess_state[click[1][1]][click[1][0]][0] == chess_state[click[0][1]][click[0][0]][0]:
        return False
    if chess_state[click[1][1]][click[1][0]] == "xx":
        chess_state[click[1][1]][click[1][0]] = chess_state[click[0][1]][click[0][0]]
        chess_state[click[0][1]][click[0][0]] = "xx"
   
    elif chess_state[click[0][1]][click[0][0]] != "xx":
        chess_state[click[1][1]][click[1][0]] = chess_state[click[0][1]][click[0][0]]  
        chess_state[click[0][1]][click[0][0]] = "xx"
    return True

    
    
    # print(click)
    # print(chess_state[click[0][1]][click[0][0]], chess_state[click[1][1]][click[1][0]])

   
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
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()
    
    node = pygame.transform.scale(pygame.image.load("image/node_xanh.png"), (100,100))
    
    chess_state = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                   ["bp","bp","bp","bp","bp","bp","bp","bp"],
                   ["xx","xx","xx","xx","xx","xx","xx","xx"],
                   ["xx","xx","xx","xx","xx","xx","xx","xx"],
                   ["xx","xx","xx","xx","xx","xx","xx","xx"],
                   ["xx","xx","xx","xx","xx","xx","xx","xx"],
                   ["wp","wp","wp","wp","wp","wp","wp","wp"],
                   ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
                   ]
    
    selected = ()
    click=[]
    color = {}
    loadImage(color)
    turn = True
    
    running = True
    while running:
        draws(screen)
        draw_co(screen,color, chess_state)
        if selected != ():
            screen.blit(node, pygame.Rect(selected[0]*100,selected[1]*100,100,100))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                location = pygame.mouse.get_pos()
                a = int (location[0] / 100)
                b = int (location[1] / 100)
                if selected == (a,b):
                    selected = ()
                    click = []
                else:
                    selected = (a,b)
                    click.append(selected)
                    if len(click) == 2: 
                        if move_co(chess_state, click):                       
                            turn = not turn
                        click = []
                        selected = ()
                        
                    elif len(click) == 1 and turn_choose(chess_state, (click[0][0], click[0][1]), turn) == False:
                        selected = ()
                        click = []
                        
                        
        clock.tick(15)
        pygame.display.flip()        
        
if __name__ ==  "__main__":
    main()        

                
            
                
                