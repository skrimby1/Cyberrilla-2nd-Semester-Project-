import pygame, sys
import pygame.display
from button import Button
import login
from intro_map import map_intro
from Overworld import Overworld
from asset import Asset
import random

pygame.init()
asset = Asset(1280, 720)
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
menu_snd = pygame.mixer.Sound("assets/music/menusnd.mp3")
menu_play_snd = pygame.mixer.Sound("assets/music/menu_play.mp3")
clock = pygame.time.Clock()
login = login.Login()
frames = [pygame.image.load(f"assets/pictures/sprites/background/menu_animation/background_{i}.gif") for i in range(20)]
background = pygame.image.load("assets/pictures/sprites/background/menu_animation/background_0.gif") 
play_img = pygame.image.load("assets/pictures/play_btn.png")
play_img2 = pygame.image.load("assets/pictures/play_btn2.png")
options_img1 = pygame.image.load("assets/pictures/options_1.png")
options_img2 = pygame.image.load("assets/pictures/options_2.png")
exit_img1 = pygame.image.load("assets/pictures/exit_1.png")
exit_img2 = pygame.image.load("assets/pictures/exit_2.png")
pygame.display.set_caption("Main Menu")
font = "assets/font/menufont.otf"

def get_font(size):
    return pygame.font.Font("assets/font/menufont.otf", size)
play_button = Button(image=play_img, pos=(225, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=play_img2)
options_button = Button(image=options_img1, pos=(650, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=options_img2) # Vi laver en knap til options menuen
exit_button = Button(image=exit_img1, pos=(1075, 600), text_input="", font=get_font(100), base_color="#d7fcd4", hovering_color="White", hovering_image=exit_img2) #
fact_img = pygame.image.load("assets/pictures/fact.png")
fact_rect = fact_img.get_rect(center=(625, 250)) 
pygame.display.flip()

menu_font = get_font(32)
clock.tick(60)

fact_dict = {
        "fact_1": "Cirka 90 procent af alle cyberangreb starter med en phishing mail",
        "fact_2": "Menneskefejl er den primære årsag bag cyberangreb",
        "fact_3": "Over halvdelen af ansatte klikker på links i phishing-mails",
    }

def options():
    pygame.display.set_caption("Options")
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        options_back = Button(image=None,text_input="Go Back", pos=(640, 650), font=get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        options_back.changeColor(options_mouse_pos)
        options_game_snd = Button(image=None,text_input="Game Volume", pos=(640, 450), font=get_font(75), base_color="#d7fcd4", hovering_color="White", hovering_image=None)
        options_game_snd.changeColor(options_mouse_pos)
        options_back.update(screen)
        options_game_snd.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    menu_snd.play()
                    main_menu()
                if options_game_snd.checkForInput(options_mouse_pos):
                    menu_snd.play()
                    main_menu()
        pygame.display.update()

def redrawWindow():
    screen.fill((0, 0, 0)) 
    screen.blit(background, (0, 0))
    screen.blit(fact_img, fact_rect)

def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)

def main_menu(): 
    frame_index = 0
    frame_delay = 5
    frame_counter = 0
    fact_slide = 3
    current_fact = ""
    fact_timer = 0
    fact_delay = 5000
    fact_ready = False
    while True:
        dt = clock.tick(60)
        fact_timer += dt 

        frame_counter += 1
        if frame_counter >= frame_delay:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(frames)
            screen.blit(frames[frame_index], (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        screen.blit(fact_img, fact_rect) 
        
        if (fact_timer > fact_delay or current_fact == ""):
            random_fact = random.choice(list(fact_dict.keys()))
            fact_ready
            current_fact = fact_dict[random_fact]
            fact_timer = 0  # Reset timer
            fact_ready = True
            
        if fact_ready:
            asset.font(current_fact, "assets/font/menufont.otf", 
                      26, 175, 225, (0,0,0))
        
        
        for button in [play_button, options_button, exit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    menu_play_snd.play()
                    pygame.mixer.music.stop()
                    pygame.display.set_caption("Cyberilla HQ")
                    fade(1920, 1080)
                    intro = map_intro()
                    intro.run()
                    if intro.next_scene == "overworld":
                        overworld = Overworld()
                        overworld.run()
    
                    print("Play button pressed")
                  
                if options_button.checkForInput(menu_mouse_pos):
                    menu_snd.play()
                    options()
                if exit_button.checkForInput(menu_mouse_pos):
                    menu_snd.play()
                    pygame.quit()
                    sys.exit()
            
            

        pygame.display.flip()

login.run() 
pygame.mixer.music.load("assets/music/menu.mp3")
pygame.mixer.music.play(-1)
if login.login_success == True:
    main_menu()


