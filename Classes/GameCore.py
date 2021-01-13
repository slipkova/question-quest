import pygame, sys, json
from pygame.locals import *
from constants import *
from Classes.Menu import Menu
from Classes.Movable import Side
from Classes.GameObject import GameObject
from Classes.Scene import Scene
from Classes.Button import ButtonInMenu, SaveButton, FightButton
from random import randrange


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
        self.load_player_data(index)
        self.loop()

    def load_player_data(self, index):
        with open(f"player-data/save{index}/scene/test.json") as json_file:
            self.scene = Scene(data=json.load(json_file))
        self.player = self.scene.get_player()

    def loop(self):
        while self.running:
            self.display.fill((146, 244, 255))
            self.check_pressed()

            if self.running:
                self.scene.update()
                if self.enemy:
                    fight = Fight(self.enemy, self.player)
                    fight.loop()
                    self.enemy = None

                surf = pygame.transform.scale(self.display, WINDOW_SIZE)
                self.draw(surf)
        self.running = True

    def check_pressed(self):
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

    @staticmethod
    def draw(display):
        GameObject.game.screen.blit(display, (0, 0))
        pygame.display.update()
        GameObject.game.clock.tick(120)


class Fight:
    def __init__(self, enemy, player):
        self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.enemy = enemy
        self.player = player
        self.ATTACK = pygame.USEREVENT + 1
        self.fight_menu = Menu(buttons=[FightButton(position=1, text="attack", pointer=self.attack),
                                        FightButton(position=2, text="defense", pointer=self.defense),
                                        FightButton(position=3, text="run", pointer=self.run)])

    def loop(self):
        self.running = True
        pygame.time.set_timer(self.ATTACK, 5000)
        while self.running:
            self.display.fill((255, 244, 255))
            GameObject.game.running = self.check_pressed()
            self.display.blit(pygame.transform.scale(self.enemy.image, [self.enemy.image.get_size()[0] * 4, self.enemy.image.get_size()[1] * 4]), (50, 100))
            self.enemy.update()
            if self.running:
                for i, b in enumerate(self.fight_menu.buttons):
                    if i == self.fight_menu.active:
                        b.draw(self.display, (100, 100, 100))
                    else:
                        b.draw(self.display)
                Game.draw(self.display)

    def check_pressed(self):
        for event in pygame.event.get():
            if event.type == self.ATTACK:
                self.player.lives -= self.enemy.attack()
                print(f"player lives: {self.player.lives}")
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = GameObject.game.menus["in_game_menu"].loop()
                    print(self.running)
                    if not self.running:
                        return False
            self.fight_menu.check_pressed(event)
            self.fight_menu.pressed_before = pygame.key.get_pressed()
            return True

    def attack(self):
        self.enemy.lives -= randrange(*self.player.attack_strength)
        print(self.enemy.lives)
        self.enemy.play("hit", 0.5)

    def defense(self):
        self.player.active_defense = True
        print(self.player.active_defense)

    def run(self):
        self.running = False
        print("run")
