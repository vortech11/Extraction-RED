import pygame

pygame.init()
window = pygame.display.set_mode((500, 350))
pygame_icon = pygame.image.load('Hammer Icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Half Life III")
clock = pygame.time.Clock()

player = pygame.Rect(0, 0, 20, 20)
player.y = 20
player.center = window.get_rect().center

worldbox = []
worldpoly = []
  
worldbox.extend([0, 0, 500, 50, 0, 300, 31, 158, 27])
worldbox.extend([0, 0, 50, 200, 0, 105, 70, 70, 70])
worldbox.extend([0, 0, 50, 200, 450, 105, 70, 70, 70])
worldbox.extend([0, 0, 100, 25, 200, 200, 45, 45, 45])

worldpoly.extend([100, 100, 200, 100, 200, 200])
worldpoly.extend([300, 200, 300, 250, 250, 250])


speed = 30
jumpspeed = 12
maxs = 11
friction = 15
gravity = 18
maxstepup = 2

xvelosity = 0
yvelosity = 0
grounded = 0
getTicksLastFrame = 0
stepup = 0



run = True
while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
          pass

    keys = pygame.key.get_pressed()

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000
    getTicksLastFrame = t
    
    xvelosity += ((keys[pygame.K_d] - keys[pygame.K_a]) * speed * deltaTime)
    
    if keys[pygame.K_w] == 1 and grounded == 1:
      yvelosity = jumpspeed
      grounded = 0
  
    if keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] == 0:
      xkey = 0
    else:
      xkey = 1
      
    if abs(xvelosity) > maxs:
      if xvelosity > 0:
        xvelosity = maxs
      else:
        xvelosity = -maxs

    if xkey == 0:
      if xvelosity > 0:
        xvelosity -= friction * deltaTime
      else:
        xvelosity += friction * deltaTime
      if abs(xvelosity) < 0:
        xvelosity = xvelosity / 100

    player.x += xvelosity

    for z in range(0, len(worldbox), 9):
      
      worldb = pygame.Rect(worldbox[int(z)], worldbox[int(z + 1)], worldbox[int(z + 2)], worldbox[int(z + 3)])
      worldb.x = worldbox[z + 4]
      worldb.y = worldbox[z + 5]
      
      if player.colliderect(worldb) == 1:
        stepup = 0
        
        while player.colliderect(worldb) == 1 and stepup < (maxstepup * abs(xvelosity)):
          player.y += 1
          stepup += 1
          
        if not stepup < maxstepup:
          player.y -= stepup
          if xvelosity > 0:
            while player.colliderect(worldb) == 1:
              player.x -= 1
          else:
            while player.colliderect(worldb) == 1:
              player.x += 1
          xvelosity = xvelosity / 100
          
    polylinecolision = []
    worldline = []

    
    for z in range(0, len(worldpoly), 3):
      worldline.extend([worldpoly[z], worldpoly[z + 1]])
      worldline.extend([worldpoly[z + 1], worldpoly[z + 2]])
      worldline.extend([worldpoly[z], worldpoly[z + 2]])

    for z in range(0, len(worldline), 4):
      if player.clipline(worldline[z], worldline[z + 1], worldline[z + 2], worldline[z + 3]):
        polylinecolision.extend([worldline[z], worldline[z + 1], worldline[z + 2], worldline[z + 3]])
    stepup = 0
  
    while len(polylinecolision) > 0 and stepup < maxstepup:
      
      player.y += 1
      stepup += 1

      nextlinecolision = []

      for z in range(0, len(polylinecolision), 4):
        
        if player.clipline(polylinecolision[z], polylinecolision[z + 1], polylinecolision[z + 2], polylinecolision[z + 3]):
          
          nextlinecolision.extend([polylinecolision[z], polylinecolision[z + 1], polylinecolision[z + 2], polylinecolision[z + 3]])

      polylinecolision = nextlinecolision
        
    if not stepup < maxstepup:
      player.y -= stepup

      while len(polylinecolision) > 0:
      
        if xvelosity > 0:
          player.x -= 1
        else:
          player.x += 1
  
        nextlinecolision = []

        for z in range(0, len(polylinecolision), 4):
        
          if not player.clipline(polylinecolision[z], polylinecolision[z + 1], polylinecolision[z + 2], polylinecolision[z + 3]) == ():
            
            nextlinecolision.extend([polylinecolision[z], polylinecolision[z + 1], polylinecolision[z + 2], polylinecolision[z + 3]])

      polylinecolision = nextlinecolision
  
    yvelosity -= gravity * deltaTime
    
    player.y -= yvelosity
    
    grounded = 0
    for z in range(0, len(worldbox), 9):
      worldb = pygame.Rect(worldbox[int(z)], worldbox[int(z + 1)], worldbox[int(z + 2)], worldbox[int(z + 3)])
      worldb.x = worldbox[z + 4]
      worldb.y = worldbox[z + 5]
      
      if player.colliderect(worldb) == 1:
        if yvelosity > 0:
          while player.colliderect(worldb) == 1:
            player.y += 1
            
        else:
          while player.colliderect(worldb) == 1:
            player.y -= 1
            grounded = 1
        yvelosity = 1
      

    player.centerx = player.centerx % window.get_width()
    player.centery = player.centery % window.get_height()

    window.fill([72, 127, 213])
    pygame.draw.rect(window, (255, 75, 75), player)
  
    for z in range(0, len(worldbox), 9):
      worldb = pygame.Rect(worldbox[z], worldbox[z + 1], worldbox[z + 2], worldbox[z + 3])
      worldb.x = worldbox[z + 4]
      worldb.y = worldbox[z + 5]
      pygame.draw.rect(window, (worldbox[z + 6], worldbox[z + 7], worldbox[z + 8]), worldb)
      
    for z in range(0, len(worldpoly), 6):
      pygame.draw.polygon(window, (255, 255, 255), [[worldpoly[z], worldpoly[z + 1]], [worldpoly[z + 2], worldpoly[z + 3]], [worldpoly[z + 4], worldpoly[z + 5]]])
      
    pygame.display.flip()
pygame.quit()
exit()