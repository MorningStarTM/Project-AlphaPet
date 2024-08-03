import pygame
import os
from player import Player

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load the background image
BACKGROUND_IMAGE = pygame.image.load("assets\\screen\\bg.png")

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Astro Avenger")
        
        self.bg_y1 = 0
        self.bg_y2 = -SCREEN_HEIGHT
        self.bg_speed = 2

    def draw_background(self):
        self.screen.blit(BACKGROUND_IMAGE, (0, self.bg_y1))
        self.screen.blit(BACKGROUND_IMAGE, (0, self.bg_y2))

    def move_background(self):
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed
        if self.bg_y1 >= SCREEN_HEIGHT:
            self.bg_y1 = -SCREEN_HEIGHT
        if self.bg_y2 >= SCREEN_HEIGHT:
            self.bg_y2 = -SCREEN_HEIGHT

    def update_screen(self):
        self.move_background()
        self.draw_background()





def main():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.fire_bullet()
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    player.launch_missile()
        
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
        screen.draw_background()
        player.draw(screen.screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()