import pygame
class melee:
    def __init__(self,x,y,image,dmg,nx,ny,angle):
        self.image = pygame.Surface((64,64))
        self.image = pygame.image.load(image)
        self.updatedImage = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.damage = dmg
        self.x = x
        self.y = y
        self.nx = nx
        self.ny = ny
        self.time = pygame.time.get_ticks()
        self.angle = angle - 90

    def set(self,x,y):
        self.x = x
        self.y = y

    def update(self):
        self.x += self.nx
        self.y += self.ny
        self.rect = self.rect.move(self.nx,self.ny)

    def updateOrientation(self):
            loc = self.image.get_rect().topleft  #rot_image is not defined 
            rot_sprite = pygame.transform.rotate(self.image, self.angle) #all melee sprites are inteneded to be created straight up
            rot_sprite.get_rect().topleft = loc
            self.updatedImage = rot_sprite

    def updateForwardMovement(self, speed):
        self.x += self.nx * speed
        self.y += self.ny * speed
        self.rect = self.rect.move(self.nx * speed,self.ny * speed)

    def updateBackwardMovement(self, speed):
        self.x -= self.nx *speed
        self.y -= self.ny * speed
        self.rect = self.rect.move(-self.nx * speed,-self.ny * speed)

    def updateWorld(self,x,y):
        self.x += x
        self.y += y
        self.rect = self.rect.move(x,y)
    def render(self, display):
        display.blit(pygame.transform.rotate(self.image,self.angle),(self.x,self.y))

    def getTime(self):
        return self.time
    
