from UserInterface.entity.entity import Entity
from parcoursBateau.bateau import Bateau
from parcoursBateau.checkpoint import CheckPoint
from UserInterface.afficheur import Afficheur
from UserInterface.inputManager import InputManager, KeyStatus
import pygame


class Visualise:



    def __init__(self, bateaux: list[Bateau], checkpoints: list[CheckPoint]):
        self.__bateaux: list[Bateau] = bateaux
        self.__checkpoints: list[CheckPoint] = checkpoints
        self.__entities: list[tuple[Bateau | CheckPoint, Entity]] = []

        self.__afficheur: Afficheur = Afficheur.get_instance()

        # calcul des dimensions de l'affichage en fonction du parcours
        cp_x: list[int] = []
        cp_y: list[int] = []

        for checkpoint in self.__checkpoints:
            entity = Entity(checkpoint, 20, 20, checkpoint.x, checkpoint.y, True)
            couple = (checkpoint, entity)
            self.__entities.append(couple)

            cp_x.append(checkpoint.x)
            cp_y.append(checkpoint.y)

        # calcul de la taille des éléments dans la fenetre
        min_x, max_x = min(cp_x), max(cp_x)
        min_y, max_y = min(cp_y), max(cp_y)

        padding = 80
        range_x = max(1, max_x - min_x)
        range_y = max(1, max_y - min_y)

        scale_x = (self.__afficheur.screen.get_width() - 2 * padding) / range_x
        scale_y = (self.__afficheur.screen.get_height() - 2 * padding) / range_y
        self._STATED_SCALE: int = min(scale_x, scale_y)
        self._STATED_MIN_MAX: tuple[int, int]  = (min_x, min_y)
        self._zoom: float = 1.0

        # création des entités à afficher
        for bateau in self.__bateaux:
            x, y = self.__to_px(bateau.x, bateau.y)
            entity = Entity(bateau, 20, 20, x, y, True)
            couple = (bateau, entity)
            self.__entities.append(couple)

        for checkpoint in self.__checkpoints:
            x, y = self.__to_px(checkpoint.x, checkpoint.y)
            entity = Entity(checkpoint, 20, 20, x, y, True)
            couple = (checkpoint, entity)
            self.__entities.append(couple)

    def init_visualisation(self):
        pygame.init()
        MOUVEMENT_BASE = 2
        ZOOM_BASE = 1.2
        def offset_right():
            self.__afficheur.add_offset(-MOUVEMENT_BASE * self._zoom, 0)

        def offset_left():
            self.__afficheur.add_offset(MOUVEMENT_BASE * self._zoom, 0)

        def offset_up():
            self.__afficheur.add_offset(0, MOUVEMENT_BASE * self._zoom)

        def offset_down():
            self.__afficheur.add_offset(0, -MOUVEMENT_BASE * self._zoom)

        def zoom():
            self._zoom = min(10.0, self._zoom * ZOOM_BASE)

        def dezoom():
            self._zoom = max(1.0, self._zoom / ZOOM_BASE)

        def center_camera():
            self.__afficheur.set_offset(0,0)

        InputManager.bind_input(pygame.K_RIGHT, KeyStatus.hold, offset_right)
        InputManager.bind_input(pygame.K_LEFT, KeyStatus.hold, offset_left)
        InputManager.bind_input(pygame.K_UP, KeyStatus.hold, offset_up)
        InputManager.bind_input(pygame.K_DOWN, KeyStatus.hold, offset_down)

        InputManager.bind_input(pygame.K_KP_PLUS, KeyStatus.pressed, zoom)
        InputManager.bind_input(pygame.K_KP_MINUS, KeyStatus.pressed, dezoom)

        InputManager.bind_input(pygame.K_c, KeyStatus.pressed, center_camera)

    def end_visualisation(self):
        for couple in self.__entities:
            entity: Entity = couple[1]
            entity.self_delete()

    def __to_px(self, x, y):
        assert self._STATED_MIN_MAX is not None and self._STATED_SCALE is not None
        m_x, m_y = self._STATED_MIN_MAX
        px = int((80 + (x - m_x) * self._STATED_SCALE) * self._zoom)
        py = int((self.__afficheur.screen.get_height() - (80 + (y - m_y) * self._STATED_SCALE)) * self._zoom)
        return px, py

    def draw_frame(self, epoque, sec, temps):
        for couple in self.__entities:


            # ce check par type pourrait être résolue par de la généricité -> class mère pour tous les éléments de l'expériences
            if type(couple[0]) == Bateau:
                entity: Entity = couple[1]
                bateau: Bateau = couple[0]

                entity.scale_image(self._zoom, self._zoom)

                x, y = self.__to_px(bateau.x, bateau.y)
                entity.rect.x = x
                entity.rect.y = y



            elif type(couple[0]).__name__ == "CheckPoint":
                entity: Entity = couple[1]
                checkpoint: CheckPoint = couple[0]

                entity.scale_image(self._zoom, self._zoom)

                x, y = self.__to_px(checkpoint.x, checkpoint.y)
                entity.rect.x = x
                entity.rect.y = y


        # récupérer les évènements
        events = pygame.event.get()

        # class qui gère les inputs
        InputManager.update(events)

        # class qui gère le jeu

        # class qui gère les animations
        self.__afficheur.update_screen()

        # class qui gère les sons

        for event in events:

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("fermeture du jeu")
