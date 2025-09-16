import pygame, sys
from button import Button
import pygame.display
import os
import requests

class Login:
    def get_font(self, size):  
        return pygame.font.Font("assets/font/overworld_font.ttf", size)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.login_box = pygame.image.load("assets/pictures/loginbox.png")
        self.login_snd = pygame.mixer.Sound("assets/music/login.mp3")
        self.login_error_snd = pygame.mixer.Sound("assets/music/login_error.mp3")
        self.login_screen = [pygame.image.load(f"assets/pictures/sprites/login_background/login_screen_{i}.png") for i in range (2)]
        self.login_music = pygame.mixer.music.load("assets/music/login_theme.mp3")
        pygame.mixer.music.play(-1)
        self.login_btn_img = pygame.image.load("assets/pictures/login_btn.png")
        self.snd_on = pygame.image.load("assets/pictures/snd_on.png")
        self.snd_off = pygame.image.load("assets/pictures/snd_off.png")
        pygame.display.set_caption("Cyberrilla")
        self.snd_btn = Button(image=self.snd_on, text_input=None, pos=(1200, 75), font=self.get_font(50), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        self.login_button_hov = pygame.image.load("assets/pictures/login_btn_1.png")
        self.menu_font = self.get_font(45)
        pygame.display.set_icon(pygame.image.load("assets/pictures/window_icon.png"))
        self.font ="assets/font/menufont.otf"
        self.login_success = False
        self.user_text1 = ''
        self.user_text2 = '' 
        self.music_state = True
        self.username_state = False
        self.password_state = False
        self.cred_error = False
        self.rect_color_active = pygame.Color('azure3')
        self.rect_color_pas = pygame.Color('gray15')
        self.color1 = self.rect_color_pas
        self.color2 = self.rect_color_pas
    def login_auth(self):
        if self.login_button.checkForInput(self.menu_mouse_pos):
                    self.url = "https://cyberrila.com/api/login"
                    try:
                        self.response = requests.post(self.url, json={"username": self.user_text1, "password": self.user_text2}, allow_redirects=False)
                    except requests.exceptions.RequestException as e:
                        print(f"Error: connecting to server {e}")
                        self.login_error_snd.play()
                        return
                    
                    if self.response.status_code == 200: 
                        os.environ["USERNAME"] = self.user_text1 
                        self.login_success = True
                        self.login_snd.play()
                        pygame.mixer.music.stop()
                        self.cred_error = False
                    else:
                        self.login_error_snd.play()
                        self.cred_error = True
                        

    def login_input(self):
        self.username_rect = pygame.Rect(420, 210, 385, 70)
        self.password_rect = pygame.Rect(420, 405, 385, 70)
        pygame.draw.rect(self.screen, self.color1, self.username_rect, 5)
        text_surface1 = self.menu_font.render(self.user_text1, True, (255, 255, 255))
        self.screen.blit(text_surface1, (self.username_rect.x + 10, self.username_rect.y + 20))
        self.username_rect.w = max(400, text_surface1.get_width() + 10)
        self.password_font = pygame.font.Font("assets/font/password-dots.otf", 35)
        pygame.draw.rect(self.screen, self.color2, self.password_rect, 5)
        text_surface2 = self.password_font.render(self.user_text2, True, (255, 255, 255))
        self.screen.blit(text_surface2, (self.password_rect.x + 10, self.password_rect.y + 20))
        self.password_rect.w = max(400, text_surface2.get_width() + 10)
        self.color1 = self.rect_color_active if self.username_state else self.rect_color_pas
        self.color2 = self.rect_color_active if self.password_state else self.rect_color_pas
    def handle_events(self):
        self.menu_mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.username_state = self.username_rect.collidepoint(event.pos)
                self.password_state = self.password_rect.collidepoint(event.pos)

                if self.snd_btn.checkForInput(self.menu_mouse_pos):
                    self.music_state = not self.music_state
                    if self.music_state:
                        self.snd_btn.image = self.snd_on
                        pygame.mixer.music.unpause()
                    else:
                        self.snd_btn.image = self.snd_off
                        pygame.mixer.music.pause()
                
                if self.login_button.checkForInput(self.menu_mouse_pos):
                    self.login_auth()

            if event.type == pygame.KEYDOWN:
                if self.username_state:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text1 = self.user_text1[:-1]
                    elif event.key == pygame.K_TAB:
                        self.username_state = False
                        self.password_state = True

                    else:
                        self.user_text1 += event.unicode

                if self.password_state:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text2 = self.user_text2[:-1]
                    elif event.key == pygame.K_TAB:
                        pass
                    else:
                        self.user_text2 += event.unicode
    def check_snd(self):
        self.snd_btn.update(self.screen)

    def login_func(self):
        self.screen.blit(self.login_button_hov, (430, 510))
        self.login_button = Button(image=self.login_btn_img, pos=(610, 570), text_input=None, font=self.get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        self.login_button.changeColor(self.menu_mouse_pos)
        self.login_button.update(self.screen)

        if self.cred_error:
            wrong_font = pygame.font.Font("Font/Danskfont.ttf", 35)
            wrong_text = wrong_font.render("Wrong Credentials!", True, "Red")
            wrong_text_place = wrong_text.get_rect(center=(610, 680))
            self.screen.blit(wrong_text, wrong_text_place)
        
    def run(self):
        self.frame_index = 0
        self.frame_delay = 35
        self.frame_counter = 0
        while not self.login_success:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.login_screen)
            self.screen.blit(self.login_screen[self.frame_index], (0, 0))
            

            self.menu_mouse_pos = pygame.mouse.get_pos()
            self.handle_events()        

            self.login_input()           
            self.login_func()  
            self.check_snd()     

            pygame.display.flip()        
            self.clock.tick(60)


if __name__ == "__main__":
    login = Login()
    login.run()