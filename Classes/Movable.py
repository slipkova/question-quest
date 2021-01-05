from enum import Enum
from Classes.Animated import Animated
from Classes.GameObject import GameObject
from constants import *


class Action(Enum):
    MOVE = 0
    NONE = 1
    INTERACT = 2


class Side(Enum):
    UP = [0, [0, 1]]
    RIGHT = [1, [1, 0]]
    DOWN = [2, [0, -1]]
    LEFT = [3, [-1, 0]]


class Movable(Animated):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actions = [Action.MOVE, Action.MOVE, Action.MOVE, Action.MOVE]
        self.surrounded = [[], [], [], []]

    def update(self):
        super().update()
        self.get_actions()

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
            for gameObject in side:
                self.actions[i] = Action.MOVE
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
                    self.surrounded[side.value[0]][0].interact()   # he he he

    def move(self, direction):
        new_indexes = [self.indexes[0] + direction.value[1][0], self.indexes[1] + direction.value[1][1]]
        print(new_indexes)
        GameObject.scene.move_object(self, self.indexes, new_indexes)
        self.position = [new_indexes[0] * TYLE_SIZE, new_indexes[1] * TYLE_SIZE]
        print(GameObject.scene)
