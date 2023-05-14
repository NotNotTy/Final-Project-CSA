import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, size, x ,y,surface,n,r):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.hitbox = pygame.Surface((96,96))
        self.image.fill('grey')
        #self.rect = self.image.get_rect(topleft = (x,y))
        self.rect = self.hitbox.get_rect(topleft = (x,y))
        print(self.image.get_rect().centerx)
        print(self.image.get_rect().centerx)
        self.image = surface
        self.type = n
        self.range = r




    def update(self,x,y):
        self.rect.x += x
        self.rect.y += y
        #print(self.rect.x)
    
    def setUpdate(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def getType(self):
        return self.type

    def getRange(self):
        return self.range

    def getCenter(self):
        return self.rect.center
    
    def editRange(self,r):
        self.range = r
        
    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y
    
