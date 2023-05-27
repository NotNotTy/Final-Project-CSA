import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Player:
    def __init__(self, x, y):
        self.x = x * 60
        self.y = y * 60

    def moveX(self, x):
        self.x += x

    def moveY(self, y):
        self.y += y

    def draw(self, screen):
        pygame.draw.rect(screen, 'blue', pygame.Rect(self.x, self.y, 60, 60))

    def update(self, map, keys):
        if keys[K_UP]:
            self.moveY(-60)
        elif keys[K_DOWN]:
            self.moveY(60)
        elif keys[K_RIGHT]:
            self.moveX(60)
        elif keys[K_LEFT]:
            self.moveX(-60)
        map.updateCurrentTile(self)





