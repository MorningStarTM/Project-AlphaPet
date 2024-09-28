import os
import random
import pygame
from explosion import Explosion
from bullet import *


class Predator:
    def __init__(self, player):
        self.image = PREDATOR
        self.rect = self.image.get_rect()
        self.player = player  # Reference to the player
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 0  # Start at the top
        self.speed = 5  # Movement speed
        self.health = 500  # Predator's health
        self.shoot_timer = 0
        self.laser_timer = 0
        self.laser_active = False  # Indicates if the laser is active
        self.laser_cooldown = 500  # Time between laser activations
        self.laser_duration = 300  # How long the laser stays active
        self.laser_color = PREDATOR_LASER  # Color from const.py
        self.bullets = pygame.sprite.Group()  # Group for predator bullets
        self.predator_bullet_interval = 40  # Time interval for firing predator bullets
        self.attack_cooldown = 1000  # Cooldown for moving downwards to attack
        self.last_attack_time = 0  # Timer for moving on y-axis to attack
        self.original_y = self.rect.y  # Store the initial y position
        self.is_attacking = False  # Track if predator is currently in attack mode

    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Handle movement on the x-axis to track the player
        self.rect.x += (self.player.rect.centerx - self.rect.centerx) * 0.05  # Smoothly track player x-axis

        # Handle periodic attack movement on y-axis
        """if not self.is_attacking and current_time - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = current_time

        if self.is_attacking:
            self.rect.y += self.speed  # Move downward to attack
            if self.rect.y >= self.player.rect.centery:  # Stop moving downwards after passing the player
                self.is_attacking = False
                self.rect.y = self.original_y  # Return to original position"""

        # Handle laser activation and deactivation
        self.laser_timer += 1
        if not self.laser_active and self.laser_timer >= self.laser_cooldown:
            self.activate_laser()
            self.laser_timer = 0

        if self.laser_active and self.laser_timer >= self.laser_duration:
            self.deactivate_laser()

        # Handle shooting predator bullets only when laser is inactive
        if not self.laser_active:
            self.shoot_timer += 1
            if self.shoot_timer >= self.predator_bullet_interval:
                self.shoot_predator_bullet()
                self.shoot_timer = 0

        # Update predator bullets
        self.bullets.update()


    def shoot_predator_bullet(self):
        """Fire the predator bullet."""
        bullet = PredatorBullet(x=self.rect.centerx, y=self.rect.centery, images=PREDATOR_BULLET_IMAGES)
        self.bullets.add(bullet)


    def activate_laser(self):
        """Activate the laser attack."""
        self.laser_active = True

    def deactivate_laser(self):
        """Deactivate the laser attack."""
        self.laser_active = False

    def draw_laser(self, screen):
        """Draw the laser if active."""
        if self.laser_active:
            laser_length = SCREEN_HEIGHT
            end_x = self.rect.centerx
            end_y = self.rect.centery + laser_length

            # Draw the laser beam
            pygame.draw.line(screen, self.laser_color, (self.rect.centerx, self.rect.centery), (end_x, end_y), 4)

            # Handle collision with player
            if self.rect.colliderect(self.player.rect):
                self.player.health -= 1  # Example: Decrease player health

    
    def draw(self, screen):
        """Draw the predator and its bullets."""
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw the laser beam
        self.draw_laser(screen)

    def collide(self, bullet):
        """Handle collision with bullets."""
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False