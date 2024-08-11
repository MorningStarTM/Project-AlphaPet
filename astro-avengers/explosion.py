import pygame
from .const import *

class Explosion:
    def __init__(self, x, y):
        self.images = LIST_OF_EXPLOSION_IMAGE  # Load explosion images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5  # Adjust for how fast the explosion animates
        self.counter = 0
        self.done = False