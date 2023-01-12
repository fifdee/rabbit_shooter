import pygame
import sys
import time

from classes.clickable import Clickable
from classes.flash import Flash
from classes.level_manager import LevelManager
from classes.text import FadingText, StaticText


class Game:
    def __init__(self, width, height):
        pygame.init()

        self.size = (width, height)
        self.black = 0, 0, 0
        self.bg = pygame.image.load("assets/bg.png")
        self.screen = pygame.display.set_mode(self.size)
        self.last_time = 0
        self.delta = 0
        self.level_manager = LevelManager(self.size)

    def update(self):
        while True:
            self.delta = (time.time_ns() - self.last_time) / 1000 / 1000
            self.last_time = time.time_ns()

            objects = self.gameplay()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for obj in objects:
                        if isinstance(obj, Clickable):
                            if obj.rect.collidepoint(pos):
                                obj.clicked = True

            self.screen.fill(self.black)
            self.screen.blit(self.bg, self.bg.get_rect())

            for obj in objects:
                if isinstance(obj, Clickable):
                    if obj.x - obj.rect.w / 2 < 0:
                        obj.x = obj.rect.w / 2
                    if obj.x + obj.rect.w / 2 > self.size[0]:
                        obj.x = self.size[0] - obj.rect.w / 2
                    if obj.y - obj.rect.h / 2 < 0:
                        obj.y = obj.rect.h / 2
                    if obj.y + obj.rect.h / 2 > self.size[1]:
                        obj.y = self.size[1] - obj.rect.h / 2

                    self.screen.blit(obj.image, obj.rect)

                elif isinstance(obj, FadingText):
                    if obj.x is not None and obj.y is not None:
                        self.screen.blit(obj.msg, obj.msg.get_rect(center=(self.screen.get_rect().center[0], obj.y)))
                    else:
                        self.screen.blit(obj.msg, obj.msg.get_rect(center=self.screen.get_rect().center))

                elif isinstance(obj, StaticText):
                    self.screen.blit(obj.msg, obj.msg.get_rect(center=(obj.x + 150, obj.y + 50)))

                elif isinstance(obj, Flash):
                    self.screen.blit(obj.surface, (0, 0))

            pygame.display.flip()

    def gameplay(self):
        to_render = self.level_manager.update(self.delta)
        return to_render
