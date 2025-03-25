import pygame
import math
import random
from const import *
from explosion import Explosion
from bullet import DecepticonBullet, ImageEnemyBullet, AnimatedBullet

class DiamondHead:
    def __init__(self, player):
        self.image = DIAMOND_HEAD
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.player = player  # Store reference to the player
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 0  # Start at the top of the segment
        self.speed = 6  # Speed of the enemy
        self.health = 400  # Set initial health
        self.shoot_timer = 0
        self.laser_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        #self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead
        self.angle = 0
        self.bounce_distance = 4
        self.bullets = pygame.sprite.Group()
        self.has_ice_bullet = random.choice([True, False])  
        self.missiles = []
        self.missile_interval = 20

        self.laser_cooldown = 200  # Cooldown duration in ms
        self.laser_fire_duration = 1000  # Fire duration in ms
        self.laser_active = False  # Is laser currently active?
        self.last_laser_fire_time = 0  # 


    def update(self):
        current_time = pygame.time.get_ticks()  

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
        #self.rect.y += math.sin(self.angle) * self.speed
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT-400:
            self.rect.bottom = SCREEN_HEIGHT-400
        
        
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if self.player.rect.colliderect(bullet.rect):
                self.player.health -= 5
                self.bullets.remove(bullet)
            
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        # missile updated
        for missile in self.missiles:
            missile.update()
            if missile.rect.bottom < 0:
                self.missiles.remove(missile)

        # Handle shooting
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.launch()
            self.shoot_timer = 0
        
        """if self.shoot_timer >= self.missile_interval:
            self.launch()
            self.shoot_timer = 0"""

        # Check if health is depleted
        if self.health <= 0:
            self.trigger_explosion()

        # Fire the laser weapon if it's time
        self.laser_timer += 1
        #print(self.laser_timer)
        if self.laser_timer >= 300:
            self.fire_laser()
            if self.laser_timer >= 400:
                self.laser_timer = 0
                self.laser_active = False
        
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
            self.check_laser_hits_targets()



    def trigger_explosion(self):
        """Trigger the explosion immediately and mark the enemy as dead"""
        if not self.explosion:
            self.explosion = Explosion(self.rect.centerx, self.rect.centery)
            self.is_dead = True  # Set the flag to indicate the enemy is dead


    def triple_shoot(self):
        # Fire three bullets: one straight, and two at ±45 degrees
        angles = [self.angle, self.angle + math.radians(25), self.angle - math.radians(25)]
        
        for angle in angles:
            bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, angle, color=YELLOW)
            self.bullets.add(bullet)

    """def triple_shoot(self):
        bullet = DecepticonBullet(self.rect.centerx, self.rect.centery, angle, color=YELLOW)
        self.bullets.add(bullet)"""

    
    def launch(self):
        #missile = ImageEnemyBullet(self.rect.centerx, self.rect.centery, self.angle)
        missile = AnimatedBullet(self.rect.centerx, self.rect.centery, self.angle, images=ANIMATED_BULLET_IMAGES)
        self.missiles.append(missile)

    def draw(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)
        
        for missile in self.missiles:
            missile.draw(screen)
        
        self.draw_laser(screen)
            
        if self.explosion:
            self.explosion.draw(screen)
            if self.explosion.done:
                return  # Stop drawing if explosion is done
        screen.blit(self.image, self.rect)

        # Handle damage or interactions with the player
        if self.rect.colliderect(self.player.rect):
            self.player.health -= 1  # Example: Decrease player health when hit by the laser

        # Check for collision with the pet (if pet exists)
        if hasattr(self.player, 'pet') and self.rect.colliderect(self.player.pet.rect):
            self.player.pet.health -= 1  # Decrease pet health if hit by the laser

        # Draw health bar
        if self.health > 0:
            health_bar_width = 100
            health_bar_height = 12
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



    def line_rect_collision(self, line_start, line_end, rect):
        """Check if a line (laser) intersects with a rectangle (target)."""
        return rect.clipline(line_start, line_end)



    def check_laser_hits_targets(self):
        """Check if DiamondHead's laser hits the player or pet and apply damage."""
        if not self.laser_active:
            return

        laser_start_1 = (self.rect.centerx - 50, self.rect.centery)
        laser_end_1 = (laser_start_1[0], SCREEN_HEIGHT)

        laser_start_2 = (self.rect.centerx + 50, self.rect.centery)
        laser_end_2 = (laser_start_2[0], SCREEN_HEIGHT)

        # Check hit on player
        if self.line_rect_collision(laser_start_1, laser_end_1, self.player.rect) or \
        self.line_rect_collision(laser_start_2, laser_end_2, self.player.rect):
            self.player.health -= 1

        # Check hit on pet (if exists)
        if hasattr(self.player, "pet"):
            pet = self.player.pet
            if self.line_rect_collision(laser_start_1, laser_end_1, pet.rect) or \
            self.line_rect_collision(laser_start_2, laser_end_2, pet.rect):
                pet.health -= 1




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
