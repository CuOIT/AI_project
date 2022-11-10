import pygame as pg
class Piece:
    def __init__(self,name):
        self.name=name
        if name[0]=='w':
            self.color='WHITE'
        else:
            self.color='BLACK'
    def loadImage(self):
        image=pg.image.load('res/'+self.name+'.png')
        return image
    def move():
        pass

class Pawn(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)
class Rook(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)
class Bishop(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)
class Knight(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)
class Queen(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)
class King(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

        