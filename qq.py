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

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
heh = Scene(width=10, height=10)
GameObject.init(display=display, scene=heh)


class Text(GameObject):
    def __init__(self, x, y):
        super().__init__(image="images/nic.png", position=[x, y])
        
    def render(self):
        super().render()
        GameObject.display.blit(font.render(f"{self.indexes[1]},{self.indexes[0]}", False, (0,0,0)), self.position)



with open("test.json") as json_file:
    yesyesyes = Scene(data=json.load(json_file))
#print(yesyesyes)
player = yesyesyes.get_player()
GameObject.init(display=display, scene=yesyesyes)



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
