from settings import *
from data_manager import *
from main_menu import MainMenu
from map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.convert_surfs()
        self.scene = MainMenu(self.display)
        # self.scene = Map(load_map('map1.tmx'), self.display)
        self.clock = pygame.time.Clock()
        self.run()

    def run(self):
        running = True
        input_event = None
        while running:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    input_event = event
                    
            self.scene = self.scene.update(dt, input_event)
            input_event = None
            self.scene.draw()

            pygame.display.update()

    def convert_surfs(self):
        global SELECT_ICON, PLAYER_ICON
        SELECT_ICON = SELECT_ICON.convert_alpha()
        PLAYER_ICON = PLAYER_ICON.convert_alpha()

game = Game()