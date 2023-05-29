import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, size, x ,y,surface):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))
        self.image = surface
        self.relativeX = x
        self.relativeY = y

    def update(self,x,y):
        self.rect.x += x
        self.rect.y += y
        #print(self.rect.x)
    def updateRelative(self,x,y):
        self.relativeX += x
        self.relativeY += y

    def render(self,display):
        display.blit(self.image,(self.rect.x,self.rect.y))

    def getRelativeX(self):
        return self.relativeX
    
    def getRelativeY(self):
        return self.relativeY
    
    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y
    