from __future__ import annotations
import pygame
import os
from pathlib import Path


class AssetManager:
    """
    Gestionnaire d'assets dynamique (Pattern Singleton)
    """

    _instance: AssetManager | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self.ASSET_DIR = Path(__file__).resolve().parent / "asset"
        self.__not_found_img = pygame.image.load(self.ASSET_DIR / "Error.png")
        self.__images: dict[str, pygame.surface.Surface] = {}

    @classmethod
    def get_instance(cls) -> AssetManager:
        if cls._instance is None:
            cls()
        return cls._instance

    def get_img(self, entity: object) -> pygame.surface.Surface:
        entity_type = type(entity).__name__

        # Si l'image n'est pas encore en cache, on essaie de la charger
        if entity_type not in self.__images:
            self.__images[entity_type] = self.__load_image(entity_type)

        return self.__images[entity_type]

    def __load_image(self, entity_type: str) -> pygame.surface.Surface:
        """Tente de charger l'image associée au nom de la classe, sinon renvoie l'image d'erreur."""
        image_path = self.ASSET_DIR / f"{entity_type}.png"

        try:
            img = pygame.image.load(image_path)
            print(f"Asset chargé avec succès pour : {entity_type}")
        except (pygame.error, FileNotFoundError):
            print(f"Attention : Asset introuvable pour {entity_type} ({image_path}), utilisation de l'image d'erreur.")
            img = self.__not_found_img

        return img