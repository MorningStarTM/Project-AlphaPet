from const import *
import math
from explosion import Explosion


class Missile:
    def __init__(self, x, y, flag=None):
        self.image = MISSILE_IMAGE
        if flag == 1:
            self.image = ARC_MISSILE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
        self.damage = 10
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)





class Nuclear_Missile:
    def __init__(self, x, y, flag=None):
        self.image = NUCLEAR_MISSILE_IMAGE
        if flag == 1:
            self.image = ARC_MISSILE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 8
        self.damage = 100
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HomingMissile:
    def __init__(self, x, y, enemies, flag=None):
        self.image = HOMING_MISSILE_IMAGE if flag != 1 else ARC_MISSILE_IMAGE
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.x, self.y = x, y
        self.speed = 5
        self.angle = 10  # Start facing up
        self.enemies = enemies
        self.target = None
        self.explosion = None
        self.active = True
        self.rotation_speed = 6

    def find_nearest_target(self):
        nearest = None
        min_dist = float('inf')
        for enemy in self.enemies:
            if hasattr(enemy, "is_dead") and enemy.is_dead:
                continue
            dist = math.hypot(enemy.rect.centerx - self.x, enemy.rect.centery - self.y)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest

    def update(self):
        if not self.active:
            if self.explosion:
                self.explosion.update()
            return

        # Track target
        if not self.target or getattr(self.target, "is_dead", False):
            self.target = self.find_nearest_target()
            if not self.target:
                self.y -= self.speed
                self.rect.center = (self.x, self.y)
                return

        # Angle to target
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        desired_angle = math.degrees(math.atan2(dy, dx))
        angle_diff = (desired_angle - self.angle + 180) % 360 - 180
        self.angle += max(-self.rotation_speed, min(self.rotation_speed, angle_diff))
        self.angle %= 360

        # Move forward based on current angle
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)
        self.rect.center = (self.x, self.y)

        # Rotate image
        self.image = pygame.transform.rotate(self.original_image, -(self.angle - 270))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Collision check
        for enemy in self.enemies:
            if self.rect.colliderect(enemy.rect):
                if hasattr(enemy, "health"):
                    enemy.health -= 50
                self.trigger_explosion()
                break

        # Off-screen cleanup
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False

    def trigger_explosion(self):
        self.explosion = Explosion(self.x, self.y)
        self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)
        elif self.explosion and not self.explosion.done:
            self.explosion.draw(screen)
