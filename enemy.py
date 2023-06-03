import pygame
import math
class enemy:
    def __init__(self,sprite,health,damage,startx,starty,endx,endy,screen,tag):
        self.image = pygame.Surface((64,64))
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.rect.topleft = (startx,starty)
        self.green = None
        self.red = None
        self.startinghealth = health
        self.health = health
        self.damage = damage
        self.screen = screen
        self.x = startx
        self.y = starty
        self.nx = 0
        self.ny = 0
        self.eyesightRect = pygame.draw.line(self.screen,(0,0,0),(self.x,self.y),(endx,endy),10)
        self.ID = tag
        self.percantage = 0
        self.width = 64
        self.height = 20
        self.vision = 1
        self.visionStatus = False
        self.obstacle = None

    def render(self):
        self.screen.blit(self.image,(self.x,self.y))
        pygame.draw.rect(self.screen,(255,0,0),self.red)
        pygame.draw.rect(self.screen,(0,255,0),self.green)
        #self.eyesightRect
        #display.blit(self.image,(self.x,self.y))

    def update(self,x,y):
        #print(self.x)
        self.x += (self.nx * self.vision) + x
        self.y += (self.ny * self.vision) + y
        self.percantage = self.health/self.startinghealth
        #self.rect = self.rect.move(self.nx,self.ny)
        self.green = pygame.Rect(self.x,self.y+self.width,self.width,self.height)
        self.red = pygame.Rect(self.x,self.y+self.width,self.width,self.height )
        self.rect= self.rect.clamp(pygame.Rect(self.x,self.y,64,64)) #clamp allowed me to clamp the rect to the enemy
        if self.percantage == 1:
            self.green = pygame.Rect(self.x,self.y + self.width,self.width,self.height )
        else:
            print(64 * self.percantage)
            difference = self.width * self.percantage
            self.green = pygame.Rect(self.x,self.y + self.width,difference,self.height)
       
    def getID(self):
        return self.ID
    
    def getHealth(self):
        return self.health
    
    def updateHealth(self, x):
        self.health += x

    def getDamage(self):
        return self.damage
    
    def setTrajectory(self,end,speed,objList): #draws a line, if the line collides with something, then stop
        self.eyesightRect = pygame.draw.line(self.screen,(0,0,0),(self.x + 32,self.y + 32),(end[0] + 32,end[1] + 32),1)
        if self.obstacle != None:
            if not pygame.Rect.colliderect(self.obstacle.getRect(),self.eyesightRect): #if we are not colliding with the same object again
                self.vision = 1
                self.visionStatus = True
        for index, obj in enumerate(objList[1]):
            if pygame.Rect.colliderect(obj.getRect(),self.eyesightRect):
                self.vision = 0
                self.visionStatus = False
                self.obstacle = obj

        distance_y = self.y - end[1]
        distance_x = self.x - end[0]
        angle = math.atan2(distance_y, distance_x)
        speed_x = speed * math.cos(angle)
        speed_y = speed * math.sin(angle)
        self.nx = -speed_x
        self.ny = -speed_y
        #print(self.eyesightRect.x,self.eyesightRect.y)
        #self.screen.blit(self.image, (self.eyesightRect.x +64,self.eyesightRect.y +64))
        #pygame.draw.line(self.screen,(0,0,0),(self.x,self.y),end,10)