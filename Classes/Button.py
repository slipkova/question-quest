import pygame
from constants import *


class Button():
    def __init__(self, x, y, text=''):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.width = 200
        self.height = 50
        self.text = text

    def draw(self, screen, color = None):

        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return False


class ButtonInMenu(Button):
    def __init__(self, position, text=''):
        self.text = text
        self.width = 300
        self.height = 50
        self.color = (255, 255, 255)
        self.x = SCREEN_WIDTH/2 - self.width/2
        self.y = 200 + 100 * position

