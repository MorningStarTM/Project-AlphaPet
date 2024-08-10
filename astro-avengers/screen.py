import pygame
import os
from player import Player
from enemyflight import EnemyFlight
from gla import Ammunition, Life, Shield, check_gla_collisions
from const import *



# Initialize Pygame
pygame.init()

# Screen dimensions


# Load the background image
BACKGROUND_IMAGE = pygame.image.load("assets\\screen\\bg.png")

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Astro Avenger")
        
        # Load the background image and create a flipped version
        self.bg_image = pygame.image.load("assets\\screen\\bg.png")
        self.bg_flipped = pygame.transform.flip(self.bg_image, False, True)
        
        # Initialize background positions
        self.bg_y1 = 0
        self.bg_y2 = -SCREEN_HEIGHT
        self.bg_speed = 2

    def draw_background(self):
        # Draw the original image
        self.screen.blit(self.bg_image, (0, self.bg_y1))
        # Draw the flipped image
        self.screen.blit(self.bg_flipped, (0, self.bg_y1 + SCREEN_HEIGHT))
        
        # Draw the original image again
        self.screen.blit(self.bg_image, (0, self.bg_y2))
        # Draw the flipped image again
        self.screen.blit(self.bg_flipped, (0, self.bg_y2 + SCREEN_HEIGHT))

    def move_background(self):
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed
        
        if self.bg_y1 >= SCREEN_HEIGHT:
            self.bg_y1 = self.bg_y2 - SCREEN_HEIGHT
        if self.bg_y2 >= SCREEN_HEIGHT:
            self.bg_y2 = self.bg_y1 - SCREEN_HEIGHT

    def update_screen(self):
        self.move_background()
        self.draw_background()



def draw_hud(screen, player):
    hud_rect = pygame.Rect(SCREEN_WIDTH - HUD_WIDTH, 0, HUD_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, LIGHT_GRAY, hud_rect)

    # Draw health bar
    health_bar_rect = pygame.Rect(SCREEN_WIDTH - HUD_WIDTH + 10, 10, 180, 20)
    pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
    pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH - HUD_WIDTH + 10, 10, player.life * 60, 20))

    # Draw shield bar
    shield_bar_rect = pygame.Rect(SCREEN_WIDTH - HUD_WIDTH + 10, 40, 180, 20)
    pygame.draw.rect(screen, (0, 0, 255), shield_bar_rect)
    pygame.draw.rect(screen, (0, 255, 255), (SCREEN_WIDTH - HUD_WIDTH + 10, 40, player.shield * 60, 20))

    # Draw missile count
    missile_text = pygame.font.SysFont(None, 24).render(f"Missiles: {player.ammunition}", True, BLACK)
    screen.blit(missile_text, (SCREEN_WIDTH - HUD_WIDTH + 10, 70))

    # Draw special bullet count (Placeholder for implementation)
    special_bullet_text = pygame.font.SysFont(None, 24).render("Special Bullets: 0", True, BLACK)
    screen.blit(special_bullet_text, (SCREEN_WIDTH - HUD_WIDTH + 10, 100))


def main():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    running = True
    
    enemies = [EnemyFlight() for _ in range(5)]


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        for enemy in enemies:
            enemy.update()
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)
        

        

        player.update()
        screen.update_screen()
        
        screen.screen.fill((0, 0, 0))

        for enemy in enemies:
            enemy.draw(screen.screen)

        screen.draw_background()
        player.draw(screen.screen)
        draw_hud(screen.screen, player)



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main2():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Astro Avenger ")

    player = Player()
    shields = [Shield() for _ in range(3)]
    lives = [Life() for _ in range(3)]
    ammunitions = [Ammunition() for _ in range(3)]
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)
        
        player.update()
        for shield in shields:
            shield.update()
            if shield.rect.top > SCREEN_HEIGHT:
                shield.reset_position()
        for life in lives:
            life.update()
            if life.rect.top > SCREEN_HEIGHT:
                life.reset_position()
        for ammunition in ammunitions:
            ammunition.update()
            if ammunition.rect.top > SCREEN_HEIGHT:
                ammunition.reset_position()
        
        check_gla_collisions(player, shields, lives, ammunitions)
        
        screen.fill((0, 0, 0))
        player.draw(screen)
        for shield in shields:
            shield.draw(screen)
        for life in lives:
            life.draw(screen)
        for ammunition in ammunitions:
            ammunition.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



def main3():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    running = True
    
    enemies = [EnemyFlight() for _ in range(5)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        # Update player and enemies
        player.update()
        for enemy in enemies:
            enemy.update()
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)

        # Update and draw the background
        screen.update_screen()
        
        # Clear the screen and redraw background
        screen.screen.fill((0, 0, 0))
        screen.draw_background()
        
        # Draw the enemies
        for enemy in enemies:
            enemy.draw(screen.screen)
        
        # Draw the player
        player.draw(screen.screen)

        # Draw the HUD
        draw_hud(screen.screen, player)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



def main4():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    running = True
    
    enemies = [EnemyFlight() for _ in range(5)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        # Update player and enemies
        player.update()
        for enemy in enemies:
            enemy.update()
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)

        # Check collisions between bullets/missiles and enemies
        for bullet in player.bullets[:]:
            for enemy in enemies[:]:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break  # No need to check other enemies

        for missile in player.missiles[:]:
            for enemy in enemies[:]:
                if enemy.collide(missile):
                    player.missiles.remove(missile)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                    break  # No need to check other enemies

        # Update and draw the background
        screen.update_screen()
        
        # Clear the screen and redraw background
        screen.screen.fill((0, 0, 0))
        screen.draw_background()
        
        # Draw the enemies
        for enemy in enemies:
            enemy.draw(screen.screen)
        
        # Draw the player
        player.draw(screen.screen)

        # Draw the HUD
        draw_hud(screen.screen, player)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
