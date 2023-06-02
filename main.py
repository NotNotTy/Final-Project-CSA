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
from melee import melee
from enemy import enemy
from fractions import Fraction
pygame.init()
pygame.font.init()
LENGTH = 1216
WIDTH = 704
screen = pygame.display.set_mode((LENGTH,WIDTH)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/red.png") #fill this
npcImg = pygame.image.load("Sprites/character64.png")
textboxImg = pygame.image.load("Sprites/textbox2.png")
clock = pygame.time.Clock() #clock
TILE_SIZE = 64 #each tile is 32x32 big
FPS = 60 #pretty self explainitory
#CAMERA_EDGE_X = LENGTH -  (TILE_SIZE * 1) #the edges are where the world will start to shift to give the impression that the camera is following the player. Multipler 8 
#CAMERA_EDGE_Y = WIDTH - (TILE_SIZE * 1) # 4
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
testenemy = enemy("Sprites/character64.png",200,20,START_COORDSX + 64,START_COORDSY + 64,START_COORDSX,START_COORDSY,screen)
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
isMoving = False
WorldVelocityX = 0 #since velocityX and velocityY are resetted to zero to account for player movement, this is used for the rest of the World
WorldVelocityY = 0
direction = 0 #WASD directions. D and W are positive, A and S are negative
lastDirection = 2 #this direction will never reset. Either be north south esat or west
facingDirection = 2 #where the character is currently facing, either north,south,east,or west. 1 - North, 2 - South, 3 - East, 4 - West
keyUp = False
collisionKey = 0
projectileFired = False #if its true, a segment of code will run
meleeSwung = False #if true, a segment of code will run
meleeInUse = False
showAttackWarning = False #if you try to use your weapon out of radius, this will update
change = True
keyDown = False #boolean to use as conditional
itemUse = False #boolean to use as conditional
currentItem = None 
previousItem = None
collisionDetected = False
running = True
projectileList = []
meleeList = []
enemyList = []
enemyList.append(testenemy)






#def updateSmooth():
    #player1.update(2,0)
    #all_sprites_list.draw(screen)
    
    #pygame.time.delay(500)



#----------------------------------------------------------COLLISION---------------------------------------------#
#manually updates the direction based on the parameters
def CollisionUpdateDirectionX(r):
    global direction
    global velocityX
    direction = r
    if direction == 0:
        pass
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
    if direction == 0:
        pass
    world.update_layout(0,-SPEED  * direction) #keep moving at speed until we are on a tile
    world.updateRelative(0,-SPEED * direction) #keep moving at speed until we are on a tile
    player1.updateRelative(0,-SPEED * direction)
    all_sprites_list.update(0,SPEED  * direction) #keep moving at speed until we are on a tile

def checkCollision(obj): #checks to see if theres a collision with obj and the world
    global keyDown
    global direction
    global collisionKey
    global currentItem
    global collisionDetected
    list = world.getObjectList()
    for row_index, row in enumerate(list[1]):
        if pygame.sprite.collide_rect(obj, row):
            if (type(obj) == type(player1)):
                collisionDetected = True
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

#--------------------------------------------------------WORLD UPDATING------------------------------------------------------#
def player(): #draws the player
    global direction
    global velocityX #the speed of the player dictated by input
    global velocityY #the speed of the player dictated by input
    global keyUp #if we let go of the movement keys
    global lastDirection
    global isMoving
    global WorldVelocityX
    global WorldVelocityY
    global enemyList
    #print(pygame.mouse.get_pos())
    player1.updateSprite(lastDirection)
    player1.updateRelative(velocityX,velocityY) #here just to keep track of the player, is basically the asme thing as worldrelative
    world.updateRelative(velocityX,velocityY) #takes in user input and moves when held
    world.update_layout(-velocityX,velocityY) #takes in user input and moves when held
    all_sprites_list.update(-velocityX,-velocityY)#keep moving at speed until we are tile
    if (velocityX != 0) or (velocityY != 0):
        isMoving = True
    if ((world.getRelativeX() % TILE_SIZE) != 0 and keyUp): #if we are not on a tile and we are not holding a key, reajust to a tile
        isMoving = True
        velocityX = 0 #reset velocity to avoid extra inputs
        world.update_layout(-SPEED  * direction,0) #keep moving at speed until we are on a tile
        world.updateRelative(SPEED * direction,0) #keep moving at speed until we are tile
        player1.updateRelative(SPEED * direction,0)
        all_sprites_list.update(-SPEED  * direction,0)#keep moving at speed until we are tile
        #updateEnemy(-SPEED  * direction,0)
    elif ((world.getRelativeY() % TILE_SIZE) != 0 and keyUp): #if we are not on a tile and we are not holding a key, reajust to a tile
        isMoving = True
        velocityY = 0  #reset velocity to avoid extra inputs
        world.update_layout(0,SPEED  * direction) #keep moving at speed until we are on a tile
        world.updateRelative(0,SPEED * direction) #keep moving at speed until we are on a tile
        player1.updateRelative(0,SPEED * direction)
        all_sprites_list.update(0,-SPEED  * direction) #keep moving at speed until we are on a tile
       #updateEnemy(0,-SPEED  * direction)

    else:
        isMoving = False
        if not isMoving:
            if ((world.getRelativeX() % TILE_SIZE) == 0 and keyUp): #used to update world velocity, becuase the regular one is solely for the player
                    WorldVelocityX = 0
                    #WorldVelocityY = 0
            if ((world.getRelativeY() % TILE_SIZE) == 0 and keyUp):
                    
                    WorldVelocityY = 0
                    #WorldVelocityX = 0
                
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
    global change
    if item != None:
         #due to flipping issues regarding size, some of the object's placement has been manually ajusted
         if facingDirection == 1: # north
            item.setObject(START_COORDSX,(START_COORDSY - TILE_SIZE * .75)) #the player will always be in the center of the screen
            if item.getID() == "bow":
             (item.getObject()).changeOrientation(90)
            else:
             (item.getObject()).changeOrientation(0)
         elif facingDirection == 2: #south
             item.setObject(START_COORDSX,(START_COORDSY + TILE_SIZE/2)) 
             if item.getID() == "bow":
                 (item.getObject()).changeOrientation(-90)
             else:
                (item.getObject()).changeOrientation(-180)
         elif facingDirection == 3: #east
             item.setObject((START_COORDSX + TILE_SIZE/2),START_COORDSY) 
             if item.getID() == "bow":
                 (item.getObject()).changeOrientation(0)
             else:
                (item.getObject()).changeOrientation(-45)
         elif facingDirection == 4: #west
             item.setObject((START_COORDSX - TILE_SIZE * .75),START_COORDSY) 
             if item.getID() == "bow":
                 (item.getObject()).changeOrientation(180)
             else:
                 (item.getObject()).changeOrientation(45)
    if itemUse:
        projectileCreation()
        meleeCreation()
        #textCreation() Unused, might use later

    else:
        projectileFired = False
        currentItem = None
        itemUse = False
#-------------------------------------------------------CREATION SECTION---------------------------------------------------------------#
def projectileCreation(): #creates the projectiles
    global projectileList
    global itemUse
    global currentItem
    global projectileFired
    if projectileFired: #projectiles create a another object. This code appends a projectile object to a list to be rendered
        mousepos = pygame.mouse.get_pos()
        distance_x = mousepos[0] - START_COORDSX
        distance_y = mousepos[1] - START_COORDSY
        #idk how this math works, stack overflow saved me
        angle = math.atan2(distance_y, distance_x)
        angledegree = math.degrees(angle) * -1
        speed_x = PROJECTILE_SPEED * math.cos(angle)
        speed_y = PROJECTILE_SPEED * math.sin(angle)
        projectileList.append(projectile(START_COORDSX,START_COORDSY,"Sprites/arrow64.png",64,speed_x,speed_y,angledegree)) #sprite is subjected to change
        projectileFired = False #so it runs only once

def meleeCreation():
    global meleeList
    global itemUse
    global currentItem
    global meleeSwung
    global previousItem
    global meleeInUse
    if meleeSwung:
        mousepos = pygame.mouse.get_pos()
        distance_x = mousepos[0] - currentItem.getObjectX()
        distance_y = mousepos[1] - currentItem.getObjectY()
        #idk how this math works, stack overflow saved me
        angle = math.atan2(distance_y, distance_x)
        angledegree = math.degrees(angle) * -1
        speed_x = PROJECTILE_SPEED * math.cos(angle)
        speed_y = PROJECTILE_SPEED * math.sin(angle)
        meleeList.append(melee(currentItem.getObjectX(),currentItem.getObjectY(),"Sprites/sword64rotated.png",TILE_SIZE,speed_x,speed_y,angledegree)) #sprite is subjected to change
        meleeSwung = False #so it runs only once
        meleeInUse = True
        previousItem = currentItem

def textCreation():
    global showAttackWarning
    if showAttackWarning:
        text2 = TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'You cannot use your weapon behind you!', 'freesansbold.ttf')
        renderText(text2)
