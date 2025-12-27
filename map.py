from settings import *
from scene import *

class Map(Scene):
    def __init__(self, map, display):
        super().__init__(display)
        self.map = map
        self.sprites = pygame.sprite.Group()
        obj_layer = self.map.get_layer_by_name('objects')

        for obj in obj_layer:
            sprite = pygame.sprite.Sprite()
            sprite.image = obj.image
            sprite.rect = sprite.image.get_frect(topleft=(obj.x, obj.y))
            
            if obj.name == 'player':
                self.player = sprite
                self.player_position = {'x': obj.x // TILE_SIZE, 'y': obj.y // TILE_SIZE}

            self.sprites.add(sprite)

    def input(self):
        keys = pygame.key.get_just_pressed()
        move_x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        move_y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        if move_x or move_y:
            desired_x = self.player_position['x'] + move_x
            desired_y = self.player_position['y'] + move_y
            props = self.map.get_tile_properties(desired_x, desired_y, 0)

            if props.get('type') and props.get('type') != 'non_traversable':
                self.player_position['x'] = desired_x
                self.player_position['y'] = desired_y
                self.player.rect.topleft = (self.player_position['x'] * TILE_SIZE, self.player_position['y'] * TILE_SIZE) 

    def update(self):
        self.input()

    def draw(self):
        self.display.fill(DARKBLUE)

        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.display.blit(image, (x * TILE_SIZE, y * TILE_SIZE))

                for sprite in self.sprites.sprites():
                    self.display.blit(sprite.image, sprite.rect)