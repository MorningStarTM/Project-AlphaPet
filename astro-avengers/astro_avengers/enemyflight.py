import pygame
import os
from astro_avengers.const import *  # Import constants such as SCREEN_WIDTH, SCREEN_HEIGHT, etc.
from astro_avengers.player import Player  # Import Player class
import random
from astro_avengers.bullet import EnemyBullet, DecepticonBullet
import math
from astro_avengers.explosion import Explosion

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
        self.rect.y = 0  # Start at the top of the segment
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        #self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead
        self.angle = 0
        self.bullets = pygame.sprite.Group()
        self.bounce_distance = 4
        self.bounce_force = 0.8
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.is_dead:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return  # Stop updating if explosion is done
            return  # Skip further update if the enemy is dead
        
        # Calculate the distance to the player
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance_to_player = math.hypot(dx, dy)
        
        min_distance_from_player = 300  # Minimum safe distance from the player
        
        if distance_to_player < min_distance_from_player:
            # If too close, move away from the player
            angle = math.atan2(dy, dx)
            self.rect.x -= math.cos(angle) * self.speed
            self.rect.y -= math.sin(angle) * self.speed
        else:
            # Move toward the player if safe distance is maintained
            self.angle = math.atan2(dy, dx)
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
            self.bounce()

    

LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)

SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]

class EnemyGroup:
    def __init__(self, player):
        self.player = player
        self.segments = SEGMENTS  # Segments to allocate enemies
        self.enemies = [] #self.create_group()
        self.spawn_timer = 0
        self.spawn_interval = 300  # Frames between each spawn
        self.arc_radius = 150  # Radius of the arc shape
        self.arc_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.min_distance = 3
        self.initialize_enemies()

    def create_group(self):
        # Shuffle segments and create enemies in segments
        random.shuffle(self.segments)
        return [DummyEnemyFlight(self.player, self.segments[i % len(self.segments)]) for i in range(5)]
    
    def initialize_enemies(self):
        """Initialize scrappers in an arc shape."""
        num_scrappers = 5  # Number of scrappers in the group
        angle_step = 360 / num_scrappers
        
        for i in range(num_scrappers):
            angle = math.radians(i * angle_step)
            x = self.arc_center[0] + self.arc_radius * math.cos(angle)
            y = self.arc_center[1] + self.arc_radius * math.sin(angle)
            
            # Choose a segment for each scrapper
            segment = random.choice(self.segments)
            scrapper = DummyEnemyFlight(self.player, segment)
            scrapper.rect.center = (x, y)
            self.enemies.append(scrapper)

    
    def maintain_distance_(self):
        """Ensure scrappers maintain a minimum distance from each other."""
        for i, enemy1 in enumerate(self.enemies):
            for enemy2 in self.enemies[i + 1:]:
                distance = math.hypot(enemy1.rect.centerx - enemy1.rect.centerx,
                                      enemy1.rect.centery - enemy1.rect.centery)
                if distance < self.min_distance:
                    # Move scrapper2 away from scrapper1
                    angle = math.atan2(enemy2.rect.centery - enemy1.rect.centery,
                                       enemy2.rect.centerx - enemy1.rect.centerx)
                    move_x = (self.min_distance - distance) * math.cos(angle)
                    move_y = (self.min_distance - distance) * math.sin(angle)
                    enemy2.rect.x += move_x
                    enemy2.rect.y += move_y
    
    def maintain_distance(self):
        """Ensure enemies maintain a minimum distance from each other."""
        min_distance = 80  # Adjust this value based on spacing needs
        for i, enemy1 in enumerate(self.enemies):
            for enemy2 in self.enemies[i + 1:]:
                distance = math.hypot(enemy1.rect.centerx - enemy2.rect.centerx,
                                    enemy1.rect.centery - enemy2.rect.centery)
                if distance < min_distance:
                    # Move enemy2 away from enemy1
                    angle = math.atan2(enemy2.rect.centery - enemy1.rect.centery,
                                    enemy2.rect.centerx - enemy1.rect.centerx)
                    move_x = (min_distance - distance) * math.cos(angle)
                    move_y = (min_distance - distance) * math.sin(angle)
                    enemy2.rect.x += move_x
                    enemy2.rect.y += move_y



    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 5:
                segment = random.choice(self.segments)
                self.enemies.append(DummyEnemyFlight(self.player, segment))

    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                segment = random.choice(self.segments)
                self.enemies.append(DummyEnemyFlight(self.player, segment))
        
        self.maintain_distance()

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
