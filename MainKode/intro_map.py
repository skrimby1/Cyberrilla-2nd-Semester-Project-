import pygame
from overworld_player import Player
from overworld_sprite import sprites, Sprite
from Overworld import Overworld
from button import Button
from asset1 import Asset

class map_intro:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.clear_color = (0, 0, 0)
        self.game_assets()
        self.next_scene = None
    
    def game_assets(self):
        sprites.clear() 
        self.player = Player("assets/pictures/sprites/player/player_0.png", 480, 250)
        self.game_map = pygame.image.load("assets/pictures/hq_map.png")
        self.game_map_rect = self.game_map.get_rect(center=(640, 360))
        self.menu_rect = pygame.Rect(300, 670, 250, 150)
        self.back_snd = pygame.mixer.Sound("assets/music/back_snd.mp3")
        self.wasd = pygame.image.load("assets/pictures/wasd.png")
        self.wasd_rect = self.wasd.get_rect(center=(1030, 370))
        pygame.mixer.music.load("assets/music/overworld.mp3")
        pygame.display.flip()
    def collision_detection(self):
        keys = self.player.get_keys()
        if self.menu_rect.colliderect(self.player.rect):
            self.player.x = self.player.old_x
            self.player.y = self.player.old_y
            pygame.mixer.music.unload()
            self.running = False
            self.next_scene = "overworld"
                
    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0), self.menu_rect)
        self.screen.fill(self.clear_color) 
        self.screen.blit(self.game_map, self.game_map_rect)
        self.screen.blit(self.wasd, self.wasd_rect) 
        Asset.img(self, "assets/pictures/arrow.png", 450, 650, self.screen)
        for s in sprites: 
            s.draw(self.screen)
    def run(self):
        pygame.mixer.music.play(-1, 0, 5000)  
        while self.running:
            self.player_rect = self.player.rect
            self.mouse_pos = pygame.mouse.get_pos()
            self.collision_detection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.update()
            self.draw()
           
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    intro_map = map_intro()
    intro_map.run()
    