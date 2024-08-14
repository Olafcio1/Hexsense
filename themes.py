import os
import json
import base64
import static

from util import arrays
from gui import *

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

        decoded = raw.decode("utf-8", "strict")
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
        t.topHr = BackgroundColor(data[3], json.loads(data[4]))
        return t

    def save(self) -> None:
        """Installs the theme, or if already installs, saves it."""
        values = [self.windowBackground.value, self.windowBackground.gradient, self.topHr.value, self.topHr.gradient]
        content = "|".join(map(lambda v: v.replace("\\", "\\\\").replace("|", "\\|"), values))
        with open(static.THEMES_DIR + os.path.sep + self.name + ".theme", "wb") as f:
            f.write("b64::" + base64.b64encode(content.encode("utf-8", "strict")))

    name: str

    windowBackground: BackgroundColor
    topHr: BackgroundColor
