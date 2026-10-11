from __future__ import annotations
import pygame

from UserInterface.afficheur import Afficheur


class Widget:
    def __init__(self):
        Afficheur.add_widget(self)
        self.surface = None
        self.rect = None

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)