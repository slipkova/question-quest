from Classes.Movable import Movable
from Classes.Final import *
from Classes.Assets import *
from Classes.Error import *
from constants import *
import numpy
from PIL import Image
import pygame, time


def validate(data, was_go, deep):
    deep += 1
    if isinstance(data, (list, tuple)):
        new = []
        for item in data:
            new.append(validate(item, was_go, deep))
        return new
    elif isinstance(data, dict):
        new = {}
        for key in data.keys():
            new[key] = validate(data[key], was_go, deep)
        return new
    elif isinstance(data, tuple([GameClasses[key] for key in GameClasses.keys()])):
        if GameObject.game:
            GameObject.game.scene.count += 1
        # print(f"{GameObject.game.scene.count} / {GameObject.game.scene.count_all} {deep}")
        return validate([{"name": name, "data": validate(data.__dict__, was_go, deep)} for name in GameClasses.keys() if isinstance(data, GameClasses[name])][0], was_go, deep)
    elif isinstance(data, tuple([all_assets()[key][0] for key in all_assets().keys()])):
        if not was_go:
            if GameObject.game:
                GameObject.game.scene.count += 1
            # print(f"{GameObject.game.scene.count} / {GameObject.game.scene.count_all} {deep} {data.name}")
            return validate([{"name": name, "data": validate(data.__dict__, True, deep)} for name in all_assets().keys() if data.name == name][0], True, deep)
        else:
            return None
    elif isinstance(data, (bool, int, float, str, range)):
        return data
    else:
        return None


def construct(**kwargs):
    if isinstance(kwargs["data"], (list, tuple)):
        new = []
        for item in kwargs["data"]:
            new.append(construct(data=item))
        return new
    elif isinstance(kwargs["data"], dict):
        if "name" in kwargs["data"] and "data" in kwargs["data"]:
            if kwargs["data"]["name"] in all_assets():
                return all_assets()[kwargs["data"]["name"]][0](data={**kwargs["data"]["data"], "indexes": kwargs["indexes"]})
            if kwargs["data"]["name"] in GameClasses:
                return GameClasses[kwargs["data"]["name"]](data=kwargs["data"]["data"])
        else:
            new = {}
            for key in kwargs["data"].keys():
                new[key] = construct(data=kwargs["data"][key])
            return new
    else:
        return kwargs["data"]


class Scene:
    """" Holds a matrix of gameObjects. Structure for making levels. """
    def __init__(self, **kwargs):
        self.full_load = kwargs["full_load"] if "full_load" in kwargs else False
        if "data" in kwargs:
            self.layers = []
            first = True
            for layer in kwargs["data"]["layers"]:
                if not self.full_load and first:
                    first = False
                    self.layers.append(kwargs["data"]["layers"][0])
                    continue
                all_rows = []
                for x, row in enumerate(layer):
                    all_tiles = []
                    for y, tile in enumerate(row):
                        all_objects = []
                        for game_object in tile:
                            obj = Scene.translate_data(data=game_object, input_type="json", indexes=[x, y])
                            all_objects.append(obj)
                        all_tiles.append(all_objects)
                    all_rows.append(all_tiles)
                self.layers.append(all_rows)
        else:
            self.layers = [[[[] for y in range(int(SCREEN_WIDTH / TILE_SIZE / 4))] for x in range(int(SCREEN_WIDTH / TILE_SIZE / 4))] for z in range(2)]
        self.name = kwargs["name"]
        self.bg_color = kwargs["data"]["bg_color"] if "data" in kwargs else kwargs["bg_color"] if "bg_color" in kwargs else (0, 0, 0)
        self.bg_img = self.construct_image(kwargs["data"]["bg_img"]) if "data" in kwargs else self.construct_image(kwargs["bg_img"]) if kwargs["bg_img"] else None
        self.count = 0
        self.count_all = 0

    def move_object(self, target, old_loc, new_loc):
        if isinstance(target, Movable):
            self.layers[old_loc[0]][old_loc[1]][old_loc[2]].remove(target)
            self.layers[new_loc[0]][new_loc[1]][new_loc[2]].append(target)
            target.indexes = [*new_loc][1:]
        else:
            raise ImmovableObject(target)

    def replace_object(self, obj1, obj2, path):
        self.layers[path[0]][path[1]][path[2]].insert(self.layers[path[0]][path[1]][path[2]].index(obj1)+1, obj2)
        self.layers[path[0]][path[1]][path[2]].remove(obj1)
        obj2.indexes = [*path][1:]

    def update(self):
        for layer in self.layers:
            for row in layer:
                for tile in row:
                    for gameObject in tile:
                        gameObject.update()

    def operate_object(self, **kwargs):
        checked_class = kwargs["obj_class"]
        for layer in self.layers:
            for x in layer:
                for y in x:
                    for z in y:
                        if isinstance(z, checked_class):
                            if kwargs["remove"] if "remove" in kwargs else False:
                                y.remove(z)
                            return z
        return None

    def delete_object(self, obj, path):
        self.layers[path[0]][path[1]][path[2]].remove(obj)

    def add_object(self, obj, path):
        self.layers[path[0]][path[1]][path[2]].append(obj)
        obj.indexes = [*path][1:]

    def export(self):
        sttime = time.time()
        # print("start")
        bgimg = Scene.deconstruct_image(self.bg_img)
        # print(time.time() - sttime, "time1")
        sttime = time.time()
        # print("start")
        for layer in self.layers:
            for x in layer:
                for y in x:
                    for z in y:
                        self.count_all += 1
        # print(f"total {self.count_all} objects,", self.full_load)
        # print(self.layers)
        if self.full_load:
            data = Scene.translate_data(data=self.layers, input_type="objects")
        else:
            data = [[], []]
            data[0] = self.layers[0]
            data[1] = Scene.translate_data(data=self.layers[1], input_type="objects")
        print(time.time() - sttime, "time2")
        return {"bg_color": self.bg_color, "bg_img": bgimg, "layers": data}

    @staticmethod
    def deconstruct_image(image):
        return numpy.array(pygame.surfarray.array3d(image).swapaxes(0,1)).tolist()

    @staticmethod
    def construct_image(image):
        img = Image.fromarray(numpy.uint8(numpy.array(image)))
        return pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()

    def get_token(self):
        res = ""
        for x in self.layers[1]:
            for y in x:
                for z in y:
                    res += z.name[0]
        return res

    @staticmethod
    def translate_data(**kwargs):
        return validate(kwargs["data"], False, 0) if kwargs["input_type"].lower() == "objects" else construct(data=kwargs["data"], indexes=kwargs["indexes"])

    def __str__(self):
        res = ""
        for i, x in enumerate(self.layers[1]):
            for j, y in enumerate(x):
                if len(y) == 0:
                    res += " "
                elif isinstance(y[0], Ground):
                    res += "#"
                else:
                    res += "@"
            res += str(i)+"\n"
        return res


