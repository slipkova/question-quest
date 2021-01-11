import pygame
from constants import TILE_SIZE


class GameObject(pygame.sprite.Sprite):
    """ Super class for every object in the game. """
    display = None
    scene = None

    @staticmethod
    def init(**kwargs):
        GameObject.display = kwargs["display"] if "display" in kwargs else None
        GameObject.scene = kwargs["scene"] if "scene" in kwargs else None

    def __init__(self, **kwargs):
        super(GameObject, self).__init__()
        if "data" in kwargs:
            self.image_path = kwargs["data"]["image_path"] if "image_path" in kwargs["data"] else None
            self.image = pygame.image.load(self.image_path).convert()
            self.solid = kwargs["data"]["solid"] if "solid" in kwargs["data"] else False
            self.position = [kwargs["data"]["indexes"][0] * TILE_SIZE,
                             kwargs["data"]["indexes"][1] * TILE_SIZE] if "indexes" in kwargs["data"] else [0, 0]
            self.interactive = kwargs["data"]["interactive"] if "interactive" in kwargs["data"] else False
            self.indexes = kwargs["data"]["indexes"] if "indexes" in kwargs["data"] else [0, 0]
        else:
            self.image_path = kwargs["image_path"] if "image_path" in kwargs else None
            self.image = pygame.image.load(self.image_path).convert()
            if "key_color" in kwargs:
                self.image.set_colorkey(kwargs["key_color"])
            self.solid = kwargs["solid"] if "solid" in kwargs else False
            self.position = [kwargs["indexes"][0] * TILE_SIZE, kwargs["indexes"][1] * TILE_SIZE] if "indexes" in kwargs else [0, 0]
            self.interactive = kwargs["interactive"] if "interactive" in kwargs else False
            self.indexes = kwargs["indexes"] if "indexes" in kwargs else [0, 0]

    def update(self):
        self.render()

    def render(self):
        GameObject.display.blit(self.image, [self.position[1] + ((TILE_SIZE - self.image.get_size()[0]) / 2),
                                             self.position[0] - self.image.get_size()[1]])

    def interact(self):
        pass
