import pygame

class enemy:
    def __init__(self,sprite,health,damage,startx,starty,endx,endy,screen):
        self.image = pygame.Surface((64,64))
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.topleft = (startx,starty)
        self.health = health
        self.damage = damage
        self.screen = screen
        self.x = startx
        self.y = starty
        self.eyesightRect = pygame.draw.line(self.screen,(0,0,0),(self.x,self.y),(endx,endy),10)

    def render(self):
        self.screen.blit(self.image,(self.x,self.y))
        self.eyesightRect
        #display.blit(self.image,(self.x,self.y))

    def update(self,x,y):
        #print(self.x)
        self.x += x 
        self.y += y
        #self.rect= self.rect.move(x,y)
        self.eyesightRect = self.eyesightRect.move(x,y)

    def setTrajectory(self,end): #draws a line, if the line collides with something, then stop
        self.eyesightRect = pygame.draw.line(self.screen,(0,0,0),(self.x,self.y),end,10)
        #print(self.eyesightRect.x,self.eyesightRect.y)
        #self.screen.blit(self.image, (self.eyesightRect.x +64,self.eyesightRect.y +64))
        #pygame.draw.line(self.screen,(0,0,0),(self.x,self.y),end,10)