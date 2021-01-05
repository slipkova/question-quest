import pygame, sys
from constants import *
from pygame.locals import * # import pygame modules
from Classes.Scene import Scene
from Classes.Assets.Ground import Ground
from Classes.GameObject import GameObject
from Classes.Button import Button
from Classes.Menu import Menu


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Pygame Window')
WINDOW_SIZE = (1000, 800)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))
GameObject.display = display

'''
heh = Scene(10, 10)


for i, x in enumerate(heh.matrix):
    if i == 2 or i == 7:
        for j, y in enumerate(x):
            y.append(Ground(i * TYLE_SIZE, j * TYLE_SIZE))
    else:
        for j, y in enumerate(x):
            if j == 1 or j == 7:
                y.append(Ground(i * TYLE_SIZE, j * TYLE_SIZE))
print(heh.matrix)


while True: # game loop
    display.fill((146, 244, 255))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                pass
            if event.key == K_LEFT:
                pass
            if event.key == K_UP:
                pass

    heh.update()
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
'''

main_menu = Menu([Button(150, 200, "opt1"), Button(150, 300, "opt2"), Button(150, 400, "opt3")])
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    main_menu.update(screen)
    pygame.display.update()
    clock.tick(60)

    '''
        screen.fill((200, 200, 200))
            
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        print(len(buttons), active)
                        if active == len(buttons)-1:
                            active = 0
                        else:
                            active += 1

                    if event.key == K_UP:
                        if active == 0:
                            active = len(buttons) - 1
                        else:
                            active -= 1
                elif event.type == QUIT:
                    running = False

            for i, b in enumerate(buttons):
                if i == active:
                    b.draw(screen, (100, 100, 100))
                else:
                    b.draw(screen)'''


buttons = [Button(150, 200, "opt1"), Button(150, 300, "opt2"), Button(150, 400, "opt3")]

