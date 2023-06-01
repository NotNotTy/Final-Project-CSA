import pygame
import math
from projectile import projectile
class Item:
    def __init__(self,image,dmg):
        self.display = False
        self.image = pygame.image.load(image)
        self.updatedImage = self.image #used to update
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 64)
        self.damage = dmg
        self.angle = 0 
        self.x = 0
        self.y = 0

    def getImage(self):
        return self.image
    
    def render(self,display):
        if ((self.angle % 90) != 0): #when rotating by 45 degrees, the surface has to expand. I did the math and calculated the difference
            display.blit(self.updatedImage,(self.x - abs(64-math.sqrt(8192)),self.y - abs(64-math.sqrt(8192)))) 
        else:
            display.blit(self.updatedImage,(self.x,self.y))

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
        if self.angle == x: #prevent looping
            pass
        else:
            self.angle = x
            loc = self.image.get_rect().topleft  #rot_image is not defined 
            rot_sprite = pygame.transform.rotate(self.image, self.angle)
            rot_sprite.get_rect().topleft = loc
            self.updatedImage = rot_sprite
            #rotated_image = pygame.transform.rotate(self.image, self.angle)
            #new_rect = rotated_image.get_rect(topleft = self.image.get_rect(topleft = (0,64)).topleft)
            #self.rect = new_rect
            #print(new_rect.topleft)
            #self.image = rotated_image

    def getOrientation(self):
        return self.angle







