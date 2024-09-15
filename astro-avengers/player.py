from const import *
from bullet import Bullet, ImageEnemyBullet
from missile import Missile
import math

class Player:
    def __init__(self):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.bullets = []
        self.missiles = []
        self.life = 3
        self.ammunition = 500
        self.shield = False
        self.missile_count = 10
        self.health = 100
        self.bullet_type = 0  
        self.missile_type = 0
        

    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Ensure the player stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def fire_bullet(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_type)
        self.bullets.append(bullet)

    def launch_missile(self):
        if self.missile_count != 0:
            missile = Missile(self.rect.centerx, self.rect.top, self.missile_type)
            self.missiles.append(missile)
            self.missile_count -= 1

    def cycle_bullet_type(self):
        """Cycles through available bullet types"""
        self.bullet_type = (self.bullet_type + 1) % 3  # Assuming 3 types: normal, double, golden
        print(self.bullet_type)

    def cycle_missile_type(self):
        """Cycles through available bullet types"""
        self.missile_type = (self.missile_type + 1) % 2  
        print(self.missile_type)


    
    def update(self):

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        
        # Update missiles
        for missile in self.missiles:
            missile.update()
            if missile.rect.bottom < 0:
                self.missiles.remove(missile)
                


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        for missile in self.missiles:
            missile.draw(screen)



def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)


def check_collisions(player, enemies):
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.life -= 1
            
    