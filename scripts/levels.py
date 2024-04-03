import os
import pygame as pg


def build_asset_path(level_number, filename):
    base_path = os.path.join(os.path.dirname(__file__), '..', 'levels', str(level_number), filename)
    return base_path


levels = {
    1: {
        'whole_picture': build_asset_path(1, 'bamboo_bridge.png'),
    },
    2: {
        'whole_picture': build_asset_path(2, 'forest_bridge.png'),
    },
    3: {
        'whole_picture': build_asset_path(3, 'sky_bridge.png'),
    },
    4: {
        'whole_picture': build_asset_path(4, 'castle_bridge.png'),
    },
}


def load_level(level_number, screen_width, screen_height):
    path = levels[level_number]['whole_picture']
    image = pg.image.load(path).convert_alpha()

    scaled_image = pg.transform.scale(image, (screen_width, screen_height))
    return scaled_image

