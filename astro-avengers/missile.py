from const import *
import math


class Missile:
    def __init__(self, x, y, flag=None):
        self.image = MISSILE_IMAGE
        if flag == 1:
            self.image = ARC_MISSILE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)