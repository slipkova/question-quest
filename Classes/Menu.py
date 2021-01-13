import pygame
import sys
from pygame.locals import *


class Menu:
    def __init__(self, **kwargs):
        self.buttons = kwargs["buttons"]
        self.active = 0
        self.running, self.click = True, False
        self.pressed_before = {}
        self.screen = kwargs["screen"]
        self.clock = kwargs["clock"]

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        if K_DOWN not in self.pressed_before:
                            if self.active == len(self.buttons) - 1:
                                self.active = 0
                            else:
                                self.active += 1

                    if event.key == K_UP:
                        if K_UP not in self.pressed_before:
                            if self.active == 0:
                                self.active = len(self.buttons) - 1
                            else:
                                self.active -= 1

                    if event.key == K_SPACE:
                        if K_SPACE not in self.pressed_before:
                            if self.buttons[self.active].pointer:
                                self.buttons[self.active].pointer()
                            if self.buttons[self.active].event == "back":
                                self.running = False
                            if self.buttons[self.active].event == "quit":
                                return False
                            if self.buttons[self.active].event == "quit game":
                                pygame.quit()
                                sys.exit()
                            self.active = 0


            self.screen.fill((200, 200, 200))

            self.pressed_before = pygame.key.get_pressed()

            for i, b in enumerate(self.buttons):
                if i == self.active:
                    b.draw(self.screen, (100, 100, 100))
                else:
                    b.draw(self.screen)

            pygame.display.update()

            self.clock.tick(60)
        self.running = True
        return True

    def update(self, keys, screen, x=1):
        screen.fill((200, 200, 200))

        if keys[K_DOWN]:
            if keys[K_DOWN] not in self.pressed_before:
                if self.active == len(self.buttons) - 1:
                    self.active = 0
                else:
                    self.active += 1

        if keys[K_UP]:
            if keys[K_UP] not in self.pressed_before:
                if self.active == 0:
                    self.active = len(self.buttons) - 1
                else:
                    self.active -= 1

        if keys[K_SPACE] and x != 0:
            if keys[K_SPACE] not in self.pressed_before:
                self.click = True

        self.pressed_before = keys

        for i, b in enumerate(self.buttons):
            if i == self.active:
                b.draw(screen, (100, 100, 100))
            else:
                b.draw(screen)


