import pygame
import math
import random
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
from healthbar import healthbar
from deathScreen import deathScreen
from hunger import hunger
from nighttime import nighttime
from crate import crate
pygame.init()
pygame.font.init()
#------------------------CONSTANTS---------------------------------
LENGTH = 1216
WIDTH = 704
screen = pygame.display.set_mode((LENGTH,WIDTH)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/red.png").convert_alpha() #fill this
npcImg = pygame.image.load("Sprites/character64.png").convert_alpha()
textboxImg = pygame.image.load("Sprites/textbox2.png").convert_alpha()
clock = pygame.time.Clock() #clock
TILE_SIZE = 64 #each tile is 32x32 big
FPS = 60 #pretty self explainitory
START_COORDSX = 512 #start coordinates, used to keep the original position in a constant
START_COORDSY = 320
NPC_STARTCOORDSX = 768
NPC_STARTCOORDSY = 384
TEXTBOX_COORDSX = 100
TEXTBOX_COORDSY = 100
WORLD_SIZE_X = 3840 #60x60 (update later if map size is changed)
WORLD_SIZE_Y = 3840
SPEED = 4 #speed of the player/world
PROJECTILE_SPEED = 8
TEXTBOX_SPRITE_WIDTH = 576 #used for translating the box in the middle
PLAYER_STARTING_HEALTH = 200
PLAYER_STARTING_HUNGER = 20
#----------------------------VARIABLE INITALIZATION---------------------------#
world = None
player1 = None
npc1 = None
npc2 = None
textbox1 = None
night = None
text = TextGenerator(START_COORDSX,START_COORDSY - 64,'press E to interact','freesansbold.ttf',pygame.time.get_ticks(),"radius") #temp is when it'll disappear after blank time, radius will show if in range
deathMessage = deathScreen("Sprites/playagain.png","Sprites/exit.png","Sprites/deathScreen.png")
hungerbar = None
healthbarIcon = None
inventory = Inventory()
all_sprites_list = None
npc_sprite_list = None
textbox_sprite_list = None
#all_sprites_list.add(player1)
velocityX = 0
velocityY = 0
hungerspeed = 1
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
textList = []
crateList = []
#all of the below is used as conditionals to show text
enemyKilled = False
emptyBag = False
showInteraction = False
NPCRadius = False
#-----#
crateRadius = False
startGameBool = True






#----------------------------------------------GAME INITALIZATION/GAME DEATH----------------------------------#
def startGame(): #used to start the game, also used to reset the game if the player dies. This assigns properties to all the variables needed
    global startGameBool
    if startGameBool:
        global player1,npc1,npc2,world,healthbarIcon,all_sprites_list,npc_sprite_list,projectileList,meleeList,enemyList,textbox1,textbox_sprite_list,textList,crateList,night
        global velocityX,velocityY,isMoving,WorldVelocityX,WorldVelocityY,direction,lastDirection,facingDirection,showInteraction,NPCRadius,crateRadius,emptyBag,hungerbar,hungerspeed
        global keyUp, collisionKey,projectileFired,meleeSwung,meleeInUse,showAttackWarning,keyDown,itemUse,previousItem,collisionDetected,running,change,currentItem,enemyKilled
        world = world_creator(data,screen,START_COORDSX,START_COORDSY) #generates the world 
        player1 = Player(TILE_SIZE,START_COORDSX,START_COORDSY,playerImg,"player",PLAYER_STARTING_HEALTH,PLAYER_STARTING_HUNGER)
        npc1 = NPC(TILE_SIZE,NPC_STARTCOORDSX,NPC_STARTCOORDSY,npcImg,'npc',False)
        npc2 = NPC(TILE_SIZE,NPC_STARTCOORDSX + 128,NPC_STARTCOORDSY,npcImg,'npc',False)
        textbox1 = textbox(TILE_SIZE,(LENGTH/2) - (384/2),player1.getY() + 7 * TILE_SIZE,textboxImg,'textbox',False)
        healthbarIcon = healthbar("Sprites/hpbar.png",LENGTH - (TILE_SIZE * 5),WIDTH - TILE_SIZE/2,TILE_SIZE * 5, TILE_SIZE/2) #currently the bar is (64*5,32)
        hungerbar = hunger("Sprites/hpbar.png",LENGTH - (TILE_SIZE * 5),WIDTH - (TILE_SIZE/2 * 2),TILE_SIZE * 4,TILE_SIZE/2)
        night = nighttime()
        all_sprites_list = pygame.sprite.Group()
        npc_sprite_list = pygame.sprite.Group()
        textbox_sprite_list = pygame.sprite.Group()
        #all_sprites_list.add(player1)
        textbox_sprite_list.add(textbox1)
        velocityX = 0
        velocityY = 0
        hungerspeed = 1
        isMoving = False
        WorldVelocityX = 0 #since velocityX and velocityY are resetted to zero to account for player movement, this is used for the rest of the World
        WorldVelocityY = 0
        direction = 0 #WASD directions. D and W are positive, A and S are negative
        lastDirection = 2 #this direction will never reset. Either be north south esat or west
        facingDirection = 2 #where the character is currently facing, either north,south,east,or west. 1 - North, 2 - South, 3 - East, 4 - West
        keyUp = False
        collisionKey = 0 #check direction of collision
        projectileFired = False #if its true, a segment of code will run to update projectile
        meleeSwung = False #if true, a segment of code will run to update melee
        meleeInUse = False #so multiple melees cannot be used at once
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
        textList = []
        crateList = []
        enemyKilled = False
        showInteraction = False
        NPCRadius = False #if we are in range of an NPC
        crateRadius = False #if we are in range of a crate
        emptyBag = False
        inventory.reset()
        startGameBool = False

        #STAGE SETUP
        crateCreation(10) #create 10 crates

def endGame():
    global player1
    if player1.getHealth() <= 0:
        return True




#----------------------------------------------------------COLLISION---------------------------------------------#
#manually updates the direction based on the parameters
def CollisionUpdateDirectionX(r): #used for obj collision
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
def CollisionUpdateDirectionY(r): #used for obj collision
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
    global enemyList
    global projectileList
    global meleeList
    global meleeSwung
    global meleeInUse
    global previousItem
    global enemyKilled
    list = world.getCollideableList()
    for row in list:
        for collideable in enumerate(row):
            if pygame.sprite.collide_rect(obj, collideable[1]): #if anything collides with the enviromental obstacles
                if (type(obj) == type(player1)) or obj.getID() == "enemy":
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

                
                
                else:
                    
                    
                    collisionKey = 0 #reset everything
                    keyDown = False
                    direction = 0

    for index, enemy in enumerate(enemyList):
        if pygame.sprite.collide_rect(enemy,obj):
            if obj.getID() == "player":
                    #invulnurbility/damage codes
                    if player1.getInvulurbility():
                        if (pygame.time.get_ticks() - player1.getTime()) >= 1000:  #if we have been invulnurble for 1 seconds
                            player1.setInvulurbility(False)
                            player1.setStartTime(0)

                    if not player1.getInvulurbility():
                        player1.updateHealth(-enemy.getDamage())
                        player1.setInvulurbility(True)
                        player1.setStartTime(pygame.time.get_ticks())
                        
        if enemy.getHealth() <= 0:
            enemyList.remove(enemy)


    #Enemy damage code
 


def checkObjectCollision(obj):
      global enemyList
      list = world.getCollideableList()
      for row in list:
        for collideable in enumerate(row):
            if pygame.sprite.collide_rect(obj, collideable[1]): #if anything collides with the enviromental obstacles
                if obj.getID() == "projectile" or obj.getID() == "melee": #all objects will have a id system
                    if collideable[1].getType() == "water":
                        return False
                return True
      for index, enemy in enumerate(enemyList):
        if pygame.sprite.collide_rect(enemy,obj):
            if obj.getID() == "projectile": #if the enemy was hit by a projectile
                if obj in projectileList:
                    projectileList.remove(obj) #remove that projectile
                enemy.updateHealth(-obj.getDamage()) #update enemy health
                if enemy.getHealth() <= 0: #if the health is less than 0, display a kill message
                    enemyKilled = True
                    textCreation("enemy-slained")

            if obj.getID() == "melee" and obj.getHit() == False:
                enemy.updateHealth(-obj.getDamage())
                obj.updateHit(True)
                if enemy.getHealth() <= 0:
                    enemyKilled = True
                    textCreation("enemy-slained")

                
        


def collision(): #checks if theres a collision
    interactable()
    checkCollision(player1)
  



def interactable(): #loops through every collideable object
    global showInteraction
    global NPCRadius
    global crateList
    global crateRadius
    for index,npc in enumerate(npc_sprite_list):
         if pygame.Rect.colliderect(player1.getRect(),npc.getHitboxRect()):
            NPCRadius = True
            if showInteraction == True:
                pass
            elif showInteraction == False and npc.getRange() == True: #if show interaction is false, but we are in range of an npc
                pass
            else:
                showInteraction = True
                textCreation("range")
            npc.editRange(True)
            #print(row[1].getRange())
         else:
             if npc.getRange() == True:
                 NPCRadius = False
             npc.editRange(False)
             #print(row[1].getRange())

    for index, crate in enumerate(crateList):
        if pygame.Rect.colliderect(player1.getRect(),crate.getHitboxRect()):
            crateRadius = True
            if showInteraction == True:
                pass
            elif showInteraction == False and crate.getRange() == True: #if show interaction is false, but we are in range of an npc
                pass
            else:
                showInteraction = True
                textCreation("range")
            crate.editRange(True)
        else:
            if crate.getRange() == True:
                crateRadius = False
            crate.editRange(False)

#--------------------------------------------------------WORLD UPDATING------------------------------------------------------#
def player(): #draws the player
    global direction
    global velocityX #the speed of the player dictated by input
    global velocityY #the speed of the player dictated by input
    global keyUp #if we let go of the movement keys
    global keyDown
    global lastDirection
    global facingDirection
    global isMoving
    global WorldVelocityX
    global WorldVelocityY
    global enemyList
    global hungerspeed
    #print(pygame.mouse.get_pos())
    if (player1.getHunger() <= 5):
        hungerspeed = 0.5 #cut speed in half
    else:
        hungerspeed = 1
    player1.updateSprite(lastDirection)
    player1.updateRelative(velocityX * hungerspeed,velocityY * hungerspeed) #here just to keep track of the player, is basically the asme thing as worldrelative
    world.updateRelative(velocityX* hungerspeed,velocityY * hungerspeed) #takes in user input and moves when held
    world.update_layout(-velocityX * hungerspeed,velocityY * hungerspeed) #takes in user input and moves when held
    all_sprites_list.update(-velocityX * hungerspeed,-velocityY * hungerspeed)#keep moving at speed until we are tile\
   # print(world.getRelativeX() % TILE_SIZE)
    if ((world.getRelativeX() % TILE_SIZE) != 0 and keyUp and not keyDown): #if we are not on a tile and we are not holding a key, reajust to a tile
        isMoving = True
        velocityX = 0 #reset velocity to avoid extra inputs
        world.update_layout(-SPEED  * direction * hungerspeed,0) #keep moving at speed until we are on a tile
        world.updateRelative(SPEED * direction* hungerspeed,0) #keep moving at speed until we are tile
        player1.updateRelative(SPEED * direction* hungerspeed,0)
        all_sprites_list.update(-SPEED  * direction* hungerspeed,0)#keep moving at speed until we are tile
        #updateEnemy(-SPEED  * direction,0)
    elif ((world.getRelativeY() % TILE_SIZE) != 0 and keyUp and not keyDown): #if we are not on a tile and we are not holding a key, reajust to a tile
        isMoving = True
        velocityY = 0  #reset velocity to avoid extra inputs
        world.update_layout(0,SPEED  * direction* hungerspeed) #keep moving at speed until we are on a tile
        world.updateRelative(0,SPEED * direction* hungerspeed) #keep moving at speed until we are on a tile
        player1.updateRelative(0,SPEED * direction* hungerspeed)
        all_sprites_list.update(0,-SPEED  * direction* hungerspeed) #keep moving at speed until we are on a tile
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

       
                
       
        direction = 0
    all_sprites_list.draw(screen)
    player1.render(screen) 

def drawItem(item): #draws the used item and the direction it is facing in
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
            if item.getID() != "sword":
             (item.getObject()).changeOrientation(90)
            else:
             (item.getObject()).changeOrientation(0)
         elif facingDirection == 2: #south
             item.setObject(START_COORDSX,(START_COORDSY + TILE_SIZE/2)) 
             if item.getID() != "sword":
                 (item.getObject()).changeOrientation(-90)
             else:
                (item.getObject()).changeOrientation(-180)
         elif facingDirection == 3: #east
             item.setObject((START_COORDSX + TILE_SIZE/2),START_COORDSY) 
             if item.getID() != "sword":
                 (item.getObject()).changeOrientation(0)
             else:
                (item.getObject()).changeOrientation(-45)
         elif facingDirection == 4: #west
             item.setObject((START_COORDSX - TILE_SIZE * .75),START_COORDSY) 
             if item.getID() != "sword":
                 (item.getObject()).changeOrientation(180)
             else:
                 (item.getObject()).changeOrientation(45)
    if itemUse:
        if item != None:
            if item.getID() == "bow":
                projectileCreation("bow")
            if item.getID() == "firebook":
                projectileCreation("firebook")
            if item.getID() == "sword":
                meleeCreation()
        #textCreation() Unused, might use later

    else:
        projectileFired = False
        currentItem = None
        itemUse = False
#-------------------------------------------------------CREATION SECTION---------------------------------------------------------------#
def projectileCreation(tag): #creates the projectiles
    global projectileList
    global itemUse
    global currentItem
    global projectileFired
    if projectileFired: #projectiles create a another object. This code appends a projectile object to a list to be rendered
        if inventory.getCurrentObject().getDurabilityStatus() == False:
            inventory.removeItem(inventory.getCurrentObject())
            currentItem = None
        else:
            inventory.getCurrentObject().updateDurability(-1)
        mousepos = pygame.mouse.get_pos()
        distance_x = mousepos[0] - START_COORDSX
        distance_y = mousepos[1] - START_COORDSY
        #idk how this math works, stack overflow saved me
        angle = math.atan2(distance_y, distance_x)
        angledegree = math.degrees(angle) * -1
        speed_x = PROJECTILE_SPEED * math.cos(angle)
        speed_y = PROJECTILE_SPEED * math.sin(angle)
        if tag == "bow":
            foundArrow = False
            for index, item in enumerate(inventory.getInventoryList()):
                if item.getID() == "arrow": #if we are capable of getting the item, that means there is atleast 1 or more arrow
                    item.updateAmount(-1)
                    foundArrow = True
                    projectileList.append(projectile(START_COORDSX,START_COORDSY,"Sprites/arrow64.png",65,speed_x,speed_y,angledegree,"projectile")) #sprite is subjected to change
            if not foundArrow:
                textCreation("out-of-arrows")
        if tag == "firebook":
            projectileList.append(projectile(START_COORDSX,START_COORDSY,"Sprites/fireball.png",20,speed_x,speed_y,angledegree,"projectile")) #sprite is subjected to change
        projectileFired = False #so it runs only once

def meleeCreation():
    global meleeList
    global itemUse
    global currentItem
    global meleeSwung
    global previousItem
    global meleeInUse
    if meleeSwung:
        if inventory.getCurrentObject().getDurabilityStatus() == False:
            inventory.removeItem(inventory.getCurrentObject())
            currentItem = None
        else:
            inventory.getCurrentObject().updateDurability(-1)
            mousepos = pygame.mouse.get_pos()
            distance_x = mousepos[0] - currentItem.getObjectX()
            distance_y = mousepos[1] - currentItem.getObjectY()
            #idk how this math works, stack overflow saved me
            angle = math.atan2(distance_y, distance_x)
            angledegree = math.degrees(angle) * -1
            speed_x = PROJECTILE_SPEED * math.cos(angle)
            speed_y = PROJECTILE_SPEED * math.sin(angle)
            meleeList.append(melee(currentItem.getObjectX(),currentItem.getObjectY(),"Sprites/sword64rotated.png",TILE_SIZE,speed_x,speed_y,angledegree,"melee")) #sprite is subjected to change
            meleeSwung = False #so it runs only once
            meleeInUse = True
            previousItem = currentItem

def textCreation(id):
    global showAttackWarning
    global textList
    global enemyKilled
    global showInteraction
    global crateRadius
    global emptyBag
    currentTime = pygame.time.get_ticks()
    if id == "range":
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32,'press E to interact','freesansbold.ttf',currentTime,"radius"))
        showInteraction = False
    if id == "range" and not NPCRadius and not crateRadius:
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'You cannot use your weapon behind you!', 'freesansbold.ttf',currentTime,"temp"))
        showAttackWarning = False
    if id == "enemy-slained" and not NPCRadius and not crateRadius:
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'You have killed an enemy!', 'freesansbold.ttf',currentTime,"temp"))
        enemyKilled = False
    if id == "warning" and not NPCRadius and not crateRadius:
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'Halfway there!', 'freesansbold.ttf',currentTime,"temp"))
    if emptyBag and not NPCRadius and not crateRadius:
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'Your bag is empty!', 'freesansbold.ttf',currentTime,"temp"))
        emptyBag = False

    if id == "out-of-arrows":
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'Out of arrows!', 'freesansbold.ttf',currentTime,"temp"))

    if id == "empty-bag":
        textList.append(TextGenerator(player1.getRelativeX(),player1.getRelativeY() - 32, 'Your bag is empty!', 'freesansbold.ttf',currentTime,"temp"))

