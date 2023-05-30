import pygame
import math
from pygame.locals import *
from sys import exit
from World import world_creator
from player import Player
from game_data import data
from npc import NPC
from textbox import textbox
from textGenerator import TextGenerator
from Inventory import Inventory
from projectile import projectile
from fractions import Fraction
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
PROJECTILE_SPEED = 8
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
direction = 0 #WASD directions
facingDirection = 2 #where the character is currently facing, either north,south,east,or west. 1 - North, 2 - South, 3 - East, 4 - West
keyUp = False
collisionKey = 0
projectileFired = False
keyDown = False
itemUse = False
currentItem = None
running = True
projectileList = []






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

def checkCollision(obj): #checks to see if theres a collision with obj and the world
    global keyDown
    global direction
    global collisionKey
    global currentItem
    list = world.getObjectList()
    for row_index, row in enumerate(list[1]):
        if pygame.sprite.collide_rect(obj, row):
            print(collisionKey)
            if (type(obj) == type(player1)):
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

                    
            #elif (keyDown and world.getRelativeY() % TILE_SIZE != 0
            
            else:
                collisionKey = 0 #reset everything
                keyDown = False
                direction = 0

                if type(obj) != type(player1): #currently, the only other object it can be is a projectile
                    return True
            print(row.getType())
        


def collision(): #checks if theres a collision
    interactable()
    checkCollision(player1)
  



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
    #print(pygame.mouse.get_pos())
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



def drawItem(item): #draws the used item
    global projectileList
    global itemUse
    global currentItem
    global direction
    global projectileFired
    global facingDirection
    if item != None:
         if facingDirection == 1: # north
            item.setObject(START_COORDSX,START_COORDSY - TILE_SIZE/2) #the player will always be in the center of the screen
         elif facingDirection == 2:
             item.setObject(START_COORDSX,START_COORDSY + TILE_SIZE/2) 
         elif facingDirection == 3:
             item.setObject(START_COORDSX + TILE_SIZE/2,START_COORDSY) 
         elif facingDirection == 4:
             item.setObject(START_COORDSX - TILE_SIZE/2,START_COORDSY) 
    if itemUse:
        item.renderObject(screen)
        if projectileFired:
            mousepos = pygame.mouse.get_pos()
            distance_x = mousepos[0] - START_COORDSX
            distance_y = mousepos[1] - START_COORDSY
            #idk how this math works, stack overflow saved me
            angle = math.atan2(distance_y, distance_x)
            angledegree = math.degrees(angle) * -1
            speed_x = PROJECTILE_SPEED * math.cos(angle)
            speed_y = PROJECTILE_SPEED * math.sin(angle)
            projectileList.append(projectile(START_COORDSX,START_COORDSY,"Sprites/arrow64.png",64,speed_x,speed_y,angledegree))
            projectileFired = False #so it runs only once
    else:
        projectileFired = False
        currentItem = None
        itemUse = False


def renderProjectiles(list):
    for index, projectile in enumerate(list):
        currenttick = pygame.time.get_ticks()
        #print(currenttick - projectile.getTime())
        if (currenttick - projectile.getTime()) >= 5000: #if 10 seconds has passed by, since sometimes there are frame skips, cannot be ==
            list.remove(projectile)
            print("removed")
            break
        elif checkCollision(projectile):
            list.remove(projectile)
            print("removed")
            break
        projectile.updateWorld(-velocityX,-velocityY) #account for the world moving
        projectile.update()
        projectile.render(screen)
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
            #not keydown is used to prevent strafing
            if key_pressed[K_d] and (not keyDown): 
                velocityX = 4
                direction = 1
                facingDirection = 3
                keyUp = False
                keyDown = True
                collisionKey = 1
                get_tile()
             

            if key_pressed[K_a] and (not keyDown):
                velocityX = -4
                direction = -1
                facingDirection = 4
                keyUp = False
                keyDown = True
                collisionKey = 2
                get_tile()

            if key_pressed[K_w] and (not keyDown):
                velocityY = -4
                direction = -1
                facingDirection = 1
                keyUp = False
                keyDown = True
                collisionKey = 3
                get_tile()

            if key_pressed[K_s] and (not keyDown):
                velocityY = 4
                direction = 1
                facingDirection = 2
                keyUp = False
                keyDown = True
                collisionKey = 4
                get_tile()

            #once inventory is true, inventory will render
            if key_pressed[K_q] and inventory.getStatus() == False:
                inventory.updateStatus(True)
            
            #to un render inventory
            elif key_pressed[K_q] and inventory.getStatus() == True:
                inventory.updateStatus(False)
            
            #if the inventory is open, make the options available to change
            if key_pressed[K_RIGHT] and inventory.getStatus() == True:
                inventory.updateSelection(1) #going right one
               
            if key_pressed[K_LEFT] and inventory.getStatus() == True:
                inventory.updateSelection(-1) #going left one
       
            if key_pressed[K_RETURN] and inventory.getStatus() == True: #when we selected something
                inventory.onEnter()
                inventorylist = inventory.getInventoryList()
                selection = inventory.getSeleciton()
                
                if selection == -1: #if we select this, then we are unselecting an item
                    itemUse = False
                else:
                    currentItem = inventorylist[selection]
                    itemUse = True

            #if the inventory is open, item can be  used
            if key_pressed[K_r] and inventory.getStatus() == True:
             if key_pressed[K_r] and itemUse == True:
                 currentItem = None
                 itemUse = False
                 break
             #for index, item in enumerate(inventory.getInventoryList()):
                 if item.getID() == "bow":
                     currentItem = item
                     itemUse = True

        elif event.type == pygame.MOUSEBUTTONDOWN: #1 -left click, #2 - right click
            print(inventory.getCurrentObject().getID())
            if event.button == 1 and itemUse and inventory.getCurrentObject().getID() == "bow":
                projectileFired = True
            

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
    #loads the world first, then checks for collison, then loads player logic, then loads in items. Lastly, it will load in projectile
    world.run(textbox_sprite_list)
    collision()
    player()
    drawItem(currentItem)
    renderProjectiles(projectileList)
    #inventory logic
    if inventory.getStatus():
        inventory.render(screen)
    pygame.display.update()