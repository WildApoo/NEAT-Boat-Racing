import math
import numpy as np
import numpy.typing as npt
from NEAT.cerveau import Cerveau


class Bateau:
    nb = 1  # compteur ID static

    def __init__(self, x: int, y: int, goal_x: int, goal_y: int, cp_name: str, fonction_activation: str = "tanh"):
        self.name = Bateau.nb
        self.id = Bateau.nb
        Bateau.nb += 1
        self.x_dep = x
        self.y_dep = y
        self.x = self.x_dep
        self.y = self.y_dep
        self.speed = 1
        self.max_speed = 5
        self.rotation = 0.0
        self.max_rotation = 45.0
        self.score = 0
        self.bonus_arrival = 0
        self.cp_name = cp_name
        self.goal_x = goal_x
        self.goal_y = goal_y

        # nb input, nb output, nb couche, neurone min, neurone max, fonction
        # self.cerveau = Cerveau(2, 2, np.random.randint(2, 5), 5, 15, fonction=fonction_activation) ancien, ne respecte pas la topoligie élémentaire de départ
        self.cerveau = Cerveau(2, 2, 0, 0, 0, fonction=fonction_activation)


    def move(self):
        rad = math.radians(self.rotation)
        # On arrondit pour éviter les erreurs de flottants (0.00000000006 -> 0)
        dx = math.cos(rad) * self.speed
        dy = math.sin(rad) * self.speed

        self.x += dx
        self.y += dy

    def recompense(self, points: int):
        self.score += points

    def calculer_fitness(self):
        # Calcul de la distance actuelle au but
        dist = math.sqrt((self.goal_x - self.x) ** 2 + (self.goal_y - self.y) ** 2)

        # On ajoute un score inversement proportionnel à la distance
        # Plus dist est petit, plus le bonus est grand.
        # Le +1 évite la division par zéro.
        bonus_proximite = 1 / (dist + 1)

        # On peut multiplier par un facteur pour que ce soit significatif
        self.score += bonus_proximite
        self.score += self.bonus_arrival
        return self.score

    def new_goal(self, x, y, name):
        self.goal_x = x
        self.goal_y = y
        self.cp_name = name

    def reset(self, goal_x, goal_y, cp_name):
        self.x = self.x_dep
        self.y = self.y_dep
        self.score = 0
        self.speed = 1
        self.rotation = 0.0
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.cp_name = cp_name
        self.bonus_arrival = 0

    def predict(self):
        reflexion = self.cerveau.reflechir(self.get_input())


        # 1. vitesse
        self.speed = abs(reflexion[1].item())* self.max_speed

        # 2. orientation +45 - 45 °
        rotation = round(reflexion[0].item() * self.max_rotation)

        # self.rotation = reflexion[0].item() * 360
        self.rotation += rotation

        # On garde la rotation dans [-180, 180]
        self.rotation = (self.rotation + 180) % 360 - 180




    def to_dict(self):
        #Utilisé pour sauvegarder les bateaux dans un fichier json
        return{
            "i": self.name,
            "x": self.x,
            "y": self.y,
            "r": self.rotation,
            "s": self.score,
        }

    def to_list(self):
        return [self.x, self.y, self.rotation, self.score]

    def get_input(self) ->  npt.NDArray[np.float64]:
        """
        # normalisation de la distance
        dx = self.goal_x - self.x
        dy = self.goal_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        # recherche de la meilleure normalisation pour la distance
        # dist_norm = tanh(dist /self.max_speed)  # Normalisation de la distance (tanh pour limiter à [-1, 1])
        # dist_norm = 1/(1+dist)
        # dist_norm = min(1, dist/(self.max_speed*4))  # Normalisation de la distance (plus c'est loin, plus c'est proche de 1)
        # dist_norm = 1 - min(1, dist / (self.max_speed * 10))
        # dist_norm = min(1, dist / (self.max_speed * 10))    # relecture avec romane, c'est mieux d'être proche de 0 quand proche de l'objectif
        
        dist_norm = math.exp(-dist / 100.0)


        # Dans Bateau.py, modifier get_input()
        angle_to_goal = math.atan2(dy, dx) # Angle vers la cible en radians
        angle_diff = angle_to_goal - math.radians(self.rotation)

        # Normalisation entre -1 et 1
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff)) / math.pi
        
        
        dist_norm = 1 / (1+dist)
        angle_to_goal = math.atan2(dy, dx) # Angle vers la cible en radians
        angle_to_goal = (self.rotation + 180) % 360 - 180

        angle_diff = (angle_to_goal - math.radians(self.rotation)) / 180.0
        """

        # distance x et y
        dx = self.goal_x - self.x
        dy = self.goal_y - self.y


        # focus angle
        # 1. Calcul de l'angle absolu vers le checkpoint (en degrés, entre -180 et 180)
        angle_checkpoint = math.degrees(math.atan2(dy, dx))

        # 2. Calcul de la différence brute avec la direction actuelle du bateau
        diff_angle = angle_checkpoint - self.rotation

        # 3. Correction pour toujours choisir le chemin le plus court (entre -180 et 180)
        # Cela règle le problème du passage de 179° à -179° (comme pour les outputs)
        diff_angle = (diff_angle + 180) % 360 - 180

        # 4. Normalisation entre -1 et 1
        angle_diff = diff_angle / 180.0

        # FOCUS distance
        dist = math.sqrt(dx ** 2 + dy ** 2) # a2 +b2 = c2

        # en théorie ceci est la meilleure formule $$input = e^{-\frac{dist}{\sigma}}$$
        # le box sigma selon moi c'est minimum 4 fois la vitesse max * temps qu'il faut pour faire demi tour complet
        # ici 5*4 (4*45°).
        # mais en réalité il faut faire un "surplace" pendant ces 4 tours, si on avance c'est raté
        # donc je vais augmenter à 2* le temps pour faire un demi tour complet
        sigma = self.max_speed * 2 * round(180.0 / self.max_rotation)
        dist_norm = math.exp(-dist / sigma)

        return np.array([
            [dist_norm],
            [angle_diff]
        ])
