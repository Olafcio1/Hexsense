import os
from util import booleans, files
from typing import Self
from themes import *
import static
import pygame

on = True
def main():
    global on
    pygame.init()
    pygame.mixer.init()

    theme = Theme.load("default")
    size = windowWidth, windowHeight = 800, 600

    scr = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.SRCALPHA | pygame.HWSURFACE, 32)
    pygame.display.set_allow_screensaver(True)
    pygame.display.set_caption("Hexsense")
    # pygame.display.set_icon(pygame.image.load_basic("./logo.png"))
    while on:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                on = False
                break
        scr.blit(theme.windowBackground.create(windowWidth, windowHeight), (0, 0))
        pygame.draw.line(scr, (170, 170, 170), (0, 30), (windowWidth, 30))
        pygame.display.update()

if __name__ == "__main__":
    main()
