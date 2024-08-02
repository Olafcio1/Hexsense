import os
import json
import base64
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

    def __str__(self):
        return f"[BackgroundColor, {self.get_rgb()} ({self.value}), {self.gradient.__str__()}]"

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
                surf.set_at((index, linei), Color(color).get_rgb())
        return pygame.transform.smoothscale(surf, (w, h))

class Theme():
    @classmethod
    def load(cls, name: str) -> "Theme":
        userTheme = static.THEMES_DIR + os.path.sep + name + ".theme"
        preTheme = "." + os.path.sep + "themes" + os.path.sep + name + ".theme"
        path = userTheme if os.path.isfile(userTheme) else (preTheme if os.path.isfile(preTheme) else None)
        if path == None:
            return None
        with open(path, "rb") as f:
            c = f.read()
        return cls.loadFromData(c)

    @staticmethod
    def loadFromData(raw: bytes) -> "Theme":
        t = Theme()
        data = []

        decoded = raw.decode("utf-16-be", "strict")
        if decoded.startswith("b64::"):
            decoded = base64.b64decode(decoded[5:])
        escaped = False
        string = ""
        for c in decoded:
            if escaped:
                string += c
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == "|":
                data.append(string)
                string = ""
            else:
                string += c
        data.append(string)
        del decoded, escaped, string

        t.name = data[0]
        t.windowBackground = BackgroundColor(data[1], json.loads(data[2]))
        return t

    def save(self) -> None:
        """Installs the theme, or if already installs, saves it."""
        values = [self.windowBackground.value, self.windowBackground.gradient]
        content = "|".join(map(lambda v: v.replace("\\", "\\\\").replace("|", "\\|"), values))
        with open(static.THEMES_DIR + os.path.sep + self.name + ".theme", "wb") as f:
            f.write("b64::" + base64.b64encode(content.encode("utf-16-be", "strict")))

    name: str

    windowBackground: BackgroundColor
