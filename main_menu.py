from settings import *
from scene import *
from new_game import NewGame

class MainMenu(Scene):
    TITLE = 0
    MAIN = 1
    NEW_GAME = 2
    LOAD_GAME = 3
    QUIT = 4
    
    def __init__(self, display):
        super().__init__(display)
        self.gothic_small = pygame.font.Font(GOTHIC, 64)
        self.gothic_big = pygame.font.Font(GOTHIC, 128)
        self.normal_font = pygame.font.Font(None, 36)
        
        self.state = MainMenu.TITLE
        
        self.main_index = 0
        self.main_options = ['New Game', 'Load Game', 'Quit']
        self.main_states = [MainMenu.NEW_GAME, MainMenu.LOAD_GAME, MainMenu.QUIT]

        self.load_index = 0

    def title(self):
        self.display.fill(WHITE)

        title_top = self.gothic_small.render('Dungeons of', False, BLACK)
        title_top_rect = title_top.get_frect(center=(SCREEN_WIDTH/2, 100))
    
        title_bottom = self.gothic_big.render('DOOM', False, BLACK)
        title_bottom_rect = title_bottom.get_frect(center=(SCREEN_WIDTH/2, title_top_rect.bottom + title_top_rect.height/1.5))
        
        press_key = self.normal_font.render('Press Enter', False, BLACK)
        press_key_rect = press_key.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + title_bottom_rect.height/2))

        self.display.blit(title_top, title_top_rect)
        self.display.blit(title_bottom, title_bottom_rect)
        self.display.blit(press_key, press_key_rect)

    def main(self):
        self.display.fill(WHITE)

        title_top = self.gothic_small.render('Dungeons of', False, BLACK)
        title_top_rect = title_top.get_frect(center=(SCREEN_WIDTH/2, 100))
    
        title_bottom = self.gothic_big.render('DOOM', False, BLACK)
        title_bottom_rect = title_bottom.get_frect(center=(SCREEN_WIDTH/2, title_top_rect.bottom + title_top_rect.height/1.5))

        self.display.blit(title_top, title_top_rect)
        self.display.blit(title_bottom, title_bottom_rect)

        leftmost = SCREEN_WIDTH
        for i, option in enumerate(self.main_options):
            button = self.normal_font.render(option, False, BLACK)
            button_rect = button.get_frect(center=(SCREEN_WIDTH/2, title_bottom_rect.bottom + title_bottom_rect.height/3 + 30 * (i+1)))
            if button_rect.left < leftmost: leftmost = button_rect.left
            self.display.blit(button, button_rect)

            if  i == self.main_index:
                select_icon_rect = SELECT_ICON.get_frect(midright=(leftmost - 30, button_rect.centery))
                self.display.blit(SELECT_ICON, select_icon_rect)

    def new_game(self):
        return NewGame(self.display)
    
    def quit(self):
        pygame.quit()
        sys.exit(0)

    def input(self):
        if self.state == MainMenu.TITLE:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.state = MainMenu.MAIN

        elif self.state == MainMenu.MAIN:
            keys = pygame.key.get_just_pressed()
            self.main_index = (self.main_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.main_options)

            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.state = self.main_states[self.main_index]

    def update(self, dt, input):
        self.input()
        match self.state:
            case MainMenu.NEW_GAME: return self.new_game()
            case MainMenu.QUIT: return self.quit()
        
        return self

    def draw(self):
        match self.state:
            case MainMenu.TITLE: self.title()
            case MainMenu.MAIN: self.main()