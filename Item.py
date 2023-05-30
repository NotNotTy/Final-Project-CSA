import pygame
from projectile import projectile
class Item:
    def __init__(self,image,dmg):
        self.display = False
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 64)
        self.damage = dmg
        self.x = 0
        self.y = 0

    def getImage(self):
        return self.image
    
    def render(self,display):
        display.blit(self.image,(self.x,self.y))

    def set(self,x,y):
        self.x = x
        self.y = y

    def update(self,x,y):
        self.x += x
        self.y += y






