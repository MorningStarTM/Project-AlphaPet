import pygame
from const import *

class Explosion:
    def __init__(self, x, y):
        self.images = LIST_OF_EXPLOSION_IMAGE  # Load explosion images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5  # Adjust for how fast the explosion animates
        self.counter = 0
        self.done = False

    def update(self):
        """ Update the explosion animation """
        if not self.done:
            self.counter += 1
            if self.counter >= self.animation_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.done = True
                else:
                    self.image = self.images[self.index]

    def draw(self, screen):
        """ Draw the explosion on the screen """
        if not self.done:
            screen.blit(self.image, self.rect)