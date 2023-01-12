class Text:
    texts = []

    @classmethod
    def remove(cls, obj):
        if obj in cls.texts:
            cls.texts.remove(obj)

    def __init__(self, font, msg, x=None, y=None):
        self.msg = font.render(msg, True, (255, 255, 255))
        self.x = x
        self.y = y


class StaticText(Text):
    def __init__(self, font, msg, x, y):
        super().__init__(font, msg, x, y)
        self.msg.set_alpha(164)

        Text.texts.append(self)


class FadingText(Text):
    def __init__(self, font, msg, time_to_wait=800, x=None, y=None):
        super().__init__(font, msg, x, y)
        self.a = 0
        self.msg.set_alpha(self.a)
        self.fade_in = True
        self.time_to_wait = time_to_wait
        self.timer = 0

        Text.texts.append(self)

    @classmethod
    def update(cls, delta):
        for text in cls.texts:
            if isinstance(text, FadingText):
                if text.fade_in:
                    text.a += delta * 0.25
                    if text.a > 255:
                        text.a = 255
                        text.fade_in = False
                else:
                    text.timer += delta
                    if text.timer > text.time_to_wait:
                        text.a -= delta * 0.25
                        if text.a < 0:
                            text.a = 0
                            text.fade_in = True
                            Text.texts.remove(text)

                text.msg.set_alpha(text.a)
