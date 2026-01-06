from settings import *
from scene import *
from battle import Battle
from data_manager import *
from random import randint

class Map(Scene):
    MAIN = 0
    BATTLE = 1
    DOOR = 2

    def __init__(self, map, display, data, position=None):
        super().__init__(display, data)
        self.map = map
        self.surfaces = self.data['actor_surfaces']
        self.special_tiles = []
        self.sprites = pygame.sprite.Group()
        self.state = Map.MAIN

        obj_layer = self.map.get_layer_by_name('objects')

        for obj in obj_layer:
            sprite = pygame.sprite.Sprite()
            sprite.image = obj.image
            sprite.rect = sprite.image.get_frect(topleft=(obj.x, obj.y))
            
            if obj.name == 'player':
                self.player = sprite
                if position: self.player_position = position
                else: self.player_position = {'x': obj.x // TILE_SIZE, 'y': obj.y // TILE_SIZE}
                self.last_position = self.player_position.copy()
                self.sprites.add(sprite)

            else:
                self.special_tiles.append({
                    'type': obj.type,
                    'x': obj.x // TILE_SIZE,
                    'y': obj.y // TILE_SIZE,
                    'contains': obj.properties['contains']
                    })

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
                

    def handle_tiles(self):
        for tile in self.special_tiles:
            tile_type = tile['type']
            match tile_type:
                case 'door':
                    if tile['x'] == self.player_position['x'] and tile['y'] == self.player_position['y']:
                        return Map(load_map(tile['contains']), self.display, self.data)
                
                case 'enemy':
                    if tile['x'] == self.player_position['x'] and tile['y'] == self.player_position['y']:
                        return Battle(self.display, self.data, tile['contains'])
                    
                    else:
                        tile['x'], tile['y'] = self.pathfind(tile)
                        if tile['x'] == self.player_position['x'] and tile['y'] == self.player_position['y']:
                            self.special_tiles.remove(tile)
                            return Battle(self.display, self.data, tile['contains'], self)

        return self

    def pathfind(self, curr_tile):
        h = abs(curr_tile['x'] - self.player_position['x']) + abs(curr_tile['y'] - self.player_position['y'])
        open = [{'x': curr_tile['x'],
                 'y': curr_tile['y'],
                 'h': h,
                 'g': 0,
                 'f': h
                 }]
        closed = []

        while open:
            search = open[0]
            for tile in open:
                if tile['f'] < search['f'] or tile['f'] == search['f'] and tile['h'] < search['h']:
                    search = tile

            open.remove(search)
            closed.append(search)

            if search['x'] == self.player_position['x'] and search['y'] == self.player_position['y']:
                return
            
            neighbors = [
                {'x': search['x'] + 1, 'y': search['y']},
                {'x': search['x'] -1, 'y': search['y']},
                {'x': search['x'], 'y': search['y'] + 1},
                {'x': search['x'], 'y': search['y'] - 1}
                ]
            for neighbor in neighbors:
                props = self.map.get_tile_properties(neighbor['x'], neighbor['y'], 0)
                if props and props.get('type') != 'non_traversable':


    
    def update(self, dt, event_list):
        self.input(event_list)

        if self.last_position != self.player_position:
            self.last_position = self.player_position.copy()
            return self.handle_tiles()

        if self.state == Map.BATTLE:
            pass

        return self

    def draw(self):
        self.display.fill(DARKBLUE)

        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.display.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

                for sprite in self.sprites.sprites():
                    self.display.blit(sprite.image, sprite.rect)

                for tile in self.special_tiles:
                    if self.surfaces.get(tile['type']):
                        self.display.blit(self.surfaces[tile['type']], (tile['x'] * TILE_SIZE, tile['y'] * TILE_SIZE))

        self.player.rect.topleft = (self.player_position['x'] * TILE_SIZE, self.player_position['y'] * TILE_SIZE)