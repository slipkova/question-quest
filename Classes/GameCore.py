import pygame, sys, json
from pygame.locals import *
from constants import *
from Classes.Menu import Menu
from Classes.Movable import Side
from Classes.GameObject import GameObject
from Classes.Scene import Scene
from Classes.Button import ButtonInMenu, SaveButton, FightButton
from random import randrange
from Classes.Final import EnterPad, Player


class Game:
    def __init__(self):
        self.running = True
        self.display = pygame.Surface((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
        self.screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.player_index = 0
        self.player_data = {}
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
                ButtonInMenu(position=3, text="Save & Quit", event="quit", pointer=self.save_game)])
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
        self.player_index = index
        self.operate_player_data(False)
        if self.player_data["prev_scene"][0] == "":
            with open(f"player-data/save{index}/scene/start.json") as json_file:
                self.scene = Scene(data=json.load(json_file), name="start")
                self.player = Player()
                self.scene.add_object(self.player, [1, 5, 5])
        else:
            with open(f"player-data/save{index}/scene/{self.player_data['scene']}.json") as json_file:
                self.scene = Scene(data=json.load(json_file), name=self.player_data['scene'])
                if self.scene.operate_player():
                    self.player = self.scene.operate_player()
                else:
                    self.player = Player()
                    enter = self.get_prev_scene_enter(self.player_data["prev_scene"])
                    self.scene.add_object(self.player, [1, *enter.indexes])
                    self.player.sync_pos()

    def save_game(self):
        self.operate_player_data(True)
        self.save_scene()

    def get_prev_scene_enter(self, prev_scene):
        for row in self.scene.layers[1]:
            for tile in row:
                for obj in tile:
                    if isinstance(obj, EnterPad):
                        if obj.origin == prev_scene[0] and obj.index == prev_scene[1]:
                            return obj

    def operate_player_data(self, write_mode):
        with open(f"player-data/save{self.player_index}/player-data.json", "w" if write_mode else "r") as json_file:
            if write_mode:
                json.dump(self.player_data, json_file)
            else:
                self.player_data = json.load(json_file)

    def save_scene(self):
        with open(f"player-data/save{self.player_index}/scene/{self.scene.name}.json", "w") as json_file:
            json.dump(self.scene.export(), json_file)

    def load_scene(self, scene, index):
        self.player_data["prev_scene"] = [self.scene.name, index]
        self.player.played_anim = [None, 0]
        self.player.pixel_loc = [[0, 0], 0]
        self.scene.operate_player(remove=True)
        self.save_scene()
        with open(f"player-data/save{self.player_index}/scene/{scene}.json") as json_file:
            self.scene = Scene(data=json.load(json_file), name=scene)
            enter = self.get_prev_scene_enter(self.player_data["prev_scene"])
            self.scene.add_object(self.player, [1, *enter.indexes])
            self.player.sync_pos()
            self.player_data["scene"] = self.scene.name
            self.operate_player_data(True)

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
