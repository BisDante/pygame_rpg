from settings import *
from scene import Scene
from data_manager import *
from actor import *
from random import randint

class Battle(Scene):
    MAIN = 0
    SELECT_ENEMY = 1
    PLAYER_TURN = 2
    ENEMY_TURN = 3
    MAGIC = 4
    DEFEND = 5
    RUN = 6
    WIN = 7
    LOSE = 8

    def __init__(self, display, data, previous_scene, encounter_name='bats'):
        super().__init__(display, data)
        
        # for helping display stuff
        self.normal_font = pygame.font.Font(None, 36)
        self.MAX_COLS = 4

        self.hp_height = 6
        self.hp_width = 100

        self.ENEMY_DIV = pygame.Rect(0, 0, SCREEN_WIDTH/100*80, SCREEN_HEIGHT/100*70)
        self.ENEMY_DIV.midtop = (SCREEN_WIDTH/2, 0)

        self.MAIN_DIV = pygame.Rect(0, 0, SCREEN_WIDTH/100*90, SCREEN_HEIGHT/100*30)
        self.MAIN_DIV.midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT)

        self.NAME_DATA_DIV = pygame.Rect(0, 0, self.MAIN_DIV.width/2, self.MAIN_DIV.height/100*95)
        self.NAME_DATA_DIV.midleft = self.MAIN_DIV.midleft + pygame.Vector2(20, 0)

        # actual data
        self.previous_scene = previous_scene
        self.party = self.data['characters']
        self.enemies = self.load_encounter(encounter_name)
        self.queue = sorted(self.party + self.enemies, key= lambda x: x.speed, reverse=True)
        self.turn_index = 0

        self.active_actor = self.queue[self.turn_index]
        self.state = Battle.MAIN if isinstance(self.active_actor, PlayerCharacter) else Battle.ENEMY_TURN

        self.action_index = 0
        self.select_enemy_index = 0
        self.actions = ['ATTACK', 'MAGIC', 'DEFEND', 'RUN']
        self.action_to_state = {
                'ATTACK': Battle.SELECT_ENEMY,
                'MAGIC': Battle.MAGIC,
                'DEFEND': Battle.DEFEND,
                'RUN': Battle.RUN
        }

        self.blackboard = {
            'turn_number': 0,
            'players_alive': 0,
            'enemies_alive': 0,
        }

        self.surfaces = {}
        for enemy in self.enemies:
            self.surfaces[enemy.name] = data['surfaces'][enemy.name]

        self.enemy_positions = self.set_enemy_positions()

    def load_encounter(self, encounter_name):
        ENCOUNTER_LIST = os.path.join('data', 'encounters.json')
        ENEMY_LIST = os.path.join('data', 'enemies.json')
        
        with open(ENCOUNTER_LIST, 'r') as rf:
            encounter_enemies = json.load(rf)[encounter_name]

        with open(ENEMY_LIST, 'r') as rf2:
            enemy_list = json.load(rf2)

        enemy_data = [enemy_list[enemy] for enemy in encounter_enemies]
        encounter=[Enemy(enemy) for enemy in enemy_data]
        return encounter

    def set_enemy_positions(self):
        if len(self.enemies) <= 1:
            surf = self.surfaces[self.enemies[0].name]
            rect = surf.get_frect(center=(self.ENEMY_DIV.centerx, self.ENEMY_DIV.centery))
            return [rect]
        
        else:
            enemy_positions = []
            x_increment = self.ENEMY_DIV.width/len(self.enemies)
            for i, enemy in enumerate(self.enemies):
                surf = self.surfaces[enemy.name]
                rect = surf.get_frect(center=(self.ENEMY_DIV.left + x_increment * (i+1) - x_increment/2, self.ENEMY_DIV.centery))
                enemy_positions.append(rect)
            
            return enemy_positions
        
        # else:
            #  rows = len(self.enemies) // self.MAX_COLS + 1 
            #  enemy_positions = []
            #  x_increment = self.ENEMY_DIV.width/len(self.enemies)
            #  y_increment = None

            #  for i, enemy in enumerate(self.enemies):
            #     surf = self.surfaces[enemy.name]
            #     rect = surf.get_frect(center=(self.ENEMY_DIV.left + x_increment * (i+1) - x_increment/2, self.ENEMY_DIV.centery))
            #     enemy_positions.append(rect)
            pass

    def input(self, event_list):
        keys=pygame.key.get_just_pressed()
        if self.state == Battle.MAIN:
            self.action_index = (self.action_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.actions)
            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.state = self.action_to_state[self.actions[self.action_index]]

        elif self.state == Battle.SELECT_ENEMY:
            left_right = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            self.select_enemy_index = (self.select_enemy_index + left_right) %len(self.enemies)

            while self.enemies[self.select_enemy_index].hp <= 0:
                self.select_enemy_index = (self.select_enemy_index + left_right) %len(self.enemies)

            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
                self.state = self.PLAYER_TURN

    def update(self, dt, event_list):
        self.input(event_list)

        if self.state == Battle.PLAYER_TURN:
            self.player_turn()

        elif self.state == Battle.ENEMY_TURN:
            self.enemy_turn()

        elif self.state == Battle.WIN:
            return self.win()

        return self
    
    def player_turn(self):
        target = self.enemies[self.select_enemy_index]
        target.hp -= self.active_actor.attack
        
        dead_before_index = 0
        enemies_alive = False
        i = 0
        while i < len(self.queue):
            if self.queue[i].hp <= 0:
                if i <= self.turn_index: dead_before_index += 1
                self.queue.pop(i)
                i = -1
            elif isinstance(self.queue[i], Enemy): enemies_alive = True
            i += 1

        if enemies_alive:
            self.select_enemy_index = 0
            while self.enemies[self.select_enemy_index].hp <= 0:
                self.select_enemy_index = (self.select_enemy_index + 1) % len(self.enemies)

            self.turn_index = (self.turn_index + 1) % len(self.queue) - dead_before_index
            self.active_actor = self.queue[self.turn_index]
            if isinstance(self.active_actor, PlayerCharacter): self.state = Battle.MAIN
            else: self.state = Battle.ENEMY_TURN

        else:
            self.state = Battle.WIN

    def enemy_turn(self):
        while isinstance(self.active_actor, Enemy):
            valid_targets = [character for character in self.party if character.hp > 0]
            target = valid_targets[randint(0, len(valid_targets)-1)]
            target.hp -= self.active_actor.attack

            dead_before_index = 0
            players_alive = False
            i = 0
            while i < len(self.queue):
                if self.queue[i].hp <= 0:
                    if i <= self.turn_index: dead_before_index += 1
                    self.queue.pop(i)
                    i = -1
                elif isinstance(self.queue[i], PlayerCharacter): players_alive = True
                i += 1

            self.turn_index = (self.turn_index + 1) % len(self.queue) - dead_before_index
            self.active_actor = self.queue[self.turn_index]

        if not players_alive: self.statee = Battle.LOSE
        else: self.state = Battle.MAIN

    def main(self):
        self.display.fill(WHITE)
        pygame.draw.rect(self.display, BLACK, self.MAIN_DIV, 4, 0)
        pygame.draw.rect(self.display, RED, self.NAME_DATA_DIV, 4, 0)

        for i, enemy in enumerate(self.enemies):
            if enemy.hp > 0:
                self.display.blit(self.surfaces[enemy.name], self.enemy_positions[i])
                
                hp_rect = pygame.FRect(0, 0, self.hp_width, self.hp_height)
                hp_rect.midtop = self.enemy_positions[i].midbottom
                pygame.draw.rect(self.display, RED, hp_rect, 0, 0)
                
                hp_left_rect = pygame.FRect(0, 0, self.hp_width/enemy.max_hp*enemy.hp, self.hp_height)
                hp_left_rect.midleft = hp_rect.midleft
                pygame.draw.rect(self.display, GREEN, hp_left_rect, 0, 0)
        
        y_increment = self.NAME_DATA_DIV.height/len(self.party)
        for i, character in enumerate(self.party):
            color = RED if self.party[i] is self.queue[self.turn_index] else BLACK
            name = self.normal_font.render(character.name, False, color)
            name_rect = name.get_frect(midleft=(self.NAME_DATA_DIV.left, self.NAME_DATA_DIV.top + y_increment * (i+1) - y_increment/2))
            self.display.blit(name, name_rect)

            hp_mp = self.normal_font.render(f'HP: {character.hp}/{character.max_hp} MN: {character.mana}/{character.max_mana}', False, color)
            hp_mp_rect = hp_mp.get_frect(midleft=(name_rect.midright + pygame.Vector2(30, 0)))
            self.display.blit(hp_mp, hp_mp_rect)

        for i, action in enumerate(self.actions):
            color = RED if action == self.actions[self.action_index] else BLACK
            text = self.normal_font.render(action, False, color)
            rect = text.get_frect(center=(self.NAME_DATA_DIV.right + (self.MAIN_DIV.right - self.NAME_DATA_DIV.right)/2, self.NAME_DATA_DIV.top + y_increment * (i+1) - y_increment/2))
            self.display.blit(text, rect)

    def select_enemy(self):
        self.main()
        for i, position in enumerate(self.enemy_positions):
            if i == self.select_enemy_index:
                rect = SELECT_ICON.get_frect(midright=(position.left, position.centery))
                self.display.blit(SELECT_ICON, rect)

    def win_screen(self):
        pass

    def win(self):
        return self.previous_scene

    def draw(self):
        match self.state:
            case Battle.MAIN: self.main()
            case Battle.SELECT_ENEMY: self.select_enemy()
            case Battle.WIN: self.win_screen()