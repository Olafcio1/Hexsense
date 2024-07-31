from typing import Any

def fulfill(array: list, wantedLength: int, filledValue: Any):
    length = len(array)
    if length == wantedLength:
        return array
    elif length < wantedLength:
        for _ in range(wantedLength - length):
            array.append(filledValue)
    else:
        for _ in range(length - wantedLength):
            array.pop()
    return array
