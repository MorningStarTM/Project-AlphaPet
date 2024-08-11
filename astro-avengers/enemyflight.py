import pygame
import os
from const import *  # Import constants such as SCREEN_WIDTH, SCREEN_HEIGHT, etc.
from player import Player  # Import Player class
import random
from bullet import EnemyBullet
import math


class EnemyFlight:
    def __init__(self, player):
        self.image = ENEMY_FLIGHT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)
        self.speed = 3
        self.health = 100
        self.shoot_timer = 0
        self.shoot_interval = 60
        self.bullets = []
        self.player = player  # Pass the player to the enemy

    def move(self):
        # Move towards the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx /= distance
            dy /= distance
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        if self.shoot_timer <= 0:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullets.append(bullet)
            self.shoot_timer = self.shoot_interval
        else:
            self.shoot_timer -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def update(self, player):
        self.move()
        self.shoot()
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        self.player = player  # Update player reference if needed
    



class DummyEnemyFlight:
    def __init__(self, player, segment):
        self.image = ENEMY_FLIGHT_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.segment = segment  # Segment that the enemy is restricted to
        self.player = player  # Store reference to the player
        self.rect.x = random.randint(segment.left, segment.right - self.rect.width)
        self.rect.y = random.randint(segment.top, segment.bottom - self.rect.height)
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []

    def update(self):
        # Calculate the angle to the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        
        # Update the position based on the angle
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed
        
        # Ensure the enemy stays within its segment
        if self.rect.left < self.segment.left:
            self.rect.left = self.segment.left
        if self.rect.right > self.segment.right:
            self.rect.right = self.segment.right
        if self.rect.top < self.segment.top:
            self.rect.top = self.segment.top
        if self.rect.bottom > self.segment.bottom:
            self.rect.bottom = self.segment.bottom
        
        # Rotate the image to face the player
        self.rotate(angle - math.pi / 2)
        
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

LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)

SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]

class EnemyGroup:
    def __init__(self, player):
        self.player = player
        self.segments = SEGMENTS  # Segments to allocate enemies
        self.enemies = self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 300  # Frames between each spawn

    def create_group(self):
        # Shuffle segments and create enemies in segments
        random.shuffle(self.segments)
        return [DummyEnemyFlight(self.player, self.segments[i % len(self.segments)]) for i in range(5)]

    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Optionally: Remove off-screen enemies and add new enemies
            self.enemies = [enemy for enemy in self.enemies if enemy.rect.top <= SCREEN_HEIGHT]
            while len(self.enemies) < 5:
                segment = random.choice(self.segments)
                self.enemies.append(DummyEnemyFlight(self.player, segment))

    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen or other conditions
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                segment = random.choice(self.segments)
                self.enemies.append(DummyEnemyFlight(self.player, segment))

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
