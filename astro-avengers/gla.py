#Gaurd Life Ammunation
from const import *
import random


class Shield:
    def __init__(self):
        self.image = SHIELD_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)




class Life:
    def __init__(self):
        self.image = LIFE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)


class Ammunition:
    def __init__(self):
        self.image = AMMUNITION_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)




def check_gla_collisions(player, shields, lives, ammunitions):
    for shield in shields:
        if player.rect.colliderect(shield.rect):
            player.shield = True
            shields.remove(shield)
    
    for life in lives:
        if player.rect.colliderect(life.rect):
            player.life += 1
            lives.remove(life)
    
    for ammunition in ammunitions:
        if player.rect.colliderect(ammunition.rect):
            player.ammunition += 1
            ammunitions.remove(ammunition)

    