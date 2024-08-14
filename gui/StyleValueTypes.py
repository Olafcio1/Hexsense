from .Color import *
from .BackgroundColor import *
from .Style import *
from .Node import *

from typing import Generic, TypeVar

T = TypeVar("T")

class PropertyDefaultValue(): ...
class INHERIT(PropertyDefaultValue):
    defaultMode = "inherit"
class INITIAL(PropertyDefaultValue):
    defaultMode = "initial"

class PropertyValue(Generic[T]):
    name: str
    _value: T|PropertyDefaultValue
    _elem: "Element"

    @property
    def value(self) -> T:
        if type(self._value) == T:
            return self._value
        elif self._value.defaultMode == "initial":
            return DefaultStyle.__getattribute__(self.name)
        elif self._value.defaultMode == "inherit":
            return self._elem.parent.style.__getattribute__(self.name)

    def __init__(self, name: str, value: T|None = None, element: "ElementOrNone" = None):
        self.name = name
        self._value = value
        self._elem = element

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

    def __format__(self, spec: str):
        return format(self.value, spec)

    def __bool__(self):
        return bool(self.value) if hasattr(self, "value") else False

class Size(int):
    """Size style property value. This exists because it has extensions - look at FIT class."""
    mode = "spec"
class FIT(Size):
    mode = "fit"
