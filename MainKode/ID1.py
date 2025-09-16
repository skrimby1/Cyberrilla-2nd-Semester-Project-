
import pygame
import random
from button import Button
from complete import complete
class gamer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.run = True
        self.screen = pygame.display.set_mode((1280, 720))
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        self.font = pygame.font.Font("assets/font/KGPerfectPenmanship.ttf", 35)
        self.mail_choice = False
        self.correct_guesses = 0
        self.incorrect_guesses = 0
        self.hover = (154, 189, 220)
        self.correct_sound = pygame.mixer.Sound("sounds/erwinyes.mp3")
        self.incorrect_sound = pygame.mixer.Sound("sounds/hell-naw-dog.mp3")
        self.background_music = pygame.mixer.music.load("sounds/phishing_music.mp3")

        self.retry_button = Button(None, 
                              pos=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2.3), 
                              text_input="Retry", 
                              font=self.font, 
                              base_color=(255, 255, 255), 
                              hovering_color=(0, 163, 108,), hovering_image=None)
        self.main_menu_button = Button(None, 
                                pos=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 1.4), 
                                text_input="Main Menu", 
                                font=self.font,
                                base_color=(255, 255, 255),
                                hovering_color=(0, 163, 108,), hovering_image=None)

        self.text_col = (0, 0, 0)
        self.text_background_col = (229, 243, 253)
        self.text_border_color = (154, 189, 220)
        self.timer_start = pygame.time.get_ticks()
        self.countdown_secs = 8
        self.countDown = None
        
        self.hearts = pygame.image.load("imgs/hp.png")

        self.background = pygame.transform.scale(pygame.image.load("imgs/phishingBackground.png"), 
                                                    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.loss_background = pygame.transform.scale(pygame.image.load("imgs/lossBackground.png"), 
                                                    (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.win_background = pygame.transform.scale(pygame.image.load("imgs/winbackground.png"),
                                                     (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.mail_buttons = []
        self.correct_mail = None
        self.correct_rect = None

        self.correctMails = [
            "michealceo@hotmail.com",
            "johndoe@gmail.com",
            "ericCEO@protonmail.com",
            "bigbozzceo@ceomail.com",
            "emilholder@stud.kea.dk",
            "tinathompson@mail.dk",
            "johnnyjohnny@johhnymail.com",
            "oscarericson@stud.kea.dk",
            "rainerbabor@gmail.com",
            "christinalund@kea.dk",
            "andersb@outlook.com",
            "ceo.kasper@firmamail.com",
            "lisalarsen@vipmail.dk",
            "peter.grant@live.com",
            "nanna.madsen@stud.kea.dk",
        ]

        self.similarMails = {
    "michealceo@hotmail.com": [
        "michaelceo@hotmail.com",
        "michealceo@hotrnail.com",
        "micheal.ceo@hotmail.com",
        "michealceoo@hotmail.com",
    ],
    "johndoe@gmail.com": [
        "johndoee@gmail.com",
        "john.doe@gmall.com",
        "j0hndoe@gmail.com",
        "johndooe@gmail.com",
    ],
    "ericCEO@protonmail.com": [
    "ericCE0@protonmail.com",      
    "ericCEO@protonmaill.com",     
    "ericCEO@protonmil.com",        
    "eric.CEO@protonmail.com",      
    ],
    "bigbozzceo@ceomail.com": [
        "bigbossceo@ceomail.com",
        "bigbozzceo@ceomall.com",
        "bigbozzceo@ceomaii.com",
        "bigbozceo@ceomail.com",
    ],
    "emilholder@stud.kea.dk": [
        "emilholde@stud.kea.dk",
        "emil.holder@studkea.dk",
        "emiiholder@stud.kea.dk",
        "emilholder@studkea.dk",
    ],
    "tinathompson@mail.dk": [
        "tinathomson@mail.dk",
        "tinathompson@maill.dk",
        "tinath0mpson@mail.dk",
        "tina.thompson@mail.dk",
    ],
    "johnnyjohnny@johhnymail.com": [
        "johnny.johnny@johnnymail.com",
        "johnnyjohnny@johnymail.com",
        "jonnyjohnny@johhnymail.com",
        "johnnyjohnny@johnnymial.com",
    ],
    "oscarericson@stud.kea.dk": [
        "oscarerikson@stud.kea.dk",
        "oscarericson@studkea.dk",
        "oscarricson@stud.kea.dk",
        "oscareericson@stud.kea.dk",
    ],
    "rainerbabor@gmail.com": [
        "rainer.babor@gmail.com",
        "rainerbabor@gmall.com",
        "rainerbabor@gmaill.com",
        "rinerbabor@gmail.com",
    ],
    "christinalund@kea.dk": [
        "christina.lund@kea.dk",
        "christinalund@kae.dk",
        "chrisstinalund@kea.dk",
        "christinalund@keaa.dk",
    ],
    "andersb@outlook.com": [
        "anders.b@outlook.com",
        "andersb@outllook.com",
        "anderzb@outlook.com",
        "andersb@outlook.dk",
    ],
    "ceo.kasper@firmamail.com": [
        "ceo.kasper@firmmail.com",
        "ceo.kaspar@firmamail.com",
        "ceo.kaspe@firmamail.com",
        "ceokasper@firmamail.com",
    ],
    "lisalarsen@vipmail.dk": [
        "lisalarsen@vipmail.dk",
        "lisalarsen@vipmaiil.dk",
        "lisalarsen@v1pmail.dk",
        "lisa.larsen@vipmail.dk",
    ],
    "peter.grant@live.com": [
        "petergrant@live.com",
        "peter.grant@liv.com",
        "peter.grantt@live.com",
        "peter_grant@live.com",
    ],
    "nanna.madsen@stud.kea.dk": [
        "nannamadsen@stud.kea.dk",
        "nanna.madsen@stud.kea.dk.net",
        "nanna.madsenn@stud.kea.dk",
        "nana.madsen@stud.kea.dk",
    ],
}

    def setup_round(self):
        self.background_music = pygame.mixer.music.play(-1)
        self.timer_start = pygame.time.get_ticks()
        self.mail_buttons.clear()
        self.correct_mail = random.choice(self.correctMails)
        fakes = self.similarMails[self.correct_mail]
        mails_to_show = fakes.copy()
        mails_to_show.append(self.correct_mail)
        random.shuffle(mails_to_show)

        left_y = self.SCREEN_HEIGHT // 2
        text_surface = self.font.render(self.correct_mail, True, self.text_col, self.text_background_col)
        rect = text_surface.get_rect(topleft=(self.SCREEN_WIDTH // 15, left_y))
        self.mail_buttons.append((rect, self.correct_mail))

        spacing_y = 130
        top_y = 70
        for i, mail in enumerate(mails_to_show):
            text_surface = self.font.render(mail, True, self.text_col, self.text_background_col)
            rect = text_surface.get_rect(topleft=(self.SCREEN_WIDTH - 500, top_y + i * spacing_y))
            self.mail_buttons.append((rect, mail))

    def draw_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.timer_start) // 1000
        remaining_time = max(0, self.countdown_secs - elapsed_time)
        self.countDown = str(remaining_time)

        box_width = 100
        box_height = 90
        left_x = 10
        left_y =  10

        border_rect = pygame.Rect(left_x, left_y, box_width, box_height)
        pygame.draw.rect(self.screen, self.text_border_color, border_rect)

        inner_rect = border_rect.inflate(-10, -10)
        pygame.draw.rect(self.screen, self.text_background_col, inner_rect)

        text_surface = self.font.render(self.countDown, True, self.text_col)
        text_rect = text_surface.get_rect(center=inner_rect.center)
        self.screen.blit(text_surface, text_rect)

        if remaining_time <= 0:
            return True
        
        for i in range(3 - self.incorrect_guesses):
            self.hearts = pygame.transform.scale(self.hearts, (90, 80))
            x = left_x + box_width + 70 + (i * 80)
            y = left_y
            self.screen.blit(self.hearts, (x, y))

        for i in range(10):
            score_text = self.font.render(f"{self.correct_guesses} / 10", True, (0, 0, 0))

            score_border_rect = pygame.Rect(left_x + 450, 10, 160, 80)

            inner_score_rect = score_border_rect.inflate(-10, -10)
            pygame.draw.rect(self.screen, self.text_border_color, score_border_rect)

            pygame.draw.rect(self.screen, self.text_background_col, inner_score_rect)
            score_rect = score_text.get_rect(center=inner_score_rect.center)
            self.screen.blit(score_text, score_rect)




    def button_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        for rect, mail in self.mail_buttons:
            if rect.collidepoint(mouse_pos) and rect.topleft[0] > self.SCREEN_WIDTH // 2:
                border_rect = rect.inflate(30, 30)
                pygame.draw.rect(self.screen, self.hover, border_rect)

    def draw_buttons(self):
        for rect, mail in self.mail_buttons:
            border_rect = rect.inflate(10, 10)
            pygame.draw.rect(self.screen, self.text_border_color, border_rect)
            text_surface = self.font.render(mail, True, self.text_col, self.text_background_col)
            self.screen.blit(text_surface, rect)

    def check_mouse_click(self, mouse_pos):
        for rect, mail in self.mail_buttons:
            if rect.collidepoint(mouse_pos):
                if mail == self.correct_mail and rect.topleft[0] < self.SCREEN_WIDTH // 2:
                    return None
                elif mail == self.correct_mail:
                    self.correct_guesses += 1
                    self.correct_sound.set_volume(0.3)
                    pygame.mixer.Sound.play(self.correct_sound)
                    return True
                else:
                    pygame.mixer.Sound.play(self.incorrect_sound)
                    self.incorrect_guesses += 1
                    return False
        return None

    def draw_end_screen(self, background, message, buttons):
        self.screen.blit(background, (0, 0))
        menu_text = self.font.render(message, True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 7))
        self.screen.blit(menu_text, menu_rect)

        for button in buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def run_game(self):
        self.setup_round()
        clock = pygame.time.Clock()
        game_state = "play"
    

        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False

                if game_state == "play":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        result = self.check_mouse_click(mouse_pos)
                        if result is True:
                            pygame.time.delay(500)
                            self.setup_round()
                            if self.correct_guesses >= 3:
                                complete.level_1_complete = True
                                pygame.mixer.music.stop()
                                game_state = "win"
                                
                        elif result is False:
                            self.setup_round()
                            if self.incorrect_guesses >= 3:
                                game_state = "loss"

                elif game_state in ["retry", "win", "loss"]:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if game_state in ["retry", "loss"] and self.retry_button.checkForInput(pygame.mouse.get_pos()):
                            self.setup_round()
                            self.correct_guesses = 0
                            self.incorrect_guesses = 0
                            game_state = "play"
                        elif self.main_menu_button.checkForInput(pygame.mouse.get_pos()):
                            pygame.mixer.music.unload()
                            self.run = False

            if game_state == "play":
                self.screen.blit(self.background, (0, 0))
                self.button_hover()
                self.draw_buttons()

                if self.draw_timer():
                    game_state = "retry"

            elif game_state == "retry":
                self.draw_end_screen(self.loss_background, "You ran out of time...", [self.retry_button, self.main_menu_button])

            elif game_state == "win":
                self.draw_end_screen(self.win_background, "You Won!", [self.main_menu_button])

            elif game_state == "loss":
                self.draw_end_screen(self.loss_background, "You guessed incorrectly 3 times...", [self.retry_button, self.main_menu_button])

            pygame.display.flip()
            clock.tick(60)

      


if __name__ == "__main__":
    game = gamer()
    game.run_game()

