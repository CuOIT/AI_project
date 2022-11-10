import pygame as pg
import Board
import Piece  
HEIGHT=1024
WIDTH=1024
status=True
pg.init()
screen=pg.display.set_mode((WIDTH,HEIGHT))
board=Board.Board()
class Game:
    def __init__(self):
        self.whiteTurn=True
        self.piecesList={}
        self.placePieces()
    def placePieces(self):
        #pass
        for col in range(8):
            self.piecesList[(1,col)]=Piece.Pawn('bPawn')
            self.piecesList[(6,col)]=Piece.Pawn('wPawn')
        for row in range(2,6):
            for col in range(8):
                self.piecesList[(row,col)]=None
        pieces=[Piece.Rook,Piece.Knight,Piece.Bishop,Piece.Queen,Piece.King,Piece.Bishop,Piece.Knight,Piece.Rook]
        for  col in range(8):
            self.piecesList[(0,col)]=pieces[col](board.board[0][col])
            self.piecesList[(7,7-col)]=pieces[col](board.board[7][7-col])
    def printBoard(self):
        for row in range(8):
            for col in range(8):
                if (row+col)%2==0:
                    pg.draw.rect(screen,(0,50,0),pg.Rect(row*128,col*128,128,128))
                else:
                    pg.draw.rect(screen,(255,255,255),pg.Rect(row*128,col*128,128,128))
        for row in range(8):
            for col in range(8):
                if self.piecesList[(row,col)]:
                    print(self.piecesList[(row,col)].name,end='')
                else:
                    print('==',end='')
            print('')
        for row in range(8):
            for col in range(8):
                if self.piecesList[(row,col)]:
                    image=pg.image.load('res/'+self.piecesList[(row,col)].name+'.png')
                    screen.blit(image,(col*128,row*128))
game=Game()
game.printBoard()
pg.display.flip()
while(status):
    for i in pg.event.get():
        if  i.type==pg.QUIT:
            status=False
pg.QUIT            
        
'''pg.init()
screen=pg.display.set_mode((WIDTH,HEIGHT))
status=True
images=[]
for row in range(8):
    lineOfImages=[]
    for col in range(8):
        if (row+col)%2==0:
            image=pg.image.load('res/black.png')
        else:
            image=pg.image.load('res/white.png')
            lineOfImages.append(image)
    images.append(lineOfImages)
for row in range(8):
        for col in range(8):
            #screen.blit(gameState.image[row][col],(row*128,col*128))
            if (row+col)%2==0:
                pg.draw.rect(screen,(0,50,0),pg.Rect(row*128,col*128,128,128))
            else:
                pg.draw.rect(screen,(255,255,255),pg.Rect(row*128,col*128,128,128))
            if pieces[row][col] is None:
                pass
            else:
                screen.blit(pieces[row][col].loadImage(),(row*128,col*128))
pg.display.flip()
while(status):
    for i in pg.event.get():
        if  i.type==pg.QUIT:
            status=False
pg.QUIT'''