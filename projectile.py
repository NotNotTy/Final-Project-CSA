import pygame

class projectile:
    def __init__(self,x,y,image,dmg,nx,ny,angle,tag):
        self.image = pygame.Surface((64,64))
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.damage = dmg
        self.x = x
        self.y = y
        self.nx = nx
        self.ny = ny
        self.time = pygame.time.get_ticks()
        self.angle = angle
        self.ID = tag

    def getID(self):
        return self.ID
    def set(self,x,y):
        self.x = x
        self.y = y

    def getDamage(self):
        return self.damage

    def update(self):
        self.x += self.nx
        self.y += self.ny
        self.rect = self.rect.move(self.nx,self.ny)

    def updateWorld(self,x,y):
        self.x += x
        self.y += y
        self.rect = self.rect.move(x,y)
    def render(self, display):
        display.blit(pygame.transform.rotate(self.image,self.angle),(self.x,self.y))

    def getTime(self):
        return self.time