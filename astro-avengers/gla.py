#Gaurd Life Ammunation
from const import *
import random
from player import Player
from pet import NewPet


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




def check_gla_collisions(player:Player, pet:NewPet, shields, lives, ammunitions):
    for shield in shields:
        if player.rect.colliderect(shield.rect) or pet.rect.colliderect(shield.rect):
            player.shield = 400
            shields.remove(shield)
    
    for life in lives:
        if player.rect.colliderect(life.rect) or pet.rect.colliderect(life.rect):
            if player.health != 100:
                player.health += 20
                pet.health += 5
                lives.remove(life)
            if player.health > 100 or pet.health > 100:
                player.health = 100
                pet.health = 100
    
    for ammunition in ammunitions:
        if player.rect.colliderect(ammunition.rect) or pet.rect.colliderect(ammunition.rect):
            player.missile_count += 5
            ammunitions.remove(ammunition)

    