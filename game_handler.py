from castle_validator import KingHasntMovedValidator, RookHasntMovedValidator, SquaresBetweenAreEmptyValidator
import time
import pieces
import random

class GameHandler:

    def __init__(self):
        self.p1Turn = True
        self.p1Wins = False
        self.p2Wins = False
    
    def clearScreen(self):
        for i in range(50):
            print()
    
    def isValidInput(self, squares, letters, numbers):
        if len(squares) == 2:
            if squares[0].isalnum() and squares[1].isalnum():
                if squares[0][0] in letters and squares[1][1] in numbers and squares[1][0] in letters and squares[1][1] in numbers:
                    return True
        return False


    def parseInput(self, requestedMove, letters, numbers, board):
        oldPosition = (numbers.index(requestedMove[0][1]), letters.index(requestedMove[0][0]))
        newPosition = (numbers.index(requestedMove[1][1]), letters.index(requestedMove[1][0]))

        if board[oldPosition[0]][oldPosition[1]].isOccupiedByWhitePiece() and self.p1Turn:
            return [oldPosition, newPosition]
        elif board[oldPosition[0]][oldPosition[1]].isOccupiedByBlackPiece() and not self.p1Turn: 
            return [oldPosition, newPosition]
        return -1

        
    def checkInput(self, requestedMove, gameBoard):
        squares = requestedMove.split(" ")
        if self.isValidInput(squares, gameBoard.letters, gameBoard.numbers):
            return self.parseInput(squares, gameBoard.letters, gameBoard.numbers, gameBoard.board)
        return -1
    

    def takeTurn(self, gameBoard):
        self.clearScreen()
        gameBoard.displayBoard()

        if self.p1Turn:
            self.p2Wins = self.isMated(gameBoard, gameBoard.whitePieces, gameBoard.blackPieces)
            if self.p2Wins:
                return
            else:
                print("Player 1, it's your turn!")
                if self.isInCheck(gameBoard.board, gameBoard.whitePieces, gameBoard.blackPieces):
                    print("You are in check!")

        else:
            self.p1Wins = self.isMated(gameBoard, gameBoard.blackPieces, gameBoard.whitePieces)
            if self.p1Wins:
                return
            else:
                print("Player 2, it's your turn!")
                if self.isInCheck(gameBoard.board, gameBoard.blackPieces, gameBoard.whitePieces):
                    print("You are in check!")

        move = input()
        if move == 'CASTLE':
            self.castle(gameBoard)

        else:
            results = self.checkInput(move, gameBoard)

            if results != -1:
                oldPosition = results[0]
                newPosition = results[1]
                whichPiece = gameBoard.board[oldPosition[0]][oldPosition[1]].whatPieceIsHere

                if whichPiece.move(newPosition, gameBoard):
                    if gameBoard.pawnReachedEnd(whichPiece):
                        if self.p1Turn:
                            gameBoard.whitePieces.append(gameBoard.convertPawn(whichPiece, 'W'))
                            gameBoard.whitePieces.remove(whichPiece)
                        else:
                            gameBoard.blackPieces.append(gameBoard.convertPawn(whichPiece, 'B'))
                            gameBoard.blackPieces.remove(whichPiece)

                    self.p1Turn = not self.p1Turn

            else:
                print("That is not a valid move.")
                time.sleep(0.5)

    
    def canCastle(self, king, rook, board):
        validatorChain = [KingHasntMovedValidator(), RookHasntMovedValidator(), SquaresBetweenAreEmptyValidator()]
        validator = pieces.Piece.setValidators(self, validatorChain)

        if validator.validate(king, rook, board):
            return True
        return False
    
    
    def castle(self, gameBoard):
        if self.p1Turn:
                king = gameBoard.board[0][3].whatPieceIsHere
                rook = gameBoard.board[0][0].whatPieceIsHere
        else:
            king = gameBoard.board[7][3].whatPieceIsHere
            rook = gameBoard.board[7][0].whatPieceIsHere
        if self.canCastle(king, rook, gameBoard.board):
            kingPos = (king.position[0], king.position[1]-2)
            rookPos = (rook.position[0], rook.position[1]+2)
            if not king.causesCheck(kingPos, gameBoard) and not rook.causesCheck(rookPos, gameBoard):
                gameBoard.updateBoard(king, (king.position[0], king.position[1]-2))
                gameBoard.updateBoard(rook, (rook.position[0], rook.position[1]+2))
                self.p1Turn = not self.p1Turn
        else:
            print("That is not a valid move")
            time.sleep(0.5)

    
    def isInCheck(self, board, playerPieces, enemyPieces):
        # TODO: Including self here feels weird - try to find another way to do this
        king = pieces.Piece.getKing(self, playerPieces)
        if king.inCheck(board, enemyPieces):
            return True
        return False
        

    def isMated(self, gameBoard, playerPieces, enemyPieces):
        king = pieces.Piece.getKing(self, playerPieces)
        if king.mated(gameBoard, playerPieces, enemyPieces):
            return True   
        return False
    
    def gameOver(self):
        if self.p1Wins or self.p2Wins:
            return True
        return False