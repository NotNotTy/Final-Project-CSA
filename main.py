import pygame
from pygame.locals import *
from sys import exit
from World import world_creator
from player import Player
from game_data import data
from npc import NPC
from textbox import textbox
from textGenerator import TextGenerator
from Inventory import Inventory
pygame.init()
pygame.font.init()
LENGTH = 1216
WIDTH = 704
screen = pygame.display.set_mode((LENGTH,WIDTH)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/character64.png") #fill this
npcImg = pygame.image.load("Sprites/character64.png")
textboxImg = pygame.image.load("Sprites/textbox2.png")
clock = pygame.time.Clock() #clock
TILE_SIZE = 64 #each tile is 32x32 big
FPS = 60 #pretty self explainitory
CAMERA_EDGE_X = LENGTH -  (TILE_SIZE * 1) #the edges are where the world will start to shift to give the impression that the camera is following the player. Multipler 8 
CAMERA_EDGE_Y = WIDTH - (TILE_SIZE * 1) # 4
START_COORDSX = 512 #start coordinates, used to keep the original position in a constant
START_COORDSY = 320
NPC_STARTCOORDSX = 768
NPC_STARTCOORDSY = 384
TEXTBOX_COORDSX = 100
TEXTBOX_COORDSY = 100
SPEED = 4 #speed of the player/world
TEXTBOX_SPRITE_WIDTH = 576 #used for translating the box in the middle
world = world_creator(data,screen,START_COORDSX,START_COORDSY) #generates the world 
player1 = Player(TILE_SIZE,START_COORDSX,START_COORDSY,playerImg)
npc1 = NPC(TILE_SIZE,NPC_STARTCOORDSX,NPC_STARTCOORDSY,npcImg,'npc',False)
npc2 = NPC(TILE_SIZE,NPC_STARTCOORDSX + 128,NPC_STARTCOORDSY,npcImg,'npc',False)
textbox1 = textbox(TILE_SIZE,(LENGTH/2) - (384/2),player1.getY() + 7 * TILE_SIZE,textboxImg,'textbox',False)
text = TextGenerator(START_COORDSX,START_COORDSY - 64,'press E to interact','freesansbold.ttf')
inventory = Inventory()
all_sprites_list = pygame.sprite.Group()
npc_sprite_list = pygame.sprite.Group()
textbox_sprite_list = pygame.sprite.Group()
#all_sprites_list.add(player1)
all_sprites_list.add(npc1,npc2)
npc_sprite_list.add(npc1,npc2)
textbox_sprite_list.add(textbox1)
velocityX = 0
velocityY = 0
direction = 0
keyUp = False
collisionKey = 0
keyDown = False
running = True






#def updateSmooth():
    #player1.update(2,0)
    #all_sprites_list.draw(screen)
    
    #pygame.time.delay(500)



def get_tile(): #returns the coordinate position of the player
    coords = [(player1.getRelativeX() - START_COORDSX)//TILE_SIZE,(player1.getRelativeY()-START_COORDSY)//TILE_SIZE]
    #print(playerXRelative//TILE_SIZE,playerYRelative//TILE_SIZE)
    #print(playerXRelative,playerYRelative)
    print(coords)

#manually updates the direction based on the parameters
def CollisionUpdateDirectionX(r):
    global direction
    global velocityX
    direction = r
    velocityX = 0 #reset velocity to avoid extra inputs
    world.update_layout(SPEED  * direction,0) #keep moving at speed until we are on a tile
    world.updateRelative(-SPEED * direction,0) #keep moving at speed until we are tile
    player1.updateRelative(-SPEED * direction,0)
    all_sprites_list.update(SPEED  * direction,0)#keep moving at speed until we are tile

#manually updates the direction based on the parameters
def CollisionUpdateDirectionY(r):
    global direction
    global velocityY
    velocityY = 0
    direction = r
    world.update_layout(0,-SPEED  * direction) #keep moving at speed until we are on a tile
    world.updateRelative(0,-SPEED * direction) #keep moving at speed until we are on a tile
    player1.updateRelative(0,-SPEED * direction)
    all_sprites_list.update(0,SPEED  * direction) #keep moving at speed until we are on a tile

def collision(): #checks if theres a collision
    global keyDown
    global direction
    global collisionKey
    interactable()
    list = world.getObjectList()
    for row_index, row in enumerate(list[1]):
        if pygame.sprite.collide_rect(player1, row):
            print(collisionKey)
            if (world.getRelativeX() % TILE_SIZE != 0):
                if collisionKey == 1: #the D key
                 CollisionUpdateDirectionX(1)
                elif collisionKey == 2: #the A key
                 CollisionUpdateDirectionX(-1)
            elif (world.getRelativeY() % TILE_SIZE != 0):
                if collisionKey == 3: #the W key
                 CollisionUpdateDirectionY(-1)
                elif collisionKey == 4: #the S key
                 CollisionUpdateDirectionY(1)
                
            #elif (keyDown and world.getRelativeY() % TILE_SIZE != 0)
            else:
                collisionKey = 0 #reset everything
                keyDown = False
                direction = 0
            print(row.getType())


def interactable(): #loops through every collideable object
    for row in enumerate(npc_sprite_list):
         if pygame.sprite.collide_rect(player1, row[1]):
            text.updateRect(player1.getX(),player1.getY()-TILE_SIZE)
            screen.blit(text.getText(),text.getTextRect())
            row[1].editRange(True)
            #print(row[1].getRange())
         else:
             row[1].editRange(False)
             #print(row[1].getRange())


def player(): #draws the player
    global direction
    global velocityX #the speed of the player dictated by input
    global velocityY #the speed of the player dictated by input
    global keyUp #if we let go of the movement keys
    player1.updateRelative(velocityX,velocityY) #here just to keep track of the player, is basically the asme thing as worldrelative
    world.updateRelative(velocityX,velocityY) #takes in user input and moves when held
    world.update_layout(-velocityX,velocityY) #takes in user input and moves when held
    all_sprites_list.update(-velocityX,-velocityY)#keep moving at speed until we are tile
    if ((world.getRelativeX() % TILE_SIZE) != 0 and keyUp): #if we are not on a tile and we are not holding a key, reajust to a tile
        velocityX = 0 #reset velocity to avoid extra inputs
        world.update_layout(-SPEED  * direction,0) #keep moving at speed until we are on a tile
        world.updateRelative(SPEED * direction,0) #keep moving at speed until we are tile
        player1.updateRelative(SPEED * direction,0)
        all_sprites_list.update(-SPEED  * direction,0)#keep moving at speed until we are tile
    elif ((world.getRelativeY() % TILE_SIZE) != 0 and keyUp): #if we are not on a tile and we are not holding a key, reajust to a tile
        velocityY = 0  #reset velocity to avoid extra inputs
        world.update_layout(0,SPEED  * direction) #keep moving at speed until we are on a tile
        world.updateRelative(0,SPEED * direction) #keep moving at speed until we are on a tile
        player1.updateRelative(0,SPEED * direction)
        all_sprites_list.update(0,-SPEED  * direction) #keep moving at speed until we are on a tile

    else:
        keyUp = False
        direction = 0
    all_sprites_list.draw(screen)
    player1.render(screen) 



    
"""
def onTile(x):
    if (player1.getRelativeX() % TILE_SIZE) != 0:
            if x == 1: #want to take us to the next tile
                print(player1.getRelativeX() % TILE_SIZE)
                player1.update((TILE_SIZE - (player1.getRelativeX() % TILE_SIZE)),0)
            else:
                player1.update((player1.getRelativeX() % TILE_SIZE) * x,0)
    elif (player1.getRelativeY() % TILE_SIZE) != 0:
        if x == 1:
            player1.update(0,TILE_SIZE - (player1.getRelativeY() % TILE_SIZE))
        else:
            player1.update(0,(player1.getRelativeY() % TILE_SIZE) * x)
"""

            

while running:


    clock.tick(60)
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_d]:
                velocityX = 4
                direction = 1
                keyUp = False
                keyDown = True
                collisionKey = 1
                get_tile()
             

            if key_pressed[K_a]:
                velocityX = -4
                direction = -1
                keyUp = False
                keyDown = True
                collisionKey = 2
                get_tile()

            if key_pressed[K_w]:
                velocityY = -4
                direction = -1
                keyUp = False
                keyDown = True
                collisionKey = 3
                get_tile()

            if key_pressed[K_s]:
                velocityY = 4
                direction = 1
                keyUp = False
                keyDown = True
                collisionKey = 4
                get_tile()

            if key_pressed[K_q] and inventory.getStatus() == False:
                inventory.updateStatus(True)
            
            elif key_pressed[K_q] and inventory.getStatus() == True:
                inventory.updateStatus(False)
            

        elif event.type == pygame.KEYUP:
            key_pressed = pygame.key.get_pressed()
            if event.key == K_d:
                 velocityX = 0
                 direction = 1
                 keyUp = True
                 keyDown = False
                 #key_d = False
                 #onTile(1)
                 #collision()

            if event.key == K_a:
                 velocityX = 0
                 direction = -1
                 keyUp = True
                 keyDown = False
                 #onTile(-1)
                 #collision()

            if event.key == K_w:
                 velocityY = 0
                 direction = -1
                 keyUp = True
                 keyDown = False
                 #onTile(-1)
                 #collision()

            if event.key == K_s:
                 velocityY = 0
                 direction = 1
                 keyUp = True
                 keyDown = False
                 #onTile(1)

 

                #collision()


            #textbox logic
            #if key_pressed[K_e]:
                #for row in enumerate(npc_sprite_list):
                    #if row[1].getRange():
                        #textbox1.updateStatus(True) #figure out a work around for this later
            

    #once we are out of range
    for row in enumerate(npc_sprite_list):
        if row[1].getRange() == True: #if we are in range of a npc
            if key_pressed[K_e]: #if the interact key is pressed
                for row in enumerate(npc_sprite_list):
                    if row[1].getRange(): #find the curernt npc thats being interacted with 
                        textbox1.updateStatus(True) #update the box to show
            break #dont go to other conditional after
        else: 
            textbox1.updateStatus(False) #textbox defaults off

        
    

    #camera logic
    """""
    if player1.getRelativeX() >= CAMERA_EDGE_X - TILE_SIZE:
        all_sprites_list.update(-TILE_SIZE,0)#playerX -= TILE_SIZE
        world.update_layout(-TILE_SIZE,0)
    if player1.getRelativeX()  <= LENGTH - CAMERA_EDGE_X:
        all_sprites_list.update(TILE_SIZE,0)#playerX += TILE_SIZE
        world.update_layout(TILE_SIZE,0)
    if player1.getY() >= CAMERA_EDGE_Y - TILE_SIZE:
        all_sprites_list.update(0,-TILE_SIZE)#playerY -= TILE_SIZE
        world.update_layout(0,TILE_SIZE)
    if player1.getY() <= WIDTH - CAMERA_EDGE_Y:
        all_sprites_list.update(0,TILE_SIZE)#playerY += TILE_SIZE
        world.update_layout(0,-TILE_SIZE)
     """""

    
    screen.fill('blue')
    world.run(textbox_sprite_list)
    collision()
    player()
    #inventory logic
    if inventory.getStatus():
        inventory.render(screen)
    pygame.display.update()