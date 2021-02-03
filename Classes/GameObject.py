import pygame
from constants import TILE_SIZE


class GameObject(pygame.sprite.Sprite):
    """ Super class for every object in the game. """
    game = None

    def __init__(self, **kwargs):
        super(GameObject, self).__init__()
        if "data" in kwargs:
            self.image_path = kwargs["data"]["image_path"] if "image_path" in kwargs["data"] else None
            self.dev_image_path = kwargs["data"]["dev_image_path"] if "dev_image_path" in kwargs["data"] else None
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.colorkey = kwargs["data"]["colorkey"] if "colorkey" in kwargs["data"] else (1, 1, 1)
            self.dev_image = pygame.image.load(self.dev_image_path if self.dev_image_path else self.image_path).convert_alpha()
            self.image.set_colorkey(self.colorkey)
            self.dev_image.set_colorkey(self.colorkey)
            self.solid = kwargs["data"]["solid"] if "solid" in kwargs["data"] else False
            self.position = [kwargs["data"]["indexes"][0] * TILE_SIZE,
                             kwargs["data"]["indexes"][1] * TILE_SIZE] if "indexes" in kwargs["data"] else [0, 0]
            self.interactive = kwargs["data"]["interactive"] if "interactive" in kwargs["data"] else False
            self.indexes = kwargs["data"]["indexes"] if "indexes" in kwargs["data"] else [0, 0]
            self.name = kwargs["data"]["name"] if "name" in kwargs["data"] else str(type(self))[str(type(self)).rindex(".")+1:][:-2].lower()
        else:
            self.image_path = kwargs["image_path"] if "image_path" in kwargs else None
            self.dev_image_path = kwargs["dev_image_path"] if "dev_image_path" in kwargs else None
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.dev_image = pygame.image.load(self.dev_image_path if self.dev_image_path else self.image_path).convert_alpha()
            self.colorkey = kwargs["colorkey"] if "colorkey" in kwargs else (1, 1, 1)
            self.image.set_colorkey(self.colorkey)
            self.dev_image.set_colorkey(self.colorkey)
            self.solid = kwargs["solid"] if "solid" in kwargs else False
            self.position = [kwargs["indexes"][0] * TILE_SIZE, kwargs["indexes"][1] * TILE_SIZE] if "indexes" in kwargs else [0, 0]
            self.interactive = kwargs["interactive"] if "interactive" in kwargs else False
            self.indexes = kwargs["indexes"] if "indexes" in kwargs else [0, 0]
            self.name = kwargs["name"] if "name" in kwargs else str(type(self))[str(type(self)).rindex(".")+1:][:-2].lower()

    def update(self):
        self.render()

    def render(self):
        GameObject.game.draw(self.image, [self.position[1] + ((TILE_SIZE - self.image.get_size()[0]) / 2),
                                             int(self.position[0] - self.image.get_size()[1] + TILE_SIZE)])

    def sync_pos(self):
        self.position = [self.indexes[0] * TILE_SIZE, self.indexes[1] * TILE_SIZE]

    def interact(self):
        pass
