from Classes.GameObject import GameObject
from Classes.Movable import Movable
from Classes.Animated import Animated
from Classes.GameCore import Fight, Game
from Classes.Movable import Side


class Player(Movable):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            super().__init__(
                image_path="images/player.png",
                solid=True,
                indexes=kwargs["indexes"] if "indexes" in kwargs else [0, 0],
                interactive=True,
                animations_folder="assets/animation/test-guy",
                **kwargs["more_data"]
            )
            
    def interact(self):
        print("fight")
        pass


class Enemy(Animated):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            super().__init__(
                image_path="assets/enemy-flower/animation/idle/idle01.png",
                solid=True,
                interactive=True,
                indexes=kwargs["indexes"] if "indexes" in kwargs else [0, 0],
                animations_folder="assets/enemy-flower/animation"
            )

    def interact(self):
        GameObject.game.enemy = self


class Chest(GameObject):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            super().__init__(
                image_path="images/player.png",
                solid=True,
                interactive=True,
                indexes=kwargs["indexes"] if "indexes" in kwargs else [0, 0],
                **kwargs["more_data"]
            )

    def interact(self):
        print("You found 32 gold!")


class Ground(GameObject):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            input_raw = {**{
                "solid": False,
                "image_path": kwargs["image_path"] if "iamge_path" in kwargs else "images/dirt.png",
                "indexes": kwargs["indexes"] if "indexes" in kwargs else [0, 0],
                },
                **kwargs["more_data"]}
            result = {}
            for key, value in input_raw.items():
                if value not in result.values():
                    result[key] = value
            super().__init__(**result)


