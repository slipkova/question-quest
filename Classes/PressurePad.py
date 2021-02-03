from Classes.GameObject import GameObject
from Classes.Movable import Movable


class PressurePad(GameObject):
    def __init__(self, **kwargs):
        self.dev_image_path = "assets/images/tool.png"
        super().__init__(**kwargs)
        self.pressed = False
        self.mode = kwargs["data"]["mode"] if "data" in kwargs else kwargs["mode"] if "mode" in kwargs else "player"
        print(self.image)


    def update(self):
        super().update()
        for obj in GameObject.game.scene.layers[1][self.indexes[0]][self.indexes[1]]:
            if self.mode == "player" and obj.name == "player":
                self.press()
            elif self.mode == "all" and isinstance(obj, Movable):
                self.press()

    def press(self):
        if not self.pressed:
            self.pressed = True
            self.on_press()

    def on_press(self):
        print("pressed")