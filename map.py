from settings import *
from scene import *
from battle import Battle
from data_manager import *
from random import randint

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, surf, traversable, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self._x = x
        self.y = y
        self.traversable = traversable
        self.h = 9999
        self.g = 9999
        self.parent = None

    @property
    def f(self):
        return self.h + self.g
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.left = self.x * TILE_SIZE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.top = self.y * TILE_SIZE 

    def get_position(self):
        return (self.x, self.y)
    
class Player(Tile):
    def __init__(self, x, y, surf, traversable, groups):
        super().__init__(x, y, surf, traversable, groups)
        self.last_position = (self.x, self.y)

class EnemyTile(Tile):
    def __init__(self, x, y, surf, groups, traversable, contains):
        super().__init__(x, y, surf, traversable, groups)
        self.contains = contains

    def trigger(self, display, data, previous_scene):
        return Battle(display, data, previous_scene, self.contains)
    
class DoorTile(Tile):
    def __init__(self, x, y, surf, groups, traversable, contains):
        super().__init__(x, y, surf, traversable, groups)
        self.contains = contains

    def trigger(self, display, data):
        return Map(load_map(self.contains), display, data)
    
        
class Map(Scene):
    MAIN = 0
    BATTLE = 1
    DOOR = 2

    def __init__(self, map, display, data, position=None):
        super().__init__(display, data)
        self.map = map
        self.grid = [[0 for _ in range(map.width)] for _ in range(map.height)]
        self.surfaces = self.data['surfaces']
        self.special_tiles = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.state = Map.MAIN

        floor_layer = self.map.get_layer_by_name('floor')
        obj_layer = self.map.get_layer_by_name('objects')

        for x, y, gid in floor_layer:
            tile = Tile(x, y, map.get_tile_image_by_gid(gid), False if map.get_tile_properties_by_gid(gid).get('type') == 'non_traversable' else True, self.sprites)
            self.grid[y][x] = tile

        for obj in obj_layer:
            if obj.type == 'player':
                self.player = Player(obj.x//TILE_SIZE, obj.y//TILE_SIZE, obj.image, True, self.sprites)

            elif obj.type == 'door':
                DoorTile(obj.x//TILE_SIZE, obj.y//TILE_SIZE, obj.image, (self.sprites, self.special_tiles), True, obj.properties.get('contains'))

            elif obj.type == 'enemy':
                EnemyTile(obj.x//TILE_SIZE, obj.y//TILE_SIZE, obj.image, (self.sprites, self.special_tiles), False, obj.properties.get('contains'))


    def input(self, event_list):
        keys = pygame.key.get_just_pressed()
        move_x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        move_y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        if move_x or move_y:
            desired_x = self.player.x + move_x
            desired_y = self.player.y + move_y
            props = self.map.get_tile_properties(desired_x, desired_y, 0)

            if props and props.get('type') != 'non_traversable':
                self.player.x = desired_x
                self.player.y = desired_y
                

    def handle_tiles(self):
        for tile in self.special_tiles:
            match tile:
                case EnemyTile():
                    if self.player.get_position() == tile.get_position():
                        tile.kill()
                        return tile.trigger(self.display, self.data, self)

                    self.pathfind(tile, self.player)

                    if self.player.get_position() == tile.get_position():
                        tile.kill()
                        return tile.trigger(self.display, self.data, self)

                case DoorTile():
                    if self.player.get_position() == tile.get_position():
                        return tile.trigger(self.display, self.data)

        return self

    def pathfind(self, start, target):
        target_pos = self.grid[int(target.y)][int(target.x)]
        start_pos = self.grid[int(start.y)][int(start.x)]
        open = [start_pos]
        open[0].g = 0
        open[0].h = self.tile_distance(open[0], self.grid[int(target.y)][int(target.x)])
        closed = []

        while open:
            search = open[0]
            for tile in open:
                if tile.f < search.f or tile.f == search.f and tile.g < search.g:
                    search = tile

            open.remove(search)
            closed.append(search)

            if search is target_pos:
                position = self.trace_path(start_pos, target_pos)
                start.x, start.y = position.x, position.y
                for row in range(len(self.grid)):
                    for col in range(len(self.grid[0])):
                        self.grid[row][col].h = 9999
                        self.grid[row][col].g = 9999
                return
            
            neighbors = self.get_neighbors(search)
            for neighbor in neighbors:
                if neighbor in closed:
                    continue

                new_g = search.g + self.tile_distance(search, neighbor)
                if new_g < neighbor.g or not neighbor in open:
                    neighbor.g = new_g
                    neighbor.h = self.tile_distance(neighbor, self.player)
                    neighbor.parent = search

                    if neighbor not in open: open.append(neighbor)

    def tile_distance(self, tile, target):
        return abs(tile.x - target.x) + abs(tile.y - target.y)
    
    def get_neighbors(self, tile):
        neighbors = []
        for i in range(3):
            for j in range(3):
                x_pos = tile.x + j - 1
                y_pos = tile.y + i - 1
                props = self.map.get_tile_properties(x_pos, y_pos, 0) if x_pos > 0 and y_pos > 0 and x_pos < self.map.width and y_pos < self.map.height else None
                if abs(i - j) != 1 or not props or props.get('type') == 'non_traversable':
                    continue

                neighbors.append(self.grid[y_pos][x_pos])
        
        return neighbors
    
    def trace_path(self, start_pos, target_pos):
        current = target_pos
        while not current.parent is start_pos:
            current = current.parent
        
        return current

    def update(self, dt, event_list):
        self.input(event_list)

        if self.player.last_position != self.player.get_position():
            self.player.last_position = self.player.get_position()
            return self.handle_tiles()

        if self.state == Map.BATTLE:
            pass

        return self

    def draw(self):
        self.display.fill(DARKBLUE)
        self.sprites.draw(self.display)