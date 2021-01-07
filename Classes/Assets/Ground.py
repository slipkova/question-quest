from Classes.GameObject import GameObject


class Ground(GameObject):
    def __init__(self, x, y):
        super().__init__(solid=True, image="images/dirt.png", position=[x, y])

