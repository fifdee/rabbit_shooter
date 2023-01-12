import random

import pygame

from classes.clickable import Clickable


class Rabbit(Clickable):
    rabbits = []

    def __init__(self, level, size):
        img_nr = random.choice([1, 2, 3, 4])
        img_path = f'assets/rabbit{img_nr}.png'
        super().__init__(img_path, random.randint(0, size[0]), random.randint(0, size[1]))
        self.hide_timer = 0
        self.hide_timer_limit = 2500 - (level * 200)
        if self.hide_timer_limit < 500:
            self.hide_timer_limit = 500
        self.destroy = False
        self.w0 = self.w0 * (size[0] / 1024)
        self.h0 = self.h0 * (size[0] / 1024)
        self.rect.w = 0
        self.rect.h = 0
        self.w = 0.0
        self.h = 0.0

        Rabbit.rabbits.append(self)

    @classmethod
    def update(cls, delta):
        kills = 0
        wounds = 0
        for rabbit in cls.rabbits:
            rabbit.hide_timer += delta
            if rabbit.hide_timer >= rabbit.hide_timer_limit:
                if not rabbit.clicked and not rabbit.destroy:
                    rabbit.destroy = True
                    wounds += 1

            if rabbit.clicked:
                rabbit.w -= rabbit.w0 * delta * 0.005
                rabbit.h -= rabbit.h0 * delta * 0.005
                if rabbit.w < 0:
                    rabbit.w = 0
                if rabbit.h < 0:
                    rabbit.h = 0
                if rabbit.w <= 10:
                    rabbit.clicked = False
                    kills += 1
                    rabbit.destroy = True

                rabbit.rect.w = rabbit.w
                rabbit.rect.h = rabbit.h
                rabbit.image = pygame.transform.scale(rabbit.image0, (rabbit.rect.w, rabbit.rect.h))
                rabbit.x = rabbit.x
                rabbit.y = rabbit.y
            else:
                if not rabbit.destroy:
                    rabbit.w += delta * 2 * (rabbit.w0 / rabbit.h0)
                    rabbit.h += delta * 2

                    if rabbit.w > rabbit.w0:
                        rabbit.w = rabbit.w0
                    if rabbit.h > rabbit.h0:
                        rabbit.h = rabbit.h0

                    rabbit.rect.w = rabbit.w
                    rabbit.rect.h = rabbit.h
                    rabbit.image = pygame.transform.scale(rabbit.image0, (rabbit.rect.w, rabbit.rect.h))
                    rabbit.x = rabbit.x
                    rabbit.y = rabbit.y

            if rabbit.destroy:
                cls.rabbits.remove(rabbit)

        return kills, wounds
