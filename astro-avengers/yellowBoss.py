import pygame
import os
import math
import random
from const import *
from bullet import *
from explosion import Explosion


class YellowBoss:
    def __init__(self, player):
        self.image = LASERER
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.player = player  # Store reference to the player
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 100  # Start at a fixed position
        self.speed = 4  # Speed of the boss
        self.health = 800  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the boss as dead
        self.angle = 0
        self.bounce_distance = 4
        self.bullets = pygame.sprite.Group()
        self.protector_ships = [ProtectorShip(self, player) for _ in range(4)]  # 4 protector ships
        self.vibration_timer = 0
        self.vibration_interval = 200  # Interval to trigger the vibration wave
        self.vibration_radius = 100  # Initial radius of vibration wave
        self.vibration_active = False
        self.vibration_max_radius = 300  # Max radius of vibration wave
        self.vibration_growth_rate = 2
        self.vibration_waves = []  # List to store active vibration waves
        self.wave_cooldown = 500  # Time between waves in milliseconds
        self.last_wave_time = pygame.time.get_ticks()


    def trigger_vibration_wave(self):
        new_wave = VibrationWave(self.rect.center)  # Start wave from boss center
        self.vibration_waves.append(new_wave)


    def activate_vibration_wave(self):
        """Activate the vibration wave around the boss."""
        self.vibration_active = True
        self.vibration_radius = 100  # Reset the radius for the wave

    def check_vibration_collision(self):
        """Check if the player collides with the vibration wave."""
        distance = math.hypot(self.player.rect.centerx - self.rect.centerx, 
                              self.player.rect.centery - self.rect.centery)
        if distance <= self.vibration_radius:
            self.player.health -= 1  # Reduce player health on collision with wave

    def trigger_vibration_wave(self):
        new_wave = VibrationWave(self.rect.center)  # Start wave from boss center
        self.vibration_waves.append(new_wave)

    def trigger_explosion(self):
        """Trigger the explosion immediately and mark the boss as dead."""
        if not self.explosion:
            self.explosion = Explosion(self.rect.centerx, self.rect.centery)
            self.is_dead = True  # Set the flag to indicate the boss is dead

    def shoot(self):
        """Fire bullets towards the player."""
        bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, self.angle, color=YELLOW)
        self.bullets.add(bullet)


    def draw(self, screen):
               
        # Draw all active vibration waves
        for wave in self.vibration_waves:
            wave.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        if self.explosion:
            self.explosion.draw(screen)
            if self.explosion.done:
                return  # Stop drawing if explosion is done

        # Draw protector ships
        for ship in self.protector_ships:
            ship.draw(screen)

        # Draw vibration wave if active
        #self.draw_vibration_wave(screen)

        # Draw boss
        screen.blit(self.image, self.rect)

        # Draw health bar
        if self.health > 0:
            health_bar_width = 100
            health_bar_height = 12
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 5

            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 800) * health_bar_width, health_bar_height))



class VibrationWave:
    def __init__(self, center, initial_radius=10, speed=5):
        self.center = center
        self.radius = initial_radius
        self.speed = speed  # How fast the radius expands

    def update(self):
        self.radius += self.speed  # Increase the radius over time

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), self.center, self.radius, 2)  # Yellow circle outline



class ProtectorShip:
    def __init__(self, boss, player):
        self.image = FX100
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.boss = boss
        self.player = player
        self.rect.x = random.randint(self.boss.rect.left - 50, self.boss.rect.right + 50)
        self.rect.y = self.boss.rect.y + 100
        self.angle = 0
        self.speed = 3
        self.bullets = pygame.sprite.Group()
        self.shoot_timer = 0
        self.shoot_interval = 90  # Protector ships shoot less frequently

    def update(self):
        # Move in a circular pattern around the boss
        dx = self.boss.rect.centerx - self.rect.centerx
        dy = self.boss.rect.centery - self.rect.centery
        self.angle += 0.05
        self.rect.x = self.boss.rect.centerx + math.cos(self.angle) * 100
        self.rect.y = self.boss.rect.centery + math.sin(self.angle) * 100

        # Handle shooting
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot()
            self.shoot_timer = 0

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

    def shoot(self):
        """Shoot bullets towards the player."""
        angle_to_player = math.atan2(self.player.rect.centery - self.rect.centery,
                                     self.player.rect.centerx - self.rect.centerx)
        bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, angle_to_player, color=YELLOW)
        self.bullets.add(bullet)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        screen.blit(self.image, self.rect)


