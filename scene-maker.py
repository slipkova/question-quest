import pygame
from pygame.locals import *
import sys, json, math, os
from constants import *
from tkinter import Tk
from tkinter import filedialog
from Classes.Button import Button
from Classes.Scene import Scene


def open_file_path():
    root = Tk()
    filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="LOOOL SCEEEEENAAAA",
                                          filetypes= (("animations","*.json"),
                                          ("all files","*.*")))
    root.destroy()
    return filepath


def close_file_path():
    root = Tk()
    filepath = filedialog.asksaveasfile(initialdir=os.getcwd(),
                                          title="Save",
                                          filetypes= (("animations","*.json"),
                                          ("all files","*.*")))
    root.destroy()
    return filepath.name


color = {
    "gray0": (55, 70, 77),
    "gray1": (60, 77, 84),
    "gray2": (35, 44, 49),
    "gray3": (31, 39, 42),
    "gray4": (29, 37, 40),
    "text": (218, 222, 224),
    "active": (0,211,51),
}


class Rect:
    def __init__(self, **kwargs):
        self.color = kwargs["color"] if "color" in kwargs else (255, 255, 255)
        self.x = kwargs["x"] if "x" in kwargs else SCREEN_WIDTH / 2 - self.width / 2
        self.y = kwargs["y"]
        self.width = kwargs["width"] if "width" in kwargs else 200
        self.height = kwargs["height"] if "height" in kwargs else 50

    def draw(self, screen, color=None):
        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)



class MakerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_click = kwargs["on_click"]
        self.bg = kwargs["bg"] if "bg" in kwargs else True

    def filter_click(self, pos):
        if self.x < pos[0] < (self.x + self.width):
            if self.y < pos[1] < (self.y + self.height):
                self.click()

    def click(self):
        self.on_click()



class Checkbox(MakerButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, width=kwargs["size"], height=kwargs["size"])
        self.checked = True
        self.images = [pygame.transform.scale(pygame.image.load(kwargs["image_path"][0]).convert(), (22, 22)),
                       pygame.transform.scale(pygame.image.load(kwargs["image_path"][1]).convert(), (22, 22))]
        self.images[1].set_colorkey((0, 0, 0))
        self.active_image = self.images[0]

    def click(self):
        self.checked = not self.checked
        self.active_image = self.images[0 if self.checked else 1]
        self.on_click(self.checked)

    def update(self, function):
        function(self.checked)

    def draw(self, screen, color=None):
        if self.bg:
            super().draw(screen, color)
        screen.blit(self.active_image, [self.x + ((self.width - self.active_image.get_size()[0]) / 2),
                                        self.y + ((self.width - self.active_image.get_size()[1]) / 2)])


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
            self.display.blit(MakerScene.get_border(color["active"], False), [self.active_tile[0] * TILE_SIZE, self.active_tile[1] * TILE_SIZE])

    def set_visible(self, bools):
        self.visible = bools

    def set_active_layer(self, layer):
        self.active_layer = layer

    def render_grid(self):
        for x in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for y in range(int(SCREEN_HEIGHT / TILE_SIZE)):
                self.display.blit(MakerScene.get_border(color["gray0"], True), (x * TILE_SIZE, y * TILE_SIZE))

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

    def render(self):
        self.display.fill((189, 246, 255))
        if self.visible[0]:
            self.render_layer(0)
        if self.visible[1]:
            self.render_layer(1)


class Sidebar:
    def __init__(self, **kwargs):
        self.buttons = kwargs["buttons"]
        self.rects = kwargs["rects"]
        self.display = kwargs["display"]

    def render_top_bar(self):
        pass

    def render(self):
        self.display.fill(color["gray4"])

        for rect in self.rects.keys():
            self.rects[rect].draw(self.display)
        for button in self.buttons.keys():
            self.buttons[button].draw(self.display)

    def find_click(self, pos):
        for button in self.buttons.keys():
            self.buttons[button].filter_click(pos)


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
pygame.display.set_caption('Pygame Window')

SIDEBAR_WIDTH = 400
scene_display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
sidebar_display = pygame.Surface([SIDEBAR_WIDTH, SCREEN_HEIGHT])
WINDOW_SIZE = (SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT)
scene_path = os.getcwd()+"/New-scene.json"
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
scene = MakerScene(display=scene_display)


