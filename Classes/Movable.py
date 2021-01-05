from enum import Enum
from Classes.Animated import Animated


class Action(Enum):
    MOVE = 0
    NONE = 1
    INTERACT = 2


class Side(Enum):
    TOP = [0, [0, 1]]
    RIGHT = [1, [1, 0]]
    BOTTOM = [2, [0, -1]]
    LEFT = [3, [-1, 0]]


class Movable(Animated):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.actions = [Action.MOVE, Action.MOVE, Action.MOVE, Action.MOVE]
        self.surrounded = [[], [], [], []]

    def update(self, surrounded):
        super().update()
        if self.surrounded != surrounded:
            self.surrounded = surrounded
            self.get_actions()

    def get_actions(self):
        for i, side in enumerate(self.surrounded):
            for gameObject in side:
                self.actions[i] = Action.MOVE
                if gameObject.solid:
                    self.actions[i] = Action.NONE
                if gameObject.interactive:
                    self.actions[i] = Action.INTERACT

    def take_action(self, direction):
        for side in Side:
            if direction == side:
                if self.actions[side.value[0]] == Action.MOVE:
                    self.move(direction)
                if self.actions[side.value[0]] == Action.INTERACT:
                    self.surrounded[side.value[0]][0].interact()   # he he he

    def move(self):
        #      COMPLETE HERE
        pass
