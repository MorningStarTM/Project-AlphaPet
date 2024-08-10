import pygame
import os
from const import *  # Import constants such as SCREEN_WIDTH, SCREEN_HEIGHT, etc.
from player import Player  # Import Player class
import random

class EnemyFlight(Player):
    def __init__(self):
        super().__init__()
        # Load enemy-specific image
        self.image = ENEMY_FLIGHT_IMAGE  # Replace with your enemy image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)  # Start above the screen
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health

    def move(self):
        # Move the enemy down the screen
        self.rect.y += self.speed

        # If the enemy moves off the bottom of the screen, reset its position
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-200, -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # Draw health bar
        if self.health > 0:
            health_bar_width = 40
            health_bar_height = 5
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 10

            # Draw the background of the health bar
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            # Draw the current health of the enemy
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 100) * health_bar_width, health_bar_height))

    def update(self):
        # Update the enemy position
        self.move()

    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False
