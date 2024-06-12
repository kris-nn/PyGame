import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = 1
        self.name = name
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Обработка сквозного прохода через стены
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        elif self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
