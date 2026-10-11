from __future__ import annotations
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UserInterface.widget.widget import Widget
    from UserInterface.entity.entity import Entity


class Afficheur:
    """
    Classe gérant l'affichage (Pattern Singleton)
    """

    _instance: Afficheur | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Afficheur, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialisation des attributs de l'instance unique."""
        # Références aux éléments à afficher
        self.widgets: list = []
        self.entities: list = []

        # Screen
        pygame.display.set_caption(f"Visualisation test")
        self.screen = pygame.display.set_mode((720, 720))

        self.bg_color = (140, 198, 249)
        self.bg_position = [0, 0, self.screen.get_width(), self.screen.get_height()]

        self.offset_x: float = 0
        self.offset_y: float = 0

    @classmethod
    def get_instance(cls) -> Afficheur:
        """Méthode pour récupérer l'unique instance de l'Afficheur."""
        if cls._instance is None:
            cls()
        return cls._instance

    def add_widget(self, widget: Widget) -> None:
        """Est censé être appelé automatiquement à la création des widgets"""
        self.widgets.append(widget)

    def remove_widget(self, widget: Widget) -> None:
        """Contrairement à add_widget, celui-ci n'est pas automatique"""
        self.widgets.remove(widget)

    def draw_widgets(self) -> None:
        """Affiche chaque widget grâce au polymorphisme"""
        for widget in self.widgets:
            widget.draw(self.screen)

    def add_entity(self, entity: Entity) -> None:
        """Est censé être appelé automatiquement à la création des entités"""
        self.entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)

    def draw_entity(self, entity: Entity) -> None:
        image = entity.image
        rect = image.get_rect()
        x, y = entity.get_coordinates()
        rect.center = (x + round(self.offset_x), y + round(self.offset_y))
        self.screen.blit(image, rect)

    def update_screen(self) -> None:
        pygame.draw.rect(self.screen, self.bg_color, self.bg_position)

        for entity in self.entities:
            if entity.is_visible:
                self.draw_entity(entity)

        self.draw_widgets()
        pygame.display.flip()

    def set_offset(self, x: float, y: float) -> None:
        self.offset_x = x
        self.offset_y = y

    def add_offset(self, x: float, y: float) -> None:
        self.offset_x += x
        self.offset_y += y