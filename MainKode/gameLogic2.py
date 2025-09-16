
import pygame
import random
from button import Button
from complete import complete

class Gamer2:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = self.font = pygame.font.Font("fonts/KGPerfectPenmanship.ttf", 45)
        self.background = pygame.transform.scale(pygame.image.load("assets/background.png"), (1280, 720))
        self.win_background = pygame.transform.scale(pygame.image.load("assets/win_background.png"), (1280, 720))
        self.loss_background = pygame.transform.scale(pygame.image.load("assets/loss_background.png"), (1280, 720))
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        self.characterList = ["assets/babydoge.png", "assets/nose.png", "assets/sting.png", "assets/cheems.png", 
                              "assets/closed.png", "assets/wisdom.png", "assets/ranse.png", "assets/joy.png", 
                              "assets/sheepman.png", "assets/cat.png", "assets/hood.png", "assets/cte.png", 
                              "assets/nap.png", "assets/bipedal.png", "assets/bee.png", "assets/goof.png", 
                              "assets/sus.png", "assets/walter.png", "assets/smile.png", "assets/demon.png", 
                              "assets/smirk.png", "assets/butter.png"] #paths her
        self.game_state = "start"
        self.timer_start = pygame.time.get_ticks()
        self.countdown_secs = 10

        self.incorrect_sound = pygame.mixer.Sound("sounds/wrong.mp3")
        self.correct_sound = pygame.mixer.Sound("sounds/right.mp3")
        self.decision_made = False
        self.background_music = pygame.mixer.Sound("sounds/background_music.mp3")
        self.hired_button = None
        self.fired_button = None
        self.target_x = None
        self.img_speed = 3  
        self.img = None
        self.rect_img = None
        self.chosen_pass = None
        self.button_size = (200, 60)
        self.hired_button_surface = pygame.Surface(self.button_size)
        self.fired_button_surface = pygame.Surface(self.button_size)
        self.pass_surface = pygame.Surface(self.button_size)
        self.button_width, self.button_height = self.button_size
        self.correct_decisions = 0
        self.incorrect_decisions = 0
        self.hearts = pygame.image.load("assets/hp.png")
        self.retry_button = Button(None, 
                              pos=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2.3), 
                              text_input="Retry", 
                              font=self.font, 
                              base_color=(255, 255, 255), 
                              hovering_color=(136, 8, 8), hovering_image= None)
        self.main_menu_button = Button(None, 
                                pos=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 1.4), 
                                text_input="Main Menu", 
                                font=self.font,
                                base_color=(255, 255, 255),
                                hovering_color=(136, 8, 8), hovering_image=None)


        self.good_passwords = [
        "nT6#Xz8Q@rPw",
        "L3f$WpZ1!oKy",
        "Bc!94sM@tZqL",
        "V8q#TyPm@3zW",
        "zA5!RvYc@X1L",
        "Gm7!KpT9#xLc",
        "uQ@8WrXm!L3z",
        "Z!fX7qB@pLc9",
        "dT6!PwK9#ZoX",
        "Mx!2VbR7@qWL",
        "qZ@5wMr!7TXc",
        "Hp3!Xt@ZvR9q",
        "Kw!7Xp2@QzvR",
        "T#6xZoY@vLq9",
        "Rf2!XwMp@Q8z"
    ]


        self.bad_passwords = [
        "nT6Xz8QrpwLa",     #  Missing special character
        "l3f$wpz1!oky",     #  Missing uppercase letter
        "BC!94SM@TZQL",     #  Missing lowercase letter
        "VqTyPm@zWLr",      #  Missing number
        "zA5RvYcX1L2",      #  Missing special character
        "Gm7KpT9xLc",       #  Too short (< 12 characters)
        "UQ8WRXML3ZP",      #  Missing special character and lowercase
        "ZfXqBpLc9",        #  Too short (< 12 characters)
        "DtPwKZoxvTR",      #  Missing number
        "MxVbR7qWL",        #  Too short (< 12 characters)
        "qZwMrTXc2023",     #  Missing special character
        "HP3XtzvR9QWL",     #  Missing special character
        "kw7xp2qzvr",       #  Missing uppercase, number, and special character
        "T6xZoYvLq9",       #  Too short (< 12 characters)
        "rf2xwmpqz89",      #  Missing uppercase and special character
    ]


    def img_setup(self):
        self.img = pygame.image.load(random.choice(self.characterList))
        self.img = pygame.transform.scale(self.img, (350, 500))
        img_height = self.img.get_height()
        self.rect_img = self.img.get_rect(center=(1280 + 20, self.SCREEN_HEIGHT - (img_height // 2)))


    def update_direction(self):
        if self.img is None:
            return
        img_width = self.img.get_width()
        if self.game_state == "play":
            self.target_x = (self.SCREEN_WIDTH // 2)
        elif self.game_state == "correct":
            self.target_x = -img_width
        elif self.game_state == "incorrect":
            self.target_x = self.SCREEN_WIDTH

    def imgs_mover(self):
        if self.img is None or self.rect_img is None or self.target_x is None:
            return
        if self.rect_img.x < self.target_x:
            self.rect_img.x += self.img_speed
            if self.rect_img.x > self.target_x:
                self.rect_img.x = self.target_x
        elif self.rect_img.x > self.target_x:
            self.rect_img.x -= self.img_speed
            if self.rect_img.x < self.target_x:
                self.rect_img.x = self.target_x

        self.screen.blit(self.img, self.rect_img)




    def draw_timer_and_score(self):
        elapsed_time = (pygame.time.get_ticks() - self.timer_start) // 1000
        remaining_time = max(0, self.countdown_secs - elapsed_time)
        self.countDown = str(remaining_time)

        box_width = 100
        box_height = 90
        border_rect = pygame.Rect(255, 20, box_width, box_height)
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect)

        inner_rect = border_rect.inflate(-15, -15)
        pygame.draw.rect(self.screen, (255, 255, 255), inner_rect)

        text_color = (255, 0, 0) if remaining_time < 4 else (0, 0, 0)
        text_surface = self.font.render(self.countDown, True, text_color)
        text_rect = text_surface.get_rect(center=inner_rect.center)
        self.screen.blit(text_surface, text_rect)

        if remaining_time <= 0:
            return True


        for i in range(3 - self.incorrect_decisions):
            self.hearts = pygame.transform.scale(self.hearts, (80, 80))
            x = 30 + (i * 60)
            y = 20
            self.screen.blit(self.hearts, (x, y))

        for i in range(10):
            score_text = self.font.render(f"{self.correct_decisions} / 10", True, (0, 0, 0))
            score_border_rect = pygame.Rect(400, 20, 160, 90)

            inner_score_rect = score_border_rect.inflate(-15, -15)
            pygame.draw.rect(self.screen, (0, 0, 0), score_border_rect)

            pygame.draw.rect(self.screen, (255, 255, 255), inner_score_rect)
            score_rect = score_text.get_rect(center=inner_score_rect.center)
            self.screen.blit(score_text, score_rect)


    def hired_fired_setup(self):
        self.fired_button_surface.fill((236, 187, 119))
        self.hired_button_surface.fill((236, 187, 119))

        self.hired_button = Button(
            image=self.hired_button_surface,
            pos=(150, 530),  
            text_input="Hired!",
            font=self.font,
            base_color=(0, 0, 0),     
            hovering_color=(255, 255, 255),
            hovering_image=None     
        )

        self.fired_button = Button(
            image=self.fired_button_surface,
            pos=(430, 530),  
            text_input="Fired!",
            font=self.font,
            base_color=(0, 0, 0),   
            hovering_color=(255, 255, 255),
            hovering_image=None         
        )

       
       



    def draw_hired_fired_buttons(self):
        border_size = (self.button_width + 15, self.button_height + 15)
        
   
        self.hired_button_surface = pygame.Surface((200, 60))
        self.hired_button_surface.fill((255, 255, 255))

        self.fired_button_surface = pygame.Surface((200, 60))
        self.fired_button_surface.fill((255, 255, 255))



        self.hired_border_surface = pygame.Surface(border_size)
        self.hired_border_surface.fill((0, 0, 0))
        self.fired_border_surface = pygame.Surface(border_size)
        self.fired_border_surface.fill((0, 0, 0))

        
       
        self.hired_border_rect = self.hired_border_surface.get_rect(center=self.hired_button.rect.center)
        self.fired_border_rect = self.fired_border_surface.get_rect(center=self.fired_button.rect.center)
       

        self.screen.blit(self.hired_border_surface, self.hired_border_rect)
        self.screen.blit(self.fired_border_surface, self.fired_border_rect)
        self.hired_button.update(self.screen)
        self.fired_button.update(self.screen)




    def pass_setup(self):
        all_pass = self.good_passwords + self.bad_passwords
        self.chosen_pass = random.choice(all_pass)

        temp_surface = self.font.render(self.chosen_pass, True, (0, 0, 0))
        text_width, text_height = temp_surface.get_size()

        self.border_surface = pygame.Surface((text_width + 35, text_height + 35))
        self.border_surface.fill((0, 0, 0))  

        self.pass_surface = pygame.Surface((text_width + 20, text_height + 20))
        self.pass_surface.fill((255, 255, 255)) 

        button_width = self.pass_surface.get_width()
        self.password_button = Button(
            image=self.pass_surface,
            pos=(self.SCREEN_WIDTH - ((button_width + 50) // 2), text_height + 5),  
            text_input=self.chosen_pass,
            font=self.font,
            base_color=(0, 0, 0),
            hovering_color=(0, 0, 0),
            hovering_image=None
        )

    def draw_password(self):
        border_rect = self.border_surface.get_rect(center=self.password_button.rect.center)
        self.screen.blit(self.border_surface, border_rect)
        self.password_button.update(self.screen)

    def hired_decision(self):
        self.game_state = "correct"
        self.update_direction()
        self.timer_start = pygame.time.get_ticks()

    def fired_decision(self):
        self.game_state = "incorrect"
        self.update_direction()
        self.timer_start = pygame.time.get_ticks()
    

    def end_screen(self, background, message, buttons):
        self.screen.blit(background, (0, 0))
        menu_text = self.font.render(message, True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 7))
        self.screen.blit(menu_text, menu_rect)

        for button in buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)


    def state_changer(self):
        if int(self.countDown) == 0:
            self.game_state = "timeLoss"
        elif self.incorrect_decisions == 3:
            self.game_state =  "guessLoss"
        elif self.correct_decisions == 3:
            self.game_state = "win"

    def draw_screens(self):
        if self.game_state == "timeLoss":
            self.end_screen(self.loss_background, "You ran out time...", [self.retry_button, self.main_menu_button])
        elif self.game_state == "guessLoss":
            self.end_screen(self.loss_background, "You ran out of guesses...", [self.retry_button, self.main_menu_button])
        elif self.game_state == "win":
            complete.level_3_complete = True
            self.end_screen(self.win_background, "You Won!", [self.main_menu_button])



    def setup(self):
        self.decision_made = False
        self.img_setup()
        self.hired_fired_setup()
        self.pass_setup()
        self.update_direction()
        self.game_state = "play"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hired_button.checkForInput(mouse_pos) and not self.decision_made:
                    if self.chosen_pass in self.good_passwords:
                        self.correct_decisions += 1
                        self.correct_sound.play()
                        self.hired_decision()
                    elif self.chosen_pass in self.bad_passwords:
                        self.incorrect_decisions += 1
                        self.incorrect_sound.play()
                        self.hired_decision()
                    self.decision_made = True
                elif self.fired_button.checkForInput(mouse_pos) and not self.decision_made:
                    if self.chosen_pass in self.good_passwords:
                        self.incorrect_decisions += 1
                        self.incorrect_sound.play()
                        self.fired_decision()
                    elif self.chosen_pass in self.bad_passwords:
                        self.correct_decisions += 1
                        self.correct_sound.play()
                        self.fired_decision()
                    self.decision_made = True
                elif self.retry_button.checkForInput(mouse_pos) and self.game_state in ["timeLoss", "guessLoss"]:
                        self.correct_decisions = 0
                        self.incorrect_decisions = 0
                        self.timer_start = pygame.time.get_ticks()
                        self.setup() 
                elif self.main_menu_button.checkForInput(mouse_pos):
                    self.background_music.stop()
                    self.running = False

                
        if self.game_state in ["correct", "incorrect"]:
            if (self.rect_img.right < 100 or self.rect_img.left > self.SCREEN_WIDTH - 100):
                self.setup()
        self.screen.blit(self.background, (0, 0))
        self.draw_hired_fired_buttons()
        self.update_direction()
        self.imgs_mover()

        self.hired_button.changeColor(mouse_pos)
        self.fired_button.changeColor(mouse_pos)
        
        self.draw_timer_and_score()
        
        self.draw_password()

        self.state_changer()
        self.draw_screens()
        return mouse_pos

    def run_game(self):
        self.setup()
        self.background_music.play(-1)
        while self.running:
            mouse_pos = self.handle_events()
            pygame.display.update()

if __name__ == "__main__":
    game2 = Gamer2()
    game2.run_game()