import pygame

class projectile:
    def __init__(self,x,y,image,dmg,nx,ny,angle):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 64)
        self.damage = dmg
        self.x = x
        self.y = y
        self.nx = nx
        self.ny = ny
        self.time = pygame.time.get_ticks()
        self.angle = angle

    def set(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        self.x += self.nx
        self.y += self.ny

    def updateWorld(self,x,y):
        self.x += x
        self.y += y
    def render(self, display):
        display.blit(pygame.transform.rotate(self.image,self.angle),(self.x,self.y))

    def getTime(self):
        return self.time