import pygame
import random
import math
from const import *
from explosion import Explosion
from bullet import EnemyBullet, DecepticonBullet


class Doubler:
    def __init__(self, player, segment):
        self.image = DOUBLER_IMAGE
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
        self.bullets = pygame.sprite.Group()
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.image)

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
        
        # Ensure the enemy stays within its segment
        if self.rect.left < self.segment.left:
            self.rect.left = self.segment.left
        if self.rect.right > self.segment.right:
            self.rect.right = self.segment.right
        if self.rect.top < self.segment.top:
            self.rect.top = self.segment.top
        if self.rect.bottom > self.segment.bottom:
            self.rect.bottom = self.segment.bottom

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
            self.is_dead = True
            self.trigger_explosion()
        
        self.maintain_distance_from_player()


    def maintain_distance_from_player(self, min_distance=200):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        
        if distance < min_distance:
            # Calculate direction away from the player
            if distance == 0:
                distance = 1  # Avoid division by zero
            
            move_x = (dx / distance) * (min_distance - distance)
            move_y = (dy / distance) * min_distance * 0.1  # Adjust vertically to ensure backward movement
            
            # Move the Doubler away from the player
            self.rect.x -= move_x
            self.rect.y -= move_y
            
            # Keep the enemy within the segment after adjusting
            self.rect.clamp_ip(self.segment)


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
        bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, self.angle, color=YELLOW)
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
    



class DoublerGroup:
    def __init__(self, player):
        self.player = player
        self.segments = SEGMENTS  # Segments to allocate enemies
        self.enemies = self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 300  # Frames between each spawn

    def create_group(self):
        # Shuffle segments and create enemies in segments
        random.shuffle(self.segments)
        return [Doubler(self.player, self.segments[i % len(self.segments)]) for i in range(2)]

    def manage_spawn(self):
        dead_count = sum(enemy.is_dead for enemy in self.enemies)

        if dead_count >= 2:
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 2:  # <-- instead of <1, now <2
                segment = random.choice(self.segments)
                self.enemies.append(Doubler(self.player, segment))



    def update(self):
        dead_count = len(self.enemies)
        print(dead_count)
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
            
        if dead_count == 0:
            # Optionally: Add new enemies to keep the group size constant
            while len(self.enemies) < 2:  # <-- instead of <1, now <2
                segment = random.choice(self.segments)
                self.enemies.append(Doubler(self.player, segment))

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
