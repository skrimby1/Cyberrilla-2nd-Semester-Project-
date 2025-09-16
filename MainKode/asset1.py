import pygame

class Asset:
    def __init__(self):
        pass

    def img(self, path, x, y, screen, place=True):
        self.image = pygame.image.load(path)
        self.rect_img = self.image.get_rect(center=(x, y))
        if place == True:
            screen.blit(self.image, self.rect_img)
        else:
            pass
        return self
    
    def font(self, text, font, size, x, y, screen, color=(0,0,0), place=True):
        self._font = pygame.font.Font(font, size)
        self.text = self._font.render(text, True, color)
        if place == True:
            screen.blit(self.text, (x, y))
        else:
            pass

    def rect(self, x, y, width, height, screen, color=(0,0,0), place = True):
        self.rect = pygame.Rect(x, y, width, height)
        if place == True:
            self.draw_rect = pygame.draw.rect(screen, color, self.rect)
        else:
            pass

    def place(self, screen):
        screen.blit(self.image, self.rect_img)

    def place_text(self, x, y, screen):
        screen.blit(self.text, (x, y) )

    def place_rect(self):
        self.draw_rect = pygame.draw.rect(self.screen, (0,0,0), self.rect)
    
    def remove(self):
        self.rect_img = self.image.get_rect(center=(10000, 10000))
    
    def collision(self):
        self.image.get_rect(center=(self.x, self.y))