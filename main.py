import pygame as pg
import sys
from scripts.player import Player

pg.init()

screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Platformer')

player = Player(100, 100)
all_sprites = pg.sprite.Group(player)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pg.display.flip()

pg.quit()
sys.exit()