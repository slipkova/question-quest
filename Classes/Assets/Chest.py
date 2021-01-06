from Classes.GameObject import GameObject


class Chest(GameObject):
    def __init__(self, x, y):
        super().__init__(image="images/player.png", solid=True, interactive=True, position=[x, y])

    def interact(self):
        print("You found 32 gold!")