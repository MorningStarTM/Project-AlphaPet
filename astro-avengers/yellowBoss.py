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

    def draw_vibration_wave(self, screen):
        """Draw the circular vibration wave around the boss."""
        if self.vibration_active:
            pygame.draw.circle(screen, WAVE_COLOR, self.rect.center, self.vibration_radius, 2)
