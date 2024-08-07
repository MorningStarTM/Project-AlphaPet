import pygame
import os
from const import *  # Import constants such as SCREEN_WIDTH, SCREEN_HEIGHT, etc.
from player import Player  # Import Player class
import random

class EnemyFlight(Player):
    def __init__(self):
        super().__init__()
        # Load enemy-specific image
        self.image = ENEMY_FLIGHT_IMAGE # Replace with your enemy image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)  # Start above the screen
        self.speed = 3  # Speed of the enemy

    def move(self):
        # Move the enemy down the screen
        self.rect.y += self.speed

        # If the enemy moves off the bottom of the screen, reset its position
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-200, -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        # Update the enemy position
        self.move()