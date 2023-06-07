import pygame
import pygame.font
class InventorySlot:
    def __init__(self,itemID,image,item,amount,durability):
        pygame.font.init()
        LENGTH = 1216
        WIDTH = 704
        TILE_SIZE = 64
        self.display = False
        self.itemID = itemID
        self.amount = amount
        self.percantage = 1
        self.width = 64
        self.height = 20
        self.green = pygame.Rect(LENGTH/2 - (TILE_SIZE * 1.5),WIDTH/2 + self.width  - (TILE_SIZE * 0.5),self.width,self.height)
        self.red = pygame.Rect(LENGTH/2 - (TILE_SIZE * 1.5),WIDTH/2 + self.width  - (TILE_SIZE * 0.5),self.width,self.height)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 64)
        self.font = pygame.font.Font('freesansbold.ttf',16)
        self.item = item
        self.selected = False
        self.startingDurability = durability
        self.durability = durability
        self.durabilityStatus = True

    def getImage(self):
        return self.image
    def getID(self):
        return self.itemID
    def getSelection(self):
        return self.selected
    
    def updateSelection(self,bool):
        self.selected = bool

    def updateDurability(self,x):
        LENGTH = 1216
        WIDTH = 704
        TILE_SIZE = 64
        print(self.durability)
        if (x + self.durability) <= 0 and self.amount > 1: #if we run out of durability but still have the item
            self.durability = self.startingDurability
            self.amount -= 1
        elif (x + self.durability) <= 0 and self.amount <= 1: #if we run out of durability and dont have anymore items
            self.durabilityStatus = False
        else: #if we arent out yet
            self.durability += x

        #sets the durability
        self.percantage = self.durability/self.startingDurability
        if self.percantage == 1:
            self.green = pygame.Rect(LENGTH/2 - (TILE_SIZE * 1.5),WIDTH/2 + self.width  - (TILE_SIZE * 0.5),self.width,self.height)
        else:
            #print(64 * self.percantage)
            difference = self.width * self.percantage
            self.green = pygame.Rect(LENGTH/2 - (TILE_SIZE * 1.5),WIDTH/2 + self.width  - (TILE_SIZE * 0.5),difference,self.height)
       

    def geDurability(self):
        return self.durability
    
    def getDurabilityStatus(self):
        return self.durabilityStatus
    
    def renderObject(self,display):
        self.item.render(display)

    def setObject(self,x,y):
        self.item.set(x,y)
    
    def updateObject(self,x,y):
        self.item.update(x,y)

    def getObject(self):
        return self.item
    
    def getObjectX(self):
        return (self.item).getX()
    
    def getObjectY(self):
        return (self.item).getY()
    
    def updateAmount(self,x):
        self.amount += x
            

    def getAmount(self):
        return self.amount
    
    



    #def updateObjecet(self,x,y):
        #self.item.update()

    def render(self, display,x,y):
        TILE_SIZE = 64
        if self.selected:
            pygame.draw.rect(display,(255,0,0),self.red)
            pygame.draw.rect(display,(0,255,0),self.green)
        if self.selected:
            text = self.font.render(str(self.amount), True, (255,0,0))
        else:
            text = self.font.render(str(self.amount), True, (0,0,0))
        display.blit(self.image, (x,y))
        display.blit(text,(x + TILE_SIZE,y + TILE_SIZE))
        