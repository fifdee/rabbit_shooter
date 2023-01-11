import random
import sys
import time

import pygame


class Game:
    def __init__(self, width, height):
        self.size = (width, height)
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.last_time = 0
        self.delta = 0

        self.objects_to_render = []

    def update(self):
        pygame.init()
        while True:
            self.delta = time.time_ns() / 1000 / 1000 - self.last_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.black)
            for obj in self.objects_to_render:
                self.screen.blit(obj.image, obj.rect)

            self.gameplay()

            pygame.display.flip()
            self.last_time = time.time_ns() / 1000 / 1000

    def gameplay(self):
        ...


class LevelManager:
    def __init__(self):
        self.level = 1
        self.spawn_timer = 0
        self.spawn_timer_limit = 2000

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.spawn_timer_limit = 2000 - (self.level * 100)
        if self.spawn_timer_limit < 300:
            self.spawn_timer_limit = 300


class Rabbit:
    def __init__(self):
        self.image = pygame.image.load("rabbit.png")
        self.rect = self.image.get_rect()
        self.x = random.randint(0, 1024)
        self.y = random.randint(0, 768)
