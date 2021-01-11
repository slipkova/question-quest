from Classes.Movable import Movable
from Classes.Final import *
from Classes.Assets import *
from Classes.Error import *
from constants import *


def validate(data):
    if isinstance(data, (list, tuple)):
        new = []
        for item in data:
            new.append(validate(item))
        return new
    elif isinstance(data, dict):
        new = {}
        for key in data.keys():
            new[key] = validate(data[key])
        return new
    elif isinstance(data, tuple([GameClasses[key] for key in GameClasses.keys()])):
        return validate([{"name": name, "data": validate(data.__dict__)} for name in GameClasses.keys() if isinstance(data, GameClasses[name])][0])
    elif isinstance(data, tuple([Assets[key] for key in Assets.keys()])):
        return validate([{"name": name, "data": validate(data.__dict__)} for name in Assets.keys() if isinstance(data, Assets[name])][0])
    elif isinstance(data, (bool, int, float, str, range)):
        return data
    else:
        return None


def construct(**kwargs):
    if isinstance(kwargs["data"], (list, tuple)):
        new = []
        for item in kwargs["data"]:
            new.append(construct(item))
        return new
    elif isinstance(kwargs["data"], dict):
        if "name" in kwargs["data"] and "data" in kwargs["data"]:
            print("class")
            if kwargs["data"]["name"] in Assets:
                return Assets[kwargs["data"]["name"]](data={**kwargs["data"]["data"], "indexes": kwargs["indexes"]})
            if kwargs["data"]["name"] in GameClasses:
                return GameClasses[kwargs["data"]["name"]](data=kwargs["data"]["data"])
        else:
            new = {}
            for key in kwargs["data"].keys():
                new[key] = construct(kwargs["data"][key])
            return new
    else:
        return kwargs["data"]


class Scene:
    """" Holds a matrix of gameObjects. Structure for making levels. """
    def __init__(self, **kwargs):
        if "data" in kwargs:
            self.layers = []
            for layer in kwargs["data"]:
                all_rows = []
                for x, row in enumerate(layer):
                    all_tiles = []
                    for y, tile in enumerate(row):
                        all_objects = []
                        for game_object in tile:
                            obj = Scene.translate_data(data=game_object, input_type="json", indexes=[x, y])
                            print(obj.indexes)
                            all_objects.append(obj)
                        all_tiles.append(all_objects)
                    all_rows.append(all_tiles)
                self.layers.append(all_rows)
        else:
            self.layers = [[[[] for y in range(int(SCREEN_WIDTH / TILE_SIZE))] for x in range(int(SCREEN_WIDTH / TILE_SIZE))] for z in range(2)]

    def move_object(self, target, old_loc, new_loc):
        if isinstance(target, Movable):
            self.layers[old_loc[0]][old_loc[1]][old_loc[2]].remove(target)
            self.layers[new_loc[0]][new_loc[1]][new_loc[2]].append(target)
            target.indexes = [*new_loc][1:]
        else:
            raise ImmovableObject(target)

    def update(self):
        for layer in self.layers:
            for row in layer:
                for tile in row:
                    for gameObject in tile:
                        gameObject.update()

    def get_player(self):
        for layer in self.layers:
            for x in layer:
                for y in x:
                    for z in y:
                        if isinstance(z, Player):
                            return z

    def export(self):
        return Scene.translate_data(data=self.layers, input_type="objects")

    @staticmethod
    def translate_data(**kwargs):
        return validate(kwargs["data"]) if kwargs["input_type"].lower() == "objects" else construct(data=kwargs["data"], indexes=kwargs["indexes"])

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


