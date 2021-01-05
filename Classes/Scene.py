from Classes.Movable import Movable
from Classes.Assets.Ground import Ground
from Classes.Error import *


class Scene:
    """" Holds a matrix of gameObjects. Structure for making levels. """
    def __init__(self, width, height):
        self.matrix = [[[] for y in range(width)] for x in range(height)]

    def move_object(self, target, old_loc, new_loc):
        if isinstance(target, Movable):
            self.matrix[old_loc[0]][old_loc[1]].remove(target)
            self.matrix[new_loc[0]][new_loc[1]].append(target)
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
            for j,y in enumerate(x):
                if len(y) == 0:
                    res += " "
                elif isinstance(y[0], Ground):
                    res += "#"
                else:
                    res += "@"
            res += str(i)+"\n"
        return res


