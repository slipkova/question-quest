from Classes.GameObject import GameObject
from Classes.Movable import Movable
from Classes.Animated import Animation
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
                animations_folder="assets/animation/test-guy"
            )


    #def update(self):
    #    super().update()


    def interact(self):
        print("fight")
        pass


class Chest(GameObject):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            super().__init__(
                image_path="images/player.png",
                solid=True,
                interactive=True,
                indexes=kwargs["indexes"] if "indexes" in kwargs else [0, 0]
            )

    def interact(self):
        print("You found 32 gold!")


class Ground(GameObject):
    def __init__(self, **kwargs):
        if "data" in kwargs:
            super().__init__(data=kwargs["data"])
        else:
            super().__init__(
                solid=True,
                image_path="images/dirt.png",
                indexes=kwargs["indexes"] if "indexes" in kwargs else [0, 0]
            )
