import pygame, sys, json
from pygame.locals import *
from constants import *
from Classes.Menu import Menu
from Classes.Movable import Side
from Classes.GameObject import GameObject
from Classes.Scene import Scene
from Classes.Button import ButtonInMenu, SaveButton


class Game:
    def __init__(self):
        self.running = True
        self.display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.scene = None
        self.player = None
        self.enemy = None
        GameObject.game = self
        self.menus = {}
        self.menus["options_menu"] = Menu(buttons=[
                ButtonInMenu(position=1, text="Volume"),
                ButtonInMenu(position=2, text="Back", event="back")])
        self.menus["in_game_menu"] = Menu(buttons=[
                ButtonInMenu(position=1, text="Back to game", event="back"),
                ButtonInMenu(position=2, text="Options", pointer=self.menus["options_menu"].loop),
                ButtonInMenu(position=3, text="Quit", event="quit")])
        self.menus["saves_menu"] = Menu(buttons=[
                SaveButton(position=1, text="save1", pointer=self.load_save),
                SaveButton(position=2, text="save2", pointer=self.load_save),
                SaveButton(position=3, text="save3", pointer=self.load_save),
                SaveButton(position=4, text="Back", event="back")])
        self.menus["main_menu"] = Menu(buttons=[
                ButtonInMenu(position=1, text="Play", pointer=self.menus["saves_menu"].loop),
                ButtonInMenu(position=2, text="Options", pointer=self.menus["options_menu"].loop),
                ButtonInMenu(position=3, text="Quit", event="quit game")])
        self.menus["main_menu"].loop()

    def load_save(self, index):
        self.load_palyer_data(index)
        self.loop()

    def load_palyer_data(self, index):
        with open(f"player-data/save{index}/scene/test.json") as json_file:
            self.scene = Scene(data=json.load(json_file))
        self.player = self.scene.get_player()

    def loop(self):
        while self.running:
            self.display.fill((146, 244, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
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
                        self.running = self.menus["in_game_menu"].loop()

            if self.running:
                self.scene.update()
                if self.enemy:
                    fight = Fight()
                    self.running = fight.loop()

                surf = pygame.transform.scale(self.display, WINDOW_SIZE)
                self.screen.blit(surf, (0, 0))
                pygame.display.update()
                self.clock.tick(120)
        self.running = True


class Fight:
    def __init__(self, **kwargs):
        self.display = pygame.Surface(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.running = True

    def loop(self):
        while self.running:
            self.display.fill((255, 244, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = GameObject.game.menus["in_game_menu"].loop()
                        return True if self.running else False

            if self.running:
                GameObject.game.screen.blit(self.display, (0, 0))
                pygame.display.update()
        return True
