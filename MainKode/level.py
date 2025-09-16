import pygame
import sys
import random
from asset import Asset
from settings import *
from pygame.math import Vector2 as vector
from complete import complete
class Trigger:
    def __init__(self, rect, anim_paths, event_image_path, shared_options, frame_delay=500):
        self.rect = rect
        self.frames = [pygame.image.load(p).convert_alpha() for p in anim_paths]
        self.event_image = pygame.image.load(event_image_path).convert()
        self.frame_delay = frame_delay
        self.timer = 0
        self.idx = 0
        self.ready = False
        self.done = False
        self.shared_options = shared_options
        self.selected = None
        
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_delay:
            self.timer -= self.frame_delay
            self.idx = (self.idx + 1) % len(self.frames)
    
    def draw(self, surf, camera_offset = (0, 0)):
        if not self.done:
            pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
            surf.blit(self.frames[self.idx], pos)

    def check_ready(self, player_rect):
        self.ready = not self.done and player_rect.colliderect(self.rect)

    def trigger(self):
        self.ready = False
        
        if self.shared_options:
            path, is_correct = random.choice(self.shared_options)
            self.shared_options.remove((path, is_correct))

            img = pygame.image.load(path).convert_alpha()
            self.selected = (img, is_correct)
        else:
            self.selected = None

class Player:
    def __init__(self,pos):
        self.frames = [
            pygame.image.load(f'assets/pictures/rat/rat_run{i}.png').convert_alpha()
            for i in range(6)
        ]
        self.anim_index = 0
        self.anim_speed = 100
        self.anim_timer = 0
        self.moving = False
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center = pos)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        v = vector(0, 0)
        if keys[pygame.K_LEFT]: v.x = -1
        if keys[pygame.K_RIGHT]: v.x = +1
        if keys[pygame.K_UP]: v.y = -1
        if keys[pygame.K_DOWN]: v.y = +1

        self.rect.move_ip(v * 5)
        self.moving = (v.x != 0 or v.y != 0)

    def update(self, dt):
        if self.moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.anim_index = (self.anim_index + 1) % len(self.frames)
            self.image = self.frames[self.anim_index]
        else:
            self.anim_index = 0
            self.anim_timer = 0
            self.image = self.frames[0]

    def draw(self, surf, camera_offset = (0, 0)):
        pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        surf.blit(self.image, pos)

