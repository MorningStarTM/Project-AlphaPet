import pygame
import random
import math
from const import *  # Assuming these are in const.py
from explosion import Explosion
from enemyflight import EnemyFlight, EnemyGroup
from bullet import EnemyBullet

class Decepticon:
    def __init__(self, player, segment):
        self.image = DECEPTICON_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.segment = segment  # Segment that the enemy is restricted to
        self.player = player  # Store reference to the player
        self.rect.x = random.randint(segment.left, segment.right - self.rect.width)
        self.rect.y = 0  # Start at the top of the segment
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead


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
        # Create an enemy bullet aimed at the player's position
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.bullets.append(bullet)

    def draw(self, screen):
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
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, (self.health / 100) * health_bar_width, health_bar_height))

    
    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 5  # Reduce health for each collision
            return True
        return False
    



class DecepticonGroup:
    def __init__(self, player):
        self.player = player
        self.segments = SEGMENTS  # Segments to allocate enemies
        self.enemies = self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 600  # Frames between each spawn

    def create_group(self):
        # Shuffle segments and create enemies in segments
        random.shuffle(self.segments)
        return [Decepticon(self.player, self.segments[i % len(self.segments)]) for i in range(3)]
    

    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 5:
                segment = random.choice(self.segments)
                self.enemies.append(Decepticon(self.player, segment))

    
    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                segment = random.choice(self.segments)
                self.enemies.append(Decepticon(self.player, segment))

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
