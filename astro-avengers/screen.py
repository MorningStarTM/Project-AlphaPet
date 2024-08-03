import pygame
import os

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
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.update_screen()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()