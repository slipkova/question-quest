import pygame
import sys
from pygame.locals import *
from Classes.GameObject import GameObject
from Classes.Button import SaveButton


class Menu:
    def __init__(self, **kwargs):
        self.buttons = kwargs["buttons"]
        self.active = 0
        self.running, self.click = True, False
        self.pressed_before = {}

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                quit_bool = self.check_pressed(event, "vertical")
                if not quit_bool:
                    self.running = True
                    return False
            if self.running:
                GameObject.game.screen.fill((200, 200, 200))
                self.pressed_before = pygame.key.get_pressed()
                for i, b in enumerate(self.buttons):
                    if i == self.active:
                        b.draw(GameObject.game.screen, (100, 100, 100))
                    else:
                        b.draw(GameObject.game.screen)

                pygame.display.update()
        self.running = True
        return True

    def check_pressed(self, event, orientation):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if (event.key == K_DOWN and orientation == "vertical") or (
                    event.key == K_RIGHT and orientation == "horizontal"):
                if K_DOWN not in self.pressed_before or K_RIGHT not in self.pressed_before:
                    if self.active == len(self.buttons) - 1:
                        self.active = 0
                    else:
                        self.active += 1

            if (event.key == K_UP and orientation == "vertical") or (
                    event.key == K_LEFT and orientation == "horizontal"):
                if K_UP not in self.pressed_before or K_LEFT not in self.pressed_before:
                    if self.active == 0:
                        self.active = len(self.buttons) - 1
                    else:
                        self.active -= 1

            if event.key == K_SPACE or event.key == K_RETURN:
                if K_SPACE not in self.pressed_before or K_RETURN not in self.pressed_before:
                    if self.buttons[self.active].pointer:
                        self.buttons[self.active].click()
                    if self.buttons[self.active].event == "back":
                        self.running = False
                    if self.buttons[self.active].event == "quit":
                        self.running = False
                        GameObject.running = False
                        return False
                    if self.buttons[self.active].event == "quit game":
                        pygame.quit()
                        sys.exit()
                    if self.buttons[self.active].event in {"attack", "defense", "run"}:
                        self.buttons[self.active].click()
                        return
                    self.active = 0

            if (event.key == K_DOWN or event.key == K_UP) and orientation == "horizontal":
                return True


        return True

