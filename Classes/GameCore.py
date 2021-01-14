import pygame, sys, json
from pygame.locals import *
from constants import *
from Classes.Menu import Menu
from Classes.Movable import Side
from Classes.GameObject import GameObject
from Classes.Scene import Scene
from Classes.Final import EnterPad, Player
from Classes.Button import ButtonInMenu, SaveButton


class Game:
    def __init__(self):
        self.running = True
        self.display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
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
        with open(f"player-data/save{index}/scene/{self.player_data['scene']}.json") as json_file:
            self.scene = Scene(data=json.load(json_file), name=self.player_data['scene'])
        self.player = self.scene.operate_player()

    def save_game(self):
        self.operate_player_data(True)
        self.save_scene()

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
        previous_name = self.scene.name
        self.player.played_anim = [None, 0]
        self.player.pixel_loc = [[0, 0], 0]
        self.scene.operate_player(remove=True)
        self.save_scene()
        with open(f"player-data/save{self.player_index}/scene/{scene}.json") as json_file:
            self.scene = Scene(data=json.load(json_file), name=scene)
            for row in self.scene.layers[1]:
                for tile in row:
                    for obj in tile:
                        if isinstance(obj, EnterPad):
                            if obj.origin == previous_name and obj.index == index:
                                # self.player = Player()
                                self.player.indexes = obj.indexes
                                self.scene.add_object(self.player, [1, *obj.indexes])
                                self.player.sync_pos()
            self.player_data["scene"] = self.scene.name
            self.operate_player_data(True)



    def loop(self):
        while self.running:
            self.display.fill((146, 244, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.save_game()
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
