import pygame
from sys import exit
from random import randint, choice
import textwrap
from complete import complete


class GDPRGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 720))
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("GDPR Hop")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Font/Danskfont.ttf", 28)
        self.quiz_font = pygame.font.Font("Font/Danskfont.ttf", 22)

        self.game_active = True
        self.show_quiz = False
        self.winner_screen = False
        self.score = 0
        self.lives = 3

        self.user_text1 = "cleared"

        self.all_questions = [
            {"question": "Du har adgang til mange borgere i systemet. Må du kigge, hvis du er nysgerrig?", 
             "options": ["A: Ja", "B: Nej, kun hvis det er nødvendigt for dit arbejde", "C: Måske"], 
             "correct": "B"
            },
            {"question": "En borger vil vide, hvorfor I behandler hendes oplysninger. Hvad svarer du?", 
             "options": ["A: Det bestemmer kommunen bare selv", "B: Det må du ikke fortælle", "C: Du oplyser formålet klart – det har hun ret til"], 
             "correct": "C"
            },
            {"question": "Du får en e-mail med persondata ved en fejl. Hvad gør du?", 
             "options": ["A: Du videresender den hurtigt", "B: Du kontakter den ansvarlige og anmelder det", "C: Du ignorerer det"], 
             "correct": "B"
            },
            {"question": "Hvem i Frederiksberg Kommune skal man kontakte, hvis man har spørgsmål om databeskyttelse?", 
             "options": ["A: Borgerservice", "B: HR-afdeling", "C: Kommunens DPO (databeskyttelsesrådgiver)"], 
             "correct": "C"
            },
            {"question": "Du er i praktik i Frederiksberg Kommune og hører om en datalæk. Hvad gør du?", 
             "options": ["A: Du siger det ikke til nogen", "B: Du rapporterer det til din leder eller DPO", "C: Du poster det på LinkedIn"], 
             "correct": "B"
            },
            {"question": "En ny kollega i din afdeling spørger, om han må bruge dit login. Hvad siger du?", 
             "options": ["A: Ja, det er jo bare midlertidigt", "B:  Nej, man må aldrig dele login", "C: Kun hvis han lover ikke at ændre noget"], 
             "correct": "B"
            },
            {"question": "Hvilken data er følsom?", 
             "options": ["A: Navn og adresse", "B: CPR-nummer", "C: Ens religion"], 
             "correct": "C"
            },
            {"question": "Du modtager en USB-nøgle med borgerdata. Hvordan håndterer du den?", 
             "options": ["A: Lader den ligge på skrivebordet", "B: Gemmer den i din jakkelomme", "C: Afleverer den til IT"], 
             "correct": "C"
            },
            {"question": "Hvem er dataansvarlig?", 
             "options": ["A: Økonomimedarbejder", "B: Personen hvis data behandles", "C: Den der bestemmer hvordan data behandles"], 
             "correct": "C"
            },
            {"question": "Skal du låse din skærm, når du forlader skrivebordet?", 
             "options": ["A: Ja", "B: Nej", "C: Kun hvis der er følsomme data åbne"], 
             "correct": "A"
            }
        ]

        self.remaining_questions = self.all_questions.copy()
        self.current_question = None
        self.quiz_timer = 0
        self.quiz_start_time = 0

        self.bg_music = pygame.mixer.Sound("Audio/game-music-loop.mp3")
        self.bg_music.play(-1)
        self.bg_music.set_volume(0.5)
        self.jump_sound = pygame.mixer.Sound("Audio/Jump10.wav")
        self.jump_sound.set_volume(0.5)
        self.collect_sound = pygame.mixer.Sound("Audio/coin.wav")
        self.collect_sound.set_volume(0.5)
        self.fail_sound = pygame.mixer.Sound("Audio/game-over.mp3")
        self.fail_sound.set_volume(0.5)
        self.correct_sound = pygame.mixer.Sound("Audio/Rigtigt.mp3")
        self.correct_sound.set_volume(0.5)

        self.background = pygame.image.load("Graphics/Background.png").convert()
        self.ground = pygame.image.load("Graphics/Ground1.png").convert()

        self.snail_frame = [
            pygame.image.load("Graphics/Enemy/snail3.png").convert_alpha(),
            pygame.image.load("Graphics/Enemy/snail33.png").convert_alpha()
        ]
        self.snail_index = 0
        self.snail_surf = self.snail_frame[self.snail_index]

        self.fly_frame = [
            pygame.image.load("Graphics/Enemy/Grønmail.png").convert_alpha(),
            pygame.image.load("Graphics/Enemy/grønmail2.png").convert_alpha()
        ]
        self.fly_index = 0
        self.fly_surf = self.fly_frame[self.fly_index]

        self.obstacle_rect_list = []

        player_walk1 = pygame.image.load("Graphics/Player/player_stand1.png").convert_alpha()
        player_walk2 = pygame.image.load("Graphics/Player/player_1_walk.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("Graphics/Player/player_jump.png").convert_alpha()
        self.player_surf = self.player_walk[self.player_index]
        self.player_rect = self.player_surf.get_rect(midbottom=(80, self.screen_height - 100))
        self.player_gravity = 0

        self.player_stand = pygame.image.load("Graphics/Player/player_spiser_banan.png").convert_alpha()
        self.player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        self.player_stand_rect = self.player_stand.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.game_name = self.font.render("GDPR Hop", False, (111, 196, 169))
        self.game_name_rect = self.game_name.get_rect(center=(self.screen_width // 2, 80))
        self.game_message = self.font.render("Tryk Enter for at starte igen", False, (111, 196, 169))
        self.game_message_rect = self.game_message.get_rect(center=(self.screen_width // 2, self.screen_height - 100))
        self.main_menu = self.font.render("Tryk ESCAPE for Hovedmenu", False, (111, 196, 169))
        self.main_menu_rect = self.main_menu.get_rect(center=(self.screen_width // 2, self.screen_height - 50))

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 2500)
        self.snail_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_timer, 500)
        self.fly_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.fly_timer, 200)
        self.running = True

    def obstacle_movement(self, obstacle_list):
        new_list = []
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.right > 0:
                new_list.append(obstacle_rect)
                if obstacle_rect.bottom == self.screen_height - 100:
                    self.screen.blit(self.snail_surf, obstacle_rect)
                else:
                    self.screen.blit(self.fly_surf, obstacle_rect)
        return new_list

    def player_animation(self):
        if self.player_rect.bottom < self.screen_height - 100:
            self.player_surf = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.player_surf = self.player_walk[int(self.player_index)]

    def display_quiz(self):
        self.screen.fill((30, 30, 30))
        margin = 60
        wrap_width = 60

        if not self.current_question:
            if not self.remaining_questions:
                self.remaining_questions = self.all_questions.copy()
            self.current_question = choice(self.remaining_questions)
            self.remaining_questions.remove(self.current_question)
            self.quiz_start_time = pygame.time.get_ticks()

        q = self.current_question
        wrapped_question = textwrap.wrap(q["question"], wrap_width)
        for i, line in enumerate(wrapped_question):
            question_text = self.quiz_font.render(line, False, (255, 255, 255))
            self.screen.blit(question_text, (margin, margin + i * 30))

        for i, option in enumerate(q["options"]):
            option_text = self.quiz_font.render(option, False, (200, 200, 200))
            self.screen.blit(option_text, (margin, margin + (len(wrapped_question) + i) * 40))

        time_elapsed = (pygame.time.get_ticks() - self.quiz_start_time) // 1000
        time_left = max(0, 15 - time_elapsed)
        timer_text = self.font.render(f"Tid: {time_left}", False, (255, 100, 100))
        self.screen.blit(timer_text, (self.screen_width - 250, 30))

        if time_left == 0:
            self.fail_sound.play()
            self.score = 0
            self.obstacle_rect_list.clear()
            self.show_quiz = False
            self.current_question = None
            self.game_active = False

    def game_run(self):
        self.game_active = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.bg_music.stop()
                    self.running = False
                    break

                if self.show_quiz:
                    if event.type == pygame.KEYDOWN:
                        key = event.unicode.upper()
                        if key in ["A", "B", "C"]:
                            if self.current_question and key == self.current_question["correct"]:
                                self.score += 1
                                self.correct_sound.play()
                                self.show_quiz = False
                                self.current_question = None
                                if self.score >= 3:
                                    complete.level_2_complete = True
                                    self.winner_screen = True
                                    self.game_active = False
                            else:
                                self.fail_sound.play()
                                self.lives -= 1
                                self.obstacle_rect_list.clear()
                                self.show_quiz = False
                                self.current_question = None
                                if self.lives == 0:
                                    self.game_active = False
                    continue  
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.bg_music.stop()
                            self.running = False
                        elif event.key == pygame.K_SPACE and self.player_rect.bottom >= self.screen_height - 100:
                            self.player_gravity = -20
                            self.jump_sound.play()
                
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.player_rect.bottom >= self.screen_height - 100:
                            self.player_gravity = -20
                            self.jump_sound.play()

                    if event.type == self.obstacle_timer:
                        if randint(0, 1):
                            self.obstacle_rect_list.append(self.snail_surf.get_rect(bottomright=(randint(self.screen_width + 100, self.screen_width + 300), self.screen_height - 100)))
                        else:
                            self.obstacle_rect_list.append(self.fly_surf.get_rect(bottomright=(randint(self.screen_width + 100, self.screen_width + 300), self.screen_height - 300)))

                    if event.type == self.snail_timer:
                        self.snail_index = 1 - self.snail_index
                        self.snail_surf = self.snail_frame[self.snail_index]

                    if event.type == self.fly_timer:
                        self.fly_index = 1 - self.fly_index
                        self.fly_surf = self.fly_frame[self.fly_index]

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_active = True
                        self.score = 0
                        self.lives = 3
                        self.obstacle_rect_list.clear()
                        self.winner_screen = False

            if self.show_quiz:
                self.display_quiz()
            elif self.game_active:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.ground, (0, self.screen_height - 130))

                self.player_gravity += 0.7
                self.player_rect.y += self.player_gravity
                if self.player_rect.bottom >= self.screen_height - 100:
                    self.player_rect.bottom = self.screen_height - 100

                self.player_animation()
                self.screen.blit(self.player_surf, self.player_rect)

                self.obstacle_rect_list = self.obstacle_movement(self.obstacle_rect_list)

                for obstacle_rect in self.obstacle_rect_list:
                    if self.player_rect.colliderect(obstacle_rect):
                        if obstacle_rect.bottom != self.screen_height - 100:
                            self.show_quiz = True
                            self.collect_sound.play()
                            self.obstacle_rect_list.remove(obstacle_rect)
                            break
                        else:
                            self.fail_sound.play()
                            self.lives -= 1
                            self.obstacle_rect_list.clear()
                            if self.lives == 0:
                                self.game_active = False

                score_display = self.font.render(f"Score: {self.score}", False, (255, 255, 255))
                self.screen.blit(score_display, (20, 20))

                lives_display = self.font.render(f"Liv: {self.lives}", False, (255, 255, 255))
                self.screen.blit(lives_display, (20, 60))

            else:
                self.screen.fill((91, 129, 162))
                self.screen.blit(self.player_stand, self.player_stand_rect)
                if self.winner_screen:
                    win_text = self.font.render("Tillykke! Du har vundet!", False, (255, 255, 0))
                    self.screen.blit(win_text, win_text.get_rect(center=(self.screen_width // 2, 100)))
                else:
                    self.screen.blit(self.game_name, self.game_name_rect)

                score_message = self.font.render(f"Din score: {self.score}", False, (255, 255, 0))
                self.screen.blit(score_message, score_message.get_rect(center=(self.screen_width // 2, self.screen_height - 200)))
                self.screen.blit(self.game_message, self.game_message_rect)
                self.screen.blit(self.main_menu, self.main_menu_rect)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = GDPRGame()
    game.game_run()
