import pygame
from InventorySlot import InventorySlot
from Item import Item
from projectile import projectile
class Inventory:
    def __init__(self):
        self.display = False
        self.slot = []
        self.image = pygame.image.load("Sprites/inventory.png") #512x128
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 128)
        self.status = False
        self.selectionnum = 0
        self.previousselection = 0
        self.slot.append(InventorySlot("sword","Sprites/sword64.png", Item("Sprites/sword64rotated.png",64)))
        self.slot.append(InventorySlot("bow","Sprites/bow64.png",Item("Sprites/bow64rotated.png",64)))

    def render(self, display):
        TILE_SIZE = 64
        #print(self.slot)
        display.blit(self.image,(0,576))
        if self.selectionnum == -1: #if nothing is chosen, pass
            pass
        else:
            if self.slot[self.selectionnum]: #if one of the slots has been selected, update it to true
                (self.slot[self.selectionnum]).updateSelection(True)

        for index, slot in enumerate(self.slot):
            multipler = index + 1 #since indexing starts at 0
            #print(multipler)
            if multipler > 1:
                slot.render(display,(TILE_SIZE * multipler) + TILE_SIZE/2,608)
                #display.blit(slot.getImage(),((TILE_SIZE * multipler) + TILE_SIZE/2,608))
            else:
                slot.render(display,(TILE_SIZE * multipler),608)
                #display.blit(slot.getImage(),((TILE_SIZE * multipler),608))
    

    #updates the selection status on all slot objects
    def updateSelection(self,x):
        #prevent out of bounds errors
        self.selectionnum += x
        print(len(self.slot))
        #add or subtract 1 to keep from going out of bounds
        if self.selectionnum >= len(self.slot):
            self.selectionnum -= 1
        if self.selectionnum < -1:
            self.selectionnum += 1

        print(self.selectionnum)
        if self.selectionnum == -1: #if we have nothing selected
            for index,slot in enumerate(self.slot):
                slot.updateSelection(False) #have all slots be unselected
        else:
            self.slot[self.selectionnum - x].updateSelection(False) #update the previous selection

    def getSeleciton(self): #returns the selection number
        return self.selectionnum
    
    def getCurrentObject(self): #returns the selected object
        return self.slot[self.previousselection]

    def onEnter(self): #once something has been selected
        self.previousselection = self.selectionnum

    def updateStatus(self, bool): #runs everytime the inventory is opened
        self.selectionnum = 0
        for index,slot in enumerate(self.slot):
            slot.updateSelection(False)
        self.status = bool
    
    def getStatus(self):
        return self.status
    
    def getInventoryList(self):
        return self.slot