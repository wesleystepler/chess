from copy import deepcopy
from move_validator import MoveInBoundsValidator, PawnCanAttackValidator, PieceCanAttackValidator
from castle_validator import KingHasntMovedValidator, RookHasntMovedValidator, SquaresBetweenAreEmptyValidator
import operator
import time


class Piece():
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color

    def getAvailableMoves(self, board):
        pass
    
    def getKing(self, pieceList):
        for piece in pieceList:
            if type(piece) == King:
                return piece
            
    
    def setValidators(self, validators):
        for i in range(0, len(validators)-1):
            validators[i].setNext(validators[i+1])
        initialValidator = validators[0]
        return initialValidator
    
    def getValidators(self):
        if type(self) == Pawn:
            return [MoveInBoundsValidator(), PawnCanAttackValidator()]
        return [MoveInBoundsValidator(), PieceCanAttackValidator()]
            

    def causesCheck(self, newPosition, gameBoard):
        # The ghost variables are used to test if a move will result in putting or keeping a king in check
        # without updating the gameBoard itself
        ghostBoard = deepcopy(gameBoard)
        ghostPiece = deepcopy(self)

        ghostBoard.updateBoard(ghostPiece, newPosition)

        if ghostPiece.color == 'white':
            if type(ghostPiece) != King:
                king = self.getKing(ghostBoard.whitePieces)
            else:
                king = ghostPiece
            enemyPieces = ghostBoard.blackPieces
        elif ghostPiece.color == 'black':
            if type(ghostPiece) != King:
                king = self.getKing(ghostBoard.blackPieces)
            else:
                king = ghostPiece
            enemyPieces = ghostBoard.whitePieces
        if king.inCheck(ghostBoard.board, enemyPieces):
            return True
        return False


    def move(self, newPosition, gameBoard):
        moves = self.getAvailableMoves(gameBoard.board)
        if newPosition in moves and not self.causesCheck(newPosition, gameBoard):
            gameBoard.updateBoard(self, newPosition)
            return True
        
        print("That is not a valid move.")
        time.sleep(0.5)
        return False


class Pawn(Piece):

    def hasMoved(self):
        if self.color == 'white' and self.position[0] == 1:
            return False
        elif self.color == 'black' and self.position[0] == 6:
            return False
        return True


    def getAvailableMoves(self, board):
        moves = []
        i = self.position[0]
        j = self.position[1]

        validator = self.setValidators(self.getValidators())

        if self.color == 'white':
            validator.validate(self, (i+1, j), moves, board)
            if not self.hasMoved():
                validator.validate(self, (i+2, j), moves, board)
            validator.validate(self, (i+1, j+1), moves, board)
            validator.validate(self, (i+1, j-1), moves, board)

        elif self.color == 'black':
            validator.validate(self, (i-1, j), moves, board)
            if not self.hasMoved():
                validator.validate(self, (i-2, j), moves, board)
            validator.validate(self, (i-1, j-1), moves, board)
            validator.validate(self, (i-1, j+1), moves, board)
        
        return moves
    

class Bishop(Piece):

    def validateMove(self, logicOp1, limit1, logicOp2, limit2, arithOp1, arithOp2, moves, board, validator):
        i = self.position[0]
        j = self.position[1]

        while logicOp1(i, limit1) and logicOp2(j, limit2):
            if validator.validate(self, (arithOp1(i,1), arithOp2(j, 1)), moves, board) == -1:
                return
            else:
                i = arithOp1(i,1)
                j = arithOp2(j,1) 

    
    def getAvailableMoves(self, board):
        moves = []
        validator = self.setValidators(self.getValidators())

        self.validateMove(operator.lt, 8, operator.lt, 8, operator.add, operator.add, moves, board, validator)
        self.validateMove(operator.lt, 8, operator.gt, 0, operator.add, operator.sub, moves, board, validator)
        self.validateMove(operator.gt, 0, operator.lt, 8, operator.sub, operator.add, moves, board, validator)
        self.validateMove(operator.gt, 0, operator.gt, 0, operator.sub, operator.sub, moves, board, validator)

        return moves
    

