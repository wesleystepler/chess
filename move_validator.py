import pieces

class MoveValidator:
    def setNext(nextValidator):
        pass
    def validate(self, proposedMove, moves):
        pass

class BaseValidator(MoveValidator):
    def __init__(self):
        self.next = None

    def setNext(self, nextValidator):
        self.next = nextValidator
        return nextValidator
    
    def validate(self, piece, proposedMove, moves, board):
        if self.next != None:
            return self.next.validate(piece, proposedMove, moves, board)
        moves.append(proposedMove)
        return 0

class MoveInBoundsValidator(BaseValidator):
    def validate(self, piece, proposedMove, moves, board):
        if proposedMove[0] > 7 or proposedMove[1] > 7:
            return -1
        if proposedMove[0] < 0 or proposedMove[1] < 0:
            return -1
    
        return super(self.__class__, self).validate(piece, proposedMove, moves, board)
    
    
class PieceCanAttackValidator(BaseValidator):
    def validate(self, piece, proposedMove, moves, board):
        if piece.color == 'white' and board[proposedMove[0]][proposedMove[1]].isOccupiedByWhitePiece():
            return -1
        if piece.color == 'black' and board[proposedMove[0]][proposedMove[1]].isOccupiedByBlackPiece():
            return -1
        if piece.color == 'white' and board[proposedMove[0]][proposedMove[1]].isOccupiedByBlackPiece():
            moves.append(proposedMove)
            return -1
        if piece.color == 'black' and board[proposedMove[0]][proposedMove[1]].isOccupiedByWhitePiece():
            moves.append(proposedMove)
            return -1
        
        return super(self.__class__, self).validate(piece, proposedMove, moves, board)
    

class PawnCanAttackValidator(BaseValidator):
    def validate(self, piece, proposedMove, moves, board):
        if abs(proposedMove[1] - piece.position[1]) == 1:
            if piece.color == 'white' and board[proposedMove[0]][proposedMove[1]].isOccupiedByBlackPiece():
                return super(self.__class__, self).validate(piece, proposedMove, moves, board) 
            if piece.color == 'black' and board[proposedMove[0]][proposedMove[1]].isOccupiedByWhitePiece():
                return super(self.__class__, self).validate(piece, proposedMove, moves, board)
            return -1
        return super(self.__class__, self).validate(piece, proposedMove, moves, board)

