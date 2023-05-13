import pygame
from pygame.locals import *
from sys import exit
from World import world_creator
from game_data import data
pygame.init()
pygame.font.init()
LENGTH = 1280
WIDTH = 704
screen = pygame.display.set_mode((LENGTH,WIDTH)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/rock.png") #fill this
world = world_creator(data,screen) #generates the world 
clock = pygame.time.Clock() #clock
TILE_SIZE = 32 #each tile is 32x32 big
FPS = 60 #pretty self explainitory
CAMERA_EDGE_X = 1120 #the edges are where the world will start to shift to give the impression that the camera is following the player
CAMERA_EDGE_Y = 576
START_COORDSX = 640 #start coordinates, used to keep the original position in a constant
START_COORDSY = 352
playerX = START_COORDSX #playerX and playerY are coordinates relative to the screen. These coords are used for the physical posiiton of the player on the screen
playerY = START_COORDSY
playerXRelative = playerX #playerXRelative and playerYRelative are coordinates relative to the map in the game. These coords are used for in-game position 
playerYRelative = playerY
running = True




def player(): #draws the player
    screen.blit(playerImg,(playerX,playerY))


def get_tile(): #returns the coordinate position of the player
    coords = [(playerXRelative - START_COORDSX)//TILE_SIZE,(playerYRelative-START_COORDSY)//TILE_SIZE]
    print(coords)



while running:
    clock.tick(60)
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_d]:
                playerX += TILE_SIZE
                playerXRelative += TILE_SIZE
                get_tile()

            if key_pressed[K_a]:
                playerX -= TILE_SIZE
                playerXRelative -= TILE_SIZE
                get_tile()

            if key_pressed[K_w]:
                playerY -= TILE_SIZE
                playerYRelative -= TILE_SIZE
                get_tile()

            if key_pressed[K_s]:
                playerY += TILE_SIZE
                playerYRelative += TILE_SIZE
                get_tile()
                
    if playerX >= CAMERA_EDGE_X:
        playerX -= 32
        world.update_layout(-32,0)
    if playerX  <= LENGTH - CAMERA_EDGE_X:
        playerX += 32
        world.update_layout(32,0)
    if playerY >= CAMERA_EDGE_Y:
        playerY -= 32
        world.update_layout(0,32)
    if playerY <= WIDTH - CAMERA_EDGE_Y:
        playerY += 32
        world.update_layout(0,-32)


    screen.fill('black')
    world.run()
    player()
    pygame.display.update()