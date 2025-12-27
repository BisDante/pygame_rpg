from settings import *

def load_map(map_name):
    map_data = pytmx.util_pygame.load_pygame(os.path.join(MAP_FOLDER, map_name))
    return map_data

def save_player_character(player_character, savefile):
    player_dict = vars(player_character)
