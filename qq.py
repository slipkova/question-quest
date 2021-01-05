import pygame, sys
from constants import *
from pygame.locals import * # import pygame modules
from Classes.Scene import Scene
from Classes.Assets.Ground import Ground
from Classes.GameObject import GameObject
from Classes.Assets.Player import Player
from Classes.Movable import Side


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.display.set_caption('Pygame Window')
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300, 200))
heh = Scene(10, 10)
GameObject.init(display=display, scene=heh)

class Text(GameObject):
    def __init__(self, x, y):
        super().__init__(image="images/nic.png", position=[x,y])

    def render(self):
        super().render()
        GameObject.display.blit(font.render(f"{self.indexes[1]},{self.indexes[0]}", False, (0,0,0)), self.position)

for i, x in enumerate(heh.matrix):
    if i == 2 or i == 7:
        for j, y in enumerate(x):
            y.append(Ground(i * TYLE_SIZE, j * TYLE_SIZE))
    else:
        for j, y in enumerate(x):
            if j == 1 or j == 8:
                y.append(Ground(i * TYLE_SIZE, j * TYLE_SIZE))
"""
for i, x in enumerate(heh.matrix):
    for j, y in enumerate(x):
        print(i,j)
        y.append(Text(i * TYLE_SIZE, j * TYLE_SIZE))
"""
player = Player(6 * TYLE_SIZE, 5 * TYLE_SIZE)
heh.matrix[6][5].append(player)


while True: # game loop
    display.fill((146, 244, 255))
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player.take_action(Side.RIGHT)
            if event.key == K_LEFT:
                player.take_action(Side.LEFT)
            if event.key == K_UP:
                player.take_action(Side.UP)
            if event.key == K_DOWN:
                player.take_action(Side.DOWN)

    heh.update()
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
