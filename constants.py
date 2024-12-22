import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 750 
ROWS, COLS = 8, 8
CHESSBOARD_SIZE = 540
SQUARE_SIZE = CHESSBOARD_SIZE // COLS
WHITE, BEIGE, BROWN, GREEN, BLACK = (255, 255, 255), (240, 255, 230), (196, 164, 132), (0, 255, 0), (0, 0, 0)
LIGHT_BROWN = (210, 180, 140)  # Tan
DARK_BROWN = (78,53,36)     # Saddle Brown
CHOCOLATE = (137,81,41)     # Chocolate
SANDY_BROWN = (244, 164, 96)   # Sandy Brown
SIENNA = (160, 82, 45) 
# Piece images (ensure the paths are correct)
PIECE_IMAGES = {
    "Pawn_white": pygame.image.load("white-pawn.png"),
    "Rook_white": pygame.image.load("white-rook.png"),
    "Knight_white": pygame.image.load("white-knight.png"),
    "Bishop_white": pygame.image.load("white-bishop.png"),
    "Queen_white": pygame.image.load("white-queen.png"),
    "King_white": pygame.image.load("white-king.png"),
    "Pawn_black": pygame.image.load("black-pawn.png"),
    "Rook_black": pygame.image.load("black-rook.png"),
    "Knight_black": pygame.image.load("black-knight.png"),
    "Bishop_black": pygame.image.load("black-bishop.png"),
    "Queen_black": pygame.image.load("black-queen.png"),
    "King_black": pygame.image.load("black-king.png"),
}
