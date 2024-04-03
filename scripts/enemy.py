import pygame as pg
import os

class Enemy(pg.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.load_frames()
        self.state = 'shield'
        self.current_frame = 0
        self.behavior_timer = pg.time.get_ticks()
        self.shield_duration = 2000  
        self.attack_duration = 2000  
        self.last_update_time = pg.time.get_ticks()
        self.image = self.animations[self.state][self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - self.rect.width  
        self.rect.y = screen_height - self.rect.height  
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = 1
        self.health = 10
        

    def is_attacking(self):
        return self.state == 'fight'
    
    def is_shielding(self):
        return self.state == 'shield'

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
            print("Entity defeated.")

    def die(self):
        if self.state != 'die':
            self.state = 'die'
            self.velocity = pg.Vector2(0, 0)
            self.current_frame = 0
            self.last_update_time = pg.time.get_ticks()
        

    def load_frames(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'enemy')
        self.animations = {
            'idle': self.load_animation(os.path.join(base_path, 'Idle.png'), 6),
            'attack': self.load_animation(os.path.join(base_path, 'Attack_3.png'), 4),
            'shield': self.load_animation(os.path.join(base_path, 'Shield.png'), 4),
            'die': self.load_animation(os.path.join(base_path, 'Dead.png'),4 )
        }

    def load_animation(self, path, frame_count):
        sprite_sheet_image = pg.image.load(path).convert_alpha()
        frame_width = sprite_sheet_image.get_width() // frame_count
        frames = [sprite_sheet_image.subsurface(pg.Rect(i * frame_width, 0, frame_width, sprite_sheet_image.get_height())) for i in range(frame_count)]
       
        return [pg.transform.flip(frame, True, False) for frame in frames]

    def update(self):
        now = pg.time.get_ticks()

       
        if self.state == 'die':
            
            if self.current_frame < len(self.animations[self.state]) - 1:  
                if now - self.last_update_time > 100: 
                    self.last_update_time = now
                    self.current_frame += 1  
           
            self.image = self.animations[self.state][self.current_frame]
            return  

      
        if self.state == 'shield' and now - self.behavior_timer > self.shield_duration:
            self.change_state('attack')
            self.behavior_timer = now
        elif self.state == 'attack' and now - self.behavior_timer > self.attack_duration:
            self.change_state('shield')
            self.behavior_timer = now
        
      
        if now - self.last_update_time > 100:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]


    def change_state(self, new_state):
        if new_state in self.animations:
            self.state = new_state
            self.current_frame = 0  
