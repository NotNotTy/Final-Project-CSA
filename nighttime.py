import pygame

class nighttime:

    def __init__(self):
        self.night = False
        self.starttime = None
        self.startnight = False

    def setNight(self,bool,starttime):
        if self.night == True:
            self.starttime = None
            self.night = False
        else:
            self.starttime = starttime
            self.night = bool

    def getNightStatus(self):
        return self.startnight

    def render(self,display):
        if self.starttime != None:
            if 0 <= (pygame.time.get_ticks() - self.starttime) <= 15: 

                self.startnight = True

            elif pygame.time.get_ticks() - self.starttime >= 500000:
                self.startnight = False

        if self.startnight == True and self.night == True:
            s = pygame.Surface((1216,704))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill((0,0,0))           # this fills the entire surface
            display.blit(s, (0,0))    # (0,0) are the top-left coordinates