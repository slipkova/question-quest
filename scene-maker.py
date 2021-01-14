import pygame
from pygame.locals import *
import sys, json, math, os, copy
from constants import *
from tkinter import Tk
from tkinter import filedialog
from Classes.Button import Button
from Classes.Scene import *
from Classes.Assets import *


def open_file_path():
    root = Tk()
    filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Load",
                                          filetypes=(("animations", "*.json"),
                                                     ("all files", "*.*")))
    root.destroy()
    return filepath


def close_file_path():
    root = Tk()
    filepath = filedialog.asksaveasfile(initialdir=os.getcwd(),
                                        title="Save",
                                        filetypes=(("animations", "*.json"),
                                                   ("all files", "*.*")))
    root.destroy()
    return filepath.name


color = {
    "gray0": (55, 70, 77),
    "gray1": (60, 77, 84),
    "gray2": (35, 44, 49),
    "gray3": (29, 37, 42),
    "gray4": (25, 30, 35),
    "text": (218, 222, 224),
    "active": (0, 211, 51),
}

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption('Scene Maker')


class Rect:
    def __init__(self, **kwargs):
        self.color = kwargs["color"] if "color" in kwargs else (255, 255, 255)
        self.x = kwargs["x"] if "x" in kwargs else SCREEN_WIDTH / 2 - self.width / 2
        self.y = kwargs["y"]
        self.width = kwargs["width"] if "width" in kwargs else 200
        self.height = kwargs["height"] if "height" in kwargs else 50

    def draw(self, screen, color=None):
        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)


class EditItemView:
    def __init__(self, **kwargs):
        self.obj = kwargs["obj"]
        self.saved_data = {}
        self.buttons = {
            "save": MakerButton(
                x=15,
                y=100,
                width=85,
                height=30,
                text="Save",
                text_color=color["text"],
                font_size=20,
                on_click=self.save_data
            ),
            "dismiss": MakerButton(
                x=105,
                y=100,
                width=95,
                height=30,
                text="Dissmiss",
                text_color=color["text"],
                font_size=20,
                on_click=self.get_saved
            ),
            "Close": MakerButton(
                x=400-20-85,
                y=100,
                width=85,
                height=30,
                text="Close",
                text_color=color["text"],
                font_size=20,
                on_click=self.close
            ),
        }
        self.get_saved()

    def get_saved(self):
        count = 0
        for attr in self.obj.__dict__.keys():
            if isinstance(self.obj.__dict__[attr], (str, bool, int)):
                font = pygame.font.SysFont('', 22)
                text = font.render(f"{attr} = ", 1, color["text"])
                self.saved_data[attr] = [InpupButton(
                    x=15 + text.get_size()[0],
                    y=137 + count * 30,
                    height=25,
                    width=400 - 30 - text.get_size()[0],
                    color=color["gray2"],
                    bg=True,
                    name=attr,
                    on_click=self.change_data,
                    value=self.obj.__dict__[attr],
                    is_text=type(self.obj.__dict__[attr]) is not bool
                ), self.obj.__dict__[attr]]
                count += 1

    def save_data(self):
        new_obj = all_assets()[self.obj.name][0](more_data={**all_assets()[self.obj.name][1], **{key: self.saved_data[key][1] for key in self.saved_data.keys()}})
        scene.replace_object(self.obj, new_obj, [scene.active_layer, *scene.active_tile])
        sidebar.edited_item = None

    def change_data(self, key, value):
        self.saved_data[key][1] = value

    def close(self):
        sidebar.edited_item = None

    def render(self):
        pygame.draw.rect(sidebar.display, color["gray3"], (10, 95, 380, 570), 0)
        for button in self.buttons.keys():
            self.buttons[button].draw(sidebar.display)
        for i, attr in enumerate(self.saved_data.keys()):
            font = pygame.font.SysFont('', 22)
            text = font.render(f"{attr} =", 1, color["text"])
            sidebar.display.blit(text, (15, 140 + i * 30))
            self.saved_data[attr][0].draw(sidebar.display)


class MakerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = color["gray2"]
        self.on_click = kwargs["on_click"]
        self.bg = kwargs["bg"] if "bg" in kwargs else True

    def filter_click(self, pos):
        if self.x < pos[0] < (self.x + self.width):
            if self.y < pos[1] < (self.y + self.height):
                self.click()

    def click(self):
        self.color = color["gray0"]
        self.on_click()

    def release(self):
        self.color = color["gray2"]