def crateCreation(num):
    global crateList
    global screen

    for i in range(num):
        x_coords = random.randrange(TILE_SIZE  * (-25 + -abs(get_tile_x())), TILE_SIZE  * (74 + -abs(get_tile_x())),TILE_SIZE)#Note, the multipler MUST BE WHATEVER THE WORLD MULTIPLIER IS in World.py
        y_coords = random.randrange(TILE_SIZE  * (-31 + -abs(get_tile_y())), TILE_SIZE  * (68 + -abs(get_tile_y())),TILE_SIZE) #Second Note, the end condition must be one less the world width subtracted by multiplier
        crateList.append(crate("Sprites/crate32.png",x_coords + 16,y_coords + 16,"crate",False)) #add 16 to center the smaller crate

def spawn(): #spawns enemies
    global enemyList
    global world
    global night
    list = world.getCollideableList()
    if night.getNightStatus():
        for row in list:
            #TILE_SIZE  * (-31 + -abs(get_tile_y())) + (TILE_SIZE * -27)
            xcoords = random.randrange(TILE_SIZE  * (-25 + -abs(get_tile_x())), TILE_SIZE  * (74 + -abs(get_tile_x())),TILE_SIZE)
            ycoords = random.randrange(TILE_SIZE  * (-31 + -abs(get_tile_y())), TILE_SIZE  * (68 + -abs(get_tile_y())),TILE_SIZE)
            for collidable in enumerate(row):
                if set(collidable[1].get_coords()) & set([xcoords,ycoords]):
                    while collidable[1].get_coords() == [xcoords,ycoords]:
                        xcoords = random.randrange(TILE_SIZE  * (-25 + -abs(get_tile_x())), TILE_SIZE  * (74 + -abs(get_tile_x())),TILE_SIZE)  #Note, the multipler MUST BE WHATEVER THE WORLD MULTIPLIER IS in World.py
                        ycoords = random.randrange(TILE_SIZE  * (-31 + -abs(get_tile_y())), TILE_SIZE  * (68 + -abs(get_tile_y())),TILE_SIZE) #Second Note, the end condition must be one less the world width subtracted by multiplier
        crateCreation(2) #create two new crates every 10 second
        health = random.randrange(200,500)
        damage = random.randrange(10,50)
        enemyList.append(enemy("Sprites/character64.png",health,damage,xcoords,ycoords,START_COORDSX,START_COORDSY,screen,"enemy"))

