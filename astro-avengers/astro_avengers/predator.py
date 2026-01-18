import os
import random
import pygame
from astro_avengers.explosion import Explosion
from astro_avengers.bullet import *

class Laser:
    def __init__(self, start_pos, end_pos, color, width):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.width = width

    def update(self, new_end_pos=None):
        if new_end_pos:
            self.end_pos = new_end_pos  # Update end position if needed

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)



class Predator:
    def __init__(self, player):
        self.image = PREDATOR
        self.rect = self.image.get_rect()
        self.player = player  # Reference to the player
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 0  # Start at the top
        self.speed = 5  # Movement speed
        self.health = 2500  # Predator's health
        self.shoot_timer = 0
        self.laser_timer = 0
        self.bullets = []
        self.laser_active = False  # Indicates if the laser is active
        self.laser_cooldown = 500  # Time between laser activations
        self.laser_duration = 300  # How long the laser stays active
        self.laser_color = PREDATOR_LASER  # Color from const.py
        self.lasers = []  # List to store active lasers
        self.predator_bullet_interval = 40  # Time interval for firing predator bullets
        self.attack_cooldown = 100000  # Cooldown for moving downwards to attack
        self.last_attack_time = 0  # Timer for moving on y-axis to attack
        self.original_y = self.rect.y  # Store the initial y position
        self.attack_time = 0  # Track if predator is currently in attack mode
        self.is_attacking = False
        self.explosion = None  # Explosion instance, initialized to None
        self.is_dead = False  # Track if the predator is dead
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        # Handle explosion if the predator is dead
        if self.is_dead:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return  # Explosion is complete; stop updates for this predator
            return  # Skip further updates while explosion is active

        # Check if health is depleted and trigger explosion
        if self.health <= 0:
            self.trigger_explosion()
            return

        # Handle movement on the x-axis to track the player
        self.rect.x += (self.player.rect.centerx - self.rect.centerx) * 0.05

        # Update lasers to follow the predator's movement
        if self.laser_active:
            self.update_lasers()

        # Handle laser activation and deactivation
        self.laser_timer += 1
        if not self.laser_active and self.laser_timer >= self.laser_cooldown:
            self.activate_laser()
            self.laser_timer = 0

        if self.laser_active and self.laser_timer >= self.laser_duration:
            self.deactivate_laser()

        if not self.laser_active:
            self.shoot_timer += 1
            if self.shoot_timer >= self.predator_bullet_interval:
                self.shoot_predator_bullet()
                self.shoot_timer = 0

        # Handle other mechanics
        self.handle_attack()
        for bullet in self.bullets:
            bullet.update()



    def update_(self):
        # Handle movement on the x-axis to track the player
        self.rect.x += (self.player.rect.centerx - self.rect.centerx) * 0.05  # Smoothly track player x-axis

        
        if self.health <= 0 and not self.is_dead:
            print("Died")
            self.trigger_explosion()

        # Update lasers to follow the predator's movement
        if self.laser_active:
            self.update_lasers()

        # Handle laser activation and deactivation
        self.laser_timer += 1
        if not self.laser_active and self.laser_timer >= self.laser_cooldown:
            self.activate_laser()
            self.laser_timer = 0

        if self.laser_active and self.laser_timer >= self.laser_duration:
            self.deactivate_laser()

        if not self.laser_active:
            self.shoot_timer += 1
            if self.shoot_timer >= self.predator_bullet_interval:
                self.shoot_predator_bullet()
                self.shoot_timer = 0

        if self.is_dead or self.health < 0:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return
            return
                
        # Update other mechanics
        self.handle_attack()
        for bullet in self.bullets:
            bullet.update()


    def trigger_explosion(self):
        if not self.explosion:
            self.explosion = Explosion(self.rect.centerx, self.rect.centery, scale=2.5)
            self.bullets.clear()
            self.is_dead = True



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
        self.bullets.append(bullet)


    def activate_laser_(self):
        """Activate the laser attack."""
        self.laser_active = True

    def activate_laser(self):
        """Activate the laser attack."""
        self.laser_active = True
        # Create new laser beams aligned with the predator's current position
        spacing = 40  # Distance between lasers
        self.lasers = [
            Laser((self.rect.centerx - spacing, self.rect.centery + 50), (self.rect.centerx - spacing, SCREEN_HEIGHT), self.laser_color, 4),
            Laser((self.rect.centerx, self.rect.centery), (self.rect.centerx, SCREEN_HEIGHT), self.laser_color, 4),
            Laser((self.rect.centerx + spacing, self.rect.centery + 50), (self.rect.centerx + spacing, SCREEN_HEIGHT), self.laser_color, 4)
        ]

    def deactivate_laser(self):
        """Deactivate the laser attack."""
        self.laser_active = False
        self.lasers = []  # Clear active lasers



    def deactivate_laser_(self):
        """Deactivate the laser attack."""
        self.laser_active = False


    def draw_laser_(self, screen):
        """Draw the laser if active."""
        if self.laser_active:
            laser_length = SCREEN_HEIGHT
            end_x = self.rect.centerx
            end_y = self.rect.centery + laser_length

            # Draw the laser beam
            pygame.draw.line(screen, self.laser_color, (self.rect.centerx, self.rect.centery), (end_x, end_y), 4)
            pygame.draw.line(screen, self.laser_color, (self.rect.centerx-40, self.rect.centery+50), (end_x-40, end_y), 4)
            pygame.draw.line(screen, self.laser_color, (self.rect.centerx+40, self.rect.centery+50), (end_x+40, end_y), 4)

            # Handle collision with player
            if self.rect.centerx - 40 <= self.player.rect.centerx <= self.rect.centerx + 40 and self.player.rect.top <= end_y:
                self.player.health -= 1  # Decrease player health if within laser range

    def draw_laser(self, screen):
        """Draw the lasers if active."""
        for laser in self.lasers:
            laser.draw(screen)


    
    def draw(self, screen):
        """Draw the predator, its bullets, lasers, and explosion (if dead)."""
        
        # ✅ If dead, only draw explosion and return
        if self.is_dead:
            if self.explosion:
                self.explosion.draw(screen)
            return

        # 🟢 If alive, draw predator sprite and other stuff
        screen.blit(self.image, self.rect)

        for bullet in self.bullets:
            bullet.draw(screen)

        self.draw_laser(screen)

        # Draw health bar
        if self.health > 0:
            health_bar_width = 100
            health_bar_height = 12
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 5

            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 2500) * health_bar_width, health_bar_height))



    def collide(self, bullet):
        """Handle collision with bullets."""
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False
    

    def collide_missile(self, missile):
        """Handle collision with bullets."""
        if self.rect.colliderect(missile.rect):
            self.health -= missile.damage  # Reduce health for each collision
            return True
        return False
    
    def check_bullet_collisions(self):
        """Check for collisions between predator bullets and the player."""
        for bullet in self.bullets:
            if bullet.rect.colliderect(self.player.rect):
                if self.player.shield > 0:
                    self.player.health -= 2.5  # Decrease player health on bullet hit
                    bullet.kill()  # Remove the bullet after collision
                else:
                    self.player.health -= 2.5
                    bullet.kill()
    

    def update_lasers(self):
        """Update the laser positions to follow the predator's movement."""
        spacing = 40  # Distance between lasers
        for i, laser in enumerate(self.lasers):
            if i == 0:  # Left laser
                laser.start_pos = (self.rect.centerx - spacing, self.rect.centery + 50)
                laser.end_pos = (self.rect.centerx - spacing, SCREEN_HEIGHT)
            elif i == 1:  # Center laser
                laser.start_pos = (self.rect.centerx, self.rect.centery)
                laser.end_pos = (self.rect.centerx, SCREEN_HEIGHT)
            elif i == 2:  # Right laser
                laser.start_pos = (self.rect.centerx + spacing, self.rect.centery + 50)
                laser.end_pos = (self.rect.centerx + spacing, SCREEN_HEIGHT)

                


