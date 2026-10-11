import pygame

from UserInterface.afficheur import Afficheur
from UserInterface.assetManager import AssetManager

class Entity(pygame.sprite.Sprite):

    def __init__(self, representant:object,  stander_width:int, stander_height: int, x_init:int, y_init:int, is_visible:bool):
        super().__init__()
        self.stander_width:int = stander_width
        self.stander_height:int = stander_height


        self.image:pygame.surface.Surface = AssetManager.get_instance().get_img(representant)
        self.image_origine:pygame.surface.Surface = self.image

        self.rect:pygame.rect.Rect = self.image.get_rect()
        self.rect.x = x_init
        self.rect.y = y_init
        self.scale_image()
        self.is_visible = is_visible

        Afficheur.get_instance().add_entity(self)

    def scale_image(self, x_modifier:float=1, y_modifier:float=1):
        """
        Recalcule la bonne taille de l'image à partir de sa dimension standard ainsi que des éventuels modificateurs
        :param x_modifier:
        :param y_modifier:
        :return:
        """

        self.image = pygame.transform.scale(self.image_origine,
                                            (self.stander_width * x_modifier, self.stander_height * y_modifier))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def move(self, x:int, y:int):
        self.rect.x += x
        self.rect.y += y

    def get_coordinates(self) -> tuple:
        return self.rect.x, self.rect.y

    def set_visibility(self, visibility:bool):
        self.is_visible = visibility

    def self_delete(self):
        Afficheur.get_instance().remove_entity(self)
