import pygame, sys, json
from pygame.locals import *
from constants import *
from Classes.Menu import Menu, FightMenu
from Classes.Movable import Side
from Classes.GameObject import GameObject
from Classes.Scene import Scene
from Classes.Button import ButtonInMenu, SaveButton, FightButton, AnswerButton, HintButton
from random import randrange
from Classes.Final import EnterPad, Player
from Classes.Quiz import Question


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
        self.hint_buttons = [HintButton(position=1, text="50/50"),
                             HintButton(position=2, text="dfgfdhg"),
                             HintButton(position=3, text="Skip question")]
        self.menus = {
            "fight_menu": Menu(buttons=[FightButton(position=1, text="attack", pointer=self.generate_question,
                                                    event="attack"),
                                        FightButton(position=2, text="defense", pointer=self.generate_question,
                                                    event="defense"),
                                        FightButton(position=3, text="run", pointer=self.run)],
                               name="fight"),

            "attack_question": FightMenu(buttons=[
                [AnswerButton(position=1, text="1", pointer=self.attack),
                 AnswerButton(position=2, text="2", pointer=self.attack),
                 AnswerButton(position=3, text="3", pointer=self.attack)],
                self.hint_buttons
            ]),

            "defense_question": FightMenu(buttons=[
                [AnswerButton(position=1, text="1", pointer=self.defense),
                 AnswerButton(position=2, text="2", pointer=self.defense),
                 AnswerButton(position=3, text="3", pointer=self.defense)],
                self.hint_buttons
            ]),
            "items": FightMenu(buttons=[player.items,
                                        self.hint_buttons
                                        ])
        }
        self.active_menu = self.menus["fight_menu"]
        self.drawn_menu = None
        self.attack_question = None
        self.defense_question = None

    def loop(self):
        self.running = True
        pygame.time.set_timer(self.ATTACK, self.enemy.attack_interval)
        while self.running:
            self.display.fill((38, 24, 23))
            self.display.blit(pygame.transform.scale(pygame.image.load("assets/images/fight/dungeon-bg.png").convert(), [SCREEN_WIDTH, 450]), [0, 0])
            GameObject.game.running = self.check_pressed()
            self.display.blit(pygame.transform.scale(self.enemy.image, [self.enemy.image.get_size()[0] * 4,
                                                                        self.enemy.image.get_size()[1] * 4]),
                              (110, 60))
            self.enemy.update()

            self.display.blit(pygame.transform.scale(self.player.image, [self.player.image.get_size()[0] * 4,
                                                                         self.player.image.get_size()[1] * 4]),
                              (700, 222))
            self.player.update()
            if self.drawn_menu:
                font = pygame.font.SysFont('', 35)
                text = font.render(self.attack_question.question if self.drawn_menu == self.menus["attack_question"]
                                   else self.defense_question.question, 1, (255, 255, 255))
                self.display.blit(text, (600, 550))
                text = font.render("Hints", 1, (255, 255, 255))
                self.display.blit(text, (600, 650))

            if self.running:
                for i, b in enumerate(self.menus["fight_menu"].buttons):
                    if i == self.menus["fight_menu"].active:
                        b.draw(self.display, "assets/images/buttons/b1-active.png")
                    else:
                        b.draw(self.display)
                if self.drawn_menu:
                    for i1 in range(len(self.drawn_menu.buttons)):
                        for i2, b in enumerate(self.drawn_menu.buttons[i1]):
                            if [i1, i2] == self.drawn_menu.active:
                                b.draw(self.display, "assets/images/buttons/b1-active.png")
                            else:
                                b.draw(self.display)
                Game.draw(self.display)

    def check_pressed(self):
        for event in pygame.event.get():
            if event.type == self.ATTACK:
                if self.player.active_defense:
                    if self.player.active_defense == "full":
                        damage = self.enemy.attack() - randrange(*self.player.DEFENSE_STRENGTH)
                    if self.player.active_defense == "not_full":
                        damage = self.enemy.attack() - randrange(*self.player.DEFENSE_STRENGTH) * 0.1
                    self.player.active_defense = None
                else:
                    damage = self.enemy.attack()
                self.player.lives -= damage

                print(f"player lives: {self.player.lives}")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = GameObject.game.menus["in_game_menu"].loop()
                    if not self.running:
                        return False

            if self.active_menu == self.drawn_menu:
                if self.active_menu.check_pressed(event) == "change menu":
                    self.active_menu.active = None
                    self.active_menu = self.menus["fight_menu"]
                    self.active_menu.pressed_before = pygame.key.get_pressed()
                    self.active_menu.active = 0
                if self.active_menu == self.drawn_menu:
                    self.active_menu.pressed_before = pygame.key.get_pressed()

            if self.active_menu == self.menus["fight_menu"]:
                if self.active_menu.check_pressed(event) == "change menu":
                    self.active_menu.active = None
                    self.active_menu = self.drawn_menu
                    self.active_menu.pressed_before = pygame.key.get_pressed()
                    self.active_menu.active = [0, 0]
                if self.active_menu == self.menus["fight_menu"]:
                    self.active_menu.pressed_before = pygame.key.get_pressed()

            return True

    def generate_question(self, action):
        if action == "attack":
            if not self.attack_question:
                self.attack_question = Question()
                self.attack_question.draw(self.menus["attack_question"].buttons[0])
            self.drawn_menu = self.menus["attack_question"]
        if action == "defense":
            if not self.defense_question:
                self.defense_question = Question()
                self.defense_question.draw(self.menus["defense_question"].buttons[0])
            self.drawn_menu = self.menus["defense_question"]

    def attack(self, is_right):
        self.enemy.lives -= randrange(*self.player.ATTACK_STRENGTH) if is_right \
            else round(randrange(*self.player.ATTACK_STRENGTH) * 0.01, 1)
        self.enemy.play("hit", 0.5)
        if self.enemy.lives <= 0:
            GameObject.game.scene.delete_object(self.enemy, [1, *self.enemy.indexes])
            self.running = False
        self.change_menu()
        self.attack_question = None

    def defense(self, is_right):
        self.player.active_defense = "full" if is_right else "not_full"
        self.change_menu()
        self.defense_question = None

    def change_menu(self):
        self.active_menu.active = None
        self.drawn_menu = None
        self.active_menu = self.menus["fight_menu"]
        self.active_menu.active = 0
        self.active_menu.pressed_before = pygame.key.get_pressed()

    def run(self):
        self.running = False
        print("run")

    def hint_50(self):
        if not self.active_menu.buttons[0][0].is_right:
            self.active_menu.buttons[0][0].grey = True
        else:
            self.active_menu.buttons[0][1].grey = True

