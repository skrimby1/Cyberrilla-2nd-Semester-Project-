import pygame
from time import sleep
from asset1 import Asset
from GDPR_Hop import GDPRGame
from ID1 import gamer
from gameLogic2 import Gamer2
from level_4 import Game


class Levels:
    def __init__(self):
        pygame.init()
        self.current_level = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.clear_color = (0, 0, 0)
        self.keys = pygame.key.get_pressed()
        self.font = pygame.font.Font("assets/font/menufont.otf", 30)
        self.font1 = "assets/font/menufont.otf"
        self.press_space = self.font.render("Tryk SPACE", True, (255, 255, 255))
        self.asset = Asset()
    
    def run_level(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.unload()
                    
                    self.running = False 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unload()
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_level == 1:
                    self.level_1_scene += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_level == 2:
                    self.level_2_scene += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_level == 3:
                    self.level_3_scene += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.current_level == 4:
                    self.level_4_scene += 1

            


    def level_1(self):
        pygame.mixer.music.load("assets/music/phishing_1.mp3")
        pygame.mixer.music.play() 
        self.current_level = 1
        self.level_1_game = gamer()
        self.level_1_scene = 0
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Phishing Level")
        self.screen.fill(self.clear_color)  
        self.phishing_img = pygame.image.load("assets/pictures/phishing.png")
        self.phishing_img_rect = self.phishing_img.get_rect(center=(640, 160))
        self.info_text_1 = self.font.render("Phishing er en type cyberangreb, hvor svindlere forsøger at narre dig til at", True, (255, 255, 255))
        self.info_text_2 = self.font.render("afsløre personlige oplysninger som adgangskoder, kontooplysninger", True, (255, 255, 255))
        self.info_text_3 = self.font.render("eller kortnumre - ofte ved at udgive sig for at være en troværdig afsender.", True, (255, 255, 255))
        self.info_text_4 = self.font.render("Dette kan foregå gennem mails, opkald, sms'er eller sociale medier", True, (255, 255, 255))
        self.phi_text_1 = self.font.render("I denne bane skal du sætte dine genkendelses-evner på prøve. Du bliver", True, (255, 255, 255))
        self.phi_text_2 = self.font.render("præsenteret for en række e-mail adresser - nogle er ægte, andre er", True, (255, 255, 255))
        self.phi_text_3 = self.font.render("ondsindede phishing-forsøg. Til venstre har du den korrekte mail, til højre", True, (255, 255, 255))
        self.phi_text_4 = self.font.render("er der phishing-mails. Din opgave er at udvælge den korrekte e-mail", True, (255,255,255)) # Play background music
        while self.running:
            self.screen.fill(self.clear_color)  
            self.run_level()
            self.screen.blit(self.phishing_img, self.phishing_img_rect)
            self.screen.blit(self.press_space, (520, 650))
            if self.level_1_scene == 0: 
                self.screen.blit(self.info_text_1, (40, 340))
                self.screen.blit(self.info_text_2, (40, 400))
                self.screen.blit(self.info_text_3, (40, 460))
                self.screen.blit(self.info_text_4, (40, 520))
            elif self.level_1_scene == 1:
                    self.screen.blit(self.phi_text_1, (40, 340))
                    self.screen.blit(self.phi_text_2, (40, 400))
                    self.screen.blit(self.phi_text_3, (40, 460))
                    self.screen.blit(self.phi_text_4, (40, 520))
            elif self.level_1_scene == 2:
                    self.level_1_game.run_game()
                    self.running = False
                    
            pygame.display.flip()
            self.clock.tick(60)
            
        
    def level_2(self):
        self.current_level = 2
        self.level_2_scene = 0
        self.level_2_game = GDPRGame()
        self.gdpr_text_1 = self.font.render("GDPR er en lovgivning, der beskytter personoplysninger og sikrer, at de ", True, (255, 255, 255))
        self.gdpr_text_2 = self.font.render("behandles ansvarligt og sikkert. Som medarbejder i kommunen håndterer du ", True, (255, 255, 255))
        self.gdpr_text_3 = self.font.render("dagligt persondata, og det er vigtigt at være opmærksom på, hvordan du skal ", True, (255, 255, 255))
        self.gdpr_text_4 = self.font.render("håndtere både brugernes samt dine egne data. ", True, (255, 255, 255))
        self.gdpr_text_5 = self.font.render("I dette spil lærer du de grundlæggende principper for GDPR, og hvordan", True, (255, 255, 255))
        self.gdpr_text_6 = self.font.render("du kan sikre, at persondata behandles korrekt i din afdeling. Spillet går ud på ", True, (255, 255, 255))
        self.gdpr_text_7 = self.font.render("at du skal hoppe over mail-sneglene, og gribe de grønne mails. Når du har", True, (255, 255, 255))
        self.gdpr_text_8 = self.font.render("grebet en mail, får du et spørgsmål omkring GDPR, som du skal svare på.", True, (255, 255, 255))
        pygame.display.set_caption("GDPR Level")
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill(self.clear_color) 
        while self.running:
            self.run_level()
            self.screen.fill(self.clear_color)
            self.screen.blit(self.press_space, (520, 650))
            self.asset.img("assets/pictures/gdpr.png", 640, 160, self.screen)
            if self.level_2_scene == 0:
                self.screen.blit(self.gdpr_text_1, (40, 340))
                self.screen.blit(self.gdpr_text_2, (40, 400))
                self.screen.blit(self.gdpr_text_3, (40, 460))
                self.screen.blit(self.gdpr_text_4, (40, 520))
            if self.level_2_scene == 1:
                self.screen.blit(self.gdpr_text_5, (40, 340))
                self.screen.blit(self.gdpr_text_6, (40, 400))
                self.screen.blit(self.gdpr_text_7, (40, 460))
                self.screen.blit(self.gdpr_text_8, (40, 520))
            if self.level_2_scene == 2:
                 self.level_2_game.game_run()
                 self.running = False
            
            pygame.display.flip()
            self.clock.tick(60)

    def level_3(self):
        self.current_level = 3
        self.level_3_scene = 0
        self.level_3_game = Gamer2()
        self.password_text_1 = self.font.render("I dag er det essentielt at have et stærkt password for at beskytte dine ", True, (255, 255, 255))
        self.password_text_2 = self.font.render("personlige og professionelle oplysninger. Det er desuden vigtigt, at passe ", True, (255, 255, 255))
        self.password_text_3 = self.font.render("godt på sit password, da et lækket password kan have yderligere", True, (255, 255, 255))
        self.password_text_4 = self.font.render("konsekvenser for dig, dine kollegaer og din arbejdsplads.", True, (255, 255, 255))
        self.password_text_5 = self.font.render("I dette spil skal du godkende de stærke passwords, og afvise de svage.", True, (255, 255, 255))
        self.password_text_6 = self.font.render("Der er nogle specfikke krav til passwordet, som du skal holde øje med", True, (255, 255, 255))
        self.password_text_7 = self.font.render("Disse krav er således: 1. Passwordet skal være minimum 12 tegn langt  ", True, (255, 255, 255))
        self.password_text_8 = self.font.render("2. Passwordet skal indeholde både store og små bogstaver  ", True, (255, 255, 255))
        self.password_text_9 = self.font.render("3. Passwordet skal indeholde tal og specialtegn  ", True, (255, 255, 255))
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Passwords")
        self.screen.fill(self.clear_color)
        while self.running:
            self.run_level()
            self.screen.fill(self.clear_color)
            self.asset.img("assets/pictures/password.png", 640, 160, self.screen)
            self.screen.blit(self.press_space, (520, 650))
            if self.level_3_scene == 0:
                self.screen.blit(self.password_text_1, (40, 340))
                self.screen.blit(self.password_text_2, (40, 400))
                self.screen.blit(self.password_text_3, (40, 460))
                self.screen.blit(self.password_text_4, (40, 520))
            if self.level_3_scene == 1:
                self.screen.blit(self.password_text_5, (40, 340))
                self.screen.blit(self.password_text_6, (40, 400))
                self.screen.blit(self.password_text_7, (40, 460))
                self.screen.blit(self.password_text_8, (40, 520))
                self.screen.blit(self.password_text_9, (40, 580))
            if self.level_3_scene == 2:
                self.level_3_game.run_game()
                self.running = False
                


            pygame.display.flip()
            self.clock.tick(60)
    
    def level_4(self):
        self.current_level = 4
        self.level_4_scene = 0
        self.level_4_text_1 = self.font.render("Sikker surfing er en vigtig del af at beskytte dig selv og din arbejdsplads", True, (255, 255, 255))
        self.level_4_text_2 = self.font.render("mod cybertrusler. Det handler om at være opmærksom på, hvilke hjemmesider", True, (255, 255, 255))
        self.level_4_text_3 = self.font.render("du besøger, samt hvilke oplysninger du deler online. Det kan nemlig have", True, (255, 255, 255))
        self.level_4_text_4 = self.font.render("konsekvenser for både dig og din arbejdsplads, hvis du ikke er opmærksom.", True, (255, 255, 255))
        self.level_4_text_5 = self.font.render("I denne bane skal du vurdere hvorvidt medarbejderne er inde på hjemmesider", True, (255, 255, 255))
        self.level_4_text_6 = self.font.render("som ser mistænkelige ud, ikke er relevante eller potientielt indeholder virus ", True, (255, 255, 255))
        self.level_4_text_7 = self.font.render("eller malware. Du skal godkende de hjemmesider, som du mener er sikre.", True, (255, 255, 255))
        self.level_4_text_8 = self.font.render("Du bevæger dig ved hjælp af piltasterne", True, (255, 255, 255))
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Sikker Surfing")
        self.screen.fill(self.clear_color)
        while self.running:
            self.run_level()
            self.screen.fill(self.clear_color)
            self.asset.img("assets/pictures/sikkersurfing.png", 640, 160, self.screen)
            if self.level_4_scene == 0:
                self.screen.blit(self.level_4_text_1, (40, 340))
                self.screen.blit(self.level_4_text_2, (40, 400))
                self.screen.blit(self.level_4_text_3, (40, 460))
                self.screen.blit(self.level_4_text_4, (40, 520))
            if self.level_4_scene == 1:
                self.screen.blit(self.level_4_text_5, (40, 340))
                self.screen.blit(self.level_4_text_6, (40, 400))
                self.screen.blit(self.level_4_text_7, (40, 460))
                self.screen.blit(self.level_4_text_8, (40, 520))
            if self.level_4_scene == 2:
                self.level_4_game = Game()
                self.level_4_game.game_run()
                self.running = False
                
            pygame.display.flip()
            self.clock.tick(60)
            

