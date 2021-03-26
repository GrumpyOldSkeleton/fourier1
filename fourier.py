import pygame
import math
from collections import deque 
  
  
done = False
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
ORIGINX = SCREEN_WIDTH / 2
ORIGINY = SCREEN_HEIGHT / 2
pygame.init()
pygame.display.set_caption("Fourier 2")
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
clock = pygame.time.Clock()


# just some colour constants
WHITE = (255, 255, 255)
COLOUR_PICO8_BLACK      = (0, 0, 0)
COLOUR_PICO8_DARKBLUE   = (29, 43, 83)
COLOUR_PICO8_PURPLE     = (126, 37, 83)
COLOUR_PICO8_DARKGREEN  = (0, 135, 81)
COLOUR_PICO8_BROWN      = (171, 82, 54)
COLOUR_PICO8_DARKGREY   = (95, 87, 79)
COLOUR_PICO8_LIGHTGREY  = (194, 195, 199)
COLOUR_PICO8_WHITE      = (255, 241, 232)
COLOUR_PICO8_RED        = (255, 0, 77)
COLOUR_PICO8_ORANGE     = (255, 163, 0)
COLOUR_PICO8_YELLOW     = (255, 236, 39)
COLOUR_PICO8_GREEN      = (0, 228, 54)
COLOUR_PICO8_BLUE       = (41, 173, 255)
COLOUR_PICO8_LAVENDER   = (131, 118, 156)
COLOUR_PICO8_PINK       = (255, 119, 168)
COLOUR_PICO8_LIGHTPEACH = (255, 204, 170)

COLOURS = [COLOUR_PICO8_LIGHTPEACH, COLOUR_PICO8_RED, COLOUR_PICO8_ORANGE, COLOUR_PICO8_YELLOW, COLOUR_PICO8_YELLOW, COLOUR_PICO8_WHITE, COLOUR_PICO8_GREEN, COLOUR_PICO8_GREEN]


# ======================================================================
# circle class from The Coding Train
# ======================================================================

class FourierCircle():
    
    def __init__(self):
        
        self.radius  = 75
        self.centre  = (self.radius + 90, ORIGINY)
        self.angle   = 0
        # using deque instead of list for insert/pop speed increase
        # plain list will work fine instead though
        self.yvals = deque([]) 
    
    def draw(self):
        
        self.angle += 2
        if self.angle > 359:
            self.angle = 0
          
        x = 0
        y = 0
        
        nvals = (1, 3, 5, 7)
        
        for n in (nvals):
                
            prevx = x
            prevy = y    
               
            self.radius  = 75 * (4 / (n * math.pi))
                
            # calculate rotator point position
            x += self.radius * math.cos(math.radians(n * self.angle)) 
            y += self.radius * math.sin(math.radians(n * self.angle))

            pygame.draw.circle(screen, COLOURS[n%5], (prevx + self.centre[0], prevy + self.centre[1]), self.radius,1)
            # draw line to rotating point
            pygame.draw.line(screen, COLOUR_PICO8_YELLOW, (prevx + self.centre[0], prevy + self.centre[1]), (x + self.centre[0], y + self.centre[1]), 2)
            
        # push the y value into the beginning of the queue
        self.yvals.insert(0, y)
            
        # work out an offset for drawing the wave
        waveoffsetx = self.centre[0] + 150
        
        # draw centre line through wave just for show
        pygame.draw.line(screen, COLOUR_PICO8_DARKGREY, (self.centre[0]+150, self.centre[1]), (950, self.centre[1]))
        
        # draw line to first point in wave
        pygame.draw.line(screen, COLOUR_PICO8_BLUE, (x + self.centre[0], self.yvals[0] + 200), (waveoffsetx, self.yvals[0] + 200), 2)
        
        # draw all points of wave
        for i in range(len(self.yvals)-1):
            pygame.draw.circle(screen, WHITE, (waveoffsetx + i, self.yvals[i] + self.centre[1]), 1)
            
        # prune the list to keep it manageable
        if len(self.yvals) > 628:
            self.yvals.pop()
            
            
            
        

fc = FourierCircle()

while not done:
    
    screen.fill([0,0,0])
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                done = True
         
    fc.draw()
    clock.tick(50)
    pygame.display.flip()
    

pygame.quit()
