import pygame

pygame.init()
W, H=500, 350
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

rectangles.extend([0, 0, 500, 50, 0, 300, 31, 158, 27])
rectangles.extend([0, 0, 50, 200, 0, 105, 70, 70, 70])
rectangles.extend([0, 0, 50, 200, 450, 105, 70, 70, 70])
rectangles.extend([0, 0, 100, 25, 200, 200, 45, 45, 45])

polygons.extend([350, 300, 450, 250, 450, 300, 450, 301])



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
            self.poly = self.createPolygon(self.x, self.y, polygons, c)
            pygame.draw.polygon(screen, wall, self.poly)
        for c in range(0, len(rectangles), 9):
            rectangle = pygame.Rect(rectangles[c], rectangles[c+1], rectangles[c+2], rectangles[c+3])
            rectangle.x = self.x+rectangles[c+4]
            rectangle.y = self.y+rectangles[c+5]
            pygame.draw.rect(screen, (rectangles[c+6], rectangles[c+7], rectangles[c+8]), rectangle)
  
    def createPolygon(self, x, y, list, z):
        return [
            (x+list[z], list[z+1]+y), (x+list[z+2], list[z+3]+y), 
            (x+list[z+4], list[z+5]+y), (x+list[z+6], list[z+7]+y)]

    def __init__(self, color, size=20, speed=.025, maxvelosity=9):
        self.x=0
        self.y=0
        self.col=color
        self.size=size
        self.speed=speed
        self.xvelosity=0
        self.yvelosity=0
        self.maxvelosity=maxvelosity
        self.direction=(0, 0)
        self.friction=0.5
        self.gravity=.025
        self.jump=False
        self.grounded=True
        self.stepup=0
        self.maxstepup=2

    def draw(self):
        s=self.size
        self.rect=pygame.Rect(W/2-s/2, H/2-s/2, self.size, self.size)
        pygame.draw.rect(screen, self.col, self.rect)

    def allcolision(self):
        coliding = 0
        for z in range(0, len(rectangles), 9):
            rectangle = pygame.Rect((rectangles[z], rectangles[z+1]), (rectangles[z+2], rectangles[z+3]))
            rectangle.x = self.x+rectangles[z+4]
            rectangle.y = self.y+rectangles[z+5]
            if rectangle.colliderect(self.rect):
                coliding += 1

        for z in range(0, len(polygons), 8):
            polygon = self.createPolygon(self.x, self.y, polygons, z)
            if collideRectPolygon(self.rect, polygon):
                coliding += 1
        
        if coliding == 0:
            return False
        else:
            return True
            
    def move(self):
        self.xvelosity += self.speed*self.direction*dt

        if self.jump == True and self.grounded == True:
            self.yvelosity = 100000
            self.grounded = False

        self.yvelosity -= self.gravity*dt
        if abs(self.yvelosity) > self.maxvelosity:
            if self.yvelosity > 0:
                self.yvelosity = self.maxvelosity
            else:
                self.yvelosity = -self.maxvelosity
        
        self.y += self.yvelosity
        if self.allcolision():
            self.y -= self.yvelosity
            if self.yvelosity < 0:
                self.grounded = True
            else:
                self.grounded = False
            self.yvelosity = 0

        if abs(self.xvelosity) > self.maxvelosity:
            self.xvelosity = self.maxvelosity*self.direction
        if self.direction==0:
            if abs(self.xvelosity) < 0.35:
                self.xvelosity = 0
            else:
                if self.xvelosity > 0:
                    self.xvelosity -= self.friction
                else:
                    self.xvelosity += self.friction
        
        self.x += self.xvelosity
        if self.allcolision():
            self.stepup = 0
            while self.allcolision() and self.stepup < self.maxstepup*abs(self.xvelosity):
                self.y += 1
                self.stepup += 1
            if self.stepup >= self.maxstepup*abs(self.xvelosity):
                self.y -= self.stepup
                self.x -= self.xvelosity
                self.xvelosity = 0
                
            

p=player(red)
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    p.bg()
    p.draw()

    keys=pygame.key.get_pressed()
    
    p.direction = ((keys[pygame.K_a]-keys[pygame.K_d]))

    if keys[pygame.K_w]: p.jump=True
    else: p.jump=False

    p.move()

    pygame.display.update()

pygame.quit()