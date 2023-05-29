import pygame

class Inventory:
    def __init__(self):
        self.display = False
        self.image = pygame.image.load("Sprites/inventory.png") #512x128
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 128)
        self.status = False

    def render(self, display):
        display.blit(self.image,(0,576))

    def updateStatus(self, bool):
        self.status = bool
    
    def getStatus(self):
        return self.status