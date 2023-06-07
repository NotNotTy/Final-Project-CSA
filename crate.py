import pygame
import random

class crate(pygame.sprite.Sprite):
    def __init__(self, img, x ,y,n,r):
        super().__init__()
        self.image = pygame.Surface((64,64))
        self.image = pygame.image.load(img).convert()
        #self.rect = self.image.get_rect(topleft = (x,y))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.hitboxrect = pygame.Rect(0,0,192,192)
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
        self.x = x 
        self.y = y 
        self.type = n
        self.range = r

    def render(self,display):
        display.blit(self.image,(self.x,self.y))
       # screen.blit(self.hitbox, (self.hitboxrect.x - 64,0))

    def getHitboxRect(self):
        return self.hitboxrect

    def update(self,x,y):
        self.x += x
        self.y += y
        self.rect.x += x
        self.rect.y += y
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
        #print(self.rect.x)
    
    def setUpdate(self,x,y):
        self.x = x
        self.y = y
        self.rect.x == x
        self.rect.y == y
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
    
    def getType(self):
        return self.type

    def getRange(self):
        return self.range
    
    def editRange(self,r):
        self.range = r
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def loot(self,inventory):
        num = random.randrange(0,4) #however many items. the end condiiton is not inclusive
        print(num)
        if num == 0:
            inventory.addItem("sword")
        if num == 1:
            inventory.addItem("bow")
        if num == 2:
            inventory.addItem("bandage")
        if num == 3:
            inventory.addItem("firebook")

    
