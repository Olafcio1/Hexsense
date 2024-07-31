from os import makedirs
from os.path import isdir

def smakedirs(*paths: str):
    for p in paths:
        if not isdir(p):
            makedirs(p)
