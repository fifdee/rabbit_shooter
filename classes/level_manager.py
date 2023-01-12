import pygame

from classes.button import Button
from classes.rabbit import Rabbit
from classes.text import FadingText, StaticText, Text


class LevelManager:
    def __init__(self):
        self.font = pygame.font.Font('assets/font.ttf', 64)

        def f():
            self.state = 'PLAY'
            FadingText(self.font, f'LEVEL {self.level}')

        self.state = 'MENU'
        self.level = 1
        self.kills = 0
        self.lives = 3
        self.start_button = Button('assets/start_button.png', 512, 384, action=f)
        self.kills_text = StaticText(self.font, f'KILLS {self.kills}', 0, 0)

    def update(self, delta):
        Button.update(delta)
        FadingText.update(delta)

        if self.state == 'MENU':
            return [self.start_button]

        elif self.state == 'PLAY':
            self.spawn_timer += delta

            if self.spawn_timer >= self.spawn_timer_limit:
                self.spawn_timer = 0
                Rabbit(self.level)

            new_kills = Rabbit.update(delta)
            self.kills += new_kills
            if new_kills > 0 or self.kills >= 10:
                if self.kills >= 10:
                    self.level += 1
                    FadingText(self.font, f'LEVEL {self.level}')
                    self.kills = 0

                StaticText.texts.remove(self.kills_text)
                self.kills_text = StaticText(self.font, f'KILLS {self.kills}', 0, 0)

            return Rabbit.rabbits + Text.texts

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.spawn_timer = -1000
        self.spawn_timer_limit = 2000 - (self.level * 100)
        if self.spawn_timer_limit < 300:
            self.spawn_timer_limit = 300