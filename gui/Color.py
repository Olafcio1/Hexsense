import colour

class Color():
    value: str
    """This value must be validated by the `colour.web2rgb` function."""

    def __init__(self, value: str):
        self.value = value

    def get_rgb(self) -> list[int, int, int]:
        if type(self.value) == tuple:
            return [*map(lambda v: int(v), self.value)]
        return [*map(lambda v: int(v * 255), colour.web2rgb(self.value))]

def rgb(*values):
    """function for highlighting colors in vscode"""
    return Color(values)
