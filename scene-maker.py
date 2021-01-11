import pygame
from pygame.locals import *
import sys, json, math
from constants import *
from Classes.Scene import Scene



class MakerScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display = kwargs["display"]
        self.active_layer = 1
        self.visible = [True, True]
        self.active_tile = None

    def render_layer(self, layer):
        if self.active_layer == layer:
            self.render_grid()
        for row in self.layers[layer]:
            for tile in row:
                for game_object in tile:
                    self.display.blit(game_object.image,
                                        [game_object.position[1] + ((TILE_SIZE - game_object.image.get_size()[0]) / 2),
                                         game_object.position[0] - game_object.image.get_size()[1]])
        if self.active_tile:
            self.display.blit(MakerScene.get_border((27, 15, 255), False), [self.active_tile[0] * TILE_SIZE, self.active_tile[1] * TILE_SIZE])

    def render_grid(self):
        for x in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for y in range(int(SCREEN_HEIGHT / TILE_SIZE)):
                self.display.blit(MakerScene.get_border((145, 200, 255), True), (x * TILE_SIZE, y * TILE_SIZE))

    @staticmethod
    def get_border(color, full):
        surf = pygame.Surface([16, 16], pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, 16, 1))
        pygame.draw.rect(surf, color, (0, 15, 16, 1))
        pygame.draw.rect(surf, color, (0, 0, 1, 16))
        pygame.draw.rect(surf, color, (15, 0, 1, 16))
        surf.set_colorkey((0, 0, 0))
        if full:
            pygame.draw.rect(surf, (255, 255, 255, 100), (1, 1, 14, 14))
        return surf

    def set_active_tile(self, pos):
        self.active_tile = [math.floor(pos[0] / TILE_SIZE / 2), math.floor(pos[1] / TILE_SIZE / 2)]
        print(self.active_tile)

    def render(self):
        if self.visible[0]:
            self.render_layer(0)
        if self.visible[1]:
            self.render_layer(1)


class Sidebar:
    def __init__(self):
        pass

    def render_top_bar(self):
        pass

    def render(self):
        pass


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.display.set_caption('Pygame Window')

SIDEBAR_WIDTH = 400
scene_display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
sidebar_display = pygame.Surface([SIDEBAR_WIDTH, SCREEN_HEIGHT])
WINDOW_SIZE = (SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
with open("scene1.json") as json_file:
    scene = MakerScene(data=json.load(json_file), display=scene_display)

def main_loop():
    running = True
    while running: # game loop
        #scene_display.fill((240, 253, 255))
        scene_display.fill((0, 0, 0))
        sidebar_display.fill((189, 246, 255))
        # pygame.draw.rect(sidebar_display, [189, 246, 255], (0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT), 0)
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                sys.exit()  # stop script
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > SIDEBAR_WIDTH:
                    scene.set_active_tile([mouse_pos[0] - SIDEBAR_WIDTH, mouse_pos[1]])

        scene.render()
        draw_sidebar()
        surf = pygame.transform.scale(scene_display, [SCREEN_WIDTH, SCREEN_HEIGHT])
        screen.blit(surf, (SIDEBAR_WIDTH, 0))
        screen.blit(sidebar_display, [0,0])
        pygame.display.update()
        clock.tick(120)


def draw_sidebar():
    pass



main_loop()