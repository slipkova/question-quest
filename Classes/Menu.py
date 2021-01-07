from pygame.locals import *


class Menu():
    def __init__(self, buttons):
        self.buttons = buttons
        self.active = 0
        self.running, self.click = True, False
        self.pressed_before = {}

    def update(self, keys, screen, x = 1):
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

