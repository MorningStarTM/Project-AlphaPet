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
        self.vibration_timer = 0
        self.vibration_interval = 200  # Interval to trigger the vibration wave
        self.vibration_radius = 100  # Initial radius of vibration wave
        self.vibration_active = False
        self.vibration_max_radius = 300  # Max radius of vibration wave
        self.vibration_growth_rate = 2
        self.vibration_waves = []  # List to store active vibration waves
        self.wave_cooldown = 500  # Time between waves in milliseconds
        self.last_wave_time = 0
        self.laser_cooldown = 200  # Cooldown duration in ms
        self.laser_fire_duration = 300  # Fire duration in ms
        self.laser_active = False  # Is laser currently active?
        self.last_laser_fire_time = 0  # 
        self.laser_timer = 0
        # Initialize four protector ships with different angles
        self.protectors = [
            ProtectorShip(self, player, math.radians(45)),   # Right side, protector 1
            ProtectorShip(self, player, math.radians(140)),  # Left side, protector 1
            ProtectorShip(self, player, math.radians(245)),  # Left side, protector 2
            ProtectorShip(self, player, math.radians(325))   # Right side, protector 2
        ]


    def update(self):
        # Update all protectors
        for protector in self.protectors:
            protector.update()

        if self.is_dead:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return  # Stop updating if explosion is done
            return  # Skip further update if the boss is dead

        # Calculate the angle to the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)

        # Update protector ships
        for ship in self.protectors:
            ship.update()

        # Update the position based on the angle
        self.rect.x += math.cos(self.angle) * self.speed

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT - 400:
            self.rect.bottom = SCREEN_HEIGHT - 400

        

        # Check if health is depleted
        if self.health <= 0:
            self.trigger_explosion()

        # Handle vibration wave attack
        """self.vibration_timer += 1
        print(self.vibration_timer)
        if self.vibration_timer >= self.vibration_interval:
            self.activate_vibration_wave()"""
        
        self.vibration_timer += 1
        if self.vibration_timer >= 300:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_wave_time > self.wave_cooldown:
                self.trigger_vibration_wave()
                self.last_wave_time = current_time
            if self.vibration_timer == 400:
                self.vibration_timer = 0
                del self.vibration_waves[-1]


        # Update all active vibration waves
        for wave in self.vibration_waves[:]:
            wave.update()
            if wave.radius > max(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.vibration_waves.remove(wave)  

        if self.vibration_active:
            self.vibration_radius += self.vibration_growth_rate
            if self.vibration_radius > self.vibration_max_radius:
                self.vibration_active = False  # Deactivate after reaching max radius

        # Collision detection with player and vibration wave
        if self.vibration_active:
            self.check_vibration_collision()

        # Fire the laser weapon if it's time
        self.laser_timer += 1
        print(self.laser_timer)
        if self.laser_timer >= 300:
            self.fire_laser()
            if self.laser_timer >= 400:
                self.laser_timer = 0
                self.laser_active = False



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

    def fire_laser(self):
        """Activate the laser weapon and manage its state."""
        self.laser_active = True
        # Set the laser duration
        self.last_laser_fire_time = pygame.time.get_ticks()

    def draw_laser(self, screen):
        """Draw the laser beam when active."""
        if self.laser_active:
            # Calculate the end position of the laser beam
            laser_length = SCREEN_HEIGHT  # Customize the length as needed
            end_x1 = self.rect.centerx-50 + math.sin(0) * laser_length
            end_y1 = self.rect.centery + math.cos(0) * laser_length
            
            end_x2 = self.rect.centerx+50 + math.sin(0) * laser_length

            # Draw the laser beam using the color from const.py (assuming it's stored as LASER_COLOR)
            pygame.draw.line(screen, ICE_LASER_COLOR, (self.rect.centerx-50, self.rect.centery), (end_x1, end_y1), 4)
            pygame.draw.line(screen, ICE_LASER_COLOR, (self.rect.centerx+50, self.rect.centery), (end_x2, end_y1), 4)
            # Handle damage or interactions with the player
            if self.rect.colliderect(self.player.rect):
                self.player.health -= 1  # Example: Decrease player health when hit by the laser


    def draw(self, screen):
        self.draw_laser(screen)
        
        for protector in self.protectors:
            protector.draw(screen)
               
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
        for ship in self.protectors:
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
    def __init__(self, boss, player, angle_offset):
        self.image = FX100
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.boss = boss
        self.player = player
        self.angle = angle_offset  # Starting angle for the protector
        self.orbit_radius = 120  # Distance from the boss
        self.speed = 1
        self.health = 100  # Health of the protector
        self.bullets = pygame.sprite.Group()
        self.shoot_timer = 0
        self.shoot_interval = 90  # Protector ships shoot less frequently

        # Set initial position based on angle
        self.rect.x = self.boss.rect.centerx + math.cos(self.angle) * self.orbit_radius
        self.rect.y = self.boss.rect.centery + math.sin(self.angle) * self.orbit_radius

    def update(self):
        # Move in a circular pattern around the boss
        self.angle += 0.01  # Controls the speed of rotation
        self.rect.x = self.boss.rect.centerx + math.cos(self.angle) * self.orbit_radius
        self.rect.y = self.boss.rect.centery + math.sin(self.angle) * self.orbit_radius

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

    def take_damage(self, damage):
        """Reduce protector's health and check if it should be destroyed."""
        self.health -= damage
        if self.health <= 0:
            self.vanish()

    def vanish(self):
        """Vanish the protector."""
        if self in self.boss.protectors:
            self.boss.protectors.remove(self)  # Remove from boss's protector list

    def shoot(self):
        """Shoot bullets towards the player."""
        angle_to_player = math.atan2(self.player.rect.centery - self.rect.centery,
                                     self.player.rect.centerx - self.rect.centerx)
        bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, angle_to_player, color=YELLOW)
        self.bullets.add(bullet)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)

        if self.health > 0:
            health_bar_width = 100
            health_bar_height = 12
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 5

            # Draw the background of the health bar
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            # Draw the current health of the enemy
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 400) * health_bar_width, health_bar_height))

        screen.blit(self.image, self.rect)