#----------------------------------------------------------------------------------------------------------------------#


#------------------------------------------RENDERING SECTION--------------------------------------------------------------------------------
def renderText(text): #function used to render all text
    global velocityX
    global velocityY
    if showAttackWarning:
        text.update(-velocityX,-velocityY)
        text.render(screen,player1.getRelativeX(), player1.getRelativeY())


def renderMelee(list): #goal - CREATE A NEW MELEE CLASS THATS FOR MELEE, INDEPENDENT OF THE ITEM CLASS
    global currentItem
    global previousItem
    global meleeInUse
    for index, melee in enumerate(list):
        currenttick = pygame.time.get_ticks()
        #print(currenttick - projectile.getTime())
        if (currenttick - melee.getTime()) >= 505: #end condition
            list.remove(melee)
            print("removed melee")
            currentItem = previousItem
            previousItem = None
            meleeInUse = False
            break

        elif checkCollision(melee):
            list.remove(melee)
            print("removed melee")
            currentItem = previousItem
            previousItem = None
            meleeInUse = False
            break
        else:
            if (currenttick - melee.getTime()) >= 0 and (currenttick - melee.getTime()) < 250:
                melee.updateWorld(-velocityX,-velocityY) #account for the world moving
                melee.updateOrientation()
                melee.updateForwardMovement(0.8)  #speed between 0-1
                melee.render(screen)
                currentItem = None

            if (currenttick - melee.getTime()) >= 250 and (currenttick - melee.getTime()) < 500:
                if pygame.sprite.collide_rect(melee, player1): #account for player movement
                    list.remove(melee)
                    print("removed melee")
                    currentItem = previousItem
                    previousItem = None
                    meleeInUse = False
                    break
                melee.updateWorld(-velocityX,-velocityY) #account for the world moving
                melee.updateOrientation()
                melee.updateBackwardMovement(0.8)
                melee.render(screen)
                currentItem = None
        
 
        #melee.updateWorld(-velocityX,-velocityY) #account for the world moving
        #melee.update()
        #melee.render(screen)

