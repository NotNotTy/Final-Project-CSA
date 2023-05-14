import pygame
from pygame.locals import *
from sys import exit
from World import world_creator
from player import Player
from game_data import data
from npc import NPC
from textbox import textbox
from textGenerator import TextGenerator
pygame.init()
pygame.font.init()
LENGTH = 1280
WIDTH = 704
screen = pygame.display.set_mode((LENGTH,WIDTH)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/playertemp.png") #fill this
npcImg = pygame.image.load("Sprites/playertemp.png")
textboxImg = pygame.image.load("Sprites/textbox.png")
world = world_creator(data,screen) #generates the world 
clock = pygame.time.Clock() #clock
TILE_SIZE = 32 #each tile is 32x32 big
FPS = 60 #pretty self explainitory
CAMERA_EDGE_X = 1120 #the edges are where the world will start to shift to give the impression that the camera is following the player
CAMERA_EDGE_Y = 576
START_COORDSX = 640 #start coordinates, used to keep the original position in a constant
START_COORDSY = 352
NPC_STARTCOORDSX = 672
NPC_STARTCOORDSY = 384
TEXTBOX_COORDSX = 100
TEXTBOX_COORDSY = 100
playerX = START_COORDSX #playerX and playerY are coordinates relative to the screen. These coords are used for the physical posiiton of the player on the screen
playerY = START_COORDSY
playerXRelative = playerX #playerXRelative and playerYRelative are coordinates relative to the map in the game. These coords are used for in-game position 
playerYRelative = playerY
player1 = Player(32,START_COORDSX,START_COORDSY,playerImg)
npc1 = NPC(32,NPC_STARTCOORDSX,NPC_STARTCOORDSY,npcImg,'npc',False)
textbox1 = textbox(32,TEXTBOX_COORDSX,TEXTBOX_COORDSY,textboxImg,'textbox',False)
text = TextGenerator(playerXRelative,playerYRelative - 64,'press E to interact','freesansbold.ttf')
all_sprites_list = pygame.sprite.Group()
npc_sprite_list = pygame.sprite.Group()
textbox_sprite_list = pygame.sprite.Group()
all_sprites_list.add(player1)
all_sprites_list.add(npc1)
npc_sprite_list.add(npc1)
textbox_sprite_list.add(textbox1)
running = True




def player(): #draws the player
    #player1 = pygame.Rect(playerX,playerY,playerX, playerY)
    #screen.blit(playerImg,player1)
    all_sprites_list.draw(screen)




def get_tile(): #returns the coordinate position of the player
    coords = [(playerXRelative - START_COORDSX)//TILE_SIZE,(playerYRelative-START_COORDSY)//TILE_SIZE]
    #print(playerXRelative//TILE_SIZE,playerYRelative//TILE_SIZE)
    print(coords)

def collision():
    interactable()
    list = world.getObjectList()
    for row_index, row in enumerate(list[1]):
        if pygame.sprite.collide_rect(player1, row):
            print(row.getType())

def interactable():
    for row in enumerate(npc_sprite_list):
         if pygame.sprite.collide_rect(player1, row[1]):
            screen.blit(text.getText(),text.getTextRect())
            row[1].editRange(True)
            #print(row[1].getRange())
         else:
             row[1].editRange(False)
             #print(row[1].getRange())






while running:
    clock.tick(60)
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_d]:
                player1.update(TILE_SIZE,0) # playerX -= TILE_SIZE
                playerXRelative += TILE_SIZE
                get_tile()
                #collision()

            if key_pressed[K_a]:
                player1.update(-TILE_SIZE,0)#playerX -= TILE_SIZE
                playerXRelative -= TILE_SIZE
                get_tile()
                #collision()

            if key_pressed[K_w]:
                player1.update(0,-TILE_SIZE)#playerY -= TILE_SIZE
                playerYRelative -= TILE_SIZE
                get_tile()
                #collision()

            if key_pressed[K_s]:
                player1.update(0,TILE_SIZE)#playerY += TILE_SIZE
                playerYRelative += TILE_SIZE
                get_tile()
                #collision()

            #textbox logic
            if key_pressed[K_e]:
                for row in enumerate(npc_sprite_list):
                    if row[1].getRange():
                        textbox1.updateStatus(True) #figure out a work around for this later
            

    #once we are out of range, also figure out a work around if the scenerio of multiple textboxes
    for row in enumerate(npc_sprite_list):
        if row[1].getRange() != True:
            textbox1.updateStatus(False)

    #camera logic
    if player1.getX() >= CAMERA_EDGE_X:
        all_sprites_list.update(-TILE_SIZE,0)#playerX -= TILE_SIZE
        world.update_layout(-TILE_SIZE,0)
    if player1.getX()  <= LENGTH - CAMERA_EDGE_X:
        all_sprites_list.update(TILE_SIZE,0)#playerX += TILE_SIZE
        world.update_layout(TILE_SIZE,0)
    if player1.getY() >= CAMERA_EDGE_Y:
        all_sprites_list.update(0,-TILE_SIZE)#playerY -= TILE_SIZE
        world.update_layout(0,TILE_SIZE)
    if player1.getY() <= WIDTH - CAMERA_EDGE_Y:
        all_sprites_list.update(0,TILE_SIZE)#playerY += TILE_SIZE
        world.update_layout(0,-TILE_SIZE)

    
    screen.fill('black')
    world.run(textbox_sprite_list)
    player()
    collision()
    pygame.display.update()