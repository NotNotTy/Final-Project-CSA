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
        self.slot.append(InventorySlot("sword","Sprites/sword64.png", Item("Sprites/sword64.png",64)))
        self.slot.append(InventorySlot("bow","Sprites/bow64.png",Item("Sprites/bow64.png",64)))

    def render(self, display):
        TILE_SIZE = 64
        #print(self.slot)
        display.blit(self.image,(0,576))
        for index, slot in enumerate(self.slot):
            multipler = index + 1 #since indexing starts at 0
            #print(multipler)
            if multipler > 1:
                slot.render(display,(TILE_SIZE * multipler) + TILE_SIZE/2,608)
                #display.blit(slot.getImage(),((TILE_SIZE * multipler) + TILE_SIZE/2,608))
            else:
                slot.render(display,(TILE_SIZE * multipler),608)
                #display.blit(slot.getImage(),((TILE_SIZE * multipler),608))

    def updateStatus(self, bool):
        self.status = bool
    
    def getStatus(self):
        return self.status
    
    def getInventoryList(self):
        return self.slot