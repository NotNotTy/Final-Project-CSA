import pygame
class textbox(pygame.sprite.Sprite):
    def __init__(self,size,x,y,surface,t,s):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))
        self.image = surface
        self.type = t
        self.status = s

    def updateStatus(self,s):
        self.status = s

    def getStatus(self):
        return self.status
    
    def hide(self):
        self.rect.width = 0
        self.rect.height = 0

