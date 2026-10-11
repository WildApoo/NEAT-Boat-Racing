# fichier destiné aux méthodes de sélection
import math
import random
from typing import List, Literal
from bateau import Bateau
from checkpoint import CheckPoint
from random import shuffle


class Selection:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, population: List[Bateau], firstCheckPoint: CheckPoint) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.__best_score: float = 0
            self.__pop: List[Bateau] = population
            self.__firstCheckPoint: CheckPoint = firstCheckPoint
            self.__epoqueDepuisBestScore: int = 0
            self.__temperature: float = 5.0
            self.__dynamismeApprentissage: str = "amelioration"    # amelioration, stagnation
            self.__methods = {
                "fitnessProportionate": self.__fitnessProportionate,
                "rangBased": self.__rangBased,
                "tournament": self.__tournament,
                "score2": self.__score2,
                "score4": self.__score4,
                "score10": self.__score10,
                "boltzmann": self.__boltzmann,

            }
            self.__compteurSelection: int = 0
        else:
            self.__firstCheckPoint = firstCheckPoint

    ###
    # Prétraitement
    ###
    def __pretraitement(self):
        self.__compteurSelection += 1
        print(f"-- Sélection & mutation n°{self.__compteurSelection} --")
        self.__pop.sort(key=lambda b: b.calculer_fitness(), reverse=True)

        meilleur_parent = self.__pop[0]
        score = meilleur_parent.score

        if score > self.__best_score:
            self.__best_score = score
            self.__epoqueDepuisBestScore = 0
            self.__dynamismeApprentissage = "amelioration"
        else:
            self.__epoqueDepuisBestScore += 1
            if self.__epoqueDepuisBestScore >= 10: # si aucune amélioration depuis 10 époques, on augmente le taux de mutation pour tenter de sortir d'un éventuel plateau
                self.__dynamismeApprentissage = "stagnation"
                
                # augmentation contrôlée de la température pour favoriser l'exploration
                self.__temperature = min(self.__temperature * 1.1, 10)

            else:
                # léger refroidissement contrôlé
                self.__temperature = max(self.__temperature * 0.99, 0.5)

        if self.__compteurSelection <= 10:
            self.__dynamismeApprentissage = "debut"    

        print(
            f"Bateau : {meilleur_parent.name} | "
            f"score : {meilleur_parent.score:.4f} | "
            f"température : {self.__temperature:.3f} | dynamisme apprentissage : {self.__dynamismeApprentissage}")
        
    
    ########################
    # Méthode de sélection #
    ########################
    def applySelection(self,
                       method: Literal["fitnessProportionate",
                                             "rangBased",
                                             "tournament",
                                             "score2",
                                             "score4",
                                             "score10"]):
        self.__pretraitement()
        self.__methods[method]()

    def __fitnessProportionate(self):
        """
        Ici, la probabilité d'être sélectionné est directement liée à la performance relative de l'individu.

    Sélection par Roulette (Roulette Wheel Selection) : Chaque individu occupe une portion d'une roulette imaginaire 
    proportionnelle à son score de fitness. On "lance" la roue pour choisir un parent.

    Stochastic Universal Sampling (SUS) : Une version améliorée de la roulette. Au lieu d'un seul curseur, 
    on utilise plusieurs curseurs équidistants. Cela réduit le biais statistique et garantit que même les individus 
    moyens ont une chance équitable si la roue tourne une seule fois.
        """
        pass

    def __rangBased(self):
        """
        Ces méthodes ignorent la valeur absolue du score pour ne regarder que le classement. Cela évite que des 
        individus "super-performants" n'écrasent la diversité génétique trop vite.

    Sélection par Rang Linéaire : On attribue une probabilité de sélection basée sur la position (1er, 2ème, etc.) 
    selon une progression linéaire.

    Sélection par Rang Exponentiel : Similaire au linéaire, mais la probabilité chute de manière exponentielle, 
    favorisant très fortement les tous meilleurs.
        """
        pass

    def __tournament(self):
        """
        C'est la méthode la plus populaire car elle est facile à implémenter et à ajuster.Tournoi Déterministe : 
        On choisit $k$ individus au hasard dans la population, et le meilleur des $k$ gagne systématiquement le 
        droit de se reproduire.Tournoi Stochastique : On choisit $k$ individus, mais le meilleur n'a qu'une 
        probabilité $p$ (ex: 80%) de gagner, laissant une chance aux moins bons de transmettre leurs gènes.
        """

        """
        >> marche uniquement si la liste est triée. De plus, 2-3-4 sont systématiquement remplacés par 1, ainsi de suite...
        pop_size = len(self.__pop)
        
        for i in range(0, pop_size, 4):
            self.__pop[i].reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)
            
            for j in range(1, 4):
                if i + j < pop_size:
                    self.__pop[i+j].reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)
                    self.__pop[i+j].cerveau.copy_cerveau(self.__pop[i].cerveau)
                    self.__pop[i+j].cerveau.mutation(dynamisme_apprentissage=self.__dynamismeApprentissage)
        """

        random_pop = self.__pop.copy()
        shuffle(random_pop)

        pop_size = len(self.__pop)
        i_max = pop_size // 4
        i_reste = pop_size % 4
        
        for i in range(0, pop_size, 4):
            
            if(i==i_max and i_reste!=0):
                groupe = random_pop[i:i+i_reste].copy()
            else:
                groupe = random_pop[i:i+4].copy()

            groupe.sort(key=lambda b: b.calculer_fitness(), reverse=True)
            groupe[0].reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)

            for j in range(1, 4):
                if i + j < pop_size: 
                    groupe[j].reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)
                    groupe[j].cerveau.copy_cerveau(groupe[0].cerveau)
                    groupe[j].cerveau.mutation(parent=groupe[0].cerveau.id,
                                               compteur=self.__compteurSelection,
                                               dynamisme_apprentissage=self.__dynamismeApprentissage)
        

        

    def __score2(self) -> None:
        """
        basé que sur le score
        """

        pop_size = len(self.__pop)
        moitie = (pop_size+1) // 2

        for i in range(pop_size):
            self.__pop[i].reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)
            if i >= moitie:
                self.__pop[i].cerveau.copy_cerveau(self.__pop[i-moitie].cerveau)
                self.__pop[i].cerveau.mutation(parent=self.__pop[i-moitie].cerveau.id,
                                               compteur=self.__compteurSelection,
                                               dynamisme_apprentissage=self.__dynamismeApprentissage)

    def __score4(self) -> None:
        """
        basé que sur le score
        """
        pop_size = len(self.__pop)
        quart = (pop_size + 1) // 4

        for b in self.__pop:
            b.reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)

        for i in range(quart, pop_size):
            index_parent = i % quart

            parent_cerveau = self.__pop[index_parent].cerveau

            self.__pop[i].cerveau.copy_cerveau(parent_cerveau)
            self.__pop[i].cerveau.mutation(
                parent=parent_cerveau.id,
                compteur=self.__compteurSelection,
                dynamisme_apprentissage=self.__dynamismeApprentissage
            )

    def __score10(self) -> None:
        """
        basé que sur le score
        """
        pop_size = len(self.__pop)
        decile = (pop_size + 1) // 10

        for b in self.__pop:
            b.reset(self.__firstCheckPoint.x, self.__firstCheckPoint.y, self.__firstCheckPoint.name)

        for i in range(decile, pop_size):
            index_parent = i % decile

            parent_cerveau = self.__pop[index_parent].cerveau

            self.__pop[i].cerveau.copy_cerveau(parent_cerveau)
            self.__pop[i].cerveau.mutation(
                parent=parent_cerveau.id,
                compteur=self.__compteurSelection,
                dynamisme_apprentissage=self.__dynamismeApprentissage
            )


    def __boltzmann(self): 
        """
        La sélection de Boltzmann introduit une "température" qui contrôle la pression de sélection. 
        Au début, avec une température élevée, même les individus moins performants ont une chance raisonnable d'être sélectionnés, 
        favorisant ainsi l'exploration. Au fil du temps, la température diminue, augmentant la pression de sélection et favorisant les meilleurs individus.
        """
        pop_size = len(self.__pop)
        T = self.__temperature # Température initiale
        
        #recupérer fitness 
        
        fitness_values = [b.calculer_fitness() for b in self.__pop]
        
        #Stabilisation numérique : pour éviter les overflow lors du calcul des exponentielles, on soustrait le max de fitness à tous les fitness. Cela ne change pas les probabilités relatives mais évite les valeurs trop grandes.
        max_fitness = max(fitness_values) 
        
        
        exp_values = []
        for fitness in fitness_values:
            exp_values.append(math.exp((fitness - max_fitness) / T)) # on soustrait le max pour éviter les overflow
            
        #Normaliser les exp_values pour obtenir des probabilités
        
        total = sum(exp_values)
        probabilities = [v / total for v in exp_values]
        
        #Creer une nouvelle population en sélectionnant des individus selon les probabilités calculées
        new_population = []
        liste_parents = self.__pop.copy()  # On garde une copie intacte des objets d'origine

        for i in range(pop_size):
            parent = random.choices(liste_parents, weights=probabilities, k=1)[0]
            
            
            child = self.__pop[i]
            child.reset(self.__firstCheckPoint.x, 
                        self.__firstCheckPoint.y, 
                        self.__firstCheckPoint.name)
            
            child.cerveau.copy_cerveau(parent.cerveau)
            child.cerveau.mutation(parent=parent.cerveau.id,
                                   compteur=self.__compteurSelection,
                                   dynamisme_apprentissage=self.__dynamismeApprentissage)
            
            new_population.append(child)
            
        self.__pop = new_population
        