from src.parcoursBateau.Bateau import Bateau
import numpy as np

def muter(bateau_parent):
    # On crée un nouveau bateau au point de départ
    enfant = Bateau(0, 0, bateau_parent.goal_x, bateau_parent.goal_y, bateau_parent.cp_name, fonction_activation=bateau_parent.fonction_choisie)

    # On copie les neurones du parent
    enfant.W_1 = bateau_parent.W_1.copy()
    enfant.W_2 = bateau_parent.W_2.copy()
    enfant.b_1 = bateau_parent.b_1.copy()
    enfant.b_2 = bateau_parent.b_2.copy()

    # On ajoute un "bruit" aléatoire (la mutation)
    taux_mutation = 0.3
    enfant.W_1 += np.random.normal(0, taux_mutation, size=enfant.W_1.shape)
    enfant.W_2 += np.random.normal(0, taux_mutation, size=enfant.W_2.shape)

    return enfant