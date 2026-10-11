from __future__ import annotations
import pygame
from typing import Literal
from UserInterface.widget.widget import Widget


class Text(Widget):
    def __init__(self,x:int, y:int,  text:str="", font:str = "Arial", size:int = 16,
        antialias: bool | Literal[0] | Literal[1] = True,
        color = (0,0,0),
        background = None):
        super().__init__()
        self.text = text
        self.font = pygame.font.SysFont("Arial", size)

        # hérité de Widget
        self.surface = self.font.render(self.text, antialias, color, background)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y