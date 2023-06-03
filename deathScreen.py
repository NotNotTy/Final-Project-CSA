import pygame

class deathScreen:
    def __init__(self,playagain,exit,message):
        self.message = pygame.image.load(message)
        self.messagerect = self.message.get_rect(topleft = (0,0))
        self.playagain = pygame.image.load(playagain)
        self.playagainrect = self.playagain.get_rect(topleft = (0,0))
        self.exit = pygame.image.load(exit)
        self.exitRect = self.exit.get_rect(topleft = (0,0))


    def render(self,display):
        LENGTH = 1216
        WIDTH = 704
        display.blit(self.message,((LENGTH/2) - (384/2),WIDTH/2 - (384/2) - 96)) #384 is width and height. All of this is manually ajusted
        display.blit(self.playagain,((LENGTH/2) - (96/2) - 320,(WIDTH/2) - (96/2) + 96))
        display.blit(self.exit,((LENGTH/2) - (96/2) + 224,(WIDTH/2) - (96/2) + 96))
        #attatches the rects to the surfacees
        self.exitRect = self.exitRect.clamp(self.exit.get_rect())
        self.playagainrect = self.playagainrect.clamp(self.playagain.get_rect())
        #this is neccesary to move the rects because I did not create a variable to track the surface position
        self.playagainrect = self.playagainrect.move((LENGTH/2) - (96/2) - 320,(WIDTH/2) - (96/2) + 96)
        self.exitRect = self.exitRect.move((LENGTH/2) - (96/2) + 224,(WIDTH/2) - (96/2) + 96)

    def getExitRect(self):
        return self.exitRect
    
    def getAgainRect(self):
        return self.playagainrect