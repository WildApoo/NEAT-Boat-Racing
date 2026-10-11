from __future__ import annotations
from NEAT.couche import Couche
import numpy as np
import numpy.typing as npt
import random
import copy
import json
import matplotlib.pyplot as plt
from pathlib import Path


class Cerveau:
    nb = 1

    def __init__(self, nb_inputs: int, nb_output: int, nb_hidden_couches: int, min_neurones: int,  max_neurones: int, fonction: str = "tanh"):
        self.id = Cerveau.nb
        Cerveau.nb += 1

        # index = compteur mutation, index 0 pour l'initialisation, valeur 0 équivaut à pas de mutation
        self.heredity: list[int] = [0]

        self.inputs = np.zeros((nb_inputs, 1), dtype=float)

        self.couches = []

        if nb_hidden_couches > 0:
            self.couches.append(
                Couche(
                    random.randint(min_neurones, max_neurones),
                    self.inputs.shape[0],
                    fonction=fonction))

            couche_a_creer = nb_hidden_couches - 1
            for i in range(couche_a_creer):
                self.couches.append(
                    Couche(
                        random.randint(min_neurones, max_neurones),
                        self.couches[-1].weight.shape[0],
                        fonction=fonction))

        taille_precedente = self.couches[-1].weight.shape[0] if self.couches else self.inputs.shape[0]

        self.outputs = Couche(
            nb_output,
            taille_precedente,
            fonction=fonction)

        self.taux_mutation = {
            "debut": {"poids": 0.1, "ajout_neurone": 0.2, "suppression_neurone": 0.004, "ajout_couche": 0.1},
            "stagnation": {"poids": 0.1, "ajout_neurone": 0.1, "suppression_neurone": 0.004, "ajout_couche": 0.01},
            "amelioration": {"poids": 0.01, "ajout_neurone": 0.01, "suppression_neurone": 0.002, "ajout_couche": 0.005},
        }


    def reflechir(self, inputs: npt.NDArray[np.float64]) ->  npt.NDArray[np.float64]:
        self.inputs = inputs

        if self.couches:
            result = self.couches[0].get_value(self.inputs)

            for couche in self.couches[1:]:
                result = couche.get_value(result)

            result = self.outputs.get_value(result)
        else:
            result = self.outputs.get_value(self.inputs)

        return result

    def _actualise_heredity(self, parent: int, compteur: int):
        # index = compteur mutation, index 0 pour l'initialisation, valeur 0 équivaut à pas de mutation
        while len(self.heredity) < compteur:
            self.heredity.append(0)
        self.heredity.append(parent)

    def mutation(self, parent: int, compteur: int, dynamisme_apprentissage: str = "amelioration") -> None:
        self._actualise_heredity(parent, compteur)
        # changement des poids (systématique)
        for couche in self.couches:
            couche.mutation(taux_mutation=self.taux_mutation[dynamisme_apprentissage]["poids"])

        self.outputs.mutation(taux_mutation=self.taux_mutation[dynamisme_apprentissage]["poids"])

        ### A FAIRE
        # ajout d'un neurone (faible)
        if (random.random() < self.taux_mutation[dynamisme_apprentissage]["ajout_neurone"]):
            self.ajouter_un_neurone_quelque_part()
        # suppression d'un neurone (faible)
        #if (random.random() < self.taux_mutation[dynamisme_apprentissage]["suppression_neurone"]):
        #    self.supprimer_un_neurone_quelque_part()    # cette fonction doit faire l'objet d'une attention spéciale à l'avenir
        # ajout d'une couche (faible)
        if (random.random() < self.taux_mutation[dynamisme_apprentissage]["ajout_couche"]):
            # sélection aléatoire de l'index
            index_insert = random.randint(0, len(self.couches))

            nb_row_previous = None
            fonction_name = self.couches[0].fonction_name if self.couches else self.outputs.fonction_name

            if index_insert == 0:
                # insertion après la couche d'entrée
                nb_row_previous = self.inputs.shape[0]
                
            else:
                # insertion entre deux couches cachées ou avant la sortie
                nb_row_previous = self.couches[index_insert-1].weight.shape[0]
                
            
            self.couches.insert(index_insert, Couche(1, 1, "tanh"))

            # matrice identitaire pour les poids et biais à 0 pour ne pas perturber le réseau
            self.couches[index_insert].copy_couche(np.identity(nb_row_previous), np.zeros((nb_row_previous, 1)), fonction_name)



    def copy_cerveau(self, model: Cerveau) -> None:
        self.couches = copy.deepcopy(model.couches)
        self.outputs = copy.deepcopy(model.outputs)

    def save(self, repertoire_sauvegarde: str | Path, params: dict = None):
        repertoire_sauvegarde = Path(repertoire_sauvegarde)
        couches_list = []
        for couche in self.couches:
            couches_list.append(couche.save_to_json())

        # On prépare les données en convertissant les tableaux numpy en listes
        data = {
            "input":self.inputs.tolist(),
            "output":self.outputs.save_to_json(),
            "couches":couches_list
        }

        if params is not None:
            data["simulation_params"] = params
        
        repertoire_sauvegarde.mkdir(parents=True, exist_ok=True)
        
        nom_fichier = input("nom du fichier (sans l'extension) : ")
        
        filename = repertoire_sauvegarde / f"{nom_fichier}.json"
       
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Cerveau du bateau sauvegardé dans {filename}")

    from pathlib import Path
    import json
    import numpy as np

    def load(self, repertoire_sauvegarde: str | Path, filename: str = None):
        repertoire_sauvegarde = Path(repertoire_sauvegarde)
        
        try:
            # 1. Gestion du nom de fichier
            if filename is None:
                nom_input = input("Nom du fichier (sans l'extension) : ")
                filename = f"{nom_input}.json"
            
            # 2. Construction propre du chemin complet
            chemin_complet = repertoire_sauvegarde / filename
            
            # On force l'extension .json si elle est absente
            if chemin_complet.suffix != ".json":
                chemin_complet = chemin_complet.with_suffix(".json")

            # 3. Lecture du fichier
            with open(chemin_complet, "r") as f:
                data = json.load(f)

            # 4. Re-construction des données
            self.inputs = np.array(data["input"])

            # Chargement de la couche de sortie
            # Note : Assure-toi que copy_couche gère le redimensionnement
            self.outputs = Couche(1, 1, fonction="tanh")
            out_w, out_b, out_f = data["output"]
            self.outputs.copy_couche(np.array(out_w), np.array(out_b), out_f)

            # Chargement des couches cachées
            self.couches.clear()
            for c_data in data["couches"]:
                nouvelle_couche = Couche(1, 1, fonction="tanh")
                nouvelle_couche.copy_couche(np.array(c_data[0]), np.array(c_data[1]), c_data[2])
                self.couches.append(nouvelle_couche)

            print(f"Cerveau chargé avec succès depuis {chemin_complet}")

        except FileNotFoundError:
            print(f"Erreur : Le fichier {chemin_complet} est introuvable.")
        except Exception as e:
            print(f"Une erreur inattendue est survenue : {e}")

    # ----------------------------------------------------------------------
    # code ia
    def ajouter_un_neurone_quelque_part(self):
        # impossible d'ajouter un neurone s'il n'y a pas de couches
        if len(self.couches) == 0:
            return

        # 1. Choisir une couche au hasard (sauf la sortie)
        index = random.randint(0, len(self.couches) - 1)

        # 2. Ajouter le neurone (ajoute une ligne dans cette couche)
        self.couches[index].add_neurone()

        # 3. Réparer la couche suivante (ajoute une colonne)
        if index < len(self.couches) - 1:
            # La couche suivante est une couche cachée
            self.couches[index + 1].add_link()
        else:
            # La couche suivante était la sortie
            self.outputs.add_link()

    def supprimer_un_neurone_quelque_part(self):
        if len(self.couches) == 0: return # Sécurité

        index_couche = random.randint(0, len(self.couches) - 1)
        index_neurone = random.randint(0, self.couches[index_couche].weight.shape[0] - 1)
        
        # 1. Supprimer le neurone physiquement
        nb_restant = self.couches[index_couche].remove_neurone(index_neurone)

        # 2. Si la couche n'est pas vide, on répare juste la couche suivante
        if nb_restant > 0:
            if index_couche == len(self.couches) - 1:
                self.outputs.remove_link(index_neurone)
            else:
                self.couches[index_couche + 1].remove_link(index_neurone)
                
        # 3. Si la couche est VIDE, on doit la supprimer et reconnecter
        else:
            del self.couches[index_couche]
            
            # Déterminer la nouvelle source (couche précédente ou inputs)
            if index_couche == 0:
                nb_entrees_pour_suivante = self.inputs.shape[0]
            else:
                nb_entrees_pour_suivante = self.couches[index_couche-1].weight.shape[0]

            # Déterminer quelle couche doit être "réparée" (la nouvelle couche à cet index ou la sortie)
            if index_couche < len(self.couches):
                cible = self.couches[index_couche]
            else:
                cible = self.outputs

            # Réinitialisation de la matrice de la couche cible
            # On recrée les poids car la dimension 'previous' a changé
            self._reconnecter_couche(cible, nb_entrees_pour_suivante)

    def _reconnecter_couche(self, couche, nb_entrees):
        # On garde le nombre de neurones actuel de la couche, mais on change ses entrées
        nb_neurones_actuels = couche.weight.shape[0]
        # Option 'Hasard' (recommandée pour la diversité génétique)
        couche.weight = np.random.uniform(-1, 1, size=(nb_neurones_actuels, nb_entrees))

    
    def visualiser(self, afficher: bool = True, ax=None, titre: str = "Visualisation du reseau"):
        """
        Ecrit entièrement par l'ia
        """
        nb_inputs = self.inputs.shape[0]
        nb_outputs = self.outputs.weight.shape[0]

        tailles_couches = [nb_inputs]
        for couche in self.couches:
            tailles_couches.append(couche.weight.shape[0])
        tailles_couches.append(nb_outputs)

        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 7))
        else:
            fig = ax.figure

        ax.clear()

        x_spacing = 2.0
        y_spacing = 1.2
        rayon = 0.18
        epaisseur_max = 4.0

        max_neurones = max(tailles_couches) if tailles_couches else 1
        positions = []

        for idx_couche, nb_neurones in enumerate(tailles_couches):
            x = idx_couche * x_spacing
            if nb_neurones <= 0:
                positions.append([])
                continue

            y_top = ((max_neurones - 1) * y_spacing) / 2.0
            y_offset = ((max_neurones - nb_neurones) * y_spacing) / 2.0

            couche_positions = []
            for i in range(nb_neurones):
                y = y_top - y_offset - i * y_spacing
                couche_positions.append((x, y))
            positions.append(couche_positions)

        for idx_couche in range(1, len(positions)):
            prev_positions = positions[idx_couche - 1]
            curr_positions = positions[idx_couche]

            if idx_couche <= len(self.couches):
                matrice_poids = self.couches[idx_couche - 1].weight
            else:
                matrice_poids = self.outputs.weight

            for i_curr, (x2, y2) in enumerate(curr_positions):
                for i_prev, (x1, y1) in enumerate(prev_positions):
                    poids = float(matrice_poids[i_curr, i_prev])
                    couleur = "red" if poids >= 0 else "blue"
                    epaisseur = min(epaisseur_max, max(0.2, abs(poids)))
                    ax.plot([x1, x2], [y1, y2], color=couleur, linewidth=epaisseur, alpha=0.7, zorder=1)

        for couche_positions in positions:
            for x, y in couche_positions:
                cercle = plt.Circle((x, y), rayon, facecolor="white", edgecolor="black", linewidth=1.5, zorder=3)
                ax.add_patch(cercle)

        ax.set_title(titre)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

        x_max = (len(tailles_couches) - 1) * x_spacing if tailles_couches else x_spacing
        y_span = max(1.0, (max_neurones - 1) * y_spacing)
        ax.set_xlim(-0.8, x_max + 0.8)
        ax.set_ylim(-y_span / 2.0 - 0.8, y_span / 2.0 + 0.8)

        if afficher:
            plt.show()

        return fig, ax
    

    def visualiser_num(self, afficher: bool = True, ax=None, titre: str = "Visualisation du reseau"):
        """
        Visualisation du réseau avec affichage des poids (2 décimales), 
        des biais dans les neurones, et accentuation des épaisseurs.
        """
        """
        Ecrit entièrement par l'ia
        """
        nb_inputs = self.inputs.shape[0]
        nb_outputs = self.outputs.weight.shape[0]

        tailles_couches = [nb_inputs]
        for couche in self.couches:
            tailles_couches.append(couche.weight.shape[0])
        tailles_couches.append(nb_outputs)

        if ax is None:
            fig, ax = plt.subplots(figsize=(14, 9))
        else:
            fig = ax.figure

        ax.clear()

        x_spacing = 2.5  # Augmenté pour laisser de la place au texte des poids
        y_spacing = 1.4  # Augmenté pour laisser de la place aux cercles/biais
        rayon = 0.25     # Légèrement agrandi pour intégrer le texte du biais
        epaisseur_max = 6.0

        max_neurones = max(tailles_couches) if tailles_couches else 1
        positions = []

        # 1. Calcul des positions de tous les neurones
        for idx_couche, nb_neurones in enumerate(tailles_couches):
            x = idx_couche * x_spacing
            if nb_neurones <= 0:
                positions.append([])
                continue

            y_top = ((max_neurones - 1) * y_spacing) / 2.0
            y_offset = ((max_neurones - nb_neurones) * y_spacing) / 2.0

            couche_positions = []
            for i in range(nb_neurones):
                y = y_top - y_offset - i * y_spacing
                couche_positions.append((x, y))
            positions.append(couche_positions)

        # 2. Dessin des connexions (Poids)
        for idx_couche in range(1, len(positions)):
            prev_positions = positions[idx_couche - 1]
            curr_positions = positions[idx_couche]

            if idx_couche <= len(self.couches):
                couche_obj = self.couches[idx_couche - 1]
            else:
                couche_obj = self.outputs
            
            matrice_poids = couche_obj.weight

            for i_curr, (x2, y2) in enumerate(curr_positions):
                for i_prev, (x1, y1) in enumerate(prev_positions):
                    poids = float(matrice_poids[i_curr, i_prev])
                    couleur = "red" if poids >= 0 else "blue"
                    
                    # Accentuation : élévation au carré pour creuser l'écart faibles/forts
                    epaisseur = min(epaisseur_max, max(0.3, (abs(poids) ** 2) * 3.0))
                    
                    # Dessin du trait
                    ax.plot([x1, x2], [y1, y2], color=couleur, linewidth=epaisseur, alpha=0.6, zorder=1)
                    
                    # 1. Base du ratio : on part du milieu (0.5)
                    ratio_base = 0.5
                    
                    # 2. On calcule un décalage unique basé sur les index des neurones connectés
                    # Cela évite que deux lignes qui se croisent partagent le même ratio.
                    # Le modulo (%) permet de varier la position (ex: 35%, 50%, 65% du chemin).
                    decalage_index = ((i_prev + i_curr) % 3) * 0.15 - 0.15
                    
                    # 3. Ajustement selon la pente (vitesse verticale) pour étaler verticalement
                    diff_y = y2 - y1
                    decalage_pente = diff_y * 0.05
                    
                    # Fusion des deux stratégies et bridage de sécurité (entre 25% et 75% du segment)
                    ratio_final = ratio_base + decalage_index + decalage_pente
                    ratio_final = max(0.25, min(0.75, ratio_final))

                    # Application des coordonnées finales
                    x_text = x1 + (x2 - x1) * ratio_final
                    y_text = y1 + (y2 - y1) * ratio_final
                    
                    # Affichage de la valeur du poids
                    ax.text(x_text, y_text, f"{poids:.2f}", color="black", fontsize=8,
                            ha="center", va="center", 
                            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75),
                            zorder=2)

        # 3. Dessin des neurones et affichage des biais
        for idx_couche, couche_positions in enumerate(positions):
            # Récupération de la couche correspondante pour obtenir le biais (pas de biais pour l'input idx 0)
            if idx_couche == 0:
                biais_vecteur = None
            elif idx_couche <= len(self.couches):
                biais_vecteur = self.couches[idx_couche - 1].bias
            else:
                biais_vecteur = self.outputs.bias

            for idx_neurone, (x, y) in enumerate(couche_positions):
                # Dessin du neurone (cercle blanc)
                cercle = plt.Circle((x, y), rayon, facecolor="white", edgecolor="black", linewidth=1.5, zorder=3)
                ax.add_patch(cercle)

                # Affichage du biais (ou "In" pour identifier l'entrée)
                if biais_vecteur is not None:
                    val_biais = float(biais_vecteur[idx_neurone, 0])
                    texte_neurone = f"b:\n{val_biais:.2f}"
                    taille_police = 8
                else:
                    texte_neurone = f"In {idx_neurone}"
                    taille_police = 9

                ax.text(x, y, texte_neurone, color="black", fontsize=taille_police,
                        ha="center", va="center", weight="bold", zorder=4)

        # Réglages de la zone de dessin
        ax.set_title(titre, fontsize=14, weight="bold")
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")

        x_max = (len(tailles_couches) - 1) * x_spacing if tailles_couches else x_spacing
        y_span = max(1.0, (max_neurones - 1) * y_spacing)
        ax.set_xlim(-0.8, x_max + 0.8)
        ax.set_ylim(-y_span / 2.0 - 0.8, y_span / 2.0 + 0.8)

        if afficher:
            plt.show()

        return fig, ax