def renderProjectiles(list): #this renders every projectile on the list
    for index, projectile in enumerate(list):
        currenttick = pygame.time.get_ticks()
        #print(currenttick - projectile.getTime())
        if (currenttick - projectile.getTime()) >= 5000: #if 5 seconds has passed by, since sometimes there are frame skips, cannot be ==
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

def renderEnemy(list): #TO FIX - COLLISION WITH OBJECT MAKES ENEMY GO VROOM, IDK WHAT IS UP WITH THE X AND Y COORDS
    global WorldVelocityX
    global WorldVelocityY
    global isMoving
    global lastDirection
    global collisionKey
    global collisionDetected
    #Only one of them can not equal zero at the same time
    if collisionDetected: #if we are colliding with something, do not move the enemy
        collisionDetected = False #this is still a little buggy, fix this'
        WorldVelocityX = 0
        WorldVelocityY = 0
    for index, enemy in enumerate(list):
            enemy.update(-WorldVelocityX,-WorldVelocityY)
            enemy.setTrajectory((START_COORDSX,START_COORDSY),SPEED/2)
            enemy.render()

def updateEnemy(list,x,y):
    for index,enemy in enumerate(list):
        enemy.update()

#----------------------------------------------------------------------------------------------------------------------------------------#
def inRadius(): #if the mouse is in a certain radius of the weapon, it will fire
    mousepos = pygame.mouse.get_pos()
    distance_x = mousepos[0] - currentItem.getObjectX()
    distance_y = mousepos[1] - currentItem.getObjectY()
    #idk how this math works, stack overflow saved me
    angle = math.atan2(distance_y, distance_x)
    angledegree = math.degrees(angle)

    if lastDirection == 1: #north
        if angledegree > -180 and angledegree < 0: #180 - 0
            return True 
        print(lastDirection)
        print(angledegree)

    if lastDirection == 2: #south
        if angledegree <= 180 and angledegree >= 0:
            return True

    if lastDirection == 3: #east
        if angledegree >= -90 and angledegree < 90:
            return True
    
    if lastDirection == 4: #west
        if angledegree < -90 or angledegree >= 90:
            return True
        
    print(lastDirection)
    print(angledegree)
    return False


