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
        self.angle = 0

    def getImage(self):
        return self.image
    
    def render(self,display):
        display.blit(pygame.transform.rotate(self.image,self.angle),(self.x,self.y))

    def set(self,x,y):
        self.x = x
        self.y = y

    def update(self,x,y):
        self.x += x
        self.y += y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def changeOrientation(self, x):
        self.angle = x
        #rotated_image = pygame.transform.rotate(image, angle)
    #new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)







