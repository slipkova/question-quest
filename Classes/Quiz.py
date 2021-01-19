import random


class Question:
    def __init__(self):
        '''
        self.a = random.randint(0, 50)
        self.b = random.randint(1, 20)
        self.operator = random.choice(["+", "-", "*", "/"])
        self.question = f"{self.a} {self.operator} {self.b}"
        self.operations = {
            "+": self.a + self.b,
            "-": self.a - self.b,
            "*": self.a * self.b,
            "/": self.a / self.b,
        }
        self.right_answer = round(self.operations[self.operator], 0)
        self.answers = ([self.right_answer,
                         self.right_answer * (round(random.random(), 0) + 0.5),
                         self.right_answer * (round(random.random(), 0) + 0.5)])

        '''
        self.a = random.randint(0, 50)
        self.b = random.randint(0, 40)
        self.question = f"{self.a} + {self.b}"
        self.right_answer = self.a + self.b
        self.answers = ([self.right_answer,
                         self.right_answer + random.randrange(1, 5),
                         self.right_answer - random.randrange(1, 5)])
        random.shuffle(self.answers)

    def draw(self, buttons):
        for i, button in enumerate(buttons):
            button.text = str(self.answers[i])
            button.right_answer = True if self.answers[i] == self.right_answer else False