class Level:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.level_music = 'assets/music/level.mp3'
        self.event_music = 'assets/music/encounter.mp3'
        pygame.mixer.music.load(self.level_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.asset = Asset(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.clock = pygame.time.Clock()

        self.bg_surf = pygame.image.load('assets/pictures/office.png').convert()
        self.lost_surf = pygame.image.load('assets/pictures/you_lost.png').convert()
        self.won_surf = pygame.image.load('assets/pictures/you_win.png').convert()

        self.lives = 1
        self.heart_surf = pygame.image.load('assets/pictures/heart.png').convert_alpha()
        self.heart_rect = self.heart_surf.get_rect()

        self.win = False

        self.initial_options = [
            ('assets/pictures/event/event_1.png', False),
            ('assets/pictures/event/event_2.png', False),
            ('assets/pictures/event/event_3.png', True),
            ('assets/pictures/event/event_4.png', True),
            ('assets/pictures/event/event_5.png', False),
            ('assets/pictures/event/event_6.png', False),
            ('assets/pictures/event/event_7.png', True),
            ('assets/pictures/event/event_8.png', True),
            ('assets/pictures/event/event_9.png', True),
        ]
        self.picture_options = self.initial_options.copy()

        anim_paths = [
                    'assets/pictures/gorilla/office_gorilla1(1).png',
                    'assets/pictures/gorilla/office_gorilla2(1).png',
                    'assets/pictures/gorilla/office_gorilla3(1).png',
                ]
        event_image = 'assets/pictures/gorilla_event.png'
        rects = [
            pygame.Rect(30, 320, 50, 50),
            pygame.Rect(325, 90, 100, 100),
            pygame.Rect(110, 550, 100, 100),
            pygame.Rect(340, 550, 100, 100),
            pygame.Rect(825, 550, 100, 100),
            pygame.Rect(1055, 550, 100, 100),
            pygame.Rect(980, 320, 100, 100),
            pygame.Rect(1055, 80, 100, 100),
            pygame.Rect(720, 80, 100, 100),
            ]
        self.triggers = [Trigger(r, anim_paths, event_image, self.picture_options) for r in rects]

        self.player = Player((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.camera_offset = vector(0, 0)

        self.in_event = False
        self.active_event= None
        self.game_over = False
        self.space_was_down = False

        self.btn_correct = pygame.Rect(200, 600, 230, 50)
        self.btn_incorrect = pygame.Rect(930, 600, 260, 50)
        self.btn_retry = pygame.Rect(535, 500, 200, 50)
        self.btn_exit = pygame.Rect(535, 600, 200, 50)

    def draw_hearts(self):
        for i in range(self.lives):
            x = 10 + i * (self.heart_rect.width + 5)
            y = 10
            self.display_surface.blit(self.heart_surf, (x, y))

    def reset_game(self):
        self.lives = 3
        self.picture_options = self.initial_options.copy()
        for trig in self.triggers:
            trig.shared_options = self.picture_options
            trig.done = False
            trig.ready = False
            trig.selected = None

        self.in_event = False
        self.active_event = None
        self.game_over = False
        self.win = False
        self.player.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.camera_offset = vector(0, 0)

    def run(self):
        self.running = True
        dt = self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if self.game_over:
                    if self.btn_retry.collidepoint(mx, my):
                        self.reset_game()
                    if (self.game_over or self.win) and self.btn_exit.collidepoint(mx, my):
                        pygame.mixer.music.unload()
                        self.running = False
                        
                        
                
                elif self.win:
                    if self.btn_retry.collidepoint(mx, my):
                        self.reset_game()
                    elif self.btn_exit.collidepoint(mx, my):
                        self.running = False
                        
                    
                elif self.in_event and self.active_event and self.active_event.selected:
                    choice = None
                    if self.btn_correct.collidepoint(mx, my): choice = True
                    elif self.btn_incorrect.collidepoint(mx, my): choice = False

                    if choice is not None:
                        _, is_correct = self.active_event.selected

                        if choice != is_correct:
                            self.lives = max(0, self.lives - 1)
                        self.active_event.done = True

                        if all(t.done for t in self.triggers) and self.lives > 0:
                            self.win = True
                        
                        pygame.mixer.music.fadeout(500)
                        pygame.mixer.music.load(self.level_music)
                        pygame.mixer.music.play(-1)
                        self.in_event = False
                        self.active_event.selected = None
                        self.active_event = None
                        
        if self.lives <= 0:
            self.game_over = True
        
        if self.game_over:
            self.display_surface.blit(self.lost_surf, (0, 0))
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_retry, border_radius = 5)
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_exit, border_radius = 5)
            font = pygame.font.Font('assets/font/Daydream.ttf', 30)
            txt_r = font.render('RETRY', True, (255, 255, 255))
            txt_e = font.render('EXIT', True, (255, 255, 255))
            self.display_surface.blit(txt_r, txt_r.get_rect(center = self.btn_retry.center))
            self.display_surface.blit(txt_e, txt_e.get_rect(center = self.btn_exit.center))
            pygame.display.update()
            return self.running
        
        if self.win:
            complete.level_4_complete = True
            self.display_surface.blit(self.won_surf, (0, 0))
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_retry, border_radius = 5)
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_exit, border_radius = 5)
            font = pygame.font.Font('assets/font/Daydream.ttf', 30)
            txt_r = font.render('RETRY', True, (255, 255, 255))
            txt_e = font.render('EXIT', True, (255, 255, 255))
            self.display_surface.blit(txt_r, txt_r.get_rect(center = self.btn_retry.center))
            self.display_surface.blit(txt_e, txt_e.get_rect(center = self.btn_exit.center))
            pygame.display.update()
            return self.running

        self.display_surface.blit(self.bg_surf, (0, 0))
        self.player.handle_input()
        self.player.update(dt)
        self.player.draw(self.display_surface, self.camera_offset)
        self.draw_hearts()

        for trig in self.triggers:
            trig.update(dt)
            trig.check_ready(self.player.rect)

        keys = pygame.key.get_pressed()
        space = keys[pygame.K_SPACE]
        rising = space and not self.space_was_down

        if self.in_event and self.active_event:
            self.display_surface.blit(self.active_event.event_image, (0, 0))
            if self.active_event.selected:
                pic_surf, is_correct = self.active_event.selected
                offset_x, offset_y = 377, -40
                pic_rect = pic_surf.get_rect(center = (WINDOW_WIDTH // 2 + offset_x , WINDOW_HEIGHT // 2 - 50 + offset_y))
                self.display_surface.blit(pic_surf, pic_rect)
            
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_correct, border_radius = 10)
            pygame.draw.rect(self.display_surface, (0, 200, 0), self.btn_incorrect, border_radius = 10)
            font = pygame.font.Font('assets/font/Daydream.ttf', 30)
            txt_c = font.render('LOVLIGT', True, (255, 255, 255))
            txt_i = font.render('ANHOLDT', True, (255, 255, 255))
            self.display_surface.blit(txt_c, txt_c.get_rect(center = self.btn_correct.center))
            self.display_surface.blit(txt_i, txt_i.get_rect(center = self.btn_incorrect.center))

            if rising:
                self.in_event = False

        else:
            for trig in self.triggers:
                trig.draw(self.display_surface, self.camera_offset)

            for trig in self.triggers:
                if trig.ready and not trig.done:
                    prompt = 'Tryk Mellemrum'
                    ft = pygame.font.Font('assets/font/Daydream.ttf', 20)
                    surf_text = ft.render(prompt, True, (255, 255, 255))
                    rect_text = surf_text.get_rect()

                    world_center_x = trig.rect.x + trig.rect.width // 2
                    rect_text.centerx = world_center_x - self.camera_offset.x
                    rect_text.bottom = (trig.rect.y - self.camera_offset.y) - 10

                    self.display_surface.blit(surf_text, rect_text)

            if rising:
                for trig in self.triggers:
                    if trig.ready and not trig.done:
                        trig.trigger()
                        self.in_event = True
                        self.active_event = trig
                        pygame.mixer.music.fadeout(500)
                        pygame.mixer.music.load(self.event_music)
                        pygame.mixer.music.play(-1)
                        break

        self.draw_hearts()
        self.space_was_down = space
        pygame.display.update()
        return self.running