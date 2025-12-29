"""
Test file for scene types.
"""

from settings import *
from data_manager import *
from battle import Battle

char1 = {
      "id": 0,
      "name": "Name",
      "level": 1,
      "experience": 0,
      "max_hp": 20,
      "attack": 25,
      "defense": 5,
      "max_mana": 20,
      "intelligence": 5,
      "willpower": 5,
      "speed": 5,
      "agility": 5,
      "accuracy": 5,
      "luck": 5
    }
characters = [char1.copy() for i in range(4)]
for i, character in enumerate(characters):
    character['name'] = f'fighter{i}'

enemy = {
      "id": 0,
      "name": "bat",
      "level": 1,
      "experience": 5,
      "max_hp": 20,
      "attack": 3,
      "defense": 5,
      "max_mana": 20,
      "intelligence": 5,
      "willpower": 5,
      "speed": 7,
      "agility": 5,
      "accuracy": 5,
      "luck": 5
    }

enemy2 = {
      "id": 0,
      "name": "knight",
      "level": 1,
      "experience": 5,
      "max_hp": 20,
      "attack": 3,
      "defense": 5,
      "max_mana": 20,
      "intelligence": 5,
      "willpower": 5,
      "speed": 5,
      "agility": 5,
      "accuracy": 5,
      "luck": 5
    }

enemies = [enemy.copy() for i in range(4)]

class TestGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeons of Doom')
        self.convert_surfs()
        
        self.data = START_SAVE.copy()
        self.data['characters'] = characters
        self.data['actor_surfaces'] = load_actor_surfaces()

        self.scene = Battle(self.display, self.data, enemies)
        self.clock = pygame.time.Clock()
        self.run()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            self.scene = self.scene.update(dt, event_list)
            self.scene.draw()

            pygame.display.update()

    def convert_surfs(self):
        global SELECT_ICON, PLAYER_ICON
        SELECT_ICON = SELECT_ICON.convert_alpha()
        PLAYER_ICON = PLAYER_ICON.convert_alpha()

game = TestGame()