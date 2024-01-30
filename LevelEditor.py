import pygame, json
from stopwatch import Stopwatch

renderxscale = 1
renderyscale = 1

camerax = 0
cameray = 0

editstatus = 0
objectedit = 0
pointedit = 0
posoffset = [0, 0]

pygame.init()
W, H=800, 450
#W, H=400, 800
screen = pygame.display.set_mode([W, H])
pygame_icon = pygame.image.load('Hammer Icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Half Life III")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial" , 12 , bold = True)

running = True

bcg=(200, 200, 200)
red=(255, 0 ,0)
purp=(255, 0, 255)
wall=(100, 100, 100)

with open("level.json", "r") as levelfile:
    leveldict = json.load(levelfile)
    levelfile.close()


def playerinput():
    global renderxscale, renderyscale, clicking, v, objectedit, editstatus, posoffset
    keys=pygame.key.get_pressed()
    mousekey=pygame.mouse.get_pressed()
    mousepos=pygame.mouse.get_pos()

    p.direction = ((keys[pygame.K_LEFT]-keys[pygame.K_RIGHT]), (keys[pygame.K_UP]-keys[pygame.K_DOWN]))

    if keys[pygame.K_c]: p.dash=True
    else: p.dash=False

    if mousekey[0] and editstatus == 0:
        if keys[pygame.K_r]:
            objectedit = len(leveldict['rect'])
            leveldict['rect'].append([{"points": [round(mousepos[0], -1)-camerax, round(mousepos[1], -1)-cameray, 10, 10]}, {"color": [70, 70, 70]}])
            editstatus = 1
        
        elif keys[pygame.K_m]:
            for x in range(len(leveldict['rect'])):
                rectangle = pygame.Rect(leveldict['rect'][x][0]['points'][0], leveldict['rect'][x][0]['points'][1], leveldict['rect'][x][0]['points'][2], leveldict['rect'][x][0]['points'][3])
                if rectangle.collidepoint(mousepos[0]-camerax, mousepos[1]-cameray):
                    editstatus = 2
                    objectedit = x
                    #posoffset = [round(leveldict['rect'][x][0]['points'][0]+mousepos[0]-camerax, -1), -round(leveldict['rect'][x][0]['points'][1]+mousepos[1]-cameray, -1)]
        
        elif keys[pygame.K_d]:
            tobedeleted = []
            for x in range(len(leveldict['rect'])):
                rectangle = pygame.Rect(leveldict['rect'][x][0]['points'][0], leveldict['rect'][x][0]['points'][1], leveldict['rect'][x][0]['points'][2], leveldict['rect'][x][0]['points'][3])
                if rectangle.collidepoint(mousepos[0]-camerax, mousepos[1]-cameray):
                    tobedeleted.append(x)
            if len(tobedeleted) > 0:
                for x in range(len(tobedeleted)):
                    del leveldict['rect'][tobedeleted[x]]

    if editstatus == 1:
        leveldict['rect'][objectedit][0]["points"][2] = round(mousepos[0]-camerax-leveldict['rect'][objectedit][0]["points"][0], -1)
        leveldict['rect'][objectedit][0]["points"][3] = round(mousepos[1]-cameray-leveldict['rect'][objectedit][0]["points"][1], -1)
        if mousekey[0] and not keys[pygame.K_r]:
            editstatus = 0
    
    if editstatus == 2:
        leveldict['rect'][objectedit][0]["points"][0] = round(mousepos[0]-camerax-posoffset[0], -1)
        leveldict['rect'][objectedit][0]["points"][1] = round(mousepos[1]-cameray-posoffset[1], -1)
        if mousekey[0] and not keys[pygame.K_m]:
            editstatus = 0
    
    if keys[pygame.K_f]: 
        p.x=leveldict['player']['startpos'][0]
        p.y=leveldict['player']['startpos'][1]

    if keys[pygame.K_o]:
        renderxscale /= 1.0125
        renderyscale /= 1.0125

    if keys[pygame.K_p]:
        renderxscale *= 1.0125
        renderyscale *= 1.0125

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
            pygame.draw.polygon(screen, wall, self.poly)
        for c in range(0, len(leveldict['rect'])):
            rectangle = pygame.Rect((leveldict['rect'][c][0]['points'][0]+camerax)*renderxscale, (leveldict['rect'][c][0]['points'][1]+cameray)*renderyscale, leveldict['rect'][c][0]['points'][2]*renderxscale, leveldict['rect'][c][0]['points'][3]*renderyscale)
            pygame.draw.rect(screen, (leveldict['rect'][c][1]['color'][0], leveldict['rect'][c][1]['color'][1], leveldict['rect'][c][1]['color'][2]), rectangle)
    
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

    def noclipmove(self):
        global camerax, cameray
        self.x -= self.direction[0]*(self.dash+1)*3
        self.y -= self.direction[1]*(self.dash+1)*3

        camerax = -self.x+W/renderxscale/2
        cameray = -self.y+H/renderyscale/2


clicking = 0
v = 0
p=player(red)
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    p.bg()

    playerinput()
    
    fps_counter()
    pygame.display.update()

pygame.quit()