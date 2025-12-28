from settings import *
from scene import Scene
from data_manager import *

class Battle(Scene):
    def __init__(self, display, data, encounter):
        super().__init__(display, data)
        self.data = data
        self.party = data['characters']
        self.enemies = load_encounter(encounter)
     