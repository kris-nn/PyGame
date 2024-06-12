import pygame
import random
from constants import BONUS_COLORS

class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = random.choice(BONUS_COLORS)
        self.image = pygame.Surface([20, 20])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
