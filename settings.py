import pygame
import pytmx
import sys
import os
import json
import copy

# display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# folder paths
FONT_FOLDER = os.path.join('data', 'fonts')
MAP_FOLDER = os.path.join('data', 'maps')
ACTOR_FOLDER = os.path.join('images', 'actors')
OTHER_FOLDER = os.path.join('images', 'other')
SAVE_FOLDER = os.path.join('data', 'save')

# game settings
PARTY_SIZE = 4
CONFIRM = [pygame.K_RETURN, pygame.K_SPACE]
CANCEL = [pygame.K_BACKSPACE, pygame.K_ESCAPE]

# colors
DARKBLUE = (6, 57, 112)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
GOTHIC = os.path.join(FONT_FOLDER, 'OldLondon.ttf')
SELECT_ICON = pygame.image.load(os.path.join(OTHER_FOLDER, 'select.png'))
PLAYER_ICON = pygame.image.load(os.path.join(ACTOR_FOLDER, 'player.png'))