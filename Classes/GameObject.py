import pygame


class GameObject(pygame.sprite.Sprite):
    """ Super class for every object in the game. """
    display = None

    def init(self, display):
        GameObject.display = display

    def __init__(self, **kwargs):
        super(GameObject, self).__init__()
        self.image = pygame.image.load(kwargs["image"] if "image" in kwargs else None)
        self.solid = kwargs["solid"] if "solid" in kwargs else False
        self.position = kwargs["position"] if "position" in kwargs else [0, 0]
        self.interactive = kwargs["interactive"] if "interactive" in kwargs else False

    def update(self):
        self.render()

    def render(self):
        GameObject.display.blit(self.image, self.position)

    def interact(self):
        pass
