import pygame
from cvslayout import import_cvs_layout
from tile import Tile
from tile import StaticTile
from npc import NPC
class world_creator: #constructs the world
    def __init__(self,world_type,surface): #the constructor of python
        self.display_surface = surface
        plain_layout = import_cvs_layout(world_type['plain'])
        self.plain_layout_sprite = self.create_tile_group(plain_layout,'plain')
        rock_layout = import_cvs_layout(world_type['rock'])
        self.rock_layout_sprite = self.create_tile_group(rock_layout,'rock')
        self.objectList = [self.plain_layout_sprite,self.rock_layout_sprite]

        
    def create_tile_group(self,l,t):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(l):
            for column_index, val in enumerate(row):
                if val != '-1':
                    x = (column_index - 9) * 32 #shifts the board to the middle x
                    y = (row_index - 18) * 32 #the center is a translation of a 1:2 ratio (9,18)
          

                    if t == 'plain':
                        texture = pygame.image.load('Sprites/grass.png')
                        #sprite = Tile(32,x,y)
                        sprite = StaticTile(32,x,y,texture,'plain',(x-640)//32,(y-352)//32)
                        sprite_group.add(sprite)

                    if t == 'rock':
                       texture = pygame.image.load('Sprites/rock.png')
                       sprite = StaticTile(32,x,y,texture,'rock', (x-640)//32,(y-352)//32)
                       sprite_group.add(sprite)
        #for al in sprite_group.sprites():
            #print(al.get_coords())
        return sprite_group
    
    def getObjectList(self):
        return self.objectList
    
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