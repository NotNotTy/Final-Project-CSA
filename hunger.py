import pygame
import math

class hunger:
    def __init__(self,border,x,y,width,height):
        self.green = pygame.Rect(x,y,width,height)
        self.red = pygame.Rect(x,y,width,height)
        self.border = pygame.image.load(border).convert_alpha()
        self.rect = self.border.get_rect()
        self.rect.topleft = (x - 32, y - 30)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self,display):
        display.blit(self.border,self.rect)
        pygame.draw.rect(display,(255,0,0),self.red)
        pygame.draw.rect(display,(0,255,0),self.green)

    def update(self,startinghunger,currenthunger):
        percentage = currenthunger/startinghunger
        if percentage >= 1:
            self.green = pygame.Rect(self.x,self.y,self.width,self.height)
        else:
            difference = self.width * percentage
            change = self.width - difference
            self.green = pygame.Rect(self.x,self.y,difference,self.height)

    
