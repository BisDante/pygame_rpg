from settings import *
from scene import *
from actor import PlayerCharacter

class NewGame(Scene):
    ROWS = 2
    COLS = 2

    MAIN = 0
    CREATE_NEW = 1

    def __init__(self, display):
        super().__init__(display)
        self.state = NewGame.MAIN
        self.gothic_font = pygame.font.Font(GOTHIC, 48)
        self.normal_font = pygame.font.Font(None, 36)
        self.main_index = {'x': 0, 'y': 0}

        self.max_points = self.remaining_points = 20
        self.default_character = {
            'id': 0,
            'name': 'SoEpic',
            'level': 1,
            'max_hp': 20,
            'attack': 5,
            'defense': 5,
            'max_mana': 20,
            'intelligence': 5,
            'willpower': 5,
            'speed': 5,
            'agility': 5,
            'accuracy': 5,
            'luck': 5
        }
        self.character = self.default_character.copy()
        self.attribute_list = ['name', 'max_hp', 'max_mana', 'attack', 'defense', 'intelligence', 'willpower', 'speed', 'agility', 'accuracy', 'luck']
        self.attribute_index = 0
        self.characters = [None, None, None, None]
        self.warning = 0
        self.type_timer = 0
        self.type_limit = 200

    def main(self):
        self.display.fill(WHITE)
        title = self.gothic_font.render('Character Creation', False, BLACK)
        title_rect = title.get_frect(center=(SCREEN_WIDTH / 2, 75))
        self.display.blit(title, title_rect)

        w, h = 300, 200
        side_margin = 25
        top_margin = 25
        bottom_margin = 50
        div = pygame.FRect(side_margin,
                           title_rect.bottom + top_margin, SCREEN_WIDTH - 2 * side_margin,
                           SCREEN_HEIGHT - title_rect.bottom - bottom_margin)
        
        # pygame.draw.rect(self.display, BLACK, div, 4, 0)

        for row in range(NewGame.ROWS):
            for col in range(NewGame.COLS):
                rect = pygame.FRect(0, 0, w, h)
                rect.center = (div.left + div.width/4 * (col * 2 + 1), div.top + div.height/4 * (row * 2 + 1))
                pygame.draw.rect(self.display, BLACK, rect, 4, 0)

                character_index = col + row * 2
                if not self.characters[character_index]:
                    name = self.gothic_font.render('Empty', False, BLACK)
                    name_rect = name.get_frect(center=rect.center)
                    self.display.blit(name, name_rect)

                else:
                    player_icon = PLAYER_ICON.copy()
                    player_icon = pygame.transform.scale_by(player_icon, 2)
                    player_icon_rect = player_icon.get_frect(center=(rect.centerx, rect.centery-20))
                    self.display.blit(player_icon, player_icon_rect)

                    name = self.normal_font.render(f'{self.characters[character_index]['name']}', False, BLACK)
                    name_rect = name.get_frect(midtop=(rect.centerx, rect.centery + 20))
                    self.display.blit(name, name_rect)

                if self.main_index['x'] == col and self.main_index['y'] == row:
                    select_icon_rect = SELECT_ICON.get_frect(center=(rect.left - side_margin, rect.centery))
                    self.display.blit(SELECT_ICON, select_icon_rect)

    def create_new_character(self):
        self.display.fill(WHITE)
        
        player_icon = PLAYER_ICON.copy()
        player_icon = pygame.transform.scale_by(player_icon, 2)
        player_icon_rect = player_icon.get_frect(center=(SCREEN_WIDTH/2, 75))
        self.display.blit(player_icon, player_icon_rect)

        for i, attribute in enumerate(self.attribute_list):
            current_attrib = self.attribute_list[i]
            if attribute == 'name':
                attrib_text = self.gothic_font.render('Name', False, BLACK)
                attrib_rect = attrib_text.get_frect(midtop=(SCREEN_WIDTH/2, player_icon_rect.bottom + 10))
                self.display.blit(attrib_text, attrib_rect)

                value_text = self.normal_font.render(str(self.character[current_attrib]), False, BLACK)
                value_rect = value_text.get_frect(midtop=(SCREEN_WIDTH/2, attrib_rect.bottom + 10))
                self.display.blit(value_text, value_rect)
                
                remaining_points_text = self.normal_font.render(f'remaining points: {self.remaining_points}', False, BLACK)
                remaining_points_rect = remaining_points_text.get_frect(topleft=(SCREEN_WIDTH/4, value_rect.bottom + 10))
                self.display.blit(remaining_points_text, remaining_points_rect)

            else:
                attrib_text = self.normal_font.render(attribute, False, BLACK)
                attrib_rect = attrib_text.get_rect(topleft=(SCREEN_WIDTH/4, remaining_points_rect.bottom + i*30))
                self.display.blit(attrib_text, attrib_rect)

                value_text = self.normal_font.render(str(self.character[self.attribute_list[i]]), False, BLACK)
                value_rect = value_text.get_frect(center=(SCREEN_WIDTH/2, attrib_rect.centery))
                self.display.blit(value_text, value_rect)

            if self.attribute_index == i:
                select_icon_rect = SELECT_ICON.get_frect(center=(attrib_rect.left - SELECT_ICON.get_width(), attrib_rect.centery))
                self.display.blit(SELECT_ICON, select_icon_rect)

        match self.warning:
            case 1:
                text = self.normal_font.render('You need to have 0 points left', False, BLACK)
                rect = text.get_frect(midtop=(SCREEN_WIDTH/2, attrib_rect.bottom + 10))
                self.display.blit(text, rect)

            case _:
                pass

    def input(self, dt, input_event):
        self.type_timer += dt
        keys = pygame.key.get_just_pressed()

        if self.state == NewGame.MAIN:
            self.main_index['x'] = (self.main_index['x'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % NewGame.COLS
            self.main_index['y'] = (self.main_index['y'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % NewGame.ROWS

            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                character_index = self.main_index['x'] + self.main_index['y'] * 2
                if self.characters[character_index]:
                    self.remaining_points = 0
                    self.character = self.characters[character_index]

                self.state = NewGame.CREATE_NEW

        if self.state == NewGame.CREATE_NEW:
            self.attribute_index = (self.attribute_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.attribute_list)
            change_value = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            if change_value > 0 and self.remaining_points <= 0 or change_value < 0 and self.remaining_points >= self.max_points:
                change_value = 0

            current_attrib = self.attribute_list[self.attribute_index]
            if current_attrib == 'name':
                if input_event:
                    if input_event.key == pygame.K_BACKSPACE:
                        self.character[current_attrib] = self.character[current_attrib][:-1]

                    elif input_event.unicode.isalnum() or input_event.unicode == ' ':
                        self.character[current_attrib] += input_event.unicode

            elif current_attrib in ['max_hp', 'max_mana']:
                self.character[current_attrib] += change_value * 5
                self.remaining_points -= change_value
            else:
                self.character[current_attrib] += change_value
                self.remaining_points -= change_value

            if keys[pygame.K_SPACE]:
                if self.remaining_points > 0:
                    self.warning = 1

                else:
                    self.add_character(self.character.copy(), self.main_index['x'] + self.main_index['y'] * 2)
                    self.remaining_points = self.max_points
                    self.character = self.default_character.copy()
                    self.state = NewGame.MAIN

    def add_character(self, character, slot):
        self.characters[slot] = character

    def update(self, dt, input_event):
        self.input(dt, input_event)
        return self

    def draw(self):
        match self.state:
            case NewGame.MAIN: self.main()
            case NewGame.CREATE_NEW: self.create_new_character()