## Librairies requises :  
#### Natives  
- math (calcul mathématiques)  
- numpy (matrice et vecteur)  
- json (stockage des reseaux de neurones)  
- os (séparateur de l'os pour sauvegarde)

#### À installer (pip install ...)  
- future (annotations)  
- typing (annotations)  
- nptyping (annotations)  -supprimé dans le dernier push au profit d'un typing natif de numpy-
- pygame (affichage graphique)  
______________________

## Exécution :
Dans le fichier main ce trouve l'appel de la fonction simulation :
```
simulation(visualisation=True, pop_size=1, fonction="tanh", epoque_min=1)
```
- visualisation : boolean > active ou désactive l'affichage graphique. Privilégier False pour gagner en vitesse de calcul
- pop_size : int > nombre de bateaux générés à chaque époque. Privilégier 1 lorsqu'il s'agit de visualiser un bateau enregistré. Eviter les nombres impairs pour l'entraintement
- fonction :  "tanh" / "sigmoid" > fonction d'activation des bateaux
- epoque_min : int > le nombre d'époque minimale à générer

Pour exécuter le programme, lancer le fichier main.py, avec les paramètres souhaités dans l'appel de la fonction ci dessus.

Lors du lancement, les questions suivantes vous vous être demandés dans le terminal :

1. set : >> set d'entrainement [1-6]
2. charger un fichier ? y : >> charger une sauvegarde de bateau, cf 4.
   3. (si y) nom du fichier sans l'extension) : >> path complet (sans .json) si le fichier est ailleurs que dans "sauvegardes bateaux/"
4. (fin du programme) enregistrer meilleur bateau ? y : >> pour charger le meilleur bateau de cette simulation (uniquement)
   5. (si y) nom du fichier (sans l'exntension) :  >> automatiquement sauvegardé dans "sauvegardes bateaux/"


## Fonctionnement :
#### But
Générer un bateau capable de faire n'importe quel parcours de vitesse sur un axe x,y en un temps records.

#### Principe
Un quantité pop_size de bateau est généré pour un parcours donné.
Chaque bateau dispose d'un réseau de neurone généré aléatoirement.
Tous les bateaux disposent du même nombre de déplacement pour finir le parcours.
À chaque fois qu'un bateau traverse un checkpoint dans le bon ordre, il gagne 10 points.
Si le bateau fini le parcours dans sa globalité, il gagne un bonus en fonction du temps passée. (amélioration de la vitesse)
S'il ne finit pas le parcours, il gagne un bonus en fonction de sa proximité avec le prochain checkpoint. (amélioration des premières générations qui ne traversent aucun checkpoint)

À la fin d'une époque la moitié des bateaux avec le meilleur score sont conservés pour la prochaine époque.
L'autre moitié est éliminée et remplacé par une copie des 50% meilleurs avec une mutation.

La simulation prends fin lorsque les deux conditions suivantes sont validées :
1. Au moins 1 bateau a réussi à faire le parcours en entier dans le temps imparti
2. Le nombre d'époque minimum a été généré (nécessaire pour améliorer la vitesse des bateaux)