import pygame
from bullet import PetBullet, EnemyBullet
from const import *
import math
import random
from explosion import Explosion


# Screen Segments
LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-180)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-180)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-180)
SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, segment, scale_factor=0.9):
        super().__init__()
        self.player = player  # Reference to the player object
        self.segment = segment  # The segment this enemy is assigned to
        
        # Load and scale the image
        try:
            original_image = pygame.image.load(PET_IMAGE).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(original_image, (255, 0, 0), (25, 25), 25)
        
        self.original_image = pygame.transform.scale(
            original_image, 
            (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor))
        )
        self.image = self.original_image
        self.max_vel = 3
        self.vel = 0
        self.rotation_vel = 2
        self.angle = 45
        self.x, self.y = self.segment.center  # Start at the center of the assigned segment
        self.acceleration = 0.1
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 30
        self.shoot_timer = 0
        self.bounce_distance = 5
        self.explosion = None

    def rotate_towards_player(self):
        player_x, player_y = self.player.rect.center
        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        target_angle = math.degrees(math.atan2(-dy, dx))  # Calculate angle towards player
        self.angle = -target_angle + 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def trigger_explosion(self):
        """Trigger the explosion immediately and mark the enemy as dead"""
        if not self.explosion:
            self.explosion = Explosion(self.rect.centerx, self.rect.centery)
            self.is_dead = True  # Set the flag to indicate the enemy is dead


    def move_towards_player(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.max_vel
        horizontal = math.sin(radians) * self.max_vel

        # Move within the assigned segment
        self.x += horizontal
        self.y -= vertical
        self.rect.center = (self.x, self.y)

        # Ensure the enemy stays within its segment bounds
        if not self.segment.contains(self.rect):
            self.rect.clamp_ip(self.segment)  # Keep the rect within the segment bounds
            self.x, self.y = self.rect.center

    def shoot(self):
        if self.shoot_timer <= 0:
            bullet = PetBullet(self.x, self.y, self.angle)
            self.bullets.add(bullet)
            self.shoot_timer = self.shoot_cooldown

    def update_bullets(self):
        self.bullets.update()

    def update(self):
        self.rotate_towards_player()
        self.move_towards_player()
        self.shoot()
        self.update_bullets()
        self.shoot_timer = max(0, self.shoot_timer - 1)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        self.bullets.draw(screen)

        if self.explosion:
            self.explosion.draw(screen)
            if self.explosion.done:
                return  # Stop drawing if explosion is done

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


    def bounce(self, player):
        """Bounce the enemy back upon collision with the player."""
        # Calculate the direction to move away from the player
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        angle = math.atan2(dy, dx)
        
        # Move the enemy in the opposite direction
        self.rect.x += math.cos(angle) * self.bounce_distance
        self.rect.y += math.sin(angle) * self.bounce_distance


    def collide(self, bullet):
        if self.rect.colliderect(bullet.rect):
            self.health -= 10  # Reduce health for each collision
            return True
        return False
    
    def collide_player(self, player):
        if self.rect.colliderect(player.rect):
            self.bounce(player)


class Enemy2Group:
    def __init__(self, player):
        self.player = player
        self.segments = SEGMENTS
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 300  # Frames between each spawn
        self.min_distance = 50  # Minimum distance between enemies

        self.initialize_enemies()

    def initialize_enemies(self):
        # Create an enemy for each segment
        for segment in self.segments:
            enemy = Enemy(self.player, segment)
            self.enemies.append(enemy)

    def maintain_distance(self):
        """Ensure enemies maintain a minimum distance from each other."""
        for i, enemy1 in enumerate(self.enemies):
            for enemy2 in self.enemies[i + 1:]:
                distance = math.hypot(enemy1.rect.centerx - enemy2.rect.centerx,
                                      enemy1.rect.centery - enemy2.rect.centery)
                if distance < self.min_distance:
                    # Move enemy2 away from enemy1
                    angle = math.atan2(enemy2.rect.centery - enemy1.rect.centery,
                                       enemy2.rect.centerx - enemy1.rect.centerx)
                    move_x = (self.min_distance - distance) * math.cos(angle)
                    move_y = (self.min_distance - distance) * math.sin(angle)
                    enemy2.rect.x += move_x
                    enemy2.rect.y += move_y
                    # Ensure enemy2 stays within its segment
                    enemy2.rect.clamp_ip(enemy2.segment)

    def manage_spawn(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # Remove off-screen and dead enemies, and add new enemies if needed
            self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]
            while len(self.enemies) < 3:  # Ensure one enemy per segment
                segment = random.choice(self.segments)
                self.enemies.append(Enemy(self.player, segment))

    def update(self):
        self.manage_spawn()
        for enemy in self.enemies:
            enemy.update()
        self.maintain_distance()

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)




def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)

