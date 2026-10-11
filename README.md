# NEAT-Boat-Racing

## Description du projet

Ce projet a pour objectif d'implémenter un réseau de neurones conçu *from scratch* (sans l'utilisation de frameworks de Deep Learning tiers) combiné à un algorithme génétique. Il vise à simuler et à étudier le pilotage autonome de bateaux évoluant au sein d'un circuit de course pour apprendre à franchir efficacement une série de points de contrôle (*checkpoints*).

---

## Fonctionnalités Principales

* **Réseau de neurones *from scratch*** : Implémentation complète de l'architecture neuronale (couches, fonctions d'activation, poids et biais) via `numpy`.
* **Algorithme Génétique** : Sélection, croisement et mutation permettant l'apprentissage de conduite autonome au fil des générations.
* **Environnement de course (Parcours Bateau)** : Simulation interactive de conduite et d'apprentissage évolutif sur différents tracés.
* **Gestion des performances** : Enregistrement de la progression et de la fitness des individus pour l'analyse de l'apprentissage.

---

## État du projet & Évolutions à venir

**Le projet est actuellement en cours de développement.**

Les évolutions suivantes sont prévues ou en cours d'intégration :
* **Interactivités & Visualisation** : Les anciens mécanismes de visualisation générés par IA vont être remplacés par une interface développée sur mesure. Cela apportera des fonctionnalités plus interactives, telles qu'une interface de création de parcours d'entrainement, la gestion simplifiée des sauvegardes et l'interaction directe en cours de simulation.
* **Obstacles** : Ajout d'obstacles dynamique ou fixes durant les phases d'entraînement pour accroître la complexité de navigation.
* **Refonte de l'architecture** : Les mécanismes de sauvegarde via le `logger` (initialement développés par **Hadrien Clément** pour une visualisation sous Unity) seront ultérieurement supprimés afin de conserver un projet 100 % Python.

---

## Installation du projet

Le projet s'appuie sur [Poetry](https://python-poetry.org/) pour la gestion des dépendances et de l'environnement virtuel.

1. **Cloner le dépôt et vous placer à la racine du projet.**
2. **Installer les dépendances avec Poetry :**
   ```bash
   poetry install
   ```
3. **Activer l'environnement virtuel :**
   ```bash
   poetry shell
   ```

---

## Comment utiliser le projet ?

Pour exécuter la simulation de course de bateaux, lancez le script principal depuis la racine du projet :

```bash
poetry run python src/parcoursBateau/main.py
```

Des invites interactives dans le terminal vous permettront de configurer votre session :
* **Affichage (o/n)** : Activer le rendu graphique Pygame ou exécuter l'entraînement en arrière-plan (mode headless).
* **Population** : Nombre de bateaux simulés par génération.
* **Époques** : Nombre minimum de générations à exécuter.
* **Méthode de sélection** : Sélection du mode de reproduction (`fitnessProportionate`, `rangBased`, `tournament`, etc.).
* **Parcours** : Choix du ou des circuits d'entraînement.

---

## Structure globale du code

```text
NEAT-Boat-Racing/
│
├── src/
│   ├── UserInterface/          # Interface utilisateur & visualisation
│   ├── NEAT/         # Module 'From Scratch' du réseau de neurones (cerveau, couches)
│   └── parcoursBateau/        # Logique de la simulation de course et entités (bateau, checkpoints)
│       ├── sauvegardes bateaux/    # Modèles réseau sauvegardés (.json)
│       └── ...
│
├── logs/                      # Fichiers de log des sessions d'entraînement
├── pyproject.toml             # Configuration et dépendances du projet (Poetry)
└── README.md                  # Documentation du projet
```