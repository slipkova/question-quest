from enum import Enum
from Classes.Animated import Animated
from Classes.GameObject import GameObject
from Classes.Error import AnimationNotFound
from constants import *
import os


class Action(Enum):
    MOVE = 0
    NONE = 1
    INTERACT = 2


class Side(Enum):
    UP = [0, [-1, 0], "top"]
    RIGHT = [1, [0, 1], "right"]
    DOWN = [2, [1, 0], "bottom"]
    LEFT = [3, [0, -1], "left"]


class Movable(Animated):
    def __init__(self, **kwargs):
        for def_anim in ["run-left.json", "run-right.json", "run-top.json", "run-bottom.json", "idle.json"]:
            if def_anim not in os.listdir(kwargs["animations_folder"]):
                raise AnimationNotFound(def_anim)
            if "data" in kwargs:
                if def_anim not in os.listdir(kwargs["data"]["animations_folder"]):
                    raise AnimationNotFound(def_anim)
        super().__init__(**kwargs)
        if "data" in kwargs:
            self.mass = kwargs["data"]["mass"]
        else:
            self.mass = 40
        self.actions = [Action.MOVE, Action.MOVE, Action.MOVE, Action.MOVE]
        self.surrounded = [[], [], [], []]
        self.pixel_loc = [[0, 0], 0]


    def update(self):
        super().update()
        self.get_actions()
        if self.pixel_loc[1] != 0:
            self.position = [self.position[0] + self.pixel_loc[0][0], self.position[1] + self.pixel_loc[0][1]]
            self.pixel_loc[1] -= 1

    def get_surrounded(self):
        surrounded = []
        for side in Side:
            new_indexes = [self.indexes[0] + side.value[1][0], self.indexes[1] + side.value[1][1]]
            surrounded.append(GameObject.scene.matrix[new_indexes[0]][new_indexes[1]])
        return surrounded

    def get_actions(self):
        if self.surrounded != self.get_surrounded():
            self.surrounded = self.get_surrounded()

        for i, side in enumerate(self.surrounded):
            self.actions[i] = Action.MOVE
            for gameObject in side:
                if gameObject.solid:
                    self.actions[i] = Action.NONE
                if gameObject.interactive:
                    self.actions[i] = Action.INTERACT

    def take_action(self, direction):
        self.get_actions()
        for side in Side:
            if direction == side:
                if self.actions[side.value[0]] == Action.MOVE:
                    self.move(direction)
                if self.actions[side.value[0]] == Action.INTERACT:
                    self.surrounded[side.value[0]][-1].interact()   # he he he

    def move(self, direction):
        self.play(f"run-{direction.value[2]}", 0.5)
        new_indexes = [self.indexes[0] + direction.value[1][0], self.indexes[1] + direction.value[1][1]]
        GameObject.scene.move_object(self, self.indexes, new_indexes)
        new_pos = [new_indexes[0] * TILE_SIZE, new_indexes[1] * TILE_SIZE]
        self.pixel_loc = [[(new_pos[0] - self.position[0]) / self.mass,
                           (new_pos[1] - self.position[1]) / self.mass], self.mass]
