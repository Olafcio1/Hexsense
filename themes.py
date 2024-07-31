import os
import colour
import static
import pygame

from util import arrays

class Color():
    value: str
    """This value must be validated by the `colour.web2rgb` function."""

    def __init__(self, value: str):
        self.value = value

    def get_rgb(self) -> list[int, int, int]:
        if type(self.value) == tuple:
            return [*map(lambda v: int(v), self.value)]
        return [*map(lambda v: int(v * 255), colour.web2rgb(self.value))]

class BackgroundColor(Color):
    def __init__(self, value: str, gradient: list[list[str]]):
        self.value = value
        self.gradient = gradient

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
        maxLineWidth = max(map(lambda line: len(line), self.gradient))
        gradient = [*map(lambda line: arrays.fulfill(line, maxLineWidth, ""), self.gradient)]
        surf = pygame.Surface((maxLineWidth, len(gradient)), pygame.SRCALPHA | pygame.HWSURFACE)
        surf.fill(self.get_rgb())
        for linei, line in enumerate(gradient):
            for index, color in enumerate(line):
                if color == "":
                    continue
                surf.set_at((linei, index), Color(color).get_rgb())
        return pygame.transform.smoothscale(surf, (w, h))

class Theme():
    @staticmethod
    def load(name: str) -> "Theme":
        t = Theme()
        t.name = name
        t.windowBackground = BackgroundColor("#000", [
            ["#004bbc", "#003bbc", "#fff000"],
            ["#5acf55", "#55aacc", "#004bbc"]
        ])
        return t

    @staticmethod
    def loadFromData(data: bytes):
        pass

    def save(self):
        """Installs the theme, or if already installs, saves it."""
        values = [self.windowBackground.value]
        content = "\x00".join(values)
        with open(static.THEMES_DIR + os.path.sep + self.name + ".theme", "w") as f:
            f.write(content)

    name: str

    windowBackground: BackgroundColor