def get_tile(): #returns the coordinate position of the player
    coords = [(player1.getRelativeX() - START_COORDSX)//TILE_SIZE,(player1.getRelativeY()-START_COORDSY)//TILE_SIZE]
    #print(playerXRelative//TILE_SIZE,playerYRelative//TILE_SIZE)
    #print(playerXRelative,playerYRelative)
    print(coords)
            

while running:


    clock.tick(60)
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.get_pressed()
            #not keydown is used to prevent strafing
            if key_pressed[K_d] and (not keyDown) and (not isMoving): 
                isMoving = True
                velocityX = 4
                WorldVelocityX = 4
                direction = 1
                lastDirection = 3
                facingDirection = 3
                keyUp = False
                keyDown = True
                collisionKey = 1
                get_tile()
             

            if key_pressed[K_a] and (not keyDown)and (not isMoving):
                isMoving = True
                velocityX = -4
                WorldVelocityX = -4
                direction = -1
                lastDirection = 4
                facingDirection = 4
                keyUp = False
                keyDown = True
                collisionKey = 2
                get_tile()

            if key_pressed[K_w] and (not keyDown)and (not isMoving):
                isMoving = True
                velocityY = -4
                WorldVelocityY = -4
                direction = -1
                lastDirection = 1
                facingDirection = 1
                keyUp = False
                keyDown = True
                collisionKey = 3
                get_tile()

            if key_pressed[K_s] and (not keyDown) and (not isMoving):
                isMoving = True
                velocityY = 4
                WorldVelocityY = 4
                direction = 1
                lastDirection = 2
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
       
            if key_pressed[K_RETURN] and inventory.getStatus() == True and not meleeInUse: #when we selected something
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
            if event.button == 1 and itemUse and inventory.getCurrentObject().getID() == "sword" and not meleeInUse: #segment used to render melee attacks
                if inRadius(): #if we are aiming infront of us 
                    meleeSwung = True
                    showAttackWarning = False
                else:
                    showAttackWarning = True

            

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
    if currentItem != None:
        currentItem.renderObject(screen)
    renderEnemy(enemyList)
    renderProjectiles(projectileList)
    renderMelee(meleeList)
    #inventory logic
    if inventory.getStatus():
        inventory.render(screen)
    pygame.display.update()