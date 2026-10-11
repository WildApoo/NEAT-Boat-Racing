from logger import Logger

from parcoursBateau.simulation import simulation
import numpy as np
from pathlib import Path
from typing import Literal

from bateau import Bateau
from UserInterface.visualisation import show_heredity
import random

seed = 2
np.random.seed(seed)
random.seed(seed)

# Diff types de log possibles
LoggerAll = Logger(mode="json", tri="all")  # "json" ou "binary"
LoggerBest = Logger(mode="json", tri="best", save_neurones=5)   # "json" ou "binary"
SAUVEGARDE_DIR = Path(__file__).resolve().parent / "sauvegardes bateaux"

visu: bool = input("Affichage o/n\n: ") == "o"
pop: int = int(input("pop\n: "))
epoque: int = int(input("epoque min\n: "))
SELECTION_METHOD: list[str] = ["fitnessProportionate",
                                "rangBased",
                                "tournament",
                                "score2",
                                "score4",
                                "score10"]

selection: str = input("methode selection\n: ")

while selection not in SELECTION_METHOD:
    print(f"Erreur : méthode inexistante. Méthodes possibles : {SELECTION_METHOD}")
    selection = input("methode selection\n: ")

parcours: list[Literal["1", "2", "3", "4", "5", "6"]] = input(
    "set  (pour faire un enchainement de parcours, séparer les noms des sets par \"-\", ex 1-2-4\n: ").split("-")

num: Literal["1", "2", "3", "4", "5", "6"]
population: list[Bateau] = []
if len(parcours) > 1:
    for num in parcours:
        population = simulation(visualisation=visu,
                                pop_size=pop,
                                fonctionActivation="tanh",
                                popDeDepart=population,
                                numeroSet=num,
                                epoque_min=epoque,
                                methode_selection=selection,
                                LoggerInput=LoggerBest,
                                repertoire_sauvegarde=SAUVEGARDE_DIR)


else:
    fileName: str = input("Nom sauvegarde bateau (skip > enter) : ")
    num = parcours[0]
    population = simulation(visualisation=visu,
                            pop_size=pop,
                            fonctionActivation="tanh",
                            fileNameBateauDepart=fileName,
                            numeroSet=num,
                            epoque_min=epoque,
                            methode_selection=selection,
                            LoggerInput=LoggerBest,
                            repertoire_sauvegarde=SAUVEGARDE_DIR)


if input("visualiser l'arbre ? o/n") == "o":
    sujet = population[0]
    print(f"sujet {sujet.cerveau.id} et heredity : {sujet.cerveau.heredity}")

    show_heredity(population, fullscreen=True)


