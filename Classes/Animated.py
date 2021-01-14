from Classes.GameObject import GameObject
from Classes.Error import AnimationNotFound
import json
import numpy
from PIL import Image
import pygame
import time
import os


class Animation:
    def __init__(self, **kwargs):
        if "data_path" in kwargs:
            with open(kwargs["data_path"]) as json_file:
                data = json.load(json_file)
            self.frames = []
            for frame in data["frames"]:
                img = Image.fromarray(numpy.uint8(numpy.array(frame)))
                pygame_img = pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()
                pygame_img.set_colorkey(data["colorkey"])
                self.frames.append(pygame_img)
            self.duration = data["duration"]
        else:
            self.frames = kwargs["frames"] if "frames" in kwargs else []
            self.duration = kwargs["duration"] if "duration" in kwargs else 1

    def get_segments(self, duration):
        return (duration if duration else self.duration) / len(self.frames)


class Animated(GameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animations = {}
        self.animations_folder = kwargs["data"]["animations_folder"] if "data" in kwargs else kwargs["animations_folder"]
        for file in os.listdir(self.animations_folder):
            if file[-5:] == ".json":
                self.animations[file[:-5]] = Animation(data_path=f'{self.animations_folder}{"/" if self.animations_folder[-1] != "/" else ""}{file}')
        self.played_anim = kwargs["data"]["played_anim"] if "data" in kwargs else kwargs["played_anim"] if "played_anim" in kwargs else [None, 0]
        self.start_time = kwargs["data"]["start_time"] if "data" in kwargs else kwargs["start_time"] if "start_time" in kwargs else time.time()
        self.is_idle = kwargs["data"]["is_idle"] if "data" in kwargs else kwargs["is_idle"] if "is_idle" in kwargs else True

    def update(self):
        # print(self.get_frame())
        if self.get_frame():
            self.image = self.get_frame()
        else:
            self.play("idle", 1)
        if not self.image:
            print(self.__dict__)
            self.image = self.animations[str(self.animations.keys()).partition("[")[2].partition(",")[0][1:-1]].frames[
                0]
        super().render()


    def get_frame(self):
        loc_time = time.time() - self.start_time
        if self.played_anim[0]:
            for i in range(len(self.animations[self.played_anim[0]].frames)):
                if loc_time < self.animations[self.played_anim[0]].get_segments(self.played_anim[1]) * i:
                    return self.animations[self.played_anim[0]].frames[i]
            return None
        else:
            return None

    def play(self, animation, duration=1):
        if animation in self.animations:
            self.played_anim = [animation, duration if duration else self.animations[animation].duration]
            self.start_time = time.time()
        else:
            raise AnimationNotFound(animation)

