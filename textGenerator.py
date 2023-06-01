import pygame
from pygame.locals import *
class TextGenerator():
    pygame.font.init()

    def __init__(self, x, y, t,f):
        self.font = pygame.font.Font(f, 16)
        self.text = self.font.render(t, True,0)
        self.rect = self.text.get_rect(topleft = (x,y))
        self.x = x
        self.y = y
    
    def getText(self):
        return self.text

    def editText(self, t):
        text = t
        self.text = self.font.render(text, True,0)

    def update(self,x,y):
        self.x += x
        self.y += y
        self.rect = self.rect.move(x,y)

    def updateRect(self,x,y):
        self.rect.update(self.text.get_rect(topleft = (x,y)))

    def render(self,display,x,y):
        display.blit(self.text,(x,y))
    
    def getTextRect(self):
        return self.rect
