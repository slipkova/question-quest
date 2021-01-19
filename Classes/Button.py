import pygame
from constants import *


class Button:
    def __init__(self, **kwargs):
        self.color = kwargs["color"] if "color" in kwargs else (255, 255, 255)
        self.width = kwargs["width"] if "width" in kwargs else 200
        self.height = kwargs["height"] if "height" in kwargs else 50
        self.x = kwargs["x"] if "x" in kwargs else SCREEN_WIDTH/2 - self.width/2
        self.y = kwargs["y"] if "x" in kwargs else 50
        self.text = kwargs["text"] if "text" in kwargs else ""
        self.font_size = kwargs["font_size"] if "font_size" in kwargs else 60
        self.text_color = kwargs["text_color"] if "text_color" in kwargs else (0, 0, 0)

    def draw(self, screen, color=None):

        pygame.draw.rect(screen, color if color else self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('',  self.font_size)
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

        return False


class ButtonInMenu(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = 320
        self.height = 70
        self.img = pygame.image.load("assets/images/buttons/b1.png").convert()
        self.img.set_colorkey((255, 255, 255))
        self.position = kwargs["position"]
        self.x = SCREEN_WIDTH/2 - self.width/2
        self.y = 200 + 100 * self.position
        self.pointer = kwargs["pointer"] if "pointer" in kwargs else None
        self.event = kwargs["event"] if "event" in kwargs else None
        self.text_color = (255, 255, 255)

    def click(self):
        self.pointer()

    def draw(self, screen, img=None):
        if img:
            img = pygame.image.load(img).convert()
            img.set_colorkey((255, 255, 255))
        screen.blit(pygame.transform.scale(img if img else self.img, [self.width, self.height]), (self.x, self.y))

        if self.text != '':
            font = pygame.font.SysFont('', self.font_size)
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

        return False



class SaveButton(ButtonInMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def click(self):
        self.pointer(self.position)


class FightButton(ButtonInMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 40
        self.width = 150
        self.x = 50
        self.y = SCREEN_HEIGHT - 300 + 60 * self.position
        self.font_size = 30

    def click(self):
        if self.event:
            self.pointer(self.event if self.event else None)
        else:
            self.pointer()


class AnswerButton(FightButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        answers = ["a", "b", "c"]
        self.text = answers[self.position - 1] + ") " + kwargs["text"]
        self.color = (185, 244, 255)
        self.y = SCREEN_HEIGHT - 200
        self.x = 350 + 180 * (self.position - 1)
        self.right_answer = None

    def click(self):
        self.pointer(self.right_answer)


class HintButton(FightButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.y = SCREEN_HEIGHT - 120
        self.x = 350 + 180 * (self.position - 1)
        self.grey = False

