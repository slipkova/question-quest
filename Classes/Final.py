from Classes.GameObject import GameObject
from Classes.Movable import *
from Classes.Animated import Animated
from Classes.Movable import Side
from Classes.PressurePad import PressurePad
from random import randrange


class Player(Movable):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": True,
                "interactive": True,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/test-guy/animation/idle/idle1.png",
                "animations_folder": kwargs[
                    "animations_folder"] if "animations_folder" in kwargs else "assets/test-guy/animation",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                         **kwargs["more_data"]}
            result = {}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)
        self.lives = 100
        self.attack_strength = [15, 30]
        self.defense_strength = [10, 20]
        self.active_defense = False

    def interact(self):
        print("fight")
        pass


class Enemy(Animated):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
          input_raw = {**{
                "solid": True,
                "interactive": True,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/enemy-flower/animation/idle/idle01.png",
                "animations_folder": kwargs[
                    "animations_folder"] if "animations_folder" in kwargs else "assets/enemy-flower/animation",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                         **kwargs["more_data"]}
          result = {}
          for key, value in input_raw.items():
            result[key] = value
            super().__init__(**result)
        self.lives = 100
        self.attack_strength = [10, 18]

            


    def interact(self):
        GameObject.game.enemy = self

    def attack(self):
        self.play("attack", 1)
        return randrange(*self.attack_strength)


class Chest(Animated):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": True,
                "interactive": True,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/images/player.png",
                "animations_folder": kwargs[
                    "animations_folder"] if "animations_folder" in kwargs else "assets/world/door/1/animation",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                         **kwargs["more_data"]}
            result = {}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)

    def interact(self):
        print("You found 32 gold!")


class Ground(GameObject):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": True,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/images/dirt.png",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                **kwargs["more_data"]}
            result = {}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)


class EnterPad(PressurePad):
    def __init__(self, **kwargs):
        result = {}
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": False,
                "interactive": False,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/images/enter.png",
                "dev_image_path": kwargs["dev_image_path"] if "dev_iamge_path" in kwargs else "assets/images/enter.png",
                "colorkey": (0, 0, 0),
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                **kwargs["more_data"]}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)
        self.origin = kwargs["data"]["origin"] if "data" in kwargs else result["origin"] if "origin" in result else ""
        self.index = kwargs["data"]["index"] if "data" in kwargs else result["index"] if "index" in result else 0


class ExitPad(PressurePad):
    def __init__(self, **kwargs):
        result = {}
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": False,
                "interactive": False,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/images/exit.png",
                "dev_image_path": kwargs["dev_image_path"] if "dev_iamge_path" in kwargs else "assets/images/exit.png",
                "colorkey": (0, 0, 0),
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                         **kwargs["more_data"]}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)
        self.destination = kwargs["data"]["destination"] if "data" in kwargs else result["destination"] if "destination" in result else ""
        self.index = kwargs["data"]["index"] if "data" in kwargs else result["index"] if "index" in result else 0

    def on_press(self):
        GameObject.game.load_scene(self.destination, self.index)


class Door(Animated):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": False,
                "interactive": True,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "assets/world/door/1/l1.png",
                "animations_folder": kwargs["animations_folder"] if "animations_folder" in kwargs else "assets/world/door/1/animation",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0]},
                **kwargs["more_data"]}
            result = {}
            for key, value in input_raw.items():
                result[key] = value
            super().__init__(**result)
        self.image = self.animations["open"].frames[0]
        self.opened = False
        self.surrounded = [[], [], [], []]

    def update(self):
        self.opened = self.is_opened()

        if self.get_frame():
            self.image = self.get_frame()
        else:
            if self.opened:
                self.image = self.animations["open"].frames[-1]
            else:
                self.image = self.animations["open"].frames[0]
        super().render()

    def is_opened(self):
        surrounded = []
        for side in Side:
            new_indexes = [self.indexes[0] + side.value[1][0], self.indexes[1] + side.value[1][1]]
            surrounded.append(GameObject.game.scene.layers[1][new_indexes[0]][new_indexes[1]])
        for side in surrounded:
            for game_object in side:
                if isinstance(game_object, Movable):
                    if not self.opened:
                        self.play("open", 1)
                    return True
        if self.opened:
            self.play("close", 1)
        return False

    def interact(self):
        print("brr")


