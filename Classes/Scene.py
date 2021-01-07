from Classes.Movable import Movable
from Classes.Final import Ground
from Classes.Assets import Assets
from Classes.Error import *


class Scene:
    """" Holds a matrix of gameObjects. Structure for making levels. """
    def __init__(self, **kwargs):
        self.matrix = []
        if "data" in kwargs:
            for row in enumerate(kwargs["data"]):
                all_tiles = []
                for tile in enumerate(row):
                    all_objects = []
                    for game_object in tile:
                        all_objects.append(Assets[game_object["name"]](data=game_object["data"]))
                    all_tiles.append(all_objects)
                self.matrix.append(all_tiles)
        else:
            self.matrix = [[[] for y in range(kwargs['width'])] for x in range(kwargs['height'])]

    def move_object(self, target, old_loc, new_loc):
        if isinstance(target, Movable):
            self.matrix[old_loc[0]][old_loc[1]].remove(target)
            self.matrix[new_loc[0]][new_loc[1]].append(target)
            target.indexes = new_loc
        else:
            raise ImmovableObject(target)

    def update(self):
        for row in self.matrix:
            for tile in row:
                for gameObject in tile:
                    gameObject.update()

    def __str__(self):
        res = ""
        for i, x in enumerate(self.matrix):
            for j, y in enumerate(x):
                if len(y) == 0:
                    res += " "
                elif isinstance(y[0], Ground):
                    res += "#"
                else:
                    res += "@"
            res += str(i)+"\n"
        return res


