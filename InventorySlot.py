import pygame
import pygame.font
class InventorySlot:
    def __init__(self,itemID,image,item):
        pygame.font.init()
        self.display = False
        self.itemID = itemID
        self.amount = 0
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 64)
        self.font = pygame.font.Font('freesansbold.ttf',16)
        self.item = item
        self.selected = False

    def getImage(self):
        return self.image
    def getID(self):
        return self.itemID
    def getSelection(self):
        return self.selected
    
    def updateSelection(self,bool):
        self.selected = bool
    
    def renderObject(self,display):
        self.item.render(display)

    def setObject(self,x,y):
        self.item.set(x,y)
    
    def updateObject(self,x,y):
        self.item.update(x,y)

    def getObject(self):
        return self.item



    #def updateObjecet(self,x,y):
        #self.item.update()

    def render(self, display,x,y):
        TILE_SIZE = 64
        if self.selected:
            text = self.font.render(str(self.amount), True, (255,0,0))
        else:
            text = self.font.render(str(self.amount), True, (0,0,0))
        display.blit(self.image, (x,y))
        display.blit(text,(x + TILE_SIZE,y + TILE_SIZE))
        