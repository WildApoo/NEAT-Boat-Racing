import matplotlib.pyplot as plt

def dessiner_simulation(bateaux, checkpoints, epoch, temps_actuel, temps_total, fig, ax):
    ax.clear()  # Efface le dessin précédent sans fermer la fenêtre

    # 1. Dessiner les Checkpoints (Cercles rouges)
    for cp in checkpoints:
        ax.plot(cp.x, cp.y, 'ro', markersize=15, alpha=0.6)
        ax.text(cp.x + 1, cp.y + 1, f"CP {cp.name}", fontsize=9)

    # 2. Dessiner les Bateaux (Carrés bleus)
    bx = [b.x for b in bateaux]
    by = [b.y for b in bateaux]

    # Au lieu de ax.quiver, on utilise ax.scatter
    # - 's' : marqueur carré (square)
    # - s=100 : taille du carré (augmente ou diminue selon tes besoins)
    # - color='blue' : couleur de remplissage
    # - edgecolors='black' : contour noir (optionnel, pour mieux voir le carré)
    ax.scatter(bx, by, marker='s', s=100, color='blue', edgecolors='black', label='Bateaux')

    # 3. Paramètres
    ax.grid(True, linestyle='--', alpha=0.7)
    # Note : Le titre et les limites d'axe restent inchangés
    ax.set_title(f"Simulation - Epoque {epoch} : {temps_actuel}/{temps_total}")
    ax.set_xlabel("Position X")
    ax.set_ylabel("Position Y")
    ax.axis('equal')

    # On force le dessin et on attend
    plt.draw()
    plt.pause(0.0001)  # La pause contrôle la vitesse de l'animation

# --- Structure de ta boucle principale ---
# (Reste inchangé)
fig, ax = plt.subplots(figsize=(10, 8))