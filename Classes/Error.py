

class Error(Exception):
    def __init__(self, message):
        super().__init__(message)

class ImmovableObject(Error):
    def __init__(self, target):
        super().__init__(f"{target} doesn't inherit from Movable")