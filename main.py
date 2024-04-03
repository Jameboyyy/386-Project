import pygame as pg
import sys
from scripts.player import Player
from scripts.levels import load_level
from scripts.enemy import Enemy

pg.init()
pg.mixer.init()

pg.mixer.music.load('./assets/music/battle-of-the-dragons-8037.mp3')
pg.mixer.music.play(-1)

screen_width, screen_height = 800, 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Platformer')

# Initialize and position player
player = Player(screen_width, screen_height)  # Temp position
player.rect.x = 0  # Left side of the screen
player.rect.y = (screen_height - player.rect.height) // 2

# Initialize and position enemy
enemy = Enemy(screen_width, screen_height)  # Temp position
enemy.rect.x = screen_width - enemy.rect.width  # Right side of the screen
enemy.rect.y = player.rect.y

# Add player and enemy to their respective sprite groups
all_sprites = pg.sprite.Group(player)
enemy_group = pg.sprite.Group(enemy)

# Load the level background
current_level = 1
level_background = load_level(current_level, screen_width, screen_height)

# Main game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    all_sprites.update()
    enemy_group.update()

    if pg.sprite.collide_rect(player, enemy):
        # Check if player is attacking and enemy is not shielding
        if player.is_attacking() and player.can_attack() and not enemy.is_shielding():
            enemy.take_damage(1)
            print(f"Enemy took damage! Health: {enemy.health}")
            if enemy.health <= 0:
                print("Enemy defeated!")

        # Check if enemy is attacking and player is not shielding
        if enemy.is_attacking() and not player.is_shielding():
            player.take_damage(1)
            print(f"Player took damage! Health: {player.health}")
            if player.health <= 0:
                print("Player defeated!")

    screen.blit(level_background, (0, 0))
    all_sprites.draw(screen)
    enemy_group.draw(screen)
    
    pg.display.flip()

pg.mixer.music.stop()
pg.quit()
sys.exit()