#----------------------------------------------------------------------------------------------------------------------#


#------------------------------------------RENDERING SECTION--------------------------------------------------------------------------------
def renderText(list): #function used to render all text
    global velocityX
    global velocityY
    global showInteraction
    global NPCRadius
    global crateRadius
    for index, text in enumerate(list):
        if text.getID() == "radius":
            if NPCRadius == False and crateRadius == False:
                textList.remove(text)
        if text.getID() == "temp":
            if pygame.time.get_ticks() - text.getTime() >= 1000: #1 sec
                list.remove(text)
        text.render(screen,player1.getX()-TILE_SIZE,player1.getY()-TILE_SIZE)


def renderMelee(list): #goal - CREATE A NEW MELEE CLASS THATS FOR MELEE, INDEPENDENT OF THE ITEM CLASS
    global currentItem
    global previousItem
    global meleeInUse
    for index, melee in enumerate(list):
        currenttick = pygame.time.get_ticks()
        #print(currenttick - projectile.getTime())
        if (currenttick - melee.getTime()) >= 505: #end condition
            list.remove(melee)
            currentItem = previousItem
            melee.updateHit(False)
            previousItem = None
            meleeInUse = False
            break

        elif checkObjectCollision(melee):
            list.remove(melee)
            currentItem = previousItem
            melee.updateHit(False)
            previousItem = None
            meleeInUse = False
            break
        else:
            if (currenttick - melee.getTime()) >= 0 and (currenttick - melee.getTime()) < 100:
                melee.updateWorld(-velocityX,-velocityY) #account for the world moving
                melee.updateOrientation()
                melee.updateForwardMovement(0.9)  #speed between 0-1
                melee.render(screen)
                currentItem = None

            if (currenttick - melee.getTime()) >= 100 and (currenttick - melee.getTime()) < 200:
                if pygame.sprite.collide_rect(melee, player1): #account for player movement
                    list.remove(melee)
                    currentItem = previousItem
                    previousItem = None
                    meleeInUse = False
                    melee.updateHit(False)
                    break
                melee.updateWorld(-velocityX,-velocityY) #account for the world moving
                melee.updateOrientation()
                melee.updateBackwardMovement(0.9)
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
            break
        elif checkObjectCollision(projectile):
            list.remove(projectile)
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
    global hungerspeed
    enemyvelocityX = WorldVelocityX
    enemyvelocityY = WorldVelocityY
    #Only one of them can not equal zero at the same time
    if hungerspeed == 0.5:
        enemyvelocityX *= 0.5
        enemyvelocityY *= 0.5
    else:
        enemyvelocityX = WorldVelocityX
        enemyvelocityY = WorldVelocityY
    if collisionDetected: #if we are colliding with something, do not move the enemy
        collisionDetected = False #this is still a little buggy, fix this'
        WorldVelocityX = 0
        WorldVelocityY = 0
    for index, enemy in enumerate(list):
            #checkCollision(enemy)
            enemy.update(-enemyvelocityX,-enemyvelocityY)
            enemy.setTrajectory([START_COORDSX,START_COORDSY],SPEED/2,world.getCollideableList())
            enemy.render()

