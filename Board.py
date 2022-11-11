import chess
import pygame as pg
class Board:
    def __init__(self):
        self.board=[
            ['bRook','bKnight','bBishop','bQueen','bKing','bBishop','bKnight','bRook'],
            ['bPawn','bPawn','bPawn','bPawn','bPawn','bPawn','bPawn','bPawn'],
            ['xx','xx','xx','xx','xx','xx','xx','xx'],
            ['xx','xx','xx','xx','xx','xx','xx','xx'],
            ['xx','xx','xx','xx','xx','xx','xx','xx'],
            ['xx','xx','xx','xx','xx','xx','xx','xx'],
            ['wPawn','wPawn','wPawn','wPawn','wPawn','wPawn','wPawn','wPawn'],
            ['wRook','wKnight','wBishop','wQueen','wKing','wBishop','wKnight','wRook']]
        self.image=[]
        self.whiteTurn=True
        for row in range(8):
            lineOfImages=[]
            for col in range(8):
                if (row+col)%2==0:
                    image=pg.image.load('res/black.png')
                else:
                    image=pg.image.load('res/white.png')
                lineOfImages.append(image)
            self.image.append(lineOfImages)
    def display(self):
        pass