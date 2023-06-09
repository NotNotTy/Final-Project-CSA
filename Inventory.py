import pygame
from InventorySlot import InventorySlot
from Item import Item
from projectile import projectile
class Inventory:
    def __init__(self):
        self.display = False
        self.slot = []
        self.image = pygame.image.load("Sprites/inventory.png").convert_alpha() #512x128
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 128)
        self.status = False
        self.selectionnum = 0
        self.previousselection = 0
        #self.slot.append(InventorySlot("sword","Sprites/sword64.png", Item("Sprites/sword64rotated.png",64)))
        #self.slot.append(InventorySlot("bow","Sprites/bow64.png",Item("Sprites/bow64rotated.png",64)))

    def render(self, display):
        TILE_SIZE = 64
        #print(self.slot)
        display.blit(self.image,(0,576)) #renders the template
        for index,slot in enumerate(self.slot): #if we run out of an item, remove it
            if slot.getAmount() <= 0:
                self.slot.remove(slot)
                self.selectionnum == 0


        if len(self.slot) != 0:  #if there is something in our inventory
            if self.selectionnum == -1: #if nothing is chosen, pass
                pass
            else:
                if self.selectionnum >= len(self.slot): #if we are out of bounds because an item at the end has been used
                    self.selectionnum = -(1 + (self.selectionnum - len(self.slot))) #go down one from the item list
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
        if len(self.slot) != 0: #if there is nothing in inventoyr, do not run
            self.selectionnum += x
            print(len(self.slot))
            #add or subtract 1 to keep from going out of bounds
            if self.selectionnum >= len(self.slot):
                self.selectionnum -= 1
            if self.selectionnum < -1:
                self.selectionnum += 1

            if self.selectionnum == -1: #if we have nothing selected
                for index,slot in enumerate(self.slot):
                    slot.updateSelection(False) #have all slots be unselected
            else:
                self.slot[self.selectionnum - x].updateSelection(False) #update the previous selection

    def getSeleciton(self): #returns the selection number
        if len(self.slot) != 0:
            return self.selectionnum
        else:
            return None
    

    def getCurrentObject(self): #returns the selected object
        return self.slot[self.previousselection]
    

    def onEnter(self): #once something has been selected
        self.previousselection = self.selectionnum

    def updateStatus(self, bool): #runs everytime the inventory is opened
        self.selectionnum = self.previousselection
        for index,slot in enumerate(self.slot):
            slot.updateSelection(False)
        self.status = bool
    
    def getStatus(self):
        return self.status
    
    def removeItem(self, x):
        self.slot.remove(x)
    
    def getInventoryList(self):
        return self.slot
    
    def addItem(self,item):
        duplicate = False
        if item == "sword":
            for index, slot in enumerate(self.slot): #checking for duplicate
                if slot.getID() == "sword":
                    slot.updateAmount(1)
                    duplicate = True
            if not duplicate:
                self.slot.append(InventorySlot("sword","Sprites/sword64.png", Item("Sprites/sword64rotated.png",64),1,30))
        elif item == "bow":
            for index, slot in enumerate(self.slot): #checking for duplicate
                if slot.getID() == "bow":
                    slot.updateAmount(1)
                    duplicate = True
            if not duplicate:
                 self.slot.append(InventorySlot("bow","Sprites/bow64.png",Item("Sprites/bow64rotated.png",64),1,50))
        elif item == "arrow":
            for index, slot in enumerate(self.slot): #checking for duplicate
                if slot.getID() == "arrow":
                    slot.updateAmount(10)
                    duplicate = True
            if not duplicate:
                 self.slot.append(InventorySlot("arrow","Sprites/arrow64.png",Item("Sprites/arrow64.png",64),10,50))

        elif item == "bandage":
            for index, slot in enumerate(self.slot): #checking for duplicate
                if slot.getID() == "bandage":
                    slot.updateAmount(1)
                    duplicate = True
            if not duplicate:
                 self.slot.append(InventorySlot("bandage","Sprites/bandage.png",Item("Sprites/bandage.png",64),1,200))
        elif item == "firebook":
            for index, slot in enumerate(self.slot): #checking for duplicate
                if slot.getID() == "firebook":
                    slot.updateAmount(1)
                    duplicate = True
            if not duplicate:
                 self.slot.append(InventorySlot("firebook","Sprites/firebook.png",Item("Sprites/firebook.png",64),1,30))

    def reset(self):
        self.slot = []