from settings import *
from scene import *
from actor import PlayerCharacter
from data_manager import *
from map import Map

class NewGame(Scene):
    ROWS = 2
    COLS = 2

    MAIN = 0
    CREATE_NEW = 1
    START = 2

    def __init__(self, display, data):
        super().__init__(display, data)
        self.data = data
        self.party = data['characters'] 
        self.state = NewGame.MAIN
        self.gothic_font = pygame.font.Font(GOTHIC, 48)
        self.normal_font = pygame.font.Font(None, 36)
        self.main_index = {'x': 0, 'y': 0}

        self.give_id = 0
        self.max_points = self.remaining_points = 20
        self.default_character = {
            'id': None,
            'name': 'Name',
            'level': 1,
            'experience': 0,
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
        self.warning = 0
        self.complete_party = False
        self.type_timer = 0
        self.type_limit = 200

    def main(self):
        self.display.fill(WHITE)
        title = self.gothic_font.render('Character Creation', False, BLACK)
        title_rect = title.get_frect(center=(SCREEN_WIDTH / 2, 75))
        self.display.blit(title, title_rect)

        w, h = 300, 175
        side_margin = 25
        top_margin = 10
        bottom_margin = 75
        div = pygame.FRect(side_margin,
                           title_rect.bottom + top_margin, SCREEN_WIDTH - 2 * side_margin,
                           SCREEN_HEIGHT - title_rect.bottom - bottom_margin)

        for row in range(NewGame.ROWS):
            for col in range(NewGame.COLS):
                rect = pygame.FRect(0, 0, w, h)
                rect.center = (div.left + div.width/4 * (col * 2 + 1), div.top + div.height/4 * (row * 2 + 1))
                pygame.draw.rect(self.display, BLACK, rect, 4, 0)

                character_index = col + row * 2
                if not self.party[character_index]:
                    name = self.gothic_font.render('Empty', False, BLACK)
                    name_rect = name.get_frect(center=rect.center)
                    self.display.blit(name, name_rect)

                else:
                    player_icon = PLAYER_ICON.copy()
                    player_icon = pygame.transform.scale_by(player_icon, 2)
                    player_icon_rect = player_icon.get_frect(center=(rect.centerx, rect.centery-20))
                    self.display.blit(player_icon, player_icon_rect)

                    name = self.normal_font.render(f'{self.party[character_index]['name']}', False, BLACK)
                    name_rect = name.get_frect(midtop=(rect.centerx, rect.centery + 20))
                    self.display.blit(name, name_rect)

                if self.main_index['x'] == col and self.main_index['y'] == row:
                    select_icon_rect = SELECT_ICON.get_frect(center=(rect.left - side_margin, rect.centery))
                    self.display.blit(SELECT_ICON, select_icon_rect)

        if self.complete_party:
            text = self.gothic_font.render('Start Game', False, BLACK)
            rect = text.get_frect(midtop=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8 * 7))
            self.display.blit(text, rect)

            if self.main_index['y'] >= NewGame.ROWS:
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

            case 2:
                text = self.normal_font.render('You can\'t repeat the name', False, BLACK)
                rect = text.get_frect(midtop=(SCREEN_WIDTH/2, attrib_rect.bottom + 10))
                self.display.blit(text, rect)

            case _:
                pass

    def input(self, event_list):
        current_attrib = self.attribute_list[self.attribute_index]
        for event in event_list:
            if event.type == pygame.KEYDOWN and self.state == NewGame.CREATE_NEW and isinstance(self.character[current_attrib], str):
                if event.key == pygame.K_BACKSPACE:
                    self.character[current_attrib] = self.character[current_attrib][:-1]

                elif event.unicode.isalnum() or event.unicode == ' ':
                    self.character[current_attrib] += event.unicode 

        keys = pygame.key.get_just_pressed()

        if self.state == NewGame.MAIN:
            self.main_index['x'] = (self.main_index['x'] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % NewGame.COLS
            if not self.complete_party:
                self.main_index['y'] = (self.main_index['y'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % NewGame.ROWS
            else:
                self.main_index['y'] = (self.main_index['y'] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % (NewGame.ROWS+1)

            if keys[pygame.K_RETURN]:
                if self.main_index['y'] >= NewGame.ROWS:
                    self.state = NewGame.START

                else:
                    character_index = self.main_index['x'] + self.main_index['y'] * 2
                    
                    if self.party[character_index]:
                        self.remaining_points = 0
                        self.character = self.party[character_index]

                    self.state = NewGame.CREATE_NEW

        elif self.state == NewGame.CREATE_NEW:
            self.attribute_index = (self.attribute_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.attribute_list)
            
            change_value = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            if change_value > 0 and self.remaining_points <= 0 or change_value < 0 and self.remaining_points >= self.max_points:
                change_value = 0

            if (current_attrib in ['max_hp', 'max_mana'] and not
                self.character[current_attrib] + change_value * 5 <
                self.default_character[current_attrib]):

                self.character[current_attrib] += change_value * 5
                self.remaining_points -= change_value
            
            elif (not current_attrib == 'name' and not
                  self.character[current_attrib] + change_value <
                  self.default_character[current_attrib]):
                
                self.character[current_attrib] += change_value
                self.remaining_points -= change_value

            if keys[pygame.K_RETURN]:
                if self.remaining_points > 0:
                    self.warning = 1

                elif self.character['name'] in [character['name'] for character in self.party if character and character['id'] != self.character['id']]:
                    self.warning = 2

                else:
                    if not self.character['id']:
                        self.character['id'] = self.give_id
                        self.give_id += 1

                    self.add_character(self.character.copy(), self.main_index['x'] + self.main_index['y'] * 2)
                    self.remaining_points = self.max_points
                    self.character = self.default_character.copy()
                    self.warning = False

                    self.complete_party = True
                    for slot in self.party:
                        if not slot:
                            self.complete_party = False
                            break

                    self.state = NewGame.MAIN

    def add_character(self, character, slot):
        self.party[slot] = character

    def start_game(self):
        create_save_data(self.party)
        for i in range(len(self.party)):
            self.party[i] = PlayerCharacter(self.party[i])

        return Map(load_map('map1.tmx'), self.display)

    def update(self, dt, event_list):
        self.input(event_list)
        
        match self.state:
            case NewGame.START: return self.start_game()

        return self

    def draw(self):
        match self.state:
            case NewGame.MAIN: self.main()
            case NewGame.CREATE_NEW: self.create_new_character()