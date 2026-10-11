# TER : Réseau de Neurones *From Scratch* & Simulations Évolutives

Bienvenue dans ce projet de création de réseau de neurones codé "from scratch" (sans l'utilisation de librairies de Machine Learning comme TensorFlow ou PyTorch) et ses applications dans différentes simulations basées sur des algorithmes génétiques.

**Note Importante ("Made with AI")** : 
Toute la logique mathématique (Numpy) et l'architecture du réseau sont propres au projet. Toutefois, **les classes dédiées à la visualisation des simulations (via Pygame/Matplotlib), ainsi que tout le système de sauvegarde et de chargement (load and save) du *Cerveau* (réseau de neurones), ont été entièrement codés à l'aide de l'Intelligence Artificielle.**

---

## Fonctionnalités Principales

* **Réseau de neurones *from scratch*** : Création d'une architecture de neurones (couches, fonctions d'activation, poids et biais) gérée via `numpy`.
* **Algorithme Génétique** : Implémentation d'algorithmes évolutionnistes (mutations, différentes méthodes de sélection : *fitness proportionate*, par rang, par tournoi, etc.).
* **Simulations** :
  * **Parcours Bateau** : Une simulation où des "bateaux" apprennent à naviguer sur un circuit et à franchir des checkpoints grâce à l'évolution.
  * **Eau et Civilisation** : Simulateur de développement d'entités autour de points d'eau.
* **Système de Logs et Sauvegardes** : Export au format JSON des meilleurs modèles ("Cerveaux") évalués au fil des époques.

---

## Installation

Le projet utilise un fichier `pyproject.toml` qui liste toutes les dépendances requises (`numpy`, `pygame`, `matplotlib`, `nptyping`, `future`).

À la racine du projet (là où se trouve le `pyproject.toml`), ouvrez un terminal. Il est fortement recommandé de créer un environnement virtuel (`.venv`) au préalable pour que tout fonctionne correctement :

1. **Créer l'environnement virtuel :**
   ```bash
   python -m venv .venv
   ```
2. **Activer l'environnement virtuel :**
   * **Sur Windows :** `.venv\Scripts\activate` ou `.\.venv\Scripts\Activate.ps1` (sur PowerShell)
   * **Sur Linux / macOS :** `source .venv/bin/activate`
3. **Installer le projet et ses dépendances :**
   ```bash
   pip install -e .
   ```
Cela installera le projet et toutes ses dépendances en mode "éditable".

---

## Comment utiliser le projet ?

Une fois l'installation terminée, vous pouvez lancer les deux simulations principales de la manière suivante. Pour vous assurer que les chemins (paths) soient toujours bien détectés, il est conseillé de lancer les scripts depuis la **racine** du projet.

### 1. Simulation "Parcours Bateau"

C'est la simulation la plus complète et interactive.
```bash
python src/parcoursBateau/main.py
```
Lors de l'exécution dans le terminal, le programme va vous poser plusieurs questions pour paramétrer la session d'entraînement évolutif :
1. **Affichage (o/n)** : Tapez `o` pour activer le rendu visuel Pygame des bateaux, ou `n` pour faire du calcul rapide en arrière-plan sans rendu.
2. **Population (pop)** : Renseignez le nombre d'individus par génération (ex: `100`).
3. **Epoque min** : Nombre de générations minimal avant l'arrêt de la simulation (ex: `50`).
4. **Méthode de sélection** : Entrez le nom exact de la méthode souhaitée pour sélectionner les individus reproduits, parmi : `fitnessProportionate`, `rangBased`, `tournament`, `score2`, `score4`, ou `score10`.
5. **Parcours (set)** : Sélectionnez le ou les circuits (de `1` à `6`) à utiliser pour l'entraînement. 
   - Pour un seul parcours, tapez simplement son numéro (ex: `1`). Le programme vous demandera ensuite si vous souhaitez charger un modèle existant ("Nom sauvegarde bateau"). Appuyez simplement sur **Entrée** pour commencer de zéro.
   - Pour faire un entraînement successif sur plusieurs parcours, séparez-les par un tiret (ex: `1-2-4` ou `1-6-4-5`). L'IA s'entraînera au fur et à mesure sur ces différents circuits.

***Astuces d'exécution :***
- **Pour l'entrainement :** Il est très fortement conseillé de **désactiver la visualisation** (`n`) lors d'un apprentissage sur un grand nombre de générations. Le script s'exécutera beaucoup plus rapidement en arrière-plan.
- **Pour la visualisation :** Si vous souhaitez voir un bateau préalablement entrainé naviguer, activez l'affichage (`o`) et définissez une **population de `1`**. Cela permet au modèle chargé de naviguer seul et d'être facilement observable.

#### Mécaniques avancées de la simulation

* **Sauvegarde et Chargement (Save & Load) :** À la fin de la simulation (ou à chaque point clé), les meilleurs réseaux de neurones sont enregistrés au format `.json` dans `src/parcoursBateau/sauvegardes bateaux/`. Ce fichier contient la topologie, les poids et les biais du *"Cerveau"*. Pour recharger un de ces modèles, il suffit d'entrer son nom (sans l'extension, ou avec, selon votre logique) à l'invite "Nom sauvegarde bateau", et le bateau reprendra son apprentissage (ou l'application) tel que vous l'avez laissé.
* **Transmission de génération et Mutations :** Chaque bateau possède des "gènes" (les poids et biais de son réseau). À la fin de chaque époque (génération), les individus avec le meilleur score (fitness) sont sélectionnés. Leurs gènes sont **transmis** pour créer la nouvelle population, tout en appliquant des **mutations** aléatoires. Cela permet d'explorer et d'apprendre de nouvelles trajectoires pour atteindre les checkpoints.
* **Système de Logs et d'Analyse :** Les performances de chaque génération (fitness maximum, fitness moyen, etc.) sont systématiquement écrites dans des fichiers de log au format JSON dans le dossier `logs/`. Ces fichiers vous permettent, par exemple, d'utiliser le script `analyse post entrainement.py` pour générer des courbes `matplotlib` et visualiser la courbe d'apprentissage et la progression de votre algorithme !

### 2. Simulation "Eau et Civilisation"

Une simulation visuelle de déplacement et de développement.
```bash
python src/eauEtCivilisation/main.py
```
Le code lancera directement la simulation (une interface graphique devrait s'ouvrir pour visualiser la logique).

---

## Structure globale du code

```text
├── install/                   # Scripts automatiques d'installation .bat
├── src/                       # Code source Python (installé en module)
│   ├── reseauNeurone/         # Le coeur "From scratch" (cerveau.py, couche.py)
│   ├── parcoursBateau/        # Code de la simulation d'évolution des bateaux
│   │   ├── sauvegardes bateaux/    # Models entrainés
│   │   ├── __init__.py, main.py, Bateau.py, etc...
│   └── eauEtCivilisation/     # Code de l'autre simulation
│       ├── __init__.py, main.py, city.py, waterPoint.py, etc...
├── logs/                      # Dossier pour les fichiers de logging
├── pyproject.toml             # Configuration du module Python
└── readme.md                  # Ce fichier
```
