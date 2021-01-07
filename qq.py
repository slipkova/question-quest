import pygame, sys
from constants import *
from pygame.locals import * # import pygame modules
from Classes.Scene import Scene
from Classes.Assets.Ground import Ground
from Classes.GameObject import GameObject
from Classes.Button import Button, ButtonInMenu
from Classes.Menu import Menu


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Pygame Window')
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))
GameObject.display = display


def end():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


main_menu = Menu([ButtonInMenu(1, "Play"), ButtonInMenu(2, "Options"), ButtonInMenu(3, "Quit")])
saves = Menu([ButtonInMenu(1, "Save 1"), ButtonInMenu(2, "Save 2"), ButtonInMenu(3, "Save 3"), ButtonInMenu(4, "Back")])
options_menu = Menu([ButtonInMenu(1, "Volume"), ButtonInMenu(2, "Back")])
in_game_menu = Menu([ButtonInMenu(1, "Back to game"), ButtonInMenu(2, "Options"), ButtonInMenu(3, "Quit")])


def main_menu_loop():
    while main_menu.running:
        end()
        main_menu.update(pygame.key.get_pressed(), screen)
        pygame.display.update()

        if main_menu.click:
            if main_menu.active == 0:
                saves_loop()
            elif main_menu.active == 1:
                options_menu_loop()
            elif main_menu.active == 2:
                main_menu.running = False
            main_menu.active = 0
            main_menu.click = False
        clock.tick(60)
    pygame.quit()
    sys.exit()


def options_menu_loop():
    options_menu.running = True
    i = 0
    while options_menu.running:
        end()
        options_menu.update(pygame.key.get_pressed(), screen, i)
        pygame.display.update()

        if options_menu.click:
            if options_menu.active == 0:
                pass
            if options_menu.active == 1:
                options_menu.running = False
            options_menu.active = 0
            options_menu.click = False
        clock.tick(60)
        i += 1


def saves_loop():
    saves.running = True
    i = 0
    while saves.running:
        end()
        saves.update(pygame.key.get_pressed(), screen, i)
        pygame.display.update()

        if saves.click:
            if saves.active == 0:
                game_loop()
            if saves.active == 1:
                pass
            if saves.active == 2:
                pass
            if saves.active == 3:
                saves.running = False
            saves.active = 0
            saves.click = False
        clock.tick(60)
        i += 1


def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = in_game_menu_loop()
        pygame.display.update()


def in_game_menu_loop():
    in_game_menu.running = True
    i = 0
    while in_game_menu.running:
        end()
        in_game_menu.update(pygame.key.get_pressed(), screen, i)
        pygame.display.update()

        if in_game_menu.click:
            if in_game_menu.active == 0:
                in_game_menu.running = False
            elif in_game_menu.active == 1:
                options_menu_loop()
            elif in_game_menu.active == 2:
                return False
            in_game_menu.active = 0
            in_game_menu.click = False
        clock.tick(60)
        i += 1
    return True


main_menu_loop()

