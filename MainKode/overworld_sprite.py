import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image_path, x, y):
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        loaded[image_path] = self.image
        self.x = x
        self.y = y
        sprites.append(self)
        self.animation_frames = []      
        self.animation_index = 0       
        self.animation_last = 0       
        self.animation_delay = 0        
        self.animated = False

    def set_animation(self, frame_paths, delay=100):
       self.animation_frames = []
       for p in frame_paths:
            img = loaded.get(p) or pygame.image.load(p)
            loaded[p] = img
            self.animation_frames.append(img)
            self.animation_index = 0
            self.animation_delay = delay
            self.animation_last = pygame.time.get_ticks()
            self.animated = True
            self.image = self.animation_frames[0]
    
    def update_animation(self):
            if not self.animated or not self.animation_frames:
                return
            now = pygame.time.get_ticks()
            if now - self.animation_last >= self.animation_delay:
                self.animation_last = now
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.animation_index]

    
    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        self.update_animation()
        screen.blit(self.image, (self.x, self.y))