def renderHealthbar():
    global screen
    global healthbarIcon
    global player1
    healthbarIcon.update(PLAYER_STARTING_HEALTH,player1.getHealth())
    healthbarIcon.render(screen)

def renderHunger():
    global screen
    global hungerbar
    global player1
    #if isMoving
    if player1.getHungerTime() != None:
       # print(player1.getHungerTime())
        if 0 <= (player1.getHungerTime() % 5000) <= 10:
            player1.updateHunger(-5)
    hungerbar.update(PLAYER_STARTING_HUNGER,player1.getHunger())
    hungerbar.render(screen)

def renderCrate(list):
    global hungerspeed
    global screen
    global player1
    for index,crate in enumerate(list):
        crate.update(-WorldVelocityX * hungerspeed,-WorldVelocityY * hungerspeed)
        crate.render(screen)
        
def renderNight():
    global night
    global enemyList
    if night.getNightStatus() == False:
        if  0 <= (pygame.time.get_ticks() % 30000) <= 15: #every 3 minutes
            night.setNight(True,pygame.time.get_ticks())
            enemyList.clear()
    night.render(screen)
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

    if lastDirection == 2: #south
        if angledegree <= 180 and angledegree >= 0:
            return True

    if lastDirection == 3: #east
        if angledegree >= -90 and angledegree < 90:
            return True
    
    if lastDirection == 4: #west
        if angledegree < -90 or angledegree >= 90:
            return True
        
    return False

