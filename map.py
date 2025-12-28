from settings import *
from scene import *
from battle import Battle
from data_manager import *

class Map(Scene):
    def __init__(self, map, display, data):
        super().__init__(display, data)
        self.map = map
        self.special_tiles = []
        self.sprites = pygame.sprite.Group()
        obj_layer = self.map.get_layer_by_name('objects')

        for obj in obj_layer:
            sprite = pygame.sprite.Sprite()
            sprite.image = obj.image
            sprite.rect = sprite.image.get_frect(topleft=(obj.x, obj.y))
            
            if obj.name == 'player':
                self.player = sprite
                self.player_position = {'x': obj.x // TILE_SIZE, 'y': obj.y // TILE_SIZE}

            else:
                self.special_tiles.append({
                    'type': obj.type,
                    'x': obj.x // TILE_SIZE,
                    'y': obj.y // TILE_SIZE,
                    'contains': obj.properties['contains']
                    })

            self.sprites.add(sprite)

    def input(self, event_list):
        keys = pygame.key.get_just_pressed()
        move_x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        move_y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        if move_x or move_y:
            desired_x = self.player_position['x'] + move_x
            desired_y = self.player_position['y'] + move_y
            props = self.map.get_tile_properties(desired_x, desired_y, 0)

            if props and props.get('type') != 'non_traversable':
                self.player_position['x'] = desired_x
                self.player_position['y'] = desired_y
                self.player.rect.topleft = (self.player_position['x'] * TILE_SIZE, self.player_position['y'] * TILE_SIZE)
                
                return self.handle_tiles()
        
        return self

    def handle_tiles(self):
        for tile in self.special_tiles:
            if tile['x'] == self.player_position['x'] and tile['y'] == self.player_position['y']:
                if tile['type'] == 'door':
                    return Map(load_map(tile['contains']), self.display, self.data)
                
                elif tile['type'] == 'enemy':
                    return Battle(self.display, self.data, tile['contains'])

        return self

    def update(self, dt, event_list):
        return self.input(event_list)

    def draw(self):
        self.display.fill(DARKBLUE)

        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.display.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

                for sprite in self.sprites.sprites():
                    self.display.blit(sprite.image, sprite.rect)