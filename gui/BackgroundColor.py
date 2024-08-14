import pygame

from .Color import *
from util import arrays

class BackgroundColor(Color):
    def __init__(self, value: Color|str, gradient: list[list[str]] = []):
        if type(value) == Color:
            self.value = value.value
        else: self.value = value
        self.gradient = gradient

    def __str__(self):
        return f"[BackgroundColor rgb{self.get_rgb()} ({self.value}), {self.gradient.__str__()}]"

    gradient: list[list[str]]
    """
    This is complicated. But gradients have a background, and colors. They are created in code like that, for large gradient options:
    [
        ["#ff0000", "", ""],
        ["", "#ff7700", ""],
        ["", "", "#fff000"]
    ]
    This gradient can be similar made in CSS with `linear-gradient(45deg, #ff0000, #ff7700, #fff000)`.
    The difference is, the background. The technique of making gradients in CSS, vs Hexsense, is huge.
    I do not know the browser's gradient implementation, but I am making a 6x6 surface here, with the background `value`. Then, I am drawing these colors as provided. An empty string means to not draw.
    """

    def create(self, w: int, h: int) -> pygame.Surface:
        if len(self.gradient) == 0:
            surf = pygame.Surface((w, h))
            surf.fill(self.get_rgb())
            return surf
        maxLineWidth = max(map(lambda line: len(line), self.gradient))
        gradient = [*map(lambda line: arrays.fulfill(line, maxLineWidth, ""), self.gradient)]
        surf = pygame.Surface((maxLineWidth, len(gradient)), pygame.SRCALPHA | pygame.HWSURFACE, 32)
        if self.value != "":
            surf.fill(self.get_rgb())
        for linei, line in enumerate(gradient):
            for index, color in enumerate(line):
                if color == "":
                    continue
                surf.set_at((index, linei), Color(color).get_rgb())
        return pygame.transform.smoothscale(surf, (w, h))
