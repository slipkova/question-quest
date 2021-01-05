import pygame, sys
from constants import *
from pygame.locals import * # import pygame modules
from Classes.Scene import Scene
from Classes.Assets.Ground import Ground
from Classes.GameObject import GameObject


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Pygame Window')
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))
GameObject.display = display


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
#test


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
