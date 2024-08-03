from .const import *

class Player:
    def __init__(self):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.bullets = []
        self.missiles = []
        self.life = 3

    
    