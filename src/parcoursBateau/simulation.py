from parcoursBateau.bateau import Bateau
from parcoursBateau.set import Set
from NEAT.selection import Selection
from UserInterface.visualisation import dessiner_pygame
from UserInterface.visualisationBis import Visualise
from parcoursBateau.logger import Logger
from pathlib import Path
from typing import Literal, List


def simulation(visualisation: bool = False,
                pop_size: int = 1,
                fonctionActivation: str = "sigmoid",
                fileNameBateauDepart: str = "",
                popDeDepart: List[Bateau] = None,
                numeroSet: Literal["1", "2", "3", "4", "5", "6"] = "1",
                epoque_min: int = 1,
                methode_selection: Literal["fitnessProportionate",
                                "rangBased",
                                "tournament",
                                "score2",
                                "score4",
                                "score10"] = "score2",
                LoggerInput: Logger = None,
                repertoire_sauvegarde: str | Path = None) -> List[Bateau]:

    if repertoire_sauvegarde is None:
        repertoire_sauvegarde = Path(__file__).resolve().parent / "sauvegardes bateaux"
    repertoire_sauvegarde = Path(repertoire_sauvegarde)

    params = locals().copy()
    params.pop("visualisation")
    params.pop("popDeDepart", None)
    params.pop("LoggerInput")
    params.pop("repertoire_sauvegarde")

    #############################################
    # Création du parcours
    #############################################
    set = Set()
    set.change_set(numeroSet)
    cp0 = set.get_first_checkpoint()
    temps = set.get_temps()
    print(f"----- set{numeroSet} -----")
    #############################################

    #############################################
    # Création des bateaux
    #############################################
    bateaux: List[Bateau] = []

    # si on nous fourni une pop de départ (enchaine de set)
    if popDeDepart:
        bateaux = popDeDepart
        if len(bateaux) == 0:
            for i in range(pop_size - len(bateaux)):
                bateaux.append(Bateau(0, 0, cp0.x, cp0.y, cp0.name, fonction_activation=fonctionActivation))
                if fileNameBateauDepart != "":
                    bateaux[-1].cerveau.copy_cerveau(bateaux[0].cerveau)
        else:
            for b in bateaux:
                b.reset(cp0.x, cp0.y, cp0.name)



    # sinon
    else:
        # est qu'on nous donne un bateau à charger ?
        if fileNameBateauDepart != "":
            bateaux.append(Bateau(0, 0, cp0.x, cp0.y, cp0.name, fonction_activation=fonctionActivation))
            bateaux[0].cerveau.load(repertoire_sauvegarde=repertoire_sauvegarde, filename=fileNameBateauDepart)

        for i in range(pop_size - len(bateaux)):
            bateaux.append(Bateau(0, 0, cp0.x, cp0.y, cp0.name, fonction_activation=fonctionActivation))
            if fileNameBateauDepart != "":
                bateaux[-1].cerveau.copy_cerveau(bateaux[0].cerveau)
    #############################################

    #############################################
    # Initialisation du Logger
    #############################################
    logger = None
    if LoggerInput:
        if input("enregistrer les données de la simulation ? y\n:") == "y":
            logger = LoggerInput    # "json" ou "binary"


    #############################################
    # Lancement de la simulation
    #############################################
    selectionManager: Selection = Selection(population=bateaux,
                                           firstCheckPoint=set.get_checkpoints()[-1])
    parcours_entier = False
    epoque = 1

    if visualisation:
        visualise: Visualise = Visualise(bateaux, set.get_checkpoints())
        visualise.init_visualisation()

    while (not parcours_entier) or (epoque <= epoque_min):
        print(epoque)

        # Réinitialisation des cp → liste des bateaux qu'ils ont rencontrés
        for cp in set.get_checkpoints():
            cp.reset()

        # --- PHASE 1 : SIMULATION (Vie des bateaux) ---
        sec = 1
        while sec <= temps:
            if visualisation:
                # dessiner_simulation(bateaux, set.get_checkpoints(), epoque, sec, temps, fig, ax)
                # dessiner_pygame(bateaux, set.get_checkpoints(), epoque, sec, temps)
                visualise.draw_frame(epoque, sec, temps)

                    
            if logger:        
                logger.add_frame(epoque, sec, bateaux, set.get_checkpoints())

            for bateau in bateaux:
                bateau.predict()
                bateau.move()
                # Vérifier les collisions ici
                for cp in set.get_checkpoints():
                    cp.collision(bateau, bateau.cp_name, 1*(temps/(temps + sec)))

            parcours_entier = len(set.get_last_checkpoint().bateau_viewed) != 0


            sec += 1

        # --- PHASE 2 : SÉLECTION & MUTATION ---
        selectionManager.applySelection(method=methode_selection)

        if logger:
            logger.end_epoque(epoque, bateaux)

        """
        if (epoque%10 == 0): #test pour le logger
            bateaux[0].cerveau.visualiser()
            # bateaux[0].cerveau.save(repertoire_sauvegarde=repertoire_sauvegarde, params=params)
            #   logger.save()
        """
        
        epoque += 1
    print("fin")

    print("Affichage du meilleur bateau...")
    if visualisation:
        visualise.end_visualisation()
        bateaux[0].cerveau.visualiser()

    print("Sauvegarde des logs...")
    if logger:
        logger.save()

    if input("enregistrer meilleur bateau ? y\n:") == "y":
        bateaux[0].cerveau.save(repertoire_sauvegarde=repertoire_sauvegarde, params=params)

    return bateaux