class Tile(MakerButton):
    def __init__(self, **kwargs):
        self.on_click = kwargs["on_click"] if "on_click" in kwargs else lambda: print("no function")
        self.pointer_to_origin = kwargs["pointer_to_origin"] if "pointer_to_origin" in kwargs else None
        self.text = kwargs["name"] if "name" in kwargs else ""
        self.index = kwargs["index"] if "index" in kwargs else 0
        self.x = 10 + 5 + self.index * 94
        self.y = 800 - 100 - 5
        self.width = 90
        self.height = 90
        self.color = color["gray2"]
        self.text_color = color["text"]
        self.image = kwargs["image"] if "image" in kwargs else None
        self.font_size = 18

    def draw(self, screen, color=None):
        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('', self.font_size)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + 5))
        if self.image:
            image = pygame.transform.scale(self.image, (50, 50))
            screen.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + 30))

    def click(self):
        if pygame.mouse.get_pressed()[2]:
            delete_object(self.pointer_to_origin)
        else:
            self.on_click(self.pointer_to_origin)


class Tab(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_drawn=False)
        self.x = 10
        self.y = 94 + self.index * 23
        self.width = 90
        self.height = 20
        self.color = color["gray2"]

    def draw(self, screen, color=None):
        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('', self.font_size)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + 5))
        if self.image:
            image = pygame.transform.scale(self.image, (50, 50))
            screen.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + 30))

    def click(self):
        self.on_click(self.index)


class Asset(Tile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, is_drawn=False)
        self.x = 105 + kwargs["pos"][0] * 72
        self.y = 94 + kwargs["pos"][1] * 72
        self.width = 69
        self.height = 69
        self.color = color["gray2"]
        self.image = self.pointer_to_origin.dev_image
        self.visible = False

    def draw(self, screen, color=None):
        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('', self.font_size)
        text = font.render(self.text, 1, self.text_color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + 3))
        if self.image:
            image = pygame.transform.scale(self.image, (40, 40))
            screen.blit(image, (self.x + (self.width / 2 - image.get_width() / 2), self.y + 20))

    def click(self):
        if self.visible:
            self.on_click(self.index)


