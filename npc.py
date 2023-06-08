import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, size, x ,y,surface,n,r):
        super().__init__()
        self.image = pygame.Surface((size,size))
        #self.rect = self.image.get_rect(topleft = (x,y))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.hitboxrect = pygame.Rect(0,0,192,192)
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
        self.image = surface
        self.type = n
        self.range = r



    def draw(self,screen):
        screen.blit(self.image,self.rect.center)
       # screen.blit(self.hitbox, (self.hitboxrect.x - 64,0))

    def getHitboxRect(self):
        return self.hitboxrect

    def update(self,x,y):
        self.rect.x += x
        self.rect.y += y
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
        #print(self.rect.x)
    
    def setUpdate(self,x,y):
        self.rect.x = x
        self.rect.y = y
        self.hitboxrect = self.hitboxrect.clamp(self.rect)
    
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
    
