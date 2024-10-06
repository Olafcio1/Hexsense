import pygame

from .Style import *
from .Color import *
from .StyleValueTypes import *

from abc import ABC, abstractmethod
from typing import final, Any, TypeVar

class Node(ABC):
    _inited: bool = False

    @final
    def clone(self):
        print(type(self).__name__)
        clone = type(self)(self._tag, self.children)
        clone.style = self.style

    @final
    @property
    def tag(self) -> str:
        return self._tag

    _events: list[list[Any]] = []
    _mouse: tuple[int, int]

    @final
    def mouse(self) -> tuple[int, int]:
        return self._mouse

    def fullRender(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None:
        if not self._inited:
            self.init(ctx, mouseX, mouseY)
            self._inited = False
        self.render(ctx, mouseX, mouseY)

    @final
    def isHovered(self) -> bool:
        x, y = self.position()
        w, h = self.size()
        return self._mouse[0] >= x and self._mouse[1] >= y and self._mouse[0] < x + w and self._mouse[1] < y + h

    # @final
    # def moveCursor(self, mouseX: int, mouseY: int) -> None:
    #     self._mouse = [mouseX, mouseY]

    @final
    def invokeClick(self, mouseX: int, mouseY: int) -> None:
        self._events.append(["click", mouseX, mouseY])

    @abstractmethod
    def size(self) -> int: ...

    def render(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None: ...
    def init(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None: ...

ElementOrNone = TypeVar("ElementOrNone", "Element", None)

class Element(Node):
    _tag: str
    children: list["Element"] = []
    style: "Style" = DefaultStyle()
    _inited: bool = False

    def __init__(self, tag: str, *children: "Element"):
        self._tag = tag
        self.children = list(children)

    @final
    def prepend(self, *children: "Element") -> None:
        for i, el in enumerate(children):
            if el.parent:
                el.parent.children.remove(el)
            el.parent = self
            self.children.insert(i, el)

    @final
    def append(self, *children: "Element") -> None:
        for el in children:
            if el.parent:
                el.parent.children.remove(el)
            el.parent = self
            self.children.append(el)

    offsetX: int
    offsetY: int
    @final
    def fullRender(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None:
        self._mouse = [mouseX, mouseY]
        if not self._inited:
            self.init(ctx, mouseX, mouseY)
            self._inited = True

        x, y = self.position()

        sizes = map(lambda ch: ch.size(), self.children)
        w, h = self.size(sizes)
        if self.style.background:
            ctx.blit(self.style.background.create(w, h), (x, y), (0, 0, w, h))

        self.offsetX = x
        self.offsetY = y

        # ---------------------------
        # Border
        if s := self.style.borderTopSize:
            ctx.blit(self.style.borderTopColor.create(w, s), (x, y), (0, 0, w, s))
            y += s
        if s := self.style.borderBottomSize:
            # print(self.tag, x, y, w, h, s)
            ctx.blit(self.style.borderBottomColor.create(w, s), (x, y), (0, 0, w, s))
        if s := self.style.borderLeftSize:
            ctx.blit(self.style.borderLeftColor.create(s, h-2), (x, y+1), (0, 0, h-2, s))
            x += s
        if s := self.style.borderRightSize:
            ctx.blit(self.style.borderRightColor.create(s, h-2), (x+w-s, y+1), (0, 0, h-2, s))

        # Padding
        x += self.style.paddingLeft
        y += self.style.paddingTop
        # ---------------------------

        self.render(ctx, mouseX, mouseY)
        y += h - self.style.paddingBottom - self.style.borderBottomSize

        ix = x

        for i, el in enumerate(self.children):
            el.offsetX = x
            el.offsetY = y
            el.fullRender(ctx, mouseX, mouseY)
            self._mouse = (mouseX, mouseY)
            for e in self._events:
                if e[0] == "click" and el.isHovered():
                    el.click(ctx, mouseX, mouseY)
                    if el.style.passthrough == False:
                        self._events.pop(i)
            s = el.size()
            if el.style.inline:
                x += s[0]
            else:
                x = ix
                y += s[1]

    @final
    def size(self, sizes: list[tuple[int, int]]|None = None) -> tuple[int, int]:
        if sizes == None:
            sizes = map(lambda ch: ch.size(), self.children)

        if self.style.width and self.style.width != FIT:
            w = self.style.width
        elif self.style.inline == False:
            print(self.tag)
            w = self.parent.size()[0] - self.parent.style.borderLeftSize - self.parent.style.borderRightSize\
                                      - self.parent.style.paddingLeft - self.parent.style.paddingRight
        else:
            w = self.style.borderLeftSize + self.style.borderRightSize +\
                self.style.paddingLeft + self.style.paddingRight
            for s in sizes:
                w += s[0]

        if self.style.height and self.style.height != FIT:
            h = self.style.height
        else:
            h = self.style.borderTopSize + self.style.borderBottomSize +\
                self.style.paddingTop + self.style.paddingBottom
            for s in sizes:
                h += s[1]

        return (w, h)

    @final
    def position(self) -> tuple[int, int]:
        if self.style.left and self.style.right:
            x = (self.style.width - (self.style.left - self.style.right)) / 2
        elif self.style.left:
            x = self.style.left
        elif self.style.right:
            x = self.style.right
        elif hasattr(self, 'offsetX'):
            x = self.offsetX
        else:
            x = 0

        if self.style.top and self.style.bottom:
            y = (self.style.height - (self.style.top - self.style.bottom)) / 2
        elif self.style.top:
            y = self.style.top
        elif self.style.bottom:
            y = self.style.bottom
        elif hasattr(self, 'offsetY'):
            y = self.offsetY
        else:
            y = 0

        return (x, y)

    parent: ElementOrNone = None
    def click(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None: ...

font: pygame.font.Font | None = None
class TextNode(Element):
    text: str

    def __init__(self, text: str):
        super().__init__("text")
        self.text = text

    def render(self, ctx: pygame.Surface, mouseX: int, mouseY: int) -> None:
        global font
        if font == None:
            font = pygame.font.SysFont("Arial", 20)
        ctx.blit(font.render(self.text, True, self.style.color.get_rgb()), (0, 0))
