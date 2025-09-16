import pygame, sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Minigame 4')

        self.current_stage = Level()

    def game_run(self):
        running = True
        while running:
            running = self.current_stage.run()
        return running


