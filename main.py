import pygame as pg
import sys

pg.init()

screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Platformer')

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.flip()

pg.quit()
sys.exit()