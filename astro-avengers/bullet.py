from const import *

class Bullet:
    def __init__(self, x, y):
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)



class EnemyBullet:
    def __init__(self, x, y):
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)



class DoubleBullet:
    def __init__(self, x, y):
        self.image = DOUBLE_BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)