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
    
    def validate(self, king, rook, board):
        if self.next != None:
            return self.next.validate(king, rook, board)
        return True
    
class KingHasntMovedValidator(BaseValidator):
    def validate(self, king, rook, board):
        if king.color == 'white':
            if king.position == (0,3) and not king.moved:
                return super(self.__class__, self).validate(king, rook, board)
            return False
        if king.color == 'black':
            if king.position == (7,3) and not king.moved:
                return super(self.__class__, self).validate(king, rook, board)
            return False
        
class RookHasntMovedValidator(BaseValidator):
    def validate(self, king, rook, board):
        if rook.color == 'white':
            if rook.position == (0,0) and not rook.moved:
                return super(self.__class__, self).validate(king, rook, board)
            return False
        if rook.color == 'black':
            if rook.position == (7,0) and not rook.moved:
                return super(self.__class__, self).validate(king, rook, board)
            return False
        

class SquaresBetweenAreEmptyValidator(BaseValidator):
    def validate(self, king, rook, board):
        if king.color == 'white':
            if board[0][1].whatPieceIsHere == None and board[0][2].whatPieceIsHere == None:
                return super(self.__class__, self).validate(king, rook, board)
            return False
        if king.color == 'black':
            if board[7][1].whatPieceIsHere == None and board[7][2].whatPieceIsHere == None:
                return super(self.__class__, self).validate(king, rook, board)
            return False