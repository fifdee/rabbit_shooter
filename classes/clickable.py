import pygame


class Clickable:
    def __init__(self, img_path, x, y):
        self.image = pygame.image.load(img_path)
        self.image0 = self.image
        self.rect = self.image0.get_rect()
        self.w0 = self.rect.w
        self.h0 = self.rect.h
        self.x = x
        self.y = y
        self.clicked = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.x = self._x - self.rect.w / 2

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.y = self._y - self.rect.h / 2
