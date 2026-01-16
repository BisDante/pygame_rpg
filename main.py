from settings import *
from data_manager import *
from main_menu import MainMenu
from actor import *

class Game:
    def __init__(self, scene=None):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dungeons of Doom')
        self.convert_surfs()
        
        self.data = START_SAVE.copy()
        self.data['surfaces'] = load_surfaces()
        self.data['maps'] = MapTree()
        self.data['last_map'] = None
        self.scene = scene if scene else MainMenu(self.display, self.data)
        self.clock = pygame.time.Clock()

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

if __name__ == "__main__":
    game = Game()
    game.run()