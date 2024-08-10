import pygame
import os
from const import *  # Import constants such as SCREEN_WIDTH, SCREEN_HEIGHT, etc.
from player import Player  # Import Player class
import random
from bullet import EnemyBullet
import math


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
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []

    def move(self):
        # Move the enemy down the screen
        self.rect.y += self.speed

        # If the enemy moves off the bottom of the screen, reset its position
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-200, -50)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)

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
        self.move()
        # Update bullets
        
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def fire_bullet(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.top)
        self.bullets.append(bullet)

    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False
    



class DummyEnemyFlight:
    def __init__(self, player):
        self.image = ENEMY_FLIGHT_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)  # Start above the screen
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []
        self.player = player  # Store reference to the player

    def update(self):
        # Calculate the angle to the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        
        # Update the position based on the angle
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed
        
        # Ensure the enemy stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        # Rotate the image to face the player
        self.rotate(angle-90)
        
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        # Handle shooting
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0

    def rotate(self, angle):
        """ Rotate the enemy image to face the player """
        rotated_image = pygame.transform.rotate(self.original_image, -math.degrees(angle))
        self.rect = rotated_image.get_rect(center=self.rect.center)  # Adjust rect position
        self.image = rotated_image

    def shoot(self):
        # Create an enemy bullet aimed at the player's position
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.bullets.append(bullet)

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

    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False