def bg_visible(a):
    scene.set_visible([a, scene.visible[1]])


def fg_visible(a):
    scene.set_visible([scene.visible[0], a])


def bg_active():
    scene.set_active_layer(0)
    sidebar.buttons["bg-active"].color = color["gray3"]
    sidebar.buttons["fg-active"].color = color["gray0"]
    sidebar.rects["visibility-bg"].color = color["gray3"]
    sidebar.rects["visibility-fg"].color = color["gray0"]


def fg_active():
    scene.set_active_layer(1)
    sidebar.buttons["bg-active"].color = color["gray0"]
    sidebar.buttons["fg-active"].color = color["gray3"]
    sidebar.rects["visibility-bg"].color = color["gray0"]
    sidebar.rects["visibility-fg"].color = color["gray3"]


def new_scene():
    global scene
    scene = MakerScene(display=scene_display)


def load_file():
    path = open_file_path()
    with open(path) as json_file:
        global scene, scene_path
        scene = MakerScene(data=json.load(json_file), display=scene_display)
        scene_path = path


def save_my():
    global scene, scene_path
    with open(scene_path, "w") as json_file:
        json.dump(scene.export(), json_file)


def save_my_ass():
    path = close_file_path()
    with open(path, "w") as json_file:
        global scene, scene_path
        json.dump(scene.export(), json_file)
        scene_path = path


sidebar = Sidebar(display=sidebar_display, buttons={
    "bg-visible": Checkbox(
        x=400-30-10-85-10-3,
        y=12,
        size=30,
        color=color["gray2"],
        bg=False,
        image_path=["assets/icon/eye/opened.png", "assets/icon/eye/closed.png"],
        on_click=bg_visible
    ),
    "fg-visible": Checkbox(
        x=400-30-10-85-10-3,
        y=45,
        size=30,
        color=color["gray2"],
        bg=False,
        image_path=["assets/icon/eye/opened.png", "assets/icon/eye/closed.png"],
        on_click=fg_visible
    ),
    "bg-active": MakerButton(
        x=400-85-10-3,
        y=13,
        width=85,
        height=30,
        color=color["gray3"],
        text="Background",
        text_color=color["text"],
        font_size=20,
        on_click=bg_active
    ),
    "fg-active": MakerButton(
        x=400-85-10-3,
        y=46,
        width=85,
        height=30,
        color=color["gray0"],
        text="Foreground",
        text_color=color["text"],
        font_size=20,
        on_click=fg_active
    ),
    "new-scene": MakerButton(
        x=10,
        y=10,
        width=85,
        height=30,
        color=color["gray0"],
        text="New scene",
        text_color=color["text"],
        font_size=20,
        on_click=new_scene
    ),
    "load-file": MakerButton(
        x=10+5+85,
        y=10,
        width=85,
        height=30,
        color=color["gray0"],
        text="LOOOL",
        text_color=color["text"],
        font_size=20,
        on_click=load_file
    ),
    "save-my": MakerButton(
        x=10,
        y=10+5+30,
        width=85,
        height=30,
        color=color["gray0"],
        text="Save my",
        text_color=color["text"],
        font_size=20,
        on_click=save_my
    ),
    "save-my-ass": MakerButton(
        x=10+5+85,
        y=10+5+30,
        width=85,
        height=30,
        color=color["gray0"],
        text="Save my ass",
        text_color=color["text"],
        font_size=20,
        on_click=save_my_ass
    ),
    }, rects={
    "visibility": Rect(
        color=color["gray0"],
        x=400-133-10,
        y=10,
        width=133,
        height=69,
        ),
    "visibility-bg": Rect(
        color=color["gray3"],
        x=400-60-80,
        y=13,
        width=60,
        height=30,
        ),
    "visibility-fg": Rect(
        color=color["gray0"],
        x=400-60-80,
        y=46,
        width=60,
        height=30,
        ),
    })


def main_loop():
    running = True
    while running: # game loop
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
                else:
                    sidebar.find_click([mouse_pos[0], mouse_pos[1]])

        scene.render()
        sidebar.render()
        surf = pygame.transform.scale(scene_display, [SCREEN_WIDTH, SCREEN_HEIGHT])
        screen.blit(surf, (SIDEBAR_WIDTH, 0))
        screen.blit(sidebar_display, [0,0])
        pygame.display.update()
        clock.tick(120)


main_loop()