import pygame as pg
import Board
import Piece

HEIGHT = 1024
WIDTH = 1024
scale = HEIGHT / 8
status = True

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
board = Board.Board()

pawn = Piece.Pawn("Pawn")
rook = Piece.Rook("Rook")
bishop = Piece.Bishop("Bishop")
knight = Piece.Knight("Knight")
queen = Piece.Queen("Queen")
King = Piece.King("King")


class Game:
    def __init__(self):
        self.whiteTurn = True
        # self.piecesList = {}
        # self.placePieces()
        self.selected = ()  # lưu vị trí được chọn
        self.click = []  # Lưu nước đi

    # def placePieces(self):
    #     # pass
    #
    #     for col in range(8):
    #         self.piecesList[(1, col)] = Piece.Pawn('bPawn')
    #         self.piecesList[(6, col)] = Piece.Pawn('wPawn')
    #
    #     for row in range(2, 6):
    #         for col in range(8):
    #             self.piecesList[(row, col)] = None
    #
    #     pieces = [Piece.Rook, Piece.Knight, Piece.Bishop, Piece.Queen, Piece.King, Piece.Bishop, Piece.Knight,
    #               Piece.Rook]
    #
    #     for col in range(8):
    #         self.piecesList[(0, col)] = pieces[col](board.board[0][col])
    #         self.piecesList[(7, 7 - col)] = pieces[col](board.board[7][7 - col])

    def printBoard(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    pg.draw.rect(screen, (0, 50, 0), pg.Rect(row * 128, col * 128, 128, 128))
                else:
                    pg.draw.rect(screen, (255, 255, 255), pg.Rect(row * 128, col * 128, 128, 128))
        # for row in range(8):
        #     for col in range(8):
        #         if self.piecesList[(row,col)]:
        #             print(self.piecesList[(row,col)].name,end='')
        #         else:
        #             print('==',end='')
        #     print('')
        for row in range(8):
            for col in range(8):
                if board.board[row][col] == "xx":
                    continue
                image = pg.image.load('res/' + board.board[row][col] + '.png')
                screen.blit(image, (col * 128, row * 128))

    def moving(self):
        oldX = self.click[0][0]
        oldY = self.click[0][1]
        newX = self.click[1][0]
        newY = self.click[1][1]

        piece = board.board[oldY][oldX]
        print(piece)
        moveList = []  # List of valid moves
        validMove = False

        if "Pawn" in piece:
            moveList = pawn.checkPawnMove(oldX, oldY, moveList, game.whiteTurn, board.board)

        elif "Rook" in piece:
            moveList = rook.checkRookMove(oldX, oldY, moveList, game.whiteTurn, board.board)

        elif "Bishop" in piece:
            moveList = bishop.checkBishopMove(oldX, oldY, moveList, game.whiteTurn, board.board)

        elif "Queen" in piece:
            moveList = queen.checkQueenMove(oldX, oldY, moveList, game.whiteTurn, board.board)

        for pos in moveList:
            if (newX, newY) == pos:
                validMove = True
                break

        if not validMove:
            return False

        # Check ăn chess khác màu
        if board.board[newY][newX][0] == board.board[oldY][oldX][0]:
            return False

        # Cập nhật lại bàn cờ
        board.board[newY][newX] = board.board[oldY][oldX]
        board.board[oldY][oldX] = "xx"

        return True

    def check_turn(self, selected):

        if self.whiteTurn == True:
            if board.board[selected[1]][selected[0]][0] == "w":
                return True
            else:
                return False
        elif self.whiteTurn == False:
            if board.board[selected[1]][selected[0]][0] == "b":
                return True
            else:
                return False
        return False
        #     if self.piecesList[self.click[0]] != None:
        #         if self.piecesList[self.click[0]].name[0] == "w":
        #             return True
        #         else:
        #             return False
        # else:
        #     if self.piecesList[self.click[0]] != None:
        #         if self.piecesList[self.click[0]].name[0] == "b":
        #             return True
        #         else:
        #             return False


if __name__ == "__main__":
    game = Game()
    game.printBoard()

    node_xanh = pg.transform.scale(pg.image.load("res/node_xanh.png"), (128, 128))

    clock = pg.time.Clock()
    while status:
        for i in pg.event.get():

            game.printBoard()
            if game.selected != ():
                screen.blit(node_xanh, pg.Rect(game.selected[0] * scale, game.selected[1] * scale, scale, scale))

            if i.type == pg.QUIT:
                status = False

            if i.type == pg.MOUSEBUTTONUP:
                location = pg.mouse.get_pos()
                x = int(location[0] / 128)
                y = int(location[1] / 128)
                if game.selected == (x, y):
                    game.selected = ()
                else:
                    game.selected = (x, y)
                    game.click.append(game.selected)

                    if len(game.click) == 2:
                        if game.moving():
                            game.whiteTurn = not game.whiteTurn
                        game.selected = ()
                        game.click = []

                    elif len(game.click) == 1 and game.check_turn((game.click[0][0], game.click[0][1])) == False:
                        game.selected = ()
                        game.click = []


        clock.tick(15)
        pg.display.flip()

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
