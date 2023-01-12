import random

from classes.clickable import Clickable


class Rabbit(Clickable):
    rabbits = []

    def __init__(self, level):
        img_nr = random.choice([1, 2, 3, 4])
        img_path = f'assets/rabbit{img_nr}.png'
        super().__init__(img_path, random.randint(0, 1024), random.randint(0, 768))
        self.hide_timer = 0
        self.hide_timer_limit = 1500 - (level * 100)
        if self.hide_timer_limit < 500:
            self.hide_timer_limit = 500
        self.destroy = False

        Rabbit.rabbits.append(self)

    @classmethod
    def update(cls, delta):
        kills = 0
        for rabbit in cls.rabbits:
            rabbit.hide_timer += delta
            if rabbit.hide_timer >= rabbit.hide_timer_limit:
                rabbit.destroy = True

            if rabbit.clicked:
                kills += 1
                rabbit.clicked = False
                rabbit.destroy = True

            if rabbit.destroy:
                cls.rabbits.remove(rabbit)

        return kills