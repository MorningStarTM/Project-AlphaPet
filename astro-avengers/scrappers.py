import pygame
import random
import math
from const import *
from player import Player


LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT)

SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]


class Scrapper:
    def __init__(self, player:Player, segment):
        self.image = SCRAPPER_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.segment = segment  # Segment that the enemy is restricted to
        self.player = player  # Store reference to the player
        self.pet = self.player.pet
        self.rect.x = random.randint(segment.left, segment.right - self.rect.width)
        self.rect.y = random.randint(-200, -50)  # Start at the top of the segment
        self.speed = 10  # Speed of the enemy
        self.health = 50  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead
        self.attack_distance = 50  # Distance within which it attacks the player
        self.attack_damage = 10  # Damage dealt to the player
        self.bounce_force = 60
        self.entered_screen = False
        self.mask = pygame.mask.from_surface(self.image)

    def rotate_towards(self, target_rect):
        """Calculate the angle to face the target."""
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        angle_to_target = math.degrees(math.atan2(dy, dx)) - 90  # Adjust for image orientation
        self.angle = angle_to_target % 360

    def move(self):
        """Move the scrapper according to its velocity and angle."""
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.rect.y -= vertical
        self.rect.x += horizontal

        # Ensure the scrapper stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        if self.is_dead:
            if self.explosion:
                self.explosion.update()
                if self.explosion.done:
                    return  # Stop updating if explosion is done
            return  # Skip further update if the enemy is dead
        

        dist_to_player = math.hypot(self.player.rect.centerx - self.rect.centerx, self.player.rect.centery - self.rect.centery)
        dist_to_pet = math.hypot(self.pet.rect.centerx - self.rect.centerx, self.pet.rect.centery - self.rect.centery)

        if dist_to_pet < dist_to_player:
            target = self.pet
        else:
            target = self.player


        # Calculate the angle to the player
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
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

        if self.collide(self.player):
            self.bounce()

        if not self.entered_screen:
            if self.rect.top >= 0:
                self.entered_screen = True
            else:
                self.rect.y += self.speed  # Move down into the screen
                return
            
    
    def rotate(self, angle):
        """ Rotate the enemy image to face the player """
        rotated_image = pygame.transform.rotate(self.original_image, -math.degrees(angle))
        self.rect = rotated_image.get_rect(center=self.rect.center)  # Adjust rect position
        self.image = rotated_image

    def draw(self, screen):
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

    def collide(self, player):
        """Check for collision with the player."""
        # Use rect collision detection
        return self.rect.colliderect(player.rect)
    

    def collide_missile(self, missile):
        """Handle collision with bullets."""
        if self.rect.colliderect(missile.rect):
            self.health -= missile.damage  # Reduce health for each collision
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
        
        # Optionally: Reduce health or mark scrapper as dead if necessary
        


    def attack(self, player):
        """Handle the attack on the player."""
        if self.collide(player):
            player.health -= self.attack_damage  # Reduce player's health
            # Optionally, remove the scrapper or handle other consequences of the attack
            self.rect.y = SCREEN_HEIGHT + self.rect.height  # Move off-screen or handle removal



class ScrapperGroup:
    def __init__(self, player:Player):
        self.player = player
        self.pet = self.player.pet
        self.segments = SEGMENTS  # Segments to allocate enemies
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 300  # Frames between each spawn
        self.min_distance = 50  # Minimum distance between scrappers
        self.arc_radius = 150  # Radius of the arc shape
        self.arc_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Center of the arc
        
        self.initialize_scrappers()

    def create_group(self):
        # Shuffle segments and create enemies in segments
        random.shuffle(self.segments)
        return [Scrapper(self.player, self.segments[i % len(self.segments)]) for i in range(10)]
    
    def initialize_scrappers(self):
        """Initialize scrappers in an arc shape."""
        num_scrappers = 10  # Number of scrappers in the group
        angle_step = 360 / num_scrappers
        
        for i in range(num_scrappers):
            angle = math.radians(i * angle_step)
            x = self.arc_center[0] + self.arc_radius * math.cos(angle)
            y = self.arc_center[1] + self.arc_radius * math.sin(angle)
            
            # Choose a segment for each scrapper
            segment = random.choice(self.segments)
            scrapper = Scrapper(self.player, segment)
            scrapper.rect.center = (x, y)
            self.enemies.append(scrapper)

    
    def maintain_distance(self):
        """Ensure scrappers maintain a minimum distance from each other."""
        for i, scrapper1 in enumerate(self.enemies):
            for scrapper2 in self.enemies[i + 1:]:
                distance = math.hypot(scrapper1.rect.centerx - scrapper2.rect.centerx,
                                      scrapper1.rect.centery - scrapper2.rect.centery)
                if distance < self.min_distance:
                    # Move scrapper2 away from scrapper1
                    angle = math.atan2(scrapper2.rect.centery - scrapper1.rect.centery,
                                       scrapper2.rect.centerx - scrapper1.rect.centerx)
                    move_x = (self.min_distance - distance) * math.cos(angle)
                    move_y = (self.min_distance - distance) * math.sin(angle)
                    scrapper2.rect.x += move_x
                    scrapper2.rect.y += move_y


    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            while len(self.enemies) < 5:
                segment = random.choice(self.segments)
                self.enemies.append(Scrapper(self.player, segment))

    def update(self):
        self.manage_spawn()  # Manage enemy spawning
        
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy is off-screen
            if enemy.rect.top > SCREEN_HEIGHT and not enemy.is_dead:
                self.enemies.remove(enemy)
                # Optionally: Add new enemies to keep the group size constant
                segment = random.choice(self.segments)
                new_scrapper = Scrapper(self.player, segment)
                self.enemies.append(new_scrapper)
        
        # Maintain distance between scrappers
        self.maintain_distance()

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
