import pygame

from classes.clickable import Clickable


class Button(Clickable):
    buttons = []

    def __init__(self, img_path, x, y, action):
        super().__init__(img_path, x, y)

        self.grow = True
        self.w0 = self.rect.w
        self.h0 = self.rect.h
        self.action = action

        Button.buttons.append(self)

    @classmethod
    def update(cls, delta):
        for btn in cls.buttons:
            if btn.clicked:
                if btn.grow:
                    btn.rect.w += btn.w0 * delta * 0.002
                    btn.rect.h += btn.h0 * delta * 0.002
                    if btn.rect.w > btn.w0 * 1.3:
                        btn.grow = False
                if not btn.grow:
                    btn.rect.w -= btn.w0 * delta * 0.002
                    btn.rect.h -= btn.h0 * delta * 0.002
                    if btn.rect.w < btn.w0:
                        btn.grow = True
                        btn.clicked = False
                        btn.action()
                btn.image = pygame.transform.scale(btn.image0, (btn.rect.w, btn.rect.h))
                btn.x = btn.x
                btn.y = btn.y