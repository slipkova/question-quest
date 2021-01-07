from Classes.GameObject import GameObject


class Animation:
    def __init__(self, **kwargs):
        self.frames = kwargs["frames"] if "frames" in kwargs else []
        self.duration = kwargs["duration"] if "duration" in kwargs else []


class Animated(GameObject):
    def __init__(self, **kwargs):
        self.animations = kwargs["animations"] if "animations" in kwargs else []
        super().__init__(**kwargs)

    def play(self, animation):
        pass
