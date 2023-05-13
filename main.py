import pygame
from pygame.locals import *
from sys import exit
from World import world_creator
from game_data import data
pygame.init()
screen = pygame.display.set_mode((1280,720)) #a single tile is 32 by 32, entire map is 60x60 tiles
playerImg = pygame.image.load("Sprites/grass.png") #fill this
world = world_creator(data,screen)
playerX = 370
playerY = 480
running = True

def player():
    screen.blit(playerImg,(playerX,playerY))

while running:
    #screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    #player()
    world.run()
    pygame.display.update()