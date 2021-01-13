import pygame, sys
from pygame.locals import *
from constants import *
from Classes.Menu import Menu
from Classes.Movable import Side
from Classes.GameObject import GameObject


class Game:
    def __init__(self, **kwargs):
        self.running = True
        self.display = kwargs["display"]
        self.screen = kwargs["screen"]
        self.clock = kwargs["clock"]
        self.player = kwargs["player"]
        self.menu = kwargs["menu"]
        self.yes = kwargs["yes"]
        self.enemy = None
        GameObject.game = self

    def loop(self):
        while self.running:
            self.display.fill((146, 244, 255))
            for event in pygame.event.get():  # event loop
                if event.type == QUIT:  # check for window quit
                    pygame.quit()  # stop pygame
                    sys.exit()  # stop script
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.player.take_action(Side.RIGHT)
                    if event.key == K_LEFT:
                        self.player.take_action(Side.LEFT)
                    if event.key == K_UP:
                        self.player.take_action(Side.UP)
                    if event.key == K_DOWN:
                        self.player.take_action(Side.DOWN)
                    if event.key == K_ESCAPE:
                        game_running = self.menu()

            if self.running:
                # test_squares()
                # heh.update()
                self.yes.update()
                if self.enemy:
                    fight = Fight(display=self.display, screen=self.screen, clock=self.clock, menu=self.menu)
                    self.running = fight.loop()

                surf = pygame.transform.scale(self.display, WINDOW_SIZE)
                self.screen.blit(surf, (0, 0))
                pygame.display.update()
                self.clock.tick(120)
        self.running = True


class Fight:
    def __init__(self, **kwargs):
        self.display = kwargs["display"]
        self.screen = kwargs["screen"]
        self.clock = kwargs["clock"]
        self.running = True
        self.menu = kwargs["menu"]

    def loop(self):
        while self.running:
            self.display.fill((255, 244, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = self.menu()
                        return False if not self.running else True

            if self.running:
                surf = pygame.transform.scale(self.display, WINDOW_SIZE)
                self.screen.blit(surf, (0, 0))
                pygame.display.update()
                self.clock.tick(120)
        return True
