import pygame
from cvslayout import import_cvs_layout
from tile import StaticTile
from npc import NPC
import random
class world_creator: #constructs the world
    def __init__(self,world_type,surface,x,y): 
        self.display_surface = surface
        plain_layout = import_cvs_layout(world_type['plain'])
        self.plain_layout_sprite = self.create_tile_group(plain_layout,'plain')

        rock_layout = import_cvs_layout(world_type['rock'])
        self.rock_layout_sprite = self.create_tile_group(rock_layout,'rock')

        sand_layout = import_cvs_layout(world_type['sand'])
        self.sand_layout_sprite = self.create_tile_group(sand_layout,'sand')

        snow_layout = import_cvs_layout(world_type['snow'])
        self.snow_layout_sprite = self.create_tile_group(snow_layout,'snow')

        water_layout = import_cvs_layout(world_type['water'])
        self.water_layout_sprite = self.create_tile_group(water_layout,'water')

        tree_layout = import_cvs_layout(world_type['tree'])
        self.tree_layout_sprite = self.create_tile_group(tree_layout,'tree')

        cactus_layout = import_cvs_layout(world_type['cactus'])
        self.cactus_layout_sprite = self.create_tile_group(cactus_layout,'cactus')

        wood_plank_layout = import_cvs_layout(world_type['wood_plank'])
        self.wood_plank_layout_sprite = self.create_tile_group(wood_plank_layout,'wood_plank')

        grass_weed_layout = import_cvs_layout(world_type['grass_weed'])
        self.grass_weed_layout_sprite = self.create_tile_group(grass_weed_layout,'grass_weed')

        ice_spike_layout = import_cvs_layout(world_type['ice_spike'])
        self.ice_spike_layout_sprite = self.create_tile_group(ice_spike_layout,'ice_spike')




        self.objectList = [self.plain_layout_sprite,self.rock_layout_sprite,self.sand_layout_sprite,self.water_layout_sprite,self.snow_layout_sprite,self.wood_plank_layout_sprite,self.cactus_layout_sprite,self.tree_layout_sprite,self.ice_spike_layout_sprite,self.grass_weed_layout_sprite]
        self.collideable = [self.rock_layout_sprite,self.water_layout_sprite,self.tree_layout_sprite,self.ice_spike_layout_sprite]
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
          
                    if t == 'rock':
                       randomnum = random.randint(0,1)
                       if randomnum == 0: texture = pygame.image.load('Sprites/rockdesign1.png').convert()
                       else:  texture = pygame.image.load('Sprites/rockdesign2.png').convert()
                       sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'rock', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)

                    if t == 'water':
                       randomnum = random.randint(0,2)
                       if randomnum == 0: texture = pygame.image.load('Sprites/water1.png').convert_alpha()
                       elif randomnum == 1: texture = pygame.image.load('Sprites/water2.png').convert_alpha()
                       else: texture = pygame.image.load('Sprites/water3.png').convert_alpha()

                       sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'water', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)

                    if t == 'wood_plank':
                       
                       texture = pygame.image.load('Sprites/wood_plank1.png').convert_alpha()
                       sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'wood_plank', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)

                    if t == 'plain':
                        randomnum = random.randint(0,3)
                        if randomnum == 0:  texture = pygame.image.load('Sprites/grassdesign1.png').convert()
                        elif randomnum == 1: texture = pygame.image.load('Sprites/grassdesign2.png').convert()
                        else: texture = pygame.image.load('Sprites/grassdesign3.png').convert()
                        #sprite = Tile(32,x,y)
                        sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'plain',(x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                        sprite_group.add(sprite)

                    if t == 'sand':
                       randomnum = random.randint(0,2)
                       if randomnum == 1: texture = pygame.image.load('Sprites/sand1.png').convert()
                       elif randomnum == 2: texture = pygame.image.load('Sprites/sand2.png').convert()
                       else: texture = pygame.image.load('Sprites/sand3.png').convert()
                       sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'sand', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)

                    if t == 'snow':
                        randomnum = random.randint(0,2)
                        if randomnum == 1: texture = pygame.image.load('Sprites/snow1.png').convert()
                        else: texture = pygame.image.load('Sprites/snow2.png').convert()
                        sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'snow', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                        sprite_group.add(sprite)

                    if t == 'ice_spike':
                        texture = pygame.image.load('Sprites/iceSpike.png').convert_alpha()
                        sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'ice_spike', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                        sprite_group.add(sprite)

                    if t == 'cactus':
                       texture = pygame.image.load('Sprites/cactus1.png').convert_alpha()
                       sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'cactus', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)

                    if t == "grass_weed":
                        randomnum = random.randint(0,1)
                        if randomnum == 1: texture = pygame.image.load('Sprites/grassweed.png').convert_alpha()
                        else: texture = pygame.image.load('Sprites/grassweed2.png').convert_alpha()
                        sprite = StaticTile(TILE_SIZE,TILE_SIZE,x,y,texture,'grass_weed', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                        sprite_group.add(sprite)

                    if t == 'tree':
                       texture = pygame.image.load('Sprites/tree1.png').convert_alpha()
                       sprite = StaticTile(TILE_SIZE,TILE_SIZE*2,x,y,texture,'tree', (x-576)//TILE_SIZE,(y-320)//TILE_SIZE)
                       sprite_group.add(sprite)
        #for al in sprite_group.sprites():
            #print(al.get_coords())
        return sprite_group
    
    def getObjectList(self):
        return self.objectList
    
    def getCollideableList(self):
        return self.collideable
    
    def updateRelative(self,x,y):
        self.relativePositionX += x
        self.relativePositionY += y

    def getRelativeX(self):
        return self.relativePositionX
    
    def getRelativeY(self):
        return self.relativePositionY
    
    def run(self):
        for list in self.objectList:
                list.draw(self.display_surface)
        #self.plain_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        #self.rock_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        #self.plain_layout_sprite.draw(self.display_surface) #draws the tile group on said surface
        #self.rock_layout_sprite.draw(self.display_surface) #draws the tile group on said surface

        #self.layout_sprite.update(1)

    def update_layout(self,x,y):
       for list in self.objectList:
           list.update(x,y)
       #self.plain_layout_sprite.update(x,y)
       #self.rock_layout_sprite.update(x,y)