import pygame
from astro_avengers.const import *

class Explosion:
    def __init__(self, x, y, scale=1.0):
        self.images = [pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                       for img in LIST_OF_EXPLOSION_IMAGE]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5
        self.counter = 0
        self.done = False

    def update(self):
        if not self.done:
            self.counter += 1
            if self.counter >= self.animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.done = True
                else:
                    self.image = self.images[self.index]
                    self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen, offset=(0, 0)):
        if not self.done:
            screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

