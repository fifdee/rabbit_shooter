import pygame


class Flash:
    flashes = []

    def __init__(self, size):
        self.surface = pygame.Surface(size)
        self.a = 96
        self.surface.set_alpha(self.a)
        self.surface.fill((255, 0, 0))

        Flash.flashes.append(self)

    @classmethod
    def update(cls, delta):
        for flash in cls.flashes:
            flash.a -= delta * 0.15

            if flash.a < 0:
                flash.a = 0
                cls.flashes.remove(flash)
            flash.surface.set_alpha(flash.a)
