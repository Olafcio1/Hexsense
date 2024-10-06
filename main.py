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

    body = BodyNode()
    body.style.background = theme.windowBackground
    body.fullRender(scr, 0, 0)

    topBar = Element("nav")
    topBar.style.height = 30
    topBar.style.borderBottomColor = theme.topHr
    topBar.style.borderBottomSize = 2
    body.append(topBar)

    logo = Element("p")
    logo.append(TextNode("Hexsense"))
    topBar.append(logo)

    print(topBar.style.height, topBar.size())

    mouseX, mouseY = 0, 0
    while on:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                on = False
                break
            elif ev.type == pygame.VIDEORESIZE:
                windowWidth, windowHeight = ev.w, ev.h
                size = ev.size
                body._inited = False
            elif ev.type == pygame.MOUSEMOTION:
                mouseX, mouseY = ev.pos
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                body.invokeClick(*ev.pos)
        body.fullRender(scr, mouseX, mouseY)
        pygame.display.update()

if __name__ == "__main__":
    main()
