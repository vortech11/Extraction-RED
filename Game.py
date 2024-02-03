import pygame, json, yaml, os
from stopwatch import Stopwatch


with open("config.yaml", "r") as yamlfile:
    settings = yaml.safe_load(yamlfile)
    yamlfile.close()

script_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_directory, "levels/level.json")
with open(json_file_path, "r") as levelfile:
    leveldict = json.load(levelfile)
    levelfile.close()


renderxscale = settings['cameraxscale']
renderyscale = settings['camerayscale']

camerax = leveldict["player"]["startpos"][0]
cameray = leveldict["player"]["startpos"][1]

pygame.init()
W, H=settings['W'], settings['H']
screen = pygame.display.set_mode([W, H])
pygame_icon = pygame.image.load('images/Hammer Icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Half Life III")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial" , 12 , bold = True)

running = True

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

def playerinput():
    global renderxscale, renderyscale, clicking, v, a, s
    keys=pygame.key.get_pressed()
    mousekey=pygame.mouse.get_pressed()
    mousepos=pygame.mouse.get_pos()

    p.direction = ((keys[pygame.K_LEFT]-keys[pygame.K_RIGHT]), (keys[pygame.K_UP]-keys[pygame.K_DOWN]))

    if keys[pygame.K_z]: p.jump=True
    else: p.jump=False

    if keys[pygame.K_c]: p.dash=True
    else: p.dash=False

    if mousekey[0] and clicking == 0: 
        clicking = 1
        print(round(mousepos[0]-camerax, -1), round(mousepos[1]-cameray, -1))
    if clicking == 1: 
        if not(mousekey[0]):
            clicking = 0
    
    if keys[pygame.K_f]: 
        p.x=leveldict['player']['startpos'][0]
        p.y=leveldict['player']['startpos'][1]

    if keys[pygame.K_o]:
        renderxscale /= 1.0125
        renderyscale /= 1.0125

    if keys[pygame.K_p]:
        renderxscale *= 1.0125
        renderyscale *= 1.0125

    if keys[pygame.K_v] and v == 0:
        p.noclip = not p.noclip
        v = 1
    if not keys[pygame.K_v]:
        v = 0
    
    if keys[pygame.K_a] and a == 0:
        leveldict['player']['save']['pos'] = [p.x, p.y]
        leveldict['player']['save']['velosity'] = [p.xvelosity, p.yvelosity]
        a = 1
    if not keys[pygame.K_a]:
        a = 0

    if keys[pygame.K_s] and s == 0:
        p.x = leveldict['player']['save']['pos'][0]
        p.y = leveldict['player']['save']['pos'][1]
        p.xvelosity = leveldict['player']['save']['velosity'][0]
        p.yvelosity = leveldict['player']['save']['velosity'][1]
        s = 1
    if not keys[pygame.K_s]:
        s = 0

    if not p.noclip:
        p.gravitymove()
    else:
        p.noclipmove()

def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

class player:
    def bg(self):        
        screen.fill((200, 200, 200))
        for c in range(0, len(leveldict['tri'])):
            self.poly = self.createrenderPolygon(camerax, cameray, leveldict['tri'][c][0]['points'])
            pygame.draw.polygon(screen, (leveldict["tri"][c][1]['color'][0], leveldict["tri"][c][1]['color'][1], leveldict["tri"][c][1]['color'][2]), self.poly)
        for c in range(0, len(leveldict['rect'])):
            rectangle = pygame.Rect((leveldict['rect'][c][0]['points'][0]+camerax)*renderxscale, (leveldict['rect'][c][0]['points'][1]+cameray)*renderyscale, leveldict['rect'][c][0]['points'][2]*renderxscale, leveldict['rect'][c][0]['points'][3]*renderyscale)
            pygame.draw.rect(screen, (leveldict['rect'][c][1]['color'][0], leveldict['rect'][c][1]['color'][1], leveldict['rect'][c][1]['color'][2]), rectangle)
  
    def createworldPolygon(self, list):
        return [
            (list[0], list[1]), (list[2], list[3]), 
            (list[4], list[5]), (list[6], list[7])]
    
    def createrenderPolygon(self, x, y, list):
        return [
            ((x+list[0])*renderxscale, (list[1]+y)*renderyscale), ((x+list[2])*renderxscale, (list[3]+y)*renderyscale), 
            ((x+list[4])*renderxscale, (list[5]+y)*renderyscale), ((x+list[6])*renderxscale, (list[7]+y)*renderyscale)]

    def __init__(self, color):
        self.x=leveldict["player"]["startpos"][0]
        self.y=leveldict["player"]["startpos"][1]
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
        self.maxstepup=1
        self.dash=False
        self.candash=False
        self.groundtimer = 0
        self.dashtimer = Stopwatch()
        self.noclip = False
    
    def draw(self):
        self.drawrect=pygame.Rect((self.x+camerax)*renderxscale-self.xsize*renderxscale, (self.y+cameray)*renderxscale-self.ysize*renderyscale, self.xsize*renderxscale, self.ysize*renderyscale)
        pygame.draw.rect(screen, self.col, self.drawrect)

    def allcolision(self):
        coliding = 0
        self.rect=pygame.Rect((self.x)-self.xsize, (self.y)-self.ysize, self.xsize, self.ysize)
        for z in range(0, len(leveldict['rect'])):
            rectangle = pygame.Rect((leveldict['rect'][z][0]['points'][0], leveldict['rect'][z][0]['points'][1]), (leveldict['rect'][z][0]['points'][2], leveldict['rect'][z][0]['points'][3]))
            if rectangle.colliderect(self.rect):
                coliding += 1

        for z in range(0, len(leveldict['tri'])):
            polygon = self.createworldPolygon(leveldict['tri'][z][0]['points'])
            if collideRectPolygon(self.rect, polygon):
                coliding += 1
        
        if coliding == 0:
            return False
        else:
            return True
    
    def trigger(self):
        global leveldict
        for x in range(len(leveldict['triggers'])):
            rectangle = pygame.Rect(leveldict['triggers'][x][0]['points'][0], leveldict['triggers'][x][0]['points'][1], leveldict['triggers'][x][0]['points'][2], leveldict['triggers'][x][0]['points'][3])
            if self.rect.colliderect(rectangle):
                if leveldict['triggers'][x][1]['func'] == "levelload":
                    print(leveldict['triggers'][x][2]['perameters'])
                    script_directory = os.path.dirname(os.path.abspath(__file__))
                    json_file_path = os.path.join(script_directory, "levels/"+leveldict['triggers'][x][2]['perameters'])
                    with open(json_file_path, "r") as levelfile:
                        leveldict = json.load(levelfile)
                        levelfile.close()
                    self.x=leveldict["player"]["startpos"][0]
                    self.y=leveldict["player"]["startpos"][1]

            
    def gravitymove(self):
        global camerax, cameray

        oldxvelosity = self.xvelosity
        self.xvelosity += self.speed*self.direction[0]*dt
        
        if abs(self.xvelosity) > self.maxxvelosity:
            if abs(oldxvelosity) < abs(self.xvelosity):
                self.xvelosity -= self.speed*self.direction[0]*dt

        self.yvelosity -= self.gravity*dt
        
        if self.jump == True and self.groundtimer > 0:
            self.yvelosity = 10
            self.groundtimer = 0

        if self.dash == True and self.candash == True and self.dashtimer.duration > 1:
            if self.direction[0] != 0:
                self.xvelosity = self.direction[0]*12.5
            if self.direction[1] != 0:
                self.yvelosity = self.direction[1]*11
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
            while self.allcolision() and self.stepup < self.maxstepup*abs(self.xvelosity)+1:
                self.y -= 1
                self.stepup += 1
            if self.stepup >= self.maxstepup*abs(self.xvelosity)+1:
                self.y += self.stepup
                self.x += self.xvelosity
                self.xvelosity = 0
            else:
                self.yvelosity = self.stepup*1.5
        
        self.trigger()

        camerax += (-self.x-camerax+W/renderxscale/2)/4
        cameray += (-self.y-cameray+H/renderyscale/2)/4

    def noclipmove(self):
        global camerax, cameray
        self.x -= self.direction[0]*(self.dash+1)*3
        self.y -= self.direction[1]*(self.dash+1)*3

        camerax = -self.x+W/renderxscale/2
        cameray = -self.y+H/renderyscale/2


clicking = 0
v = 0
p=player((255, 0 ,0))
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    p.bg()
    p.draw()

    playerinput()
    
    fps_counter()
    pygame.display.update()

pygame.quit()