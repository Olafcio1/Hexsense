from pygame import Surface
from ..Node import *
from ..StyleValueTypes import *

class BodyNode(Element):
    _tag = "body"

    def __init__(self, *children: Element):
        self.children = list(children)
        self.style.background = BackgroundColor(rgb(255, 255, 255))

    def init(self, ctx: Surface, mouseX: int, mouseY: int) -> None:
        self.style.width = ctx.get_width()
        self.style.height = ctx.get_height()
