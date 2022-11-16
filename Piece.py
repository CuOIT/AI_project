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
    def move(self):
        pass

class Pawn(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkPawnMove(self, x, y, moveList, turn, board):
        if turn == True:
            if board[y - 1][x] == "xx":  # White move ahead 1 step
                pos = (x, y - 1)
                moveList.append(pos)

                if y == 6 and board[y - 2][x] == "xx":  # White move ahead 2 step
                    pos = (x, y - 2)
                    moveList.append(pos)

            if x - 1 >= 0:
                if board[y - 1][x - 1][0] == 'b':  # Check enemy chess
                    pos = (x - 1, y - 1)
                    moveList.append(pos)
            if x + 1 <= 7:
                if board[y - 1][x + 1][0] == 'b':
                    pos = (x + 1, y - 1)
                    moveList.append(pos)
        else:
            if board[y + 1][x] == "xx":  # White move ahead 1 step
                pos = (x, y + 1)
                moveList.append(pos)

                if y == 1 and board[y + 2][x] == "xx":  # White move ahead 2 step
                    pos = (x, y + 2)
                    moveList.append(pos)

            if x - 1 >= 0:
                if board[y + 1][x - 1][0] == 'w':  # Check enemy chess
                    pos = (x - 1, y + 1)
                    moveList.append(pos)
            if x + 1 <= 7:
                if board[y + 1][x + 1][0] == 'w':
                    pos = (x + 1, y + 1)
                    moveList.append(pos)

        return moveList


class Rook(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkRookMove(self, x, y, moveList, turn, board):
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
                    if board[newY][newX] == "xx":
                        pos = (newX, newY)
                        moveList.append(pos)

                    elif board[newY][newX][0] == enemyColor:
                        pos = (newX, newY)
                        moveList.append(pos)
                        break  # Can not move piece behind chess

                    else:  # frendly chess
                        break
                else:  # Out of the board
                    break
        return moveList
class Bishop(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkBishopMove(self, x, y, moveList, turn, board):
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
                    if board[newY][newX] == "xx":
                        pos = (newX, newY)
                        moveList.append(pos)

                    elif board[newY][newX][0] == enemyColor:
                        pos = (newX, newY)
                        moveList.append(pos)
                        break  # Can not move piece behind chess

                    else:  # frendly chess
                        break
                else:  # Out of the board
                    break
        return moveList
class Knight(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkKnightMove(self, x, y, moveList, turn, board):
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

class Queen(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkQueenMove(self, x, y, moveList, turn, board):
        moveList.append(Rook.checkRookMove(self, x, y, moveList, turn, board))
        moveList.append(Bishop.checkBishopMove(self, x, y, moveList, turn, board))

        return moveList
class King(Piece):
    def __init__(self,name):
        Piece.__init__(self,name)

    def checkKingMove(self, x, y, moveList, turn, board):
        direction = ((-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
        if turn == True:
            enemyColor = "b"
        else:
            enemyColor = "w"

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