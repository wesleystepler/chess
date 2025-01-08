from board import Board
from game_handler import GameHandler

gameBoard = Board()
gameBoard.createBoard()
gameBoard.initializePieces()

handler = GameHandler()

print("------------------------------------------------------")
print()
print("Welcome! Please read the brief instructions below:")
print()
print("HOW TO PLAY:")
print()
print("Each square on the board is designated a letter and a number as its coordinate")
print("(e.g., A1, B4, G5, etc.). To move a piece, you will type two letter/number coordinates,")
print("separated by a space. The first is the current location of the piece you want to move,")
print("the second is the position you want to move that piece to. For example, to move a pawn")
print("from square A7 to A5, you simply type, 'A7 A5'.") 
print("If you want to castle, and it is legal to do so, simply input 'CASTLE'.")
print()
print("PIECE REFERENCE:")
print("B/W: Black/White.  P: Pawn.  R: Rook.  k:  Knight.  B: Bishop. K: King.  Q: Queen.")
print("------------------------------------------------------")
print()
input("Ready to play? Press ENTER to begin!")
print()

while not handler.gameOver():
    handler.takeTurn(gameBoard)

if handler.p1Wins:
    print("Checkmate!")
    print("Player 1 Wins!")
    exit()

if handler.p2Wins:
    print("Checkmate!")
    print("Player 2 Wins!")
    exit()
