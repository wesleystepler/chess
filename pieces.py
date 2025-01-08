import pygame
import os

class CheckerSquare(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, tile):
        super().__init__()
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos, y_pos]

    def occupied(self, pieces):
        for piece in pieces:
            if self.rect.colliderect(piece):
                return True
        return False
    
    def __str__(self):
        return f"Checker Square a position ({self.x_pos}, {self.y_pos})"