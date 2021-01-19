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
        self.orientation = kwargs["orientation"] if "orientation" in kwargs else "vertical"
        self.name = kwargs["name"] if "name" in kwargs else None

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                quit_bool = self.check_pressed(event)
                if not quit_bool:
                    self.running = True
                    return False
            if self.running:
                GameObject.game.screen.fill((200, 200, 200))
                self.pressed_before = pygame.key.get_pressed()
                for i, b in enumerate(self.buttons):
                    if i == self.active:
                        b.draw(GameObject.game.screen, "assets/images/buttons/b1-active.png")
                    else:
                        b.draw(GameObject.game.screen)

                pygame.display.update()
        self.running = True
        return True

    def check_pressed(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if (event.key == K_DOWN and self.orientation == "vertical") or (
                    event.key == K_RIGHT and self.orientation == "horizontal"):
                if K_DOWN not in self.pressed_before or K_RIGHT not in self.pressed_before:
                    if self.active == len(self.buttons) - 1:
                        self.active = 0
                    else:
                        self.active += 1

            if (event.key == K_UP and self.orientation == "vertical") or (
                    event.key == K_LEFT and self.orientation == "horizontal"):
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

            if event.key == K_RIGHT and self.name == "fight":
                return "change menu"

        return True


class FightMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = None

    def check_pressed(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if K_DOWN not in self.pressed_before:
                    if self.active[0] != len(self.buttons[0]) - 2:
                        self.active[0] += 1

            if event.key == K_UP:
                if K_UP not in self.pressed_before:
                    if self.active[0] != 0:
                        self.active[0] -= 1

            if event.key == K_RIGHT:
                if K_RIGHT not in self.pressed_before:
                    if self.active[1] != len(self.buttons):
                        self.active[1] += 1

            if event.key == K_LEFT:
                if K_LEFT not in self.pressed_before:
                    if self.active[1] != 0:
                        self.active[1] -= 1
                    else:
                        return "change menu"

            if event.key == K_SPACE or event.key == K_RETURN:
                if K_SPACE not in self.pressed_before or K_RETURN not in self.pressed_before:
                    if self.buttons[self.active[0]][self.active[1]].pointer:
                        self.buttons[self.active[0]][self.active[1]].click()
                    self.active = [0, 0]



