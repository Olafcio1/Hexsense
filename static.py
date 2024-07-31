import os
import util.booleans, util.files

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

APP_DATA: str = util.booleans.check(
    os.name == "nt",
    lambda: os.environ.get("APPDATA") + "\\Hexsense",
    lambda: os.environ.get("HOME", "") + "/config/.hexsense"
)

THEMES_DIR: str = APP_DATA + os.path.sep + "themes"

util.files.smakedirs(APP_DATA, THEMES_DIR)