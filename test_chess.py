import unittest

import unittest.test
from pieces import Pawn, Rook, Knight, Bishop, Queen, King, Piece
from board import Board, BoardSquare
from game_handler import GameHandler

class TestPiecesInit(unittest.TestCase):

    def testBoardSquare(self):
        b = BoardSquare((5, 2))
        self.assertEqual( (5, 2), b.xy, "Board initialization failed")
        self.assertTrue(type(b.xy) == tuple, "Square coordinate is not a tuple")

    def testPawn(self):
        p = Pawn("pawn", (0,0), 'white')
        self.assertEqual("pawn", p.name, "Pawn name initialization failed")
        self.assertEqual((0,0), p.position, "Pawn coordinate initialization failed")
        self.assertEqual('white', p.color, "Pawn color initialization failed")

    def testBishop(self):
        p = Bishop("bishop", (0,0), 'white')
        self.assertEqual("bishop", p.name, "Bishop name initialization failed")
        self.assertEqual((0,0), p.position, "Bishop coordinate initialization failed")
        self.assertEqual('white', p.color, "Bishop color initialization failed")

    def testKnight(self):
        p = Knight("knight", (0,0), 'white')
        self.assertEqual("knight", p.name, "Knight name initialization failed")
        self.assertEqual((0,0), p.position, "Knight coordinate initialization failed")
        self.assertEqual('white', p.color, "Knight color initialization failed")

    def testRook(self):
        p = Rook("rook", (0,0), 'white')
        self.assertEqual("rook", p.name, "Rook name initialization failed")
        self.assertEqual((0,0), p.position, "Rook coordinate initialization failed")
        self.assertEqual('white', p.color, "Rook color initialization failed")

    def testQueen(self):
        p = Queen("king", (0,0), 'white')
        self.assertEqual("king", p.name, "Queen name initialization failed")
        self.assertEqual((0,0), p.position, "Queen coordinate initialization failed")
        self.assertEqual('white', p.color, "Queen color initialization failed")

    def testKing(self):
        p = Queen("queen", (0,0), 'white')
        self.assertEqual("queen", p.name, "King name initialization failed")
        self.assertEqual((0,0), p.position, "King coordinate initialization failed")
        self.assertEqual('white', p.color, "King color initialization failed")


class TestBoard(unittest.TestCase):

    def testBoardCreation(self):
        for i in range(0, 7):
            for j in range(0, 7):
                self.assertEqual((i, j), self.b.board[i][j].xy, "Board coordinates initialized incorrectly")

    def setUp(self):
        self.b = Board()
        self.b.createBoard()
        self.b.initializePieces()

    def testBoardIsNotNull(self):
        self.assertTrue(self.b != None, "The board is null")

    def testPieceInitialization(self):
        self.assertTrue(len(self.b.whitePieces) == 16, "Piece initialization failed. Too many or not enough white pieces")
        self.assertTrue(len(self.b.blackPieces) == 16, "Piece initialization failed. Too many or not enough black pieces")

    def testBoardSquareIsOccupiedByWhitePawn(self):
        self.assertTrue(self.b.board[1][0].isOccupied, "Occupied BoardSquare thinks it's empty")
        self.assertEqual(self.b.board[1][0].whatPieceIsHere.name, 'WP', "Incorrect piece on board square: name is wrong")
        self.assertEqual(self.b.board[1][0].whatPieceIsHere.position, (1, 0), "Incorrect piece on board square: coordinates are wrong")
        self.assertEqual(self.b.board[1][0].whatPieceIsHere.color, 'white', "Incorrect piece on board square: color is wrong")

    def testBoardSquareIsOccupiedByBlackPawn(self):
        self.assertTrue(self.b.board[6][0].isOccupied, "Occupied BoardSquare thinks it's empty")  
        self.assertEqual(self.b.board[6][0].whatPieceIsHere.name, 'BP', "Incorrect piece on board square: name is wrong")
        self.assertEqual(self.b.board[6][0].whatPieceIsHere.position, (6, 0), "Incorrect piece on board square: coordinates are wrong")
        self.assertEqual(self.b.board[6][0].whatPieceIsHere.color, 'black', "Incorrect piece on board square: color is wrong")

    def testBoardSquareOccupiedByWhiteKing(self):
        self.assertTrue(self.b.board[0][3].isOccupied, "Occupied BoardSquare thinks it's empty")  
        self.assertTrue(self.b.board[0][3].isOccupiedByWhitePiece, "BoardSquare thinks white piece is black")
        self.assertEqual(self.b.board[0][3].whatPieceIsHere.name, 'WK', "Incorrect piece on board square: name is wrong")
        self.assertEqual(self.b.board[0][3].whatPieceIsHere.position, (0, 3), "Incorrect piece on board square: coordinates are wrong")
        self.assertEqual(self.b.board[0][3].whatPieceIsHere.color, 'white', "Incorrect piece on board square: color is wrong")

    def testBoardSquareOccupiedByBlackKing(self):
            self.assertTrue(self.b.board[7][3].isOccupied, "Occupied BoardSquare thinks it's empty")  
            self.assertTrue(self.b.board[7][3].isOccupiedByBlackPiece, "BoardSquare thinks black piece is white")
            self.assertEqual(self.b.board[7][3].whatPieceIsHere.name, 'BK', "Incorrect piece on board square: name is wrong")
            self.assertEqual(self.b.board[7][3].whatPieceIsHere.position, (7, 3), "Incorrect piece on board square: coordinates are wrong")
            self.assertEqual(self.b.board[7][3].whatPieceIsHere.color, 'black', "Incorrect piece on board square: color is wrong")


