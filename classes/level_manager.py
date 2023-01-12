import json
import random

import pygame

from classes.button import Button
from classes.flash import Flash
from classes.rabbit import Rabbit
from classes.text import FadingText, StaticText, Text


class LevelManager:
    def __init__(self, size):
        self.font = pygame.font.Font('assets/font.ttf', 64)

        def f():
            self.state = 'PLAY'
            self.kills = 0
            self.level = 1
            self.lives = 3
            Rabbit.rabbits.clear()
            FadingText(self.font, f'LEVEL {self.level}')
            Text.remove(self.kills_text)
            Text.remove(self.lives_text)
            self.kills_text = StaticText(self.font, f'Kills: {self.kills}', 0, 0)
            self.lives_text = StaticText(self.font, f'Lives: {self.lives}', 400, 0)
            Text.remove(self.highscore_text)
            self.highscore_text = None

        self.size = size
        self.highscore = self.update_highscore()
        self.level = 1
        self.kills = 0
        self.lives = 3
        self.kills_text = None
        self.lives_text = None
        self.highscore_text = StaticText(self.font, f'Highscore: {self.highscore}', 100, 0)
        self.state = 'MENU'
        self.start_button = Button('assets/start_button.png', self.size[0] / 2, self.size[1] / 2, action=f)

    def update(self, delta):
        Button.update(delta)
        FadingText.update(delta)
        Flash.update(delta)

        if self.state == 'MENU':
            return [self.start_button] + Text.texts + Flash.flashes

        elif self.state == 'PLAY':
            self.spawn_timer += delta

            if self.spawn_timer >= self.spawn_timer_limit:
                self.spawn_timer = 0
                Rabbit(self.level, self.size)

            new_kills, new_wounds = Rabbit.update(delta)
            self.kills += new_kills
            if new_kills > 0 or self.kills >= 10:
                if self.kills >= self.level * 10:
                    self.level += 1
                    FadingText(self.font, f'LEVEL {self.level}')

                Text.remove(self.kills_text)
                self.kills_text = StaticText(self.font, f'Kills: {self.kills}', 0, 0)

            if new_wounds > 0:
                Flash(self.size)
                self.lives -= new_wounds
                if self.lives <= 0:
                    this_score = self.kills
                    self.highscore = self.update_highscore(this_score)
                    FadingText(self.font, f'GAME OVER. Your score: {this_score}',
                               time_to_wait=2000, x=0, y=self.size[1] * 0.78)
                    self.state = 'MENU'
                    Text.remove(self.lives_text)
                    Text.remove(self.kills_text)
                    self.highscore_text = StaticText(self.font, f'Highscore: {self.highscore}', self.size[0] * 0.1, 0)
                else:
                    Text.remove(self.lives_text)
                    self.lives_text = StaticText(self.font, f'Lives: {self.lives}', self.size[0] * 0.4, 0)

            return Rabbit.rabbits + Text.texts + Flash.flashes

    def update_highscore(self, current_score=None):
        try:
            with open('data.json', 'r') as f:
                content = json.loads(f.read())
                highscore = content['highscore']
        except FileNotFoundError:
            with open('data.json', 'w') as f:
                f.write(json.dumps({'highscore': 0}))
                highscore = 0
        finally:
            if current_score:
                if highscore < current_score:
                    with open('data.json', 'w') as f:
                        f.write(json.dumps({'highscore': current_score}))
                        highscore = current_score

            return highscore

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.spawn_timer = -1000
        self.spawn_timer_limit = 2000 - (self._level * 200) - random.randint(0, 300)
        if self.spawn_timer_limit < 300:
            self.spawn_timer_limit = 300
        Rabbit.rabbits.clear()
