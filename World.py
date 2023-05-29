import pygame
from cvslayout import import_cvs_layout
from tile import Tile
from tile import StaticTile
from npc import NPC
import random
class world_creator: #constructs the world
    def __init__(self,world_type,surface,x,y): #the constructor of python
        self.display_surface = surface
        plain_layout = import_cvs_layout(world_type['plain'])
        self.plain_layout_sprite = self.create_tile_group(plain_layout,'plain')
        rock_layout = import_cvs_layout(world_type['rock'])
        self.rock_layout_sprite = self.create_tile_group(rock_layout,'rock')
        self.objectList = [self.plain_layout_sprite,self.rock_layout_sprite]
        self.relativePositionX = x
        self.relativePositionY = y

        
    def create_tile_group(self,l,t):
        TILE_SIZE = 64
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(l):
            for column_index, val in enumerate(row):
                if val != '-1':
                    x = (column_index - 27) * TILE_SIZE #shifts the board to the middle x
                    y = (row_index - 27) * TILE_SIZE #the center is a translation of a 1:2 ratio (9,18)
          

                    if t == 'plain':
                        randomnum = random.randint(0,2)
                        if randomnum == 0:
                            texture = pygame.image.load('Sprites/grassdesign1.png')
                        elif randomnum == 1:
                            texture = pygame.image.load('Sprites/grassdesign2.png')
                        else:
                            texture = pygame.image.load('Sprites/grassdesign3.png')
                        #sprite = Tile(32,x,y)
                        sprite = StaticTile(TILE_SIZE,x,y,texture,'plain',(x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                        sprite_group.add(sprite)

                    if t == 'rock':
                       randomnum = random.randint(0,1)
                       if randomnum == 0:
                         texture = pygame.image.load('Sprites/rockdesign1.png')
                       else:
                           texture = pygame.image.load('Sprites/rockdesign2.png')
                       sprite = StaticTile(TILE_SIZE,x,y,texture,'rock', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)
        #for al in sprite_group.sprites():
            #print(al.get_coords())
        return sprite_group
    
    def getObjectList(self):
        return self.objectList
    
    def updateRelative(self,x,y):
        self.relativePositionX += x
        self.relativePositionY += y

    def getRelativeX(self):
        return self.relativePositionX
    
    def getRelativeY(self):
        return self.relativePositionY
    
    def run(self,textbox):
        for row_index, row in enumerate(textbox):
            if row.getStatus() == True:
                self.plain_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
                self.rock_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
                textbox.draw(self.display_surface)
            else:
                self.plain_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
                self.rock_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        #self.plain_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        #self.rock_layout_sprite.draw(self.display_surface) #draws the tile group on said surface

        #self.layout_sprite.update(1)
        pass

    def update_layout(self,x,y):
       self.plain_layout_sprite.update(x,y)
       self.rock_layout_sprite.update(x,y)