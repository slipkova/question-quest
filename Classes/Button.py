import pygame
from constants import *


class Button():
    def __init__(self, **kwargs):
        self.color = kwargs["color"] if "color" in kwargs else (255, 255, 255)
        self.x = kwargs["x"] if "x" in kwargs else SCREEN_WIDTH/2 - self.width/2
        self.y = kwargs["y"]
        self.width = kwargs["width"] if "width" in kwargs else 200
        self.height = kwargs["height"] if "height" in kwargs else 50
        self.text = kwargs["text"] if "text" in kwargs else ""

    def draw(self, screen, color=None):

        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return False


class ButtonInMenu(Button):
    def __init__(self, position, text=''):
        self.text = text
        self.width = 300
        self.height = 50
        self.color = (255, 255, 255)
        self.x = SCREEN_WIDTH/2 - self.width/2
        self.y = 200 + 100 * position

