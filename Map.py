import pygame
import numpy as np


class Map:
    def __init__(self, length, width, tileAmt):
        self.length = length
        self.width = width
        self.tileAmt = tileAmt
        self.currentTile = 0
        self.tileBlueprints = [self.loadtile(i) for i in range(self.tileAmt)]

    def updateCurrentTile(self, player):
        if player.x < 0:
            player.x = 0
            if self.currentTile != 0:
                self.currentTile -= 1
                player.x = 480
        if player.x > 480:
            self.currentTile += 1
            player.x = 0
        if player.y < 0:
            self.currentTile -= 3
            player.y = 480
        if player.y > 480:
            self.currentTile += 3
            player.y = 0

    def loadtile(self, tileNum):
        data = open(f"tile#{tileNum}.csv")
        return np.loadtxt(data, delimiter=",")

    def blueprints(self):
        return self.tileBlueprints

    def createtile(self, screen):
        x, y = 0, 0
        for i in self.tileBlueprints[self.currentTile]:
            for j in i:
                if j == 0:
                    pygame.draw.rect(screen, 'brown', pygame.Rect(x, y, 60, 60))
                if j == 1:
                    pygame.draw.rect(screen, 'green', pygame.Rect(x, y, 60, 60))
                x += 60
            x = 0
            y += 60