class TestPawnMoves(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testAvailableMovesWhitePawn(self):
        p = Pawn('p', (1,0), 'white')
        self.assertEqual(p.getAvailableMoves(self.board.board), [(2, 0), (3, 0)])

    def testMovePawnOneForward(self):
        p = self.board.board[1][0].whatPieceIsHere
        p.move((2,0), self.board)
        self.assertTrue(self.board.board[2][0].isOccupiedByWhitePiece())
        self.assertFalse(self.board.board[1][0].isOccupiedByWhitePiece())

    
    def testMovePawnTwoForward(self):
        p = self.board.board[1][0].whatPieceIsHere
        p.move((3,0), self.board)
        self.assertTrue(self.board.board[3][0].isOccupiedByWhitePiece())
        self.assertFalse(self.board.board[1][0].isOccupiedByWhitePiece())

    def testPawnAttack(self):
        p1 = Pawn('WP', (3,1), 'white')
        p2 = Pawn('BP', (4, 2), 'black')

        self.placePieces(p1, self.board.whitePieces)
        self.placePieces(p2, self.board.blackPieces)

        p1.move((4,2), self.board)
        self.assertTrue(self.board.board[4][2].isOccupiedByWhitePiece())
        self.assertTrue(len(self.board.whitePieces) - len(self.board.blackPieces) == 1)


class TestBishopMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testBishopCantMove(self):
        bishop = self.board.board[7][2].whatPieceIsHere
        self.assertEqual(bishop.getAvailableMoves(self.board.board), [])

    def testBishopCanMove(self):
        bishop = Bishop('WB', (2, 2), 'white')
        self.placePieces(bishop, self.board.whitePieces)
        expectedMoves = [(3, 3), (4, 4), (5, 5), (3, 1), (4, 0)]
        moves = bishop.getAvailableMoves(self.board.board)
        print(moves)
        # .sort() is used here to ensure order of both lists is correct
        self.assertEqual(expectedMoves.sort(), moves.sort())
        bishop.move((6,6), self.board)
        self.assertFalse(self.board.board[2][2].isOccupiedByWhitePiece())
        self.assertTrue(self.board.board[6][6].isOccupiedByWhitePiece())

    def testBishopCantMovePastBlackPiece(self):
        bishop1 = Bishop('WB', (2, 2), 'white')
        self.placePieces(bishop1, self.board.whitePieces)

        bishop2 = Bishop('WB', (3, 3), 'black')
        self.placePieces(bishop2, self.board.blackPieces)

        moves = bishop1.getAvailableMoves(self.board.board)

        self.assertIn((3,3), moves)
        self.assertNotIn((4,4), moves)


    def testBishopCanAttack(self):
        bishop1 = Bishop('WB', (2, 2), 'white')
        self.placePieces(bishop1, self.board.whitePieces)

        bishop2 = Bishop('WB', (3, 3), 'black')
        self.placePieces(bishop2, self.board.blackPieces)

        bishop1.move((3,3), self.board)
        self.assertTrue(self.board.board[3][3].isOccupiedByWhitePiece())
        self.assertTrue(len(self.board.whitePieces) - len(self.board.blackPieces) == 1)


class TestKnightMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testKnightCantMove(self):
        p1 = self.board.board[1][0].whatPieceIsHere
        p2 = self.board.board[1][2].whatPieceIsHere
        p1.move((2,0), self.board)
        p2.move((2,2), self.board)
        knight = self.board.board[0][1].whatPieceIsHere
        moves = knight.getAvailableMoves(self.board.board)   
        self.assertEqual(moves, [])
    
    def testKnightCanMove(self):
        knight = self.board.board[0][1].whatPieceIsHere
        expectedMoves = ([(2,0), (2,2)])
        moves = knight.getAvailableMoves(self.board.board)
        self.assertEqual(expectedMoves.sort(), moves.sort())

    def testKnightCanAttack(self):
        k1 = Knight('Wk', (2, 2), 'white')
        self.placePieces(k1, self.board.whitePieces)

        k2 = Knight('Wk', (4, 3), 'black')
        self.placePieces(k2, self.board.blackPieces)

        k1.move((4,3), self.board)
        self.assertTrue(self.board.board[4][3].isOccupiedByWhitePiece())
        self.assertTrue(len(self.board.whitePieces) - len(self.board.blackPieces) == 1)   


class TestRookMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testRookCantMove(self):
        self.board.initializePieces()
        rook = self.board.board[0][0].whatPieceIsHere
        moves = rook.getAvailableMoves(self.board.board)
        self.assertEqual(moves, [])

    def testRookCanMove(self):
        rook = Rook("WR", (4, 3), 'white')
        self.placePieces(rook, self.board.whitePieces)

        expectedMoves = [(4,4), (4,5), (4,6), (4,7), (4,3), (4,2), (4,1), (4,0), (5,3), (3,3), (2,3)]
        
        moves = rook.getAvailableMoves(self.board.board)

        self.assertEqual(expectedMoves.sort(), moves.sort())

    def testRookCantMovePastBlackPiece(self):
        rook = Rook("WR", (4, 3), 'white')
        self.placePieces(rook, self.board.whitePieces)

        pawn = Pawn("BP", (5,3), 'black')
        self.placePieces(pawn, self.board.blackPieces)

        moves = rook.getAvailableMoves(self.board.board)
        self.assertIn((5,3), moves)
        self.assertNotIn((6,3), moves)

    
    def testRookCanAttack(self):
        rook = Rook("WR", (4, 3), 'white')
        self.placePieces(rook, self.board.whitePieces)

        pawn = Pawn("BP", (6,3), 'black')
        self.placePieces(pawn, self.board.blackPieces)

        rook.move((6,3), self.board)
        self.assertTrue(self.board.board[6][3].isOccupiedByWhitePiece())
        self.assertTrue(len(self.board.whitePieces) - len(self.board.blackPieces) == 1)


class TestQueenMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testQueenCantMove(self):
        self.board.initializePieces()
        queen = self.board.board[7][4].whatPieceIsHere
        moves = queen.getAvailableMoves(self.board.board)
        self.assertEqual([], moves)

    def testQueenCanMove(self):
        queen = Queen('test', (4,3), 'white')
        expectedMoves = [(4, 0), (4,1), (4,2), (4,4), (4,5), (4,6), (4,7), 
                        (2,3), (3,3), (5,3), (5,4), (5,2), 
                        (3, 4), (2, 5), (3,2), (2,1)]
        
        moves = queen.getAvailableMoves(self.board.board)

        self.assertEqual(expectedMoves.sort(), moves.sort())

    def testQueenCanAttack(self):
        queen = Queen('test', (4,3), 'black')
        self.placePieces(queen, self.board.blackPieces)

        pawn = Pawn('test', (1,6), 'white')
        self.placePieces(pawn, self.board.whitePieces)

        queen.move((1,6), self.board)
        self.assertTrue(self.board.board[1][6].isOccupiedByBlackPiece)
        self.assertTrue(len(self.board.blackPieces) - len(self.board.whitePieces) == 1)


class TestKingMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.createBoard()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testKingCantMove(self):
        self.board.initializePieces()
        king = self.board.board[0][3].whatPieceIsHere
        moves = king.getAvailableMoves(self.board.board)
        self.assertEqual([], moves)

    def testKingCantMoveIntoCheck(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)
        
        rook = Rook('test', (7, 2), 'black')  
        self.placePieces(rook, self.board.blackPieces) 

        self.assertFalse(king.move((0, 2), self.board))

class TestCastleLogic(unittest.TestCase):
    def setUp(self):
        self.g = GameHandler()
        self.board = Board()
        self.board.createBoard()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testCanCastle(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        rook = Rook('test', (0,0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        self.assertTrue(self.g.canCastle(king, rook, self.board.board))

    def testCantCastleBlocked(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        bishop = Bishop('test', (0,2), 'white')
        self.placePieces(bishop, self.board.whitePieces)

        rook = Rook('test', (0,0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        self.assertFalse(self.g.canCastle(king, rook, self.board.board))

    def testCantCastleKingMoved(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        rook = Rook('test', (0,0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        king.move((1,3), self.board)
        king.move((0,3), self.board)

        self.assertFalse(self.g.canCastle(king, rook, self.board.board))   

    def testCantCastleRookMoved(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        rook = Rook('test', (0,0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        rook.move((3,0), self.board)
        rook.move((0,0), self.board)

        self.assertFalse(self.g.canCastle(king, rook, self.board.board)) 

    def testCantCastleIntoCheck(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        rook = Rook('test', (0,0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        queen = Queen('test', (6, 1), 'black')
        self.placePieces(queen, self.board.blackPieces)

        self.assertTrue(king.causesCheck((king.position[0], king.position[1]-2), self.board))    


class TestPawnConversion(unittest.TestCase):
    def setUp(self):
        self.g = GameHandler()
        self.board = Board()
        self.board.createBoard()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testPawnReachedEnd(self):
        pawn1 = Pawn('test', (7, 2), 'white')
        pawn2 = Pawn('test', (0, 5), 'black')

        self.placePieces(pawn1, self.board.whitePieces)
        self.placePieces(pawn2, self.board.blackPieces)   

        self.assertTrue(self.board.pawnReachedEnd(pawn1))
        self.assertTrue(self.board.pawnReachedEnd(pawn2))

    def testConversion(self):
        pawn1 = Pawn('test', (7, 2), 'white')
        self.placePieces(pawn1, self.board.whitePieces)

        queen = self.board.getConvertedPiece(pawn1, 'Q', 'W')
        self.assertTrue(type(queen) == Queen)

        


class TestCheckLogic(unittest.TestCase):
    def setUp(self):
        self.g = GameHandler()
        self.board = Board()
        self.board.createBoard()

    def placePieces(self, piece, pieces):
        self.board.board[piece.position[0]][piece.position[1]].occupied = True
        self.board.board[piece.position[0]][piece.position[1]].whatPieceIsHere = piece
        pieces.append(piece)

    def testGetKing(self):
        self.board.initializePieces()
        king1 = Piece.getKing(self, self.board.whitePieces)
        king2 = Piece.getKing(self, self.board.blackPieces)

        self.assertTrue(type(king1) == King)
        self.assertTrue(type(king2) == King)

    def testCanOnlyMoveOutOfCheckWhenInCheck(self):
        self.g.p1Turn = True

        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)

        pawn = Pawn('test', (0, 6), 'white')
        self.placePieces(pawn, self.board.whitePieces)

        knight = Knight('test', (3, 2), 'white')
        self.placePieces(knight, self.board.whitePieces)
        
        rook = Rook('test', (7, 3), 'black')  
        self.placePieces(rook, self.board.blackPieces)

        self.assertFalse(pawn.move((1,6), self.board))
        self.assertTrue(knight.move((5,3), self.board))

    def testKingCanMoveOutOfCheck(self):
        king = King('test', (0, 3), 'white')
        self.placePieces(king, self.board.whitePieces)  

        rook = Rook('test', (7, 3), 'black')  
        self.placePieces(rook, self.board.blackPieces)

        self.assertTrue(king.inCheck(self.board.board, self.board.blackPieces))

        king.move((0, 4), self.board)

        self.assertFalse(king.inCheck(self.board.board, self.board.blackPieces))

    def testKingCantMoveBackwardsInCheck(self):
        king = King('test', (5, 3), 'white')
        self.placePieces(king, self.board.whitePieces)  

        rook = Rook('test', (7, 3), 'black')  
        self.placePieces(rook, self.board.blackPieces)

        king.move((4, 3), self.board)

        self.assertTrue(king.position, (5, 3)) 


    def testPieceMoveCantCauseCheck(self):
        self.g.p1Turn = True
        king = King('test', (0, 5), 'white')
        self.placePieces(king, self.board.whitePieces)  

        rook = Rook('test', (0, 1), 'black')
        self.placePieces(rook, self.board.blackPieces)

        bishop = Bishop('test', (0, 2), 'white')
        self.placePieces(bishop, self.board.whitePieces)

        self.assertTrue(bishop.causesCheck((1, 3), self.board))  
        self.assertFalse(bishop.move((1, 3), self.board))

    def testP1Wins(self):
        king = King('test', (0, 0), 'black')
        self.placePieces(king, self.board.blackPieces)

        rook = Rook('test', (5, 0), 'white')
        self.placePieces(rook, self.board.whitePieces)

        queen = Queen('test', (0, 2), 'white')
        self.placePieces(queen, self.board.whitePieces)

        self.g.p1Wins = self.g.isMated(self.board, self.board.blackPieces, self.board.whitePieces)
        self.assertTrue(self.g.p1Wins)

    def testP2Wins(self):
        king = King('test', (0, 0), 'white')
        self.placePieces(king, self.board.whitePieces)

        rook = Rook('test', (5, 0), 'black')
        self.placePieces(rook, self.board.blackPieces)

        queen = Queen('test', (0, 2), 'black')
        self.placePieces(queen, self.board.blackPieces)

        self.g.p2Wins = self.g.isMated(self.board, self.board.whitePieces, self.board.blackPieces)   
        self.assertTrue(self.g.p2Wins)

    def testPieceCanSaveKing(self):
        king1 = King('BK', (0,0), 'black')
        self.placePieces(king1, self.board.blackPieces)

        rook = Rook('BR', (2, 4), 'black')
        self.placePieces(rook, self.board.blackPieces)

        queen = Queen('WQ', (3,1), 'white')
        rook = Rook("WR", (5,0), 'white')

        self.placePieces(queen, self.board.whitePieces)
        self.placePieces(rook, self.board.whitePieces)

        self.assertTrue(king1.inCheck(self.board.board, self.board.whitePieces))
        self.assertFalse(king1.mated(self.board, self.board.blackPieces, self.board.whitePieces))


class TestGameHandler(unittest.TestCase):
    def setUp(self):
        self.g = GameHandler()
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.board = Board()
        self.board.createBoard()
        self.board.initializePieces()

    def testIsValidInputWithInvalidInput(self):
        input1 = "This is not valid input".split(" ")
        input2 = "A7 A6 A5".split()
        input3 = "A9 M2".split()

        self.assertFalse(self.g.isValidInput(input1, self.letters, self.numbers))
        self.assertFalse(self.g.isValidInput(input2, self.letters, self.numbers))
        self.assertFalse(self.g.isValidInput(input3, self.letters, self.numbers))

    def testIsValidInputWithValidInput(self):
        input1 = "D8 C7".split()
        input2 = "A7 A6".split()
        input3 = "H6 E3".split()

        self.assertTrue(self.g.isValidInput(input1, self.letters, self.numbers))
        self.assertTrue(self.g.isValidInput(input2, self.letters, self.numbers))
        self.assertTrue(self.g.isValidInput(input3, self.letters, self.numbers))

    def testParseInput(self):
        self.g.p1Turn = False
        self.assertEqual(self.g.parseInput(["B7", "B6"], self.letters, self.numbers, self.board.board), [(6, 1), (5, 1)])

    def testPlayerOneCantMoveBlackPiece(self):
        self.g.p1Turn = True
        self.assertEqual(self.g.parseInput(["B7", "B6"], self.letters, self.numbers, self.board.board), -1)

    def testPlayerTwoCantMoveWhitePiece(self):
        self.g.p1Turn = False
        self.assertEqual(self.g.parseInput(["A2", "A4"], self.letters, self.numbers, self.board.board), -1)


if __name__ == '__main__':
    unittest.main()
