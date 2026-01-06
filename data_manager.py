from settings import *
from actor import *

def load_map(map_name):
    map_data = pytmx.util_pygame.load_pygame(os.path.join(MAP_FOLDER, map_name))
    return map_data

def load_game(name='save.json'):
    data = {}
    path = os.path.join(SAVE_FOLDER, name)
    with open(path, 'r') as rf:
        read = json.load(rf)
    
    for key in read.keys():
        data[key] = read[key]
    data['characters'] = [PlayerCharacter(attributes) for attributes in data['characters']]
    data['surfaces'] = load_surfaces()
    return data

def load_surfaces():
    surfaces = {}
        
    for root, dirs, files in os.walk('images'):
        for filename in files:
            new_surf = pygame.image.load(os.path.join(root, filename)).convert_alpha()
            surfaces[filename.split('.')[0]] = new_surf
       
    return surfaces

def create_encounter():
    pass

def create_enemy():
    pass

def create_save_data(character_list, name='save.json'):
    path = os.path.join(SAVE_FOLDER, name)
    
    new_save = START_SAVE.copy()
    new_save['characters'] = character_list
    with open (path, 'w') as wf:
        json.dump(new_save, wf, indent=2)

if __name__ == '__main__':
    load_surfaces()