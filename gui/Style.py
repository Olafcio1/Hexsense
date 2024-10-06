# from typing import Literal
## Literal["inherit", "initial"] | 
from .StyleValueTypes import *

class Style():
    # Position
    left: int
    top: int
    right: int
    bottom: int
    # Size
    width: Size
    height: Size
    # Display
    inline: bool
    # Colors
    background: BackgroundColor
    color: Color
    # Visibility
    passthrough: bool
    opacity: float
    visible: bool
    # Margin
    marginTop: int
    marginLeft: int
    marginBottom: int
    marginRight: int
    # Padding
    paddingTop: int
    paddingLeft: int
    paddingBottom: int
    paddingRight: int
    # Border
    borderTopColor: BackgroundColor
    borderTopSize: int
    borderLeftColor: BackgroundColor
    borderLeftSize: int
    borderRightColor: BackgroundColor
    borderRightSize: int
    borderBottomColor: BackgroundColor
    borderBottomSize: int
    def setBorder(self, color: BackgroundColor, size: int):
        self.borderTopColor = color
        self.borderTopSize = size
        self.borderBottomColor = color
        self.borderBottomSize = size
        self.borderLeftColor = color
        self.borderLeftSize = size
        self.borderRightColor = color
        self.borderRightSize = size
        return color

class DefaultStyle(Style):
    left = None
    top = None
    right = None
    bottom = None

    width = FIT
    height = FIT

    inline = False
    background = None
    color = Color("#f00")

    passthrough = False
    opacity = 1
    visible = True

    marginTop = 0
    marginLeft = 0
    marginBottom = 0
    marginRight = 0

    paddingTop = 0
    paddingLeft = 0
    paddingBottom = 0
    paddingRight = 0

    borderTopSize = 0
    borderLeftSize = 0
    borderRightSize = 0
    borderBottomSize = 0
