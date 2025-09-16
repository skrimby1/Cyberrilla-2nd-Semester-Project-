import pygame 
from overworld_sprite import Sprite

class Player(Sprite):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y) 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.movement_speed = 2
        self.keys = pygame.key.get_pressed()
        self.channel = pygame.mixer.Channel(0)  
        self.step_snd = pygame.mixer.Sound("assets/music/step.mp3") 
        self.moving = False
        self.old_x = self.x
        self.old_y = self.y
        self.set_animation([f"assets/pictures/sprites/player/player_{i}.png" for i in range(0, 2)], delay=350)
        self.new_animation = "idle" 
   

    def update(self):
        self.old_x = self.x
        self.old_y = self.y
        self.keys = pygame.key.get_pressed()
        moving = self.keys[pygame.K_a] or self.keys[pygame.K_d] or self.keys[pygame.K_w] or self.keys[pygame.K_s]
        if not moving:
            if not self.new_animation == "idle":
                self.set_animation([f"assets/pictures/sprites/player/player_{i}.png" for i in range(0, 2)], delay=350)
                self.new_animation = "idle"

        if moving and not self.moving:
            self.channel.play(self.step_snd, loops=-1)
            self.moving = True

        elif not moving and self.moving:
            self.channel.stop()
            self.moving = False
        
        if self.keys[pygame.K_a]:
            self.x -= self.movement_speed
            if not self.new_animation == "left":
                if self.keys[pygame.K_a] and self.keys[pygame.K_w]:
                    pass
                else:
                    self.set_animation([f"assets/pictures/sprites/player_left/player_{i}.png" for i in range(0, 1)], delay=350)
                    self.new_animation = "left"
                
        
        if self.keys[pygame.K_d]:
            self.x += self.movement_speed
            if not self.new_animation == "right":
                if self.keys[pygame.K_d] and self.keys[pygame.K_w]:
                    pass
                else:
                    self.set_animation([f"assets/pictures/sprites/player_run/player_{i}.png" for i in range(0, 1)], delay=350)
                    self.new_animation = "right"
            
        if self.keys[pygame.K_w]:
            self.y -= self.movement_speed
            if not self.new_animation == "up":
                self.set_animation([f"assets/pictures/sprites/player_up/player_{i}.png" for i in range(0, 2)], delay=250)
                self.new_animation = "up"
     
        
        if self.keys[pygame.K_s]:
            self.y += self.movement_speed
            if not self.new_animation == "right":
                self.set_animation([f"assets/pictures/sprites/player_run/player_{i}.png" for i in range(0, 1)], delay=350)
                self.new_animation = "right"

             
        self.rect.center = (self.x, self.y)
        
    def get_keys(self):
        return self.keys
       
    
       
         
   