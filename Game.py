import pygame
from stopwatch import Stopwatch

worldxscale = 1
worldyscale = 1
renderxscale = 1
renderyscale = 1

camerax = 0
cameray = 0

pygame.init()
W, H=800, 450
#W, H=400, 800
screen = pygame.display.set_mode([W, H])
pygame_icon = pygame.image.load('Hammer Icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Half Life III")
clock = pygame.time.Clock()

running = True

bcg=(200, 200, 200)
red=(255, 0 ,0)
purp=(255, 0, 255)
wall=(100, 100, 100)

rectangles = []
polygons = []

rectangles.extend([0, 0, 800, 200, 0, 300, 31, 158, 27]) #main green floor
rectangles.extend([0, 0, 100, 30, 200, 200, 50, 50, 50]) #start floating platform
rectangles.extend([0, 0, 50, 200, 0, 200, 70, 70, 70])
rectangles.extend([0, 0, 50, 200, 450, 100, 70, 70, 70])

polygons.extend([350, 300, 450, 250, 450, 300, 450, 301])
polygons.extend([590, 300, 720, 240, 720, 300, 719, 300])

def collideLineLine(l1_p1, l1_p2, l2_p1, l2_p2):

    # normalized direction of the lines and start of the lines
    P  = pygame.math.Vector2(*l1_p1)
    line1_vec = pygame.math.Vector2(*l1_p2) - P
    R = line1_vec.normalize()
    Q  = pygame.math.Vector2(*l2_p1)
    line2_vec = pygame.math.Vector2(*l2_p2) - Q
    S = line2_vec.normalize()

    # normal vectors to the lines
    RNV = pygame.math.Vector2(R[1], -R[0])
    SNV = pygame.math.Vector2(S[1], -S[0])
    RdotSVN = R.dot(SNV)
    if RdotSVN == 0:
        return False

    # distance to the intersection point
    QP  = Q - P
    t = QP.dot(SNV) / RdotSVN
    u = QP.dot(RNV) / RdotSVN

    return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

def colideRectLine(rect, p1, p2):
    return (collideLineLine(p1, p2, rect.topleft, rect.bottomleft) or
            collideLineLine(p1, p2, rect.bottomleft, rect.bottomright) or
            collideLineLine(p1, p2, rect.bottomright, rect.topright) or
            collideLineLine(p1, p2, rect.topright, rect.topleft))

def collideRectPolygon(rect, polygon):
    for i in range(len(polygon)-1):
        if colideRectLine(rect, polygon[i], polygon[i+1]):
            return True
    return False

class player:
    def bg(self):        
        screen.fill((200, 200, 200))
        for c in range(0, len(polygons), 8):
            self.poly = self.createrenderPolygon(camerax, cameray, polygons, c)
            pygame.draw.polygon(screen, wall, self.poly)
        for c in range(0, len(rectangles), 9):
            rectangle = pygame.Rect(rectangles[c]*renderxscale, rectangles[c+1]*renderyscale, rectangles[c+2]*renderxscale, rectangles[c+3]*renderyscale)
            rectangle.x = (camerax+rectangles[c+4])*renderxscale
            rectangle.y = (cameray+rectangles[c+5])*renderxscale
            pygame.draw.rect(screen, (rectangles[c+6], rectangles[c+7], rectangles[c+8]), rectangle)
  
    def createworldPolygon(self, x, y, list, z):
        return [
            (x+list[z], list[z+1]+y), (x+list[z+2], list[z+3]+y), 
            (x+list[z+4], list[z+5]+y), (x+list[z+6], list[z+7]+y)]
    
    def createrenderPolygon(self, x, y, list, z):
        return [
            ((x+list[z])*renderxscale, (list[z+1]+y)*renderyscale), ((x+list[z+2])*renderxscale, (list[z+3]+y)*renderyscale), 
            ((x+list[z+4])*renderxscale, (list[z+5]+y)*renderyscale), ((x+list[z+6])*renderxscale, (list[z+7]+y)*renderyscale)]

    def __init__(self, color):
        self.x=250*renderxscale
        self.y=170*renderyscale
        self.col=color
        self.xsize=20
        self.ysize=20
        self.speed=.025
        self.xvelosity=0
        self.yvelosity=0
        self.maxxvelosity=9
        self.maxyvelosity=20
        self.direction=(0, 0)
        self.friction=0.5
        self.gravity=.025
        self.jump=False
        self.stepup=0
        self.maxstepup=10
        self.dash=False
        self.candash=False
        self.groundtimer = 0
        self.dashtimer = Stopwatch()
        self.noclip = False
    
    def draw(self):
        #self.drawrect=pygame.Rect(W/2-self.xsize*renderxscale/2, H/2-self.ysize*renderyscale/2, self.xsize*renderxscale, self.ysize*renderyscale)
        #self.drawrect=pygame.Rect(camerax-self.x+W/2-self.xsize*renderxscale/2, cameray-self.y+H/2-self.ysize*renderyscale/2, self.xsize*renderxscale, self.ysize*renderyscale)
        self.drawrect=pygame.Rect((self.x+camerax)*renderxscale-self.xsize*renderxscale, (self.y+cameray)*renderxscale-self.ysize*renderyscale, self.xsize*renderxscale, self.ysize*renderyscale)
        print(self.x+camerax)
        pygame.draw.rect(screen, self.col, self.drawrect)

    def allcolision(self):
        coliding = 0
        self.rect=pygame.Rect((self.x+camerax)-self.xsize, (self.y+cameray)-self.ysize, self.xsize, self.ysize)
        for z in range(0, len(rectangles), 9):
            rectangle = pygame.Rect((rectangles[z], rectangles[z+1]), (rectangles[z+2], rectangles[z+3]))
            rectangle.x = camerax+rectangles[z+4]
            rectangle.y = cameray+rectangles[z+5]
            if rectangle.colliderect(self.rect):
                coliding += 1

        for z in range(0, len(polygons), 8):
            polygon = self.createworldPolygon(camerax, cameray, polygons, z)
            if collideRectPolygon(self.rect, polygon):
                coliding += 1
        
        if coliding == 0:
            return False
        else:
            return True
            
    def gravitymove(self):
        global camerax, cameray

        self.xvelosity += self.speed*self.direction[0]*dt
        
        self.yvelosity -= self.gravity*dt
        
        if self.jump == True and self.groundtimer > 0:
            self.yvelosity = 10
            self.groundtimer = 0

        if self.dash == True and self.candash == True and self.dashtimer.duration > 1:
            if self.direction[0] != 0:
                self.xvelosity = self.direction[0]*15
            if self.direction[1] != 0:
                self.yvelosity = self.direction[1]*10
            if self.groundtimer > 0:
                self.dashtimer.reset()
                self.dashtimer.start()
            self.candash = False
            
        if self.groundtimer > 2:
            self.maxxvelosity = 7
            self.maxyvelosity = 10
            self.speed = .03
            self.friction = .4
        else:
            self.maxxvelosity = 11
            self.maxyvelosity = 30
            self.speed = .025
            self.friction = .2

        if abs(self.yvelosity) > self.maxyvelosity:
            if self.yvelosity > 0:
                self.yvelosity = self.maxyvelosity
            else:
                self.yvelosity = -self.maxyvelosity

        if abs(self.xvelosity) > self.maxxvelosity:
            self.xvelosity = self.maxxvelosity*self.direction[0]
        if self.direction[0]==0:
            if abs(self.xvelosity) < 0.35:
                self.xvelosity = 0
            else:
                if self.xvelosity > 0:
                    self.xvelosity -= self.friction
                else:
                    self.xvelosity += self.friction

        self.y -= self.yvelosity
        if self.allcolision():
            self.y += self.yvelosity
            if self.yvelosity < 0:
                self.groundtimer += 1
                self.candash = True
            else:
                self.groundtimer = 0
            self.yvelosity = 0


        self.x -= self.xvelosity
        if self.allcolision():
            self.stepup = 0
            while self.allcolision() and self.stepup < self.maxstepup*(abs(self.xvelosity)/4):
                self.y -= 1
                self.stepup += 1
            if self.stepup >= self.maxstepup*(abs(self.xvelosity)/4):
                self.y += self.stepup
                self.x += self.xvelosity
                self.xvelosity = 0
                
        camerax = -self.x+W/2
        cameray = -self.y+H/2

    def noclipmove(self):
        global camerax, cameray
        self.x -= self.direction[0]*(self.dash+1)*3
        self.y -= self.direction[1]*(self.dash+1)*3

        camerax = -self.x+W/2
        cameray = -self.y+H/2


clicking = 0
e = 0
p=player(red)
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    p.bg()
    p.draw()

    keys=pygame.key.get_pressed()
    mousekey=pygame.mouse.get_pressed()
    mousepos=pygame.mouse.get_pos()
    

    p.direction = ((keys[pygame.K_a]-keys[pygame.K_d]), (keys[pygame.K_w]-keys[pygame.K_s]))

    if keys[pygame.K_SPACE]: p.jump=True
    else: p.jump=False

    if keys[pygame.K_LSHIFT]: p.dash=True
    else: p.dash=False

    if mousekey[0] and clicking == 0: 
        clicking = 1
        print(round(mousepos[0]-camerax, -1), round(mousepos[1]-cameray, -1))
    if clicking == 1: 
        if not(mousekey[0]):
            clicking = 0
    
    if keys[pygame.K_r]: 
        p.x=300*renderxscale 
        p.y=200*renderyscale

    if keys[pygame.K_o]:
        renderxscale -= .0125
        renderyscale -= .0125

    if keys[pygame.K_p]:
        renderxscale += .0125
        renderyscale += .0125

    if keys[pygame.K_e] and e == 0:
        p.noclip = not p.noclip
        e = 1
    if not keys[pygame.K_e]:
        e = 0
    
    if not p.noclip:
        p.gravitymove()
    else:
        p.noclipmove()

    pygame.display.update()

pygame.quit()