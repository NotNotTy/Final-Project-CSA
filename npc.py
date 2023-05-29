import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, size, x ,y,surface,n,r):
        super().__init__()
        self.image = pygame.Surface((size * 3,size * 3))
        self.hitbox = pygame.Surface((192,192))
        self.image.fill('grey')
        #self.rect = self.image.get_rect(topleft = (x,y))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.hitboxrect = self.hitbox.get_rect(topleft = (x,y))
        print(self.image.get_rect().centerx)
        print(self.image.get_rect().centerx)
        self.image = surface
        self.type = n
        self.range = r



    def draw(self,screen):
        screen.blit(self.image,self.rect.center)
       # screen.blit(self.hitbox, (self.hitboxrect.x - 64,0))



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
    
