from Classes.Movable import Movable


class Player(Movable):
    def __init__(self, x, y):
        super().__init__(image="images/player.png", solid=True, position=[x, y], interactive=True)

    def update(self):
        super().update()


    def interact(self):
        print("fight")
        pass
