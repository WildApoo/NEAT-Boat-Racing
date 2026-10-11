from __future__ import annotations

import pygame
from UserInterface.widget.widget import Widget

class Button(Widget):
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str = "",
            function_executed_on_click = None):

        super().__init__()
        self.width = width
        self.height = height
        self.text = text
        self.is_hovered = False

        self.function_executed_on_click = function_executed_on_click

        # 1. On crée la surface propre au bouton et son rect de position
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(x, y))

        # 2. On génère le visuel initial
        self.update_surface()

    def update_surface(self):
        """Redessine le contenu sur self.surface selon l'état actuel (survol, etc.)"""
        # Choix de la couleur selon l'état
        color = (180, 180, 180) if self.is_hovered else (220, 220, 220)

        # On remplit la surface du bouton (et non pas l'écran !)
        self.surface.fill(color)

        # On peut aussi ajouter une bordure
        pygame.draw.rect(self.surface, (50, 50, 50), (0, 0, self.width, self.height), width=2)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            # Vérifie si la souris est au-dessus du bouton
            hover_state = self.rect.collidepoint(event.pos)

            # On ne re-dessine la surface QUE si l'état de survol a changé (optimisation)
            if hover_state != self.is_hovered:
                self.is_hovered = hover_state
                self.update_surface()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.on_click()

    def on_click(self):
        self.function_executed_on_click()
        print(f"Bouton cliqué ! exécution : {self.function_executed_on_click}")