import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x ,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))


    def update(self,x,y):
        self.rect.x += x
        self.rect.y -= y
        #print(self.rect.x)



class StaticTile(Tile):
    def __init__(self,size,x,y,surface,t,cx,cy):
        super().__init__(size,x,y)
        self.image = surface
        self.type = t
        self.coordx = cx
        self.coordy = cy

    def get_coords(self):
        coord = [self.coordx,self.coordy]
        return coord
    
    def getType(self):
        return self.type

