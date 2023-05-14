import pygame
from pygame.locals import *
class TextGenerator():
    pygame.font.init()

    def __init__(self, x, y, t,f):
        self.font = pygame.font.Font(f, 16)
        self.text = self.font.render(t, True,0)
        self.rect = self.text.get_rect(topleft = (x,y))
    
    def getText(self):
        return self.text
    
    def getTextRect(self):
        return self.rect