class Checkbox(MakerButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checked = True
        self.images = [pygame.transform.scale(pygame.image.load(kwargs["image_path"][0] if "image_path" in kwargs else "assets/icon/tick/1.png").convert(), (22, 22)),
                       pygame.transform.scale(pygame.image.load(kwargs["image_path"][1] if "image_path" in kwargs else "assets/icon/tick/2.png").convert(), (22, 22))]
        self.images[1].set_colorkey((0, 0, 0))
        self.active_image = self.images[0]

    def click(self):
        self.checked = not self.checked
        self.active_image = self.images[0 if self.checked else 1]
        self.on_click(self.checked)

    def draw(self, screen, color=None):
        if self.bg:
            super().draw(screen, color)
        screen.blit(self.active_image, [self.x + ((self.width - self.active_image.get_size()[0]) / 2),
                                        self.y + ((self.width - self.active_image.get_size()[1]) / 2)])


class InpupButton(Checkbox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs["name"]
        self.is_text = kwargs["is_text"]
        self.value = kwargs["value"]
        self.checked = self.value
        self.active_image = self.images[0 if self.checked else 1]
        self.width = self.width if self.is_text else self.height
        self.is_updated = False

    def click(self):
        if self.is_text:
            self.is_updated = True
        else:
            self.checked = not self.checked
            self.active_image = self.images[0 if self.checked else 1]
            self.value = self.checked
            self.on_click(self.name, self.checked)

    def draw(self, screen):
        if self.is_text:
            if self.is_updated:
                self.write()
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
            font = pygame.font.SysFont('', 22)
            text = font.render(str(self.value), 1, color["text"])
            screen.blit(text, (self.x + 5, self.y + 5))
            if self.is_updated:
                pygame.draw.rect(screen, color["text"], (self.x + text.get_size()[0] + 5, self.y + 5, 1, 15), 0)
        else:
            super().draw(screen)

    def write(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                was_int = isinstance(self.value, int)
                self.value = str(self.value)
                if event.key == K_RETURN:
                    self.is_updated = False
                elif event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]

                else:
                    self.value += event.unicode
                if was_int:
                    if self.value == "":
                        self.value = 0
                    self.value = int(self.value)
                self.on_click(self.name, self.value)





class MakerScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display = kwargs["display"]
        self.active_layer = 0
        self.visible = [True, True]
        self.active_tile = None

    def render_layer(self, layer):
        if self.active_layer == layer:
            self.render_grid()
        for row in self.layers[layer]:
            for tile in row:
                for game_object in tile:
                    self.display.blit(game_object.dev_image,
                                      [game_object.position[1] + ((TILE_SIZE - game_object.image.get_size()[0]) / 2),
                                       game_object.position[0] - (game_object.image.get_size()[1] - TILE_SIZE)])
        if self.active_tile:
            self.display.blit(MakerScene.get_border(color["active"], False),
                              [self.active_tile[1] * TILE_SIZE, self.active_tile[0] * TILE_SIZE])

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
        self.active_tile = [math.floor(pos[0] / TILE_SIZE / 4), math.floor(pos[1] / TILE_SIZE / 4)]

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
        self.active_tile = []
        self.tabs = []
        self.active_tab = 0
        self.active_asset = None
        self.edited_item = None

        for i, tab in enumerate(Assets.keys()):
            self.tabs.append([Tab(index=i, name=tab, on_click=set_sidebar_active_tab), []])
            x, y = 0, 0
            for j, asset in enumerate(Assets[tab].keys()):
                ptr = Assets[tab][asset][0](more_data={**Assets[tab][asset][1], "name": asset})
                print("asset more data" ,Assets[tab][asset][1])
                print("ptr dick" ,ptr.__dict__)
                self.tabs[-1][1].append(Asset(
                    pos=[x, y],
                    index=j,
                    name=ptr.name,
                    pointer_to_origin=ptr,
                    on_click=set_sidebar_active_asset,
                ))
                x += 1
                if x == 4:
                    x = 0
                    y += 1
        for asset in self.tabs[0][1]:
            asset.visible = True

    def render(self):
        self.display.fill(color["gray4"])

        for rect in self.rects.keys():
            self.rects[rect].draw(self.display)
        font = pygame.font.SysFont('', 22)
        text = font.render('Click to delete', 1, color["text"])
        self.display.blit(text, (15, 800 - 100 - 27))
        for button in self.buttons.keys():
            self.buttons[button].draw(self.display)
        for button in self.active_tile:
            button.draw(self.display)

        if self.edited_item:
            self.edited_item.render()
        else:
            for tab in self.tabs:
                tab[0].draw(self.display)
            for asset in self.tabs[self.active_tab][1]:
                asset.draw(self.display)
            self.tabs[self.active_tab][0].draw(self.display, color["gray0"])
            if self.active_asset is not None:
                self.tabs[self.active_tab][1][self.active_asset].draw(self.display, color["gray0"])

    def release(self):
        for name in ["new-scene", "save-my", "save-my-ass", "load-file"]:
            self.buttons[name].release()
        if self.edited_item:
            for btn in self.edited_item.buttons.keys():
                self.edited_item.buttons[btn].release()

    def find_click(self, pos):
        for button in self.buttons.keys():
            self.buttons[button].filter_click(pos)
        for button in self.active_tile:
            button.filter_click(pos)
        if self.edited_item:
            for button in self.edited_item.buttons.keys():
                if self.edited_item:
                    self.edited_item.buttons[button].filter_click(pos)
                    if self.edited_item:
                        for attr in self.edited_item.saved_data.keys():
                            self.edited_item.saved_data[attr][0].filter_click(pos)
        else:
            for tab in self.tabs:
                tab[0].filter_click(pos)
            for asset in self.tabs[self.active_tab][1]:
                asset.filter_click(pos)


SIDEBAR_WIDTH = 400
scene_display = pygame.Surface((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
sidebar_display = pygame.Surface([SIDEBAR_WIDTH, SCREEN_HEIGHT])
WINDOW_SIZE = (SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT)
scene_path = os.getcwd() + "/New-scene.json"
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
scene = MakerScene(display=scene_display, name="")


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
    scene.active_tile = [-1, -1]


def fg_active():
    scene.set_active_layer(1)
    sidebar.buttons["bg-active"].color = color["gray0"]
    sidebar.buttons["fg-active"].color = color["gray3"]
    sidebar.rects["visibility-bg"].color = color["gray0"]
    sidebar.rects["visibility-fg"].color = color["gray3"]
    scene.active_tile = [-1, -1]


def new_scene():
    global scene
    scene = MakerScene(display=scene_display, name="New-scene")


def load_file():
    path = open_file_path()
    with open(path) as json_file:
        global scene, scene_path
        scene = MakerScene(data=json.load(json_file), display=scene_display, name=path[path.rindex("/")+1:-5])
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


def set_edited_item(item):
    sidebar.edited_item = EditItemView(obj=item)


def delete_object(obj):
    scene.delete_object(obj, [scene.active_layer, *scene.active_tile])
    set_active_tile()


def set_active_tile():
    sidebar.active_tile = []
    if len(scene.layers[scene.active_layer][scene.active_tile[0]][scene.active_tile[1]]) > 0:
        for i, game_object in enumerate(scene.layers[scene.active_layer][scene.active_tile[0]][scene.active_tile[1]]):
            sidebar.active_tile.append(Tile(
                index=i,
                image=game_object.dev_image,
                name=game_object.name,
                on_click=set_edited_item,
                pointer_to_origin=game_object
            ))


def set_sidebar_active_tab(tab):
    sidebar.active_tab = tab
    sidebar.active_asset = None
    for tabb in sidebar.tabs:
        for asset in tabb[1]:
            asset.visible = False
    for asset in sidebar.tabs[tab][1]:
        asset.visible = True


def set_sidebar_active_asset(asset):
    sidebar.active_asset = asset


sidebar = Sidebar(display=sidebar_display, buttons={
    "bg-visible": Checkbox(
        x=400 - 30 - 10 - 85 - 10 - 3,
        y=12,
        width=30,
        height=30,
        color=color["gray2"],
        bg=False,
        image_path=["assets/icon/eye/opened.png", "assets/icon/eye/closed.png"],
        on_click=bg_visible
    ),
    "fg-visible": Checkbox(
        x=400 - 30 - 10 - 85 - 10 - 3,
        y=45,
        width=30,
        height=30,
        color=color["gray0"],
        bg=False,
        image_path=["assets/icon/eye/opened.png", "assets/icon/eye/closed.png"],
        on_click=fg_visible
    ),
    "bg-active": MakerButton(
        x=400 - 85 - 10 - 3,
        y=13,
        width=85,
        height=30,
        color=color["gray2"],
        text="Background",
        text_color=color["text"],
        font_size=20,
        on_click=bg_active
    ),
    "fg-active": MakerButton(
        x=400 - 85 - 10 - 3,
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
        color=color["gray2"],
        text="New scene",
        text_color=color["text"],
        font_size=20,
        on_click=new_scene
    ),
    "load-file": MakerButton(
        x=10 + 5 + 85,
        y=10,
        width=85,
        height=30,
        color=color["gray2"],
        text="LOOOL",
        text_color=color["text"],
        font_size=20,
        on_click=load_file
    ),
    "save-my": MakerButton(
        x=10,
        y=10 + 5 + 30,
        width=85,
        height=30,
        color=color["gray2"],
        text="Save my",
        text_color=color["text"],
        font_size=20,
        on_click=save_my
    ),
    "save-my-ass": MakerButton(
        x=10 + 5 + 85,
        y=10 + 5 + 30,
        width=85,
        height=30,
        color=color["gray2"],
        text="Save my ass",
        text_color=color["text"],
        font_size=20,
        on_click=save_my_ass
    ),
}, rects={
    "visibility": Rect(
        color=color["gray0"],
        x=400 - 133 - 10,
        y=10,
        width=133,
        height=69,
    ),
    "visibility-bg": Rect(
        color=color["gray3"],
        x=400 - 60 - 80,
        y=13,
        width=60,
        height=30,
    ),
    "visibility-fg": Rect(
        color=color["gray0"],
        x=400 - 60 - 80,
        y=46,
        width=60,
        height=30,
    ),
    "active-tile": Rect(
        color=color["gray0"],
        x=10,
        y=800 - 100 - 10,
        width=400 - 10 - 10,
        height=100,
    ),
    "separator": Rect(
        color=color["gray0"],
        x=10,
        y=85,
        width=400 - 10 - 10,
        height=2,
    ),
})


def main_loop():
    running = True
    while running:  # game loop
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
                    scene.set_active_tile([mouse_pos[1], mouse_pos[0] - SIDEBAR_WIDTH])
                    set_active_tile()
                    if pygame.mouse.get_pressed()[2] and sidebar.active_asset is not None:
                        short = sidebar.tabs[sidebar.active_tab][1][sidebar.active_asset].pointer_to_origin
                        print("short", short.__dict__)
                        obj_to_push = all_assets()[short.name][0](more_data=short.__dict__)
                        print("short data copy", obj_to_push.__dict__)
                        obj_to_push.indexes = [scene.active_tile[0], scene.active_tile[1]]
                        obj_to_push.position = [scene.active_tile[0] * TILE_SIZE, scene.active_tile[1] * TILE_SIZE]
                        scene.add_object(obj_to_push, [scene.active_layer, *scene.active_tile])
                        set_active_tile()
                else:
                    sidebar.find_click([mouse_pos[0], mouse_pos[1]])
            if event.type == MOUSEBUTTONUP:
                sidebar.release()

        scene.render()
        sidebar.render()
        surf = pygame.transform.scale(scene_display, [SCREEN_WIDTH, SCREEN_HEIGHT])
        screen.blit(surf, (SIDEBAR_WIDTH, 0))
        screen.blit(sidebar_display, [0, 0])
        pygame.display.update()
        clock.tick(120)


main_loop()
