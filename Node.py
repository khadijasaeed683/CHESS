
from constants import SQUARE_SIZE
import pygame 

class Node:
    def __init__(self, position, rect):
        self.position = position  # (row, col)
        self.piece = None         # Stores the piece on the square
        self.rect = rect          # Pygame rectangle for rendering
        self.image = None         # Image for the piece
        self.color = None
        self.has_moved = False
    def set_piece(self, piece, image,color):
        self.piece = piece
        self.image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
        self.color = color

    def remove_piece(self):
        self.piece = None
        self.image = None
        self.color = None
        self.has_moved = False

