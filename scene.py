from settings import *

class Scene:
    def __init__(self, display, data):
        self.display = display
        self.data = data
        self.enter()

    def input(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

