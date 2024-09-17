import pygame
import math
import random
from const import *
from explosion import Explosion
from bullet import DecepticonBullet

class DiamondHead:
    def __init__(self, player):
        self.image = DIAMOND_HEAD
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.player = player  # Store reference to the player
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 0  # Start at the top of the segment
        self.speed = 3  # Speed of the enemy
        self.health = 400  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        #self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead
        self.angle = 0
        self.bounce_distance = 4
        self.bullets = pygame.sprite.Group()

    def update(self):
        if self.is_dead:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return  # Stop updating if explosion is done
            return  # Skip further update if the enemy is dead
        
        # Calculate the angle to the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        self.angle = math.atan2(dy, dx)
        
        # Update the position based on the angle
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT-400:
            self.rect.bottom = SCREEN_HEIGHT-400
        
        # Rotate the image to face the player
        self.rotate(self.angle - math.pi / 2)
        
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

        # Check if health is depleted
        if self.health <= 0:
            self.trigger_explosion()


    def trigger_explosion(self):
        """Trigger the explosion immediately and mark the enemy as dead"""
        if not self.explosion:
            self.explosion = Explosion(self.rect.centerx, self.rect.centery)
            self.is_dead = True  # Set the flag to indicate the enemy is dead

    def rotate(self, angle):
        """ Rotate the enemy image to face the player """
        rotated_image = pygame.transform.rotate(self.original_image, -math.degrees(angle))
        self.rect = rotated_image.get_rect(center=self.rect.center)  # Adjust rect position
        self.image = rotated_image

    def shoot(self):
        # Fire three bullets: one straight, and two at ±45 degrees
        angles = [self.angle, self.angle + math.radians(25), self.angle - math.radians(25)]
        
        for angle in angles:
            bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, angle, color=YELLOW)
            self.bullets.add(bullet)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
            
        if self.explosion:
            self.explosion.draw(screen)
            if self.explosion.done:
                return  # Stop drawing if explosion is done

        screen.blit(self.image, self.rect)

        # Draw health bar
        if self.health > 0:
            health_bar_width = 70
            health_bar_height = 5
            health_bar_x = self.rect.centerx - health_bar_width // 2
            health_bar_y = self.rect.top - 5

            # Draw the background of the health bar
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            # Draw the current health of the enemy
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 400) * health_bar_width, health_bar_height))

    
    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 5  # Reduce health for each collision
            return True
        return False
    
    def bounce(self):
        """Bounce backward upon collision."""
        # Calculate the direction to move backward from the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1  # Prevent division by zero
        
        # Normalize the direction
        move_x = (dx / distance) * self.bounce_force
        move_y = (dy / distance) * self.bounce_force
        
        # Move the scrapper backward
        self.rect.x -= move_x
        self.rect.y -= move_y

    def collide_player(self, player):
        if self.rect.colliderect(player.rect):
            self.bounce(player)



class DiamondHeadGroup:
    def __init__(self, player):
        self.player = player
        self.enemies = self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 8000  # Frames between each spawn

    def create_group(self):
        # Shuffle segments and create enemies in segments
        return [DiamondHead(self.player)]
    

    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 5:
                self.enemies.append(DiamondHead(self.player))

    
    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                self.enemies.append(DiamondHead(self.player))

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
