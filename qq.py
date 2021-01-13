from constants import *
from pygame.locals import *
from Classes.Scene import Scene
from Classes.Movable import Side
from Classes.Animated import *
from Classes.Assets import Assets
from Classes.Button import ButtonInMenu
from Classes.Menu import Menu
from Classes.GameCore import Game
import random as r
import inspect

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.display.set_caption('Pygame Window')

display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

game_running = True

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
heh = Scene(width=10, height=10)
GameObject.init(display=display, scene=heh)


class Text(GameObject):
    def __init__(self, x, y):
        super().__init__(image="images/nic.png", position=[x, y])
        
    def render(self):
        super().render()
        GameObject.display.blit(font.render(f"{self.indexes[1]},{self.indexes[0]}", False, (0,0,0)), self.position)


g = {"name": "ground", "data": {**Assets["ground"](indexes=[0, 0]).__dict__, "solid": True}}
p = {"name": "player", "data": Assets["player"](indexes=[0, 0]).__dict__}
ch = {"name": "chest", "data": Assets["chest"](indexes=[0, 0]).__dict__}
e = {"name": "enemy", "data": Assets["enemy"](indexes=[0, 0]).__dict__}

bg1 = [
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[],[],[],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[],[],[],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[],[],[p],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[],[],[],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[e],[],[],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[],[],[],[],[],[],[],[],[g],[],[],[],[],[],[]],
[[],[],[],[],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
]
bg = [
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
]
data = [
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
[[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g],[g]],
]

yesyesyes = Scene(data=[bg, bg1])
player = yesyesyes.get_player()
GameObject.init(display=display, scene=yesyesyes)
heh = Assets["ground"](indexes=[0, 0])

'''
def game_loop():
    global game_running
    game_running = True
    while game_running:  # game loop
        display.fill((146, 244, 255))
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                sys.exit()  # stop script
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    player.take_action(Side.RIGHT)
                if event.key == K_LEFT:
                    player.take_action(Side.LEFT)
                if event.key == K_UP:
                    player.take_action(Side.UP)
                if event.key == K_DOWN:
                    player.take_action(Side.DOWN)
                if event.key == K_ESCAPE:
                    game_running = in_game_menu_loop()

        if game_running:
            #test_squares()
            #heh.update()
            yesyesyes.update()

            surf = pygame.transform.scale(display, WINDOW_SIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(120)
'''
'''
def fight_loop():
    global game_running
    running = True
    while running:
        display.fill((146, 244, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = in_game_menu_loop()
                    game_running = False if not running else True

        if running:

            surf = pygame.transform.scale(display, WINDOW_SIZE)
            screen.blit(surf, (0, 0))
            pygame.display.update()
            clock.tick(120)
'''


options_menu = Menu(buttons=[ButtonInMenu(position=1, text="Volume"),
                             ButtonInMenu(position=2, text="Back", event="back")],
                    screen=screen,
                    clock=clock)

in_game_menu = Menu(buttons=[ButtonInMenu(position=1, text="Back to game", event="back"),
                             ButtonInMenu(position=2, text="Options", pointer=options_menu.loop),
                             ButtonInMenu(position=3, text="Quit", event="quit")],
                    screen=screen,
                    clock=clock)

game = Game(display=display, screen=screen, clock=clock, player=player, menu=in_game_menu.loop, yes=yesyesyes)

saves_menu = Menu(buttons=[ButtonInMenu(position=1, text="save1", pointer=game.loop),
                           ButtonInMenu(position=2, text="save2"),
                           ButtonInMenu(position=3, text="save3"),
                           ButtonInMenu(position=4, text="Back", event="back")],
                  screen=screen,
                  clock=clock,)

main_menu = Menu(buttons=[ButtonInMenu(position=1, text="Play", pointer=saves_menu.loop),
                          ButtonInMenu(position=2, text="Options", pointer=options_menu.loop),
                          ButtonInMenu(position=3, text="Quit", event="quit game")],
                 screen=screen,
                 clock=clock)

main_menu.loop()
