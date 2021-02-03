from enum import Enum
from Classes.Animated import Animated
from Classes.GameObject import GameObject
from Classes.Error import AnimationNotFound
from constants import *
import os, time


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
            self.animations_folder = kwargs["data"]["animations_folder"] if "data" in kwargs else kwargs[
                "animations_folder"]
            if def_anim not in os.listdir(self.animations_folder):
                raise AnimationNotFound(def_anim)
        super().__init__(**kwargs)

        self.speed = kwargs["data"]["speed"] if "data" in kwargs else kwargs["speed"] if "speed" in kwargs else 3
        self.actions = [Action.MOVE, Action.MOVE, Action.MOVE, Action.MOVE]
        self.surrounded = [[], [], [], []]
        self.move_pos = [[0, 0], [0, 0]]
        self.move_time = time.time()
        self.moving = False

    def get_pos(self, time):
        mult = self.normalize(time)
        return [self.move_pos[0][0] + (self.move_pos[1][0] - self.move_pos[0][0]) * mult, self.move_pos[0][1] + (self.move_pos[1][1] - self.move_pos[0][1]) * mult]

    def normalize(self, value):
        return (value - 0) / ((1 / self.speed) - 0)

    def update(self):
        super().update()
        self.get_actions()
        if self.position != self.move_pos[1] and self.move_pos[1] != [0, 0]:
            if time.time() - self.move_time < 1 / self.speed:
                self.position = self.get_pos(time.time() - self.move_time)
            elif self.moving:
                self.moving = False

    def get_surrounded(self):
        surrounded = []
        for side in Side:
            new_indexes = [self.indexes[0] + side.value[1][0], self.indexes[1] + side.value[1][1]]
            surrounded.append(GameObject.game.scene.layers[1][new_indexes[0]][new_indexes[1]])
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
                    self.surrounded[side.value[0]][-1].interact()  # he he he

    def move(self, direction):
        self.moving = True
        self.play(f"run-{direction.value[2]}", 1 / self.speed * 1.2)
        new_indexes = [self.indexes[0] + direction.value[1][0], self.indexes[1] + direction.value[1][1]]

        self.move_pos = [[self.indexes[0] * TILE_SIZE, self.indexes[1] * TILE_SIZE], [new_indexes[0] * TILE_SIZE, new_indexes[1] * TILE_SIZE]]
        GameObject.game.scene.move_object(self, [1, *self.indexes], [1, *new_indexes])
        self.move_time = time.time()
