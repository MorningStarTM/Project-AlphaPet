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
        self.attack_cooldown = 100000  # Cooldown for moving downwards to attack
        self.last_attack_time = 0  # Timer for moving on y-axis to attack
        self.original_y = self.rect.y  # Store the initial y position
        self.attack_time = 0  # Track if predator is currently in attack mode
        self.is_attacking = False
        self.down_time = 0


    def update(self):
                
        # Handle movement on the x-axis to track the player
        self.rect.x += (self.player.rect.centerx - self.rect.centerx) * 0.05  # Smoothly track player x-axis

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

        self.handle_attack()
        # Update predator bullets
        self.bullets.update()


    def handle_attack(self):
        """Handles predator moving down to attack and returning to its original position."""
        
        if self.is_attacking:
            self.attack_time += 1

            # Move predator down to the screen height for 200 frames
            if self.attack_time <= 200:
                self.rect.y += 5  # Move down
                if self.rect.y >= SCREEN_HEIGHT - self.rect.height:  # If predator reaches the screen bottom
                    self.rect.y = SCREEN_HEIGHT - self.rect.height  # Ensure it doesn't go beyond the screen

            # After 200 frames, move back up to the original position
            elif self.attack_time > 200 and self.rect.y > self.original_y:
                self.rect.y -= 5  # Move up to the original position

            # Stop attacking once back in the original position
            if self.rect.y <= self.original_y:
                self.rect.y = self.original_y  # Ensure it's exactly at the original position
                self.attack_time = 0  # Reset attack time
                self.is_attacking = False  # End attack mode
        else:
            # Initiate attack every `attack_cooldown`
            if pygame.time.get_ticks() - self.last_attack_time >= self.attack_cooldown:
                self.is_attacking = True  # Start attacking
                self.last_attack_time = pygame.time.get_ticks()  # Reset cooldown timer




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
    



class PredatorGroup:
    def __init__(self, player):
        self.player = player
        self.enemies = self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 8000  # Frames between each spawn

    def create_group(self):
        # Shuffle segments and create enemies in segments
        return [Predator(self.player)]
    

    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 5:
                self.enemies.append(Predator(self.player))


    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                self.enemies.append(Predator(self.player))

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)