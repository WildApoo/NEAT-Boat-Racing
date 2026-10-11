from __future__ import annotations
import numpy as np
import numpy.typing as npt
from typing import List
from NEAT.projectException import CoucheIsoleeError, CoucheVideError


class Couche:
    compteur_id = 1

    # la méthode de création peut encore changer, notamment sur la partie précédents/suivants
    def __init__(self, size: int, previous_size: int, fonction: str = "tanh"):
        self.id = Couche.compteur_id
        Couche.compteur_id += 1
        self.fonction_activation_allowed = {"sigmoid": Couche.sigmoid, "tanh": Couche.tanh}
        self.fonction_activation = self.fonction_activation_allowed[fonction]
        self.fonction_name = fonction

        self.weight = np.random.uniform(-1, 1, size=(size, previous_size))   # couche * couche précédente = colonne
        self.bias = np.random.uniform(-1, 1, size=(size, 1))    # une colonne = la couche

    @staticmethod
    def sigmoid(x: npt.NDArray[np.float64]):
        return 1/(1+np.exp(-x))

    @staticmethod
    def tanh(x: npt.NDArray[np.float64]):
        return np.tanh(x)

    def get_value(self, X: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if self.weight.shape[0] > 0 and self.weight.shape[1] > 0:
            return self.fonction_activation(np.dot(self.weight, X) + self.bias)
        elif self.weight.shape[1] == 0:
            raise CoucheIsoleeError("Couche isolée",
                                                     "Impossible de faire les calculs car tous les neurones précédents ont été supprimés sans modifier la liaison avec cette couche")
        else:
            raise CoucheVideError("Couche vide",
                                                   "Impossible de produire un calcul car cette couche ne contient plus de neurone et doit être supprimée")

    def add_link(self) -> None:
        new_column = np.random.uniform(-1, 1, size=(self.weight.shape[0], 1))
        self.weight = np.hstack((self.weight, new_column))

    def remove_link(self, index: int) -> int:
        if self.weight.shape[1] >= 1:
            self.weight = np.delete(self.weight, index, axis=1)
        else:
            print("Erreur : le neurone est isolé, il n'y a plus de poids à supprimer.")

        return self.weight.shape[1]  # permettra de savoir si la couche est devenue isolée

    def add_neurone(self) -> None:
        new_row_w = np.random.uniform(-1, 1, size=(1, self.weight.shape[1]))
        new_row_b = np.random.uniform(-1, 1, size=(1, 1))

        self.weight = np.vstack((self.weight, new_row_w))
        self.bias = np.vstack((self.bias, new_row_b))

    def remove_neurone(self, index: int) -> int:
        if self.weight.shape[0] >= 1:
            self.weight = np.delete(self.weight, index, axis=0)
            self.bias = np.delete(self.bias, index, axis=0)
        else:
            print("Erreur : la couche ne contient plus de neurone à supprimer.")

        return self.weight.shape[0]  # permettra de savoir quand supprimer la couche

    def mutation(self, taux_mutation: float = 0.1) -> None:
        self.weight += np.random.normal(0, taux_mutation, size=self.weight.shape)
        self.bias += np.random.normal(0, taux_mutation, size=self.bias.shape)

        # correction des valeurs si elles sortent de l'interval
        # if self.fonction_activation == Couche.tanh:
        #    self.weight = np.clip(self.weight, -1, 1)
        #    self.bias = np.clip(self.bias, -1, 1)
        #else:
        #    self.weight = np.clip(self.weight, 0, 1)
        #    self.bias = np.clip(self.bias, 0, 1)

    def copy_couche(self, weight: npt.NDArray[np.float64], bias: npt.NDArray[np.float64], fonction_activation_name: str) -> None:
        self.weight = weight.copy()
        self.bias = bias.copy()
        self.fonction_activation = self.fonction_activation_allowed[fonction_activation_name]

    def save_to_json(self) -> List[List[List[float]]]:
        data = [self.weight.tolist(), self.bias.tolist(), self.fonction_name]
        return data
    
    
    def save_for_log(self) -> List:
        """Exporte les poids et biais arrondis à 3 décimales pour les logs."""
        return [
            np.round(self.weight, 3).tolist(),
            np.round(self.bias, 3).tolist(),
            self.fonction_name
        ]