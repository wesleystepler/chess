from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = []
        self.whitePieces = []
        self.blackPieces = []
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

    
    def populateSquare(self, piece, position, occupied):
        self.board[position[0]][position[1]].occupied = occupied
        self.board[position[0]][position[1]].whatPieceIsHere = piece    
    
    def initializePieces(self):
        self.whitePieces = [Rook('WR', (0, 0), 'white'), Knight('Wk', (0, 1), 'white'), Bishop('WB', (0, 2), 'white'),
                            King('WK', (0, 3), 'white'), Queen('WQ', (0, 4), 'white'), Bishop('WB', (0, 5), 'white'), 
                            Knight('Wk', (0, 6), 'white'), Rook('WR', (0, 7), 'white')]
        
        self.blackPieces = [ Rook('BR', (7, 0), 'black'), Knight('Bk', (7, 1), 'black'), Bishop('BB', (7, 2), 'black'),
                           King('BK', (7, 3), 'black'), Queen('BQ', (7, 4), 'black'), Bishop('BB', (7, 5), 'black'), 
                           Knight('Bk', (7, 6), 'black'), Rook('BR', (7, 7), 'black') ]
        
        for piece in self.whitePieces:
            self.populateSquare(piece, piece.position, True)

        for piece in self.blackPieces:
            self.populateSquare(piece, piece.position, True)

        for i in range(0, 8):
            p1 = Pawn('WP', (1,i), 'white')
            p2 = Pawn('BP', (6,i), 'black')

            self.whitePieces.append(p1)
            self.populateSquare(p1, p1.position, True)

            self.blackPieces.append(p2)
            self.populateSquare(p2, p2.position, True)

    
    def createBoard(self):
        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(BoardSquare((i, j)))
            self.board.append(row)
        return self.board
    

    def updateBoard(self, piece, newPosition):
        self.populateSquare(None, piece.position, False)

        if type(piece) == King or type(piece) == Rook:
            piece.moved = True

        piece.position = newPosition
        x = newPosition[0]
        y = newPosition[1]

        if self.board[x][y].isOccupiedByWhitePiece():
            self.whitePieces.remove(self.board[x][y].whatPieceIsHere)
            self.board[x][y].whatPieceIsHere = piece

        elif self.board[x][y].isOccupiedByBlackPiece():
            self.blackPieces.remove(self.board[x][y].whatPieceIsHere)
            self.board[x][y].whatPieceIsHere = piece
        else:
            self.populateSquare(piece, piece.position, True)


    def getConvertedPiece(self, pawn, piece, color):
        if piece == 'R':
            converted = Rook(f'{color}R', pawn.position, pawn.color)
        elif piece == 'B':
            converted = Bishop(f"{color}B", pawn.position, pawn.color)
        elif piece == 'K':
            converted = Knight(f"{color}k", pawn.posiiton, pawn.color)
        else:
            converted = Queen(f'{color}Q', pawn.position, pawn.color)

        self.board[pawn.position[0]][pawn.position[1]].whatPieceIsHere = converted
        return converted
    
    def pawnReachedEnd(self, piece):
        if type(piece) == Pawn and (piece.position[0] == 0 or piece.position[0] == 7):
            return True
        return False
    
    def convertPawn(self, pawn, color):
        print("Congrats! Your pawn reached the other side!")
        print("What piece would you like to convert it to?")
        print("R: Rook,  B: Bishop,  K: Knight,  Q: Queen")
        pieces = ["R", "B", "K", "Q"]
        newPiece = input("Select your piece: ")
        if newPiece not in pieces:
            print("Please enter 'R', 'B', 'K', or 'Q'")
            while newPiece not in pieces:
                newPiece = input("Select your piece: ")
        return self.getConvertedPiece(pawn, newPiece, color)


    def displayBoard(self):

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()
        for i in range(0, 8):
            print(str(self.numbers[i]) + " ",end = '')
            for j in range(0, 8):
                if self.board[i][j].isOccupied():
                    print(f"[{self.board[i][j].whatPieceIsHere.name}]", end='')
                else:
                    print("[  ]", end='')
            print()
        for n in self.letters:
            print(f"   {n}", end='')
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()


class BoardSquare:
    def __init__(self, xy):
        self.xy = xy
        self.occupied = False
        self.whatPieceIsHere = None

    def isOccupied(self):
        return self.occupied
    
    def isOccupiedByBlackPiece(self):
        if self.occupied:
            if self.whatPieceIsHere.color == 'black':
                return True
        return False
    
    def isOccupiedByWhitePiece(self):
        if self.occupied:
            if self.whatPieceIsHere.color == 'white':
                return True
        return False
    
    def __str__(self):
        return f"Square is located at coordinate {self.xy} on the board"