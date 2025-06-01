import random
import pygame
from gla import Shield, Life, Ammunition



class GLATimer:
    def __init__(self):
        self.spawn_interval_shield = 800  # frames
        self.spawn_interval_life = 600    # frames
        self.spawn_interval_ammunition = 300  # frames

        self.shield_timer = 0
        self.life_timer = 0
        self.ammunition_timer = 0

        self.shields = []
        self.lives = []
        self.ammunitions = []


    def update(self):
        self.shield_timer += 1
        self.life_timer += 1
        self.ammunition_timer += 1

        if self.shield_timer >= self.spawn_interval_shield:
            self.shields.append(Shield())
            self.shield_timer = 0

        if self.life_timer >= self.spawn_interval_life:
            self.lives.append(Life())
            self.life_timer = 0

        if self.ammunition_timer >= self.spawn_interval_ammunition:
            self.ammunitions.append(Ammunition())
            self.ammunition_timer = 0

        # Update positions
        for shield in self.shields:
            shield.update()
        for life in self.lives:
            life.update()
        for ammunition in self.ammunitions:
            ammunition.update()
            

    def draw(self, screen):
        for shield in self.shields:
            shield.draw(screen)
        for life in self.lives:
            life.draw(screen)
        for ammunition in self.ammunitions:
            ammunition.draw(screen)
