import pygame
from constants import TYLE_SIZE

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
        self.image = pygame.image.load(kwargs["image"] if "image" in kwargs else None)
        self.solid = kwargs["solid"] if "solid" in kwargs else False
        self.position = [kwargs["position"][0] * TYLE_SIZE, kwargs["position"][1] * TYLE_SIZE] if "position" in kwargs else [0, 0]
        self.interactive = kwargs["interactive"] if "interactive" in kwargs else False
        self.indexes = kwargs["position"] if "position" in kwargs else [0, 0]

    def update(self):
        self.render()

    def render(self):
        GameObject.display.blit(self.image, [self.position[1], self.position[0]])

    def interact(self):
        pass
