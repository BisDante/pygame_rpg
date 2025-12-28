from settings import *
from actor import Enemy

def load_map(map_name):
    map_data = pytmx.util_pygame.load_pygame(os.path.join(MAP_FOLDER, map_name))
    return map_data

def load_game(data, name='save.json'):
    path = os.path.join(SAVE_FOLDER, name)
    with open(path, 'r') as rf:
        read = json.load(rf)
    
    for key in read.keys():
            data[key] = read[key]

def load_enemy(name='bat'):
    with open(os.path.join('data', 'enemies', 'enemies.json')) as rf:
        read = json.load(rf)
    
    for enemy in read:
        if enemy['name'] == name: return Enemy(enemy)

def load_encounter(name='bats'):
    with open(os.path.join('data', 'enemies', 'encounters.json')) as rf:
        read = json.load(rf)
    
    for encounter in read:
        if encounter['name'] == name:
            enemies = [load_enemy(enemy_name) for enemy_name in encounter['enemies']]
            return enemies

def load_actor_surfaces(data):
    for root, _, files in os.walk(ACTOR_FOLDER):
        for file in files:
            new_surf = pygame.image.load(os.path.join(root, file)).convert_alpha()
            data['actor_surfaces'][file.split('.')[0]] = new_surf

def create_save_data(character_list, name='save.json'):
    path = os.path.join(SAVE_FOLDER, name)
    
    new_save = START_SAVE.copy()
    new_save['characters'] = character_list
    with open (path, 'w') as wf:
        json.dump(new_save, wf, indent=2)