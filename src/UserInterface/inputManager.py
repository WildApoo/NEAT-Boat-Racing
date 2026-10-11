from collections.abc import Callable
from symtable import Function

import pygame.event

from enum import Enum


class KeyStatus(Enum):
    pressed = 0
    hold = 1
    released = 2


class InputManager:
    """
    Cette class a pour but de gérer les inputs du jeu
    1. Input > fonction
    2. input enclenché ?

    Les keys sur pygame sont des constantes int
    """

    is_down: dict[int, bool] = {}
    """
    Permet de savoir si une touche est encore enfoncée ou non
    """

    correspondance: dict[tuple[int, KeyStatus], Callable[[], None]] = {}
    """
    Clef tuple(pygame key, pressée/maintenue/relachée : fonction/méthode à appeler

    Les fonctions et/ou méthodes renseignées ne doivent ni avoir de paramètres ni retourner de valeur.
    """

    @staticmethod
    def show_is_down() -> None:
        print("\nTouches maintenues")
        print("------------------------------------------------------")
        for key in InputManager.is_down:
            print(f"{key} : {InputManager.is_down[key]}")
        print("------------------------------------------------------")

    @staticmethod
    def show_correspondance() -> None:
        print("\nCorrespondance")
        print("------------------------------------------------------")
        for input in InputManager.correspondance:
            print(f"{input[0]} | {input[1]} : {InputManager.correspondance[input]}")
        print("------------------------------------------------------")

    @staticmethod
    def update_inputs(events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                InputManager.is_down[event.key] = True
            if event.type == pygame.KEYUP:
                InputManager.is_down.pop(event.key)

    @staticmethod
    def bind_input(key: int, status: KeyStatus, function: Callable[[], None]) -> None:
        """
        Il n'y a aucune vérification ! C'est la responsabilité du dev
        """
        InputManager.correspondance[(key, status)] = function

    @staticmethod
    def call(key: int, status: KeyStatus) -> None:
        if InputManager.is_bind(key, status):
            InputManager.correspondance[(key, status)]()

    @staticmethod
    def is_bind(key: int, status: KeyStatus) -> bool:
        return (key, status) in InputManager.correspondance.keys()

    @staticmethod
    def update(events: list[pygame.event.Event]) -> None:
        """
        C'est la fonction principale qui doit être appelé à chaque boucle.
        Elle met à jour les touches maintenues et appelle toutes les méthodes concernées

        Une touche qui vient d'être "pressée" est aussi déclenchée en "maintenue"
        """
        InputManager.update_inputs(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                InputManager.call(event.key, KeyStatus.pressed)
            elif event.type == pygame.KEYUP:
                InputManager.call(event.key, KeyStatus.released)

        for key in InputManager.is_down:
            InputManager.call(key, KeyStatus.hold)