def isInteractable():
    global npc_sprite_list
    for row in enumerate(npc_sprite_list):
        if row[1].getRange() == True: #if we are in range of a npc
            if key_pressed[K_e]: #if the interact key is pressed
                for row in enumerate(npc_sprite_list):
                    if row[1].getRange(): #find the curernt npc thats being interacted with 
                        textbox1.updateStatus(True) #update the box to show
            break #dont go to other conditional after
        else: 
            textbox1.updateStatus(False) #textbox defaults off


def get_tile(): #returns the coordinate position of the player
    coords = [(player1.getRelativeX() - START_COORDSX)//TILE_SIZE,(player1.getRelativeY()-START_COORDSY)//TILE_SIZE]
    #print(playerXRelative//TILE_SIZE,playerYRelative//TILE_SIZE)
    #print(playerXRelative,playerYRelative)
    print(coords)

def get_tile_x():
    return (player1.getRelativeX() - START_COORDSX)//TILE_SIZE
 
def get_tile_y():
    return (player1.getRelativeY()-START_COORDSY)//TILE_SIZE



            

while running:


    clock.tick(60)
    #screen.fill((0,0,0))
    #print(pygame.time.get_ticks() % 10000)
    
    if (pygame.time.get_ticks() % 10000 >= 0)and (pygame.time.get_ticks() % 10000 <= 20): #for every 10 seconds, spawn an enemy
        num = random.randrange(1,10) #chooses a random number of enemy to spawn
        for i in range(num):
            spawn()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
    
            key_pressed = pygame.key.get_pressed()
            #not keydown is used to prevent strafing
            if key_pressed[K_d] and (not keyDown) and (not isMoving) and WorldVelocityX == 0: 
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
             

            elif key_pressed[K_a] and (not keyDown)and (not isMoving) and WorldVelocityX == 0:
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

            elif key_pressed[K_w] and (not keyDown)and (not isMoving)and WorldVelocityY == 0:
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

            elif key_pressed[K_s] and (not keyDown) and (not isMoving)and WorldVelocityY == 0:
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
                if inventory.getSeleciton() == None: #if there is nothing in our inventory
                    
                    emptyBag = True
                    textCreation("empty-bag")
                else:
                    inventory.onEnter()
                    inventorylist = inventory.getInventoryList()
                    selection = inventory.getSeleciton()
                
                    if selection == -1: #if we select this, then we are unselecting an item
                        itemUse = False
                    else:
                        currentItem = inventorylist[selection]
                        itemUse = True
            
            #crate interacction
            if key_pressed[K_e] and crateRadius == True:
                for index, obj in enumerate(crateList):
                    if obj.getRange() == True:
                        obj.loot(inventory)
                        crateList.remove(obj)
                        crateRadius = False

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

            elif event.key == K_a:
                 velocityX = 0
                 direction = -1
                 keyUp = True
                 keyDown = False
                 #onTile(-1)
                 #collision()

            elif event.key == K_w:
                 velocityY = 0
                 direction = -1
                 keyUp = True
                 keyDown = False
                 #onTile(-1)
                 #collision()

            elif event.key == K_s:
                 velocityY = 0
                 direction = 1
                 keyUp = True
                 keyDown = False
                 #onTile(1)

        elif event.type == pygame.MOUSEBUTTONDOWN and not startGameBool: #1 -left click, #2 - right click
            mousePos = pygame.mouse.get_pos()
         
            #print(inventory.getCurrentObject().dgetID())
            if currentItem != None:
                if event.button == 1 and itemUse and currentItem != None and inventory.getCurrentObject().getID() == "bow" or inventory.getCurrentObject().getID() == "firebook":
                    projectileFired = True
                if event.button == 1 and itemUse and currentItem != None and inventory.getCurrentObject().getID() == "sword" and not meleeInUse: #segment used to render melee attacks
                    if inRadius(): #if we are aiming infront of us 
                        meleeSwung = True
                        showAttackWarning = False
                    else:
                        showAttackWarning = True
                        textCreation("range")

            if event.button == 1 and currentItem != None and currentItem.getID() == "bandage":
                player1.updateHealth(20)
                currentItem.updateAmount(-1)
                if currentItem.getAmount() <= 0:
                    currentItem = None
                    Item = None


            #death button logic
            if event.button == 1 and endGame() == True and deathMessage.getExitRect().collidepoint(mousePos):
                running = False

            if event.button == 1 and endGame() == True and deathMessage.getAgainRect().collidepoint(mousePos):
                startGameBool = True


 

            



        
    

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
  
    startGame() #starts the game
    if endGame(): #if the player health is 0, everything is unrendered
        screen.fill('black')
        deathMessage.render(screen)
    else:
        isInteractable() #checks if we are in range of npcs
        world.run() #generates the world
        collision() #checks if anything is colldiing
        player() #renders player and player logic
        renderCrate(crateList)
        drawItem(currentItem) #draws any item in used
        if currentItem != None: #if there is a current item in use
            currentItem.renderObject(screen) #render the held object
        renderEnemy(enemyList) #render enemy
        renderProjectiles(projectileList) #render projectile
        renderMelee(meleeList) #render melee
        renderHealthbar() #render healthnar
        #renderHunger()
        renderText(textList)
        if inventory.getStatus():
            inventory.render(screen)
        renderNight()
        #inventory logic
    pygame.display.update()