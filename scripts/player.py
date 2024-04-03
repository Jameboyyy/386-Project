import os
import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.load_frames()
        self.state = 'idle'
        self.current_frame = 0
        self.last_update_time = pg.time.get_ticks()
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect()
        self.velocity = pg.math.Vector2(0, 0)
        self.set_initial_position(screen_width, screen_height)
        self.acceleration = pg.math.Vector2(0, 0.15)
        self.speed = 1
        self.jump_strength = -5
        self.on_ground = True
        self.health = 10
        self.attack_cooldown = 500
        self.last_attack_time = pg.time.get_ticks()

    def is_attacking(self):
        return self.state == 'fight'
    
    def is_shielding(self):
        return self.state == 'shield'

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Entity defeated.")

    def can_attack(self):
        if pg.time.get_ticks() - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = pg.time.get_ticks()
            return True
        return False

    def set_initial_position(self, screen_width, screen_height):
        self.rect.x = screen_width / 2 - self.rect.width / 2
        self.rect.y = screen_height  - self.rect.height - 50

    def load_frames(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'player')
        self.animations = {
            'idle': self.load_animation(os.path.join(base_path, 'Idle.png'), 6),
            'fight': self.load_animation(os.path.join(base_path, 'Attack_3.png'), 4),
            'shield': self.load_animation(os.path.join(base_path, 'Shield.png'), 2),
            'die': self.load_animation(os.path.join(base_path, 'Dead.png'), 3),
            'run': self.load_animation(os.path.join(base_path, 'Run.png'), 8 )
        }

    def load_animation(self, path, frame_count):
        sprite_sheet_image = pg.image.load(path).convert_alpha()
        frame_width = sprite_sheet_image.get_width() // frame_count
        return [sprite_sheet_image.subsurface(pg.Rect(i * frame_width, 0, frame_width, sprite_sheet_image.get_height())) for i in range(frame_count)]

    def update(self):
        self.handle_keys()
        self.rect.x += self.velocity.x
        if not self.on_ground:
            self.velocity.y += self.acceleration.y
        self.rect.y += self.velocity.y
        self.check_collisions()
        now = pg.time.get_ticks()
        if now - self.last_update_time > 100:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]

    def handle_keys(self):
        keys = pg.key.get_pressed()
        self.velocity.x = 0
        if keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.state = 'run'
        elif keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.state = 'run'
        elif keys[pg.K_SPACE]:
            self.state = 'fight'
        elif keys[pg.K_s]:
            self.state = 'shield'
        if not keys[pg.K_LEFT] and not keys[pg.K_RIGHT] and not keys[pg.K_SPACE] and not keys[pg.K_s]:
            self.state = 'idle'

    def check_collisions(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.velocity.y = 0
            self.rect.top = 0
        if self.rect.bottom >= 365:
            self.velocity.y = 0
            self.rect.bottom = 365
            self.on_ground = True
        else:
            self.on_ground = False
