import pygame
from pygame.locals import *

class Menu():
    def __init__(self, buttons):
        self.buttons = buttons
        self.active = 0

    def update(self, screen):

        screen.fill((200, 200, 200))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    print(len(self.buttons), self.active)
                    if self.active == len(self.buttons) - 1:
                        self.active = 0
                    else:
                        self.active += 1

                if event.key == K_UP:
                    if self.active == 0:
                        self.active = len(self.buttons) - 1
                    else:
                        self.active -= 1

        for i, b in enumerate(self.buttons):
            if i == self.active:
                b.draw(screen, (100, 100, 100))
            else:
                b.draw(screen)

