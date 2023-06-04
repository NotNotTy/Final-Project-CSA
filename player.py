import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, size, x ,y,surface,tag,health):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.image = surface
        self.relativeX = x
        self.relativeY = y
        self.cropped_region = (0,0,64,64)
        self.cropped_subsurf = self.image.subsurface(self.cropped_region)
        self.ID = tag
        self.startHealth = health
        self.health = health
        self.invul = False
        self.starttime = 0 #startime for invul

    def update(self,x,y):
        self.rect.x += x
        self.rect.y += y
        #print(self.rect.x)
    def updateRelative(self,x,y):
        self.relativeX += x
        self.relativeY += y
        #self.rect.x += x
        #self.rect.y += y

    def updateHealth(self,x):
        if (self.health + x > self.startHealth):
            x = self.health + x - self.startHealth
        self.health += x

    def getHealth(self):
        return self.health

    def getDamage(self):
        return 0
    
    def setInvulurbility(self,x):
        self.invul = x

    def setStartTime(self,starttime):
        self.starttime = starttime

    def getRect(self):
        return self.rect

    def getInvulurbility(self):
        return self.invul
    
    def getTime(self):
        return self.starttime

    def updateSprite(self, id):
        TILE_SIZE = 64
        if id == 1: #north
            if (self.relativeY % TILE_SIZE) != 0: #if he is moving
                self.cropped_region = (TILE_SIZE,TILE_SIZE * 3,TILE_SIZE,TILE_SIZE)
            else:
                self.cropped_region = (0, TILE_SIZE* 3,TILE_SIZE,TILE_SIZE)
        if id == 2: #south
            if (self.relativeY % TILE_SIZE) != 0:
                self.cropped_region = (TILE_SIZE,0,TILE_SIZE,TILE_SIZE)
            else:
                self.cropped_region = (0,0,TILE_SIZE,TILE_SIZE)

        if id == 3: #east
            if (self.relativeX % TILE_SIZE) != 0:
                self.cropped_region = (TILE_SIZE,TILE_SIZE * 2,TILE_SIZE,TILE_SIZE)
            else:
                self.cropped_region = (0,TILE_SIZE * 2,TILE_SIZE,TILE_SIZE)

        if id == 4: #west
            if (self.relativeX % TILE_SIZE) != 0:
                self.cropped_region = (TILE_SIZE,TILE_SIZE,TILE_SIZE,TILE_SIZE)
            else:
                self.cropped_region = (0,TILE_SIZE,TILE_SIZE,TILE_SIZE)




    def render(self,display):
        self.cropped_subsurf = self.image.subsurface(self.cropped_region)
        display.blit(self.cropped_subsurf,(self.rect.x,self.rect.y - 3)) #the sprite for red has an offset of about 3 pixels

    def getRelativeX(self):
        return self.relativeX
    
    def getRelativeY(self):
        return self.relativeY
    
    def getX(self):
        return self.rect.x
    
    def getY(self):
        return self.rect.y
    
    def getID(self):
        return self.ID
    