class Knight(Piece):

    def getAvailableMoves(self, board):
        i = self.position[0]
        j = self.position[1]

        possibleMoves = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1), (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j+2)]
        moves = []

        validator = self.setValidators(self.getValidators())

        for move in possibleMoves:
            validator.validate(self, move, moves, board)

        return moves


class Rook(Piece):
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color
        self.moved = False
        
    
    def validateMoveVertical(self, logicOp, limit, arithOp, moves, board, validator):
        i = self.position[0]
        j = self.position[1]

        while logicOp(i, limit):
            if validator.validate(self, (arithOp(i,1), j), moves, board) == -1:
                return
            else:
                i = arithOp(i, 1)

    def validateMoveHorizontal(self, logicOp, limit, arithOp, moves, board, validator):
        i = self.position[0]
        j = self.position[1]

        while logicOp(j, limit):
            if validator.validate(self, (i, arithOp(j,1)), moves, board) == -1:
                return
            else:
                j = arithOp(j, 1)
    
    def getAvailableMoves(self, board):
        moves = []
        validator = self.setValidators(self.getValidators())

        self.validateMoveVertical(operator.lt, 8, operator.add, moves, board, validator)
        self.validateMoveVertical(operator.gt, 0, operator.sub, moves, board, validator)
        self.validateMoveHorizontal(operator.lt, 8, operator.add, moves, board, validator)
        self.validateMoveHorizontal(operator.gt, 0, operator.sub, moves, board, validator)

        return moves


class Queen(Piece):
    def getAvailableMoves(self, board):

        # The Queen is just a Rook/Bishop hybrid, so no need to make a whole new function
        # when you can just combine the available moves for a rook and bishop
        rook = Rook('Test', (self.position[0], self.position[1]), self.color)
        rookMoves = rook.getAvailableMoves(board)

        bishop = Bishop('Test', (self.position[0], self.position[1]), self.color)
        bishopMoves = bishop.getAvailableMoves(board)

        moves = rookMoves + bishopMoves

        return moves


class King(Piece):
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.color = color
        self.checkMate = False
        self.moved = False

    
    def getAvailableMoves(self, board):
        i = self.position[0]
        j = self.position[1]
        
        possibleMoves = [(i+1, j), (i-1, j), (i+1, j+1), (i+1, j-1), (i-1, j-1), (i-1, j+1), (i, j+1), (i, j-1)]
        moves = []

        validator = self.setValidators(self.getValidators())

        for move in possibleMoves:
            validator.validate(self, move, moves, board)

        return moves
    
    
    def move(self, newPosition, gameBoard):
        moves = self.getAvailableMoves(gameBoard.board)
        if newPosition in moves and not self.causesCheck(newPosition, gameBoard):
            gameBoard.updateBoard(self, newPosition)
            return True
        
        print("That is not a valid move.")
        time.sleep(0.5)
        return False

    def inCheck(self, board, enemyPieces):
        for piece in enemyPieces:
            enemyMoves = piece.getAvailableMoves(board)
            if self.position in enemyMoves:
                return True

        return False
    
    def canBeSaved(self, playerPieces, gameBoard):
        save = False
        for piece in playerPieces:
            nonKingMoves = piece.getAvailableMoves(gameBoard.board)
            for move in nonKingMoves:
                if not piece.causesCheck(move, gameBoard):
                    save = True
                    return save
        return save

    
    def mated(self, gameBoard, playerPieces, enemyPieces):
        moves = self.getAvailableMoves(gameBoard.board)
        for move in moves:
            if not self.causesCheck(move, gameBoard):
                return False

        if not self.canBeSaved(playerPieces, gameBoard):
            return True
        return False    