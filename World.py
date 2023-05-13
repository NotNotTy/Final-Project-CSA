import pygame
from cvslayout import import_cvs_layout
from tile import Tile
from tile import StaticTile
class world_creator: #constructs the world
    def __init__(self,world_type,surface): #the constructor of python
        self.display_surface = surface
        layout = import_cvs_layout(world_type['plain'])
        self.layout_sprite = self.create_tile_group(layout,'plain')
        #print(layout)

    def create_tile_group(self,l,t):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(l):
            for column_index, col in enumerate(row):
                if col != '-1':
                    x = column_index * 32
                    y = row_index * 32
          

                    if t == 'plain':
                        print('typefound')
                        texture = 'Sprites/grass.png'
                        sprite = Tile(32,x,y)
                        #sprite = StaticTile(32,x,y,texture)
                        sprite_group.add(sprite) #java conversion: creates a plain object with x and y coords, stores it in an 2d array :)
        return sprite_group


    def run(self):
        self.layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        self.layout_sprite.update(1)
        pass
