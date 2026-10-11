from __future__ import annotations
from parcoursBateau.bateau import Bateau


class Noeud:
    def __init__(self, num: str):
        self.num: str = num
        # où key = époque de l'enfant et key = noeud de l'enfant
        self.enfants: dict[int, list[Noeud]] = {}


def createArbreGenealogique(bateaux: list[Bateau]) -> Noeud:
    # [expression for item in iterable if condition]
    cerveaux = [b.cerveau for b in bateaux]

    max_len = 0
    for cerveau in cerveaux:
        max_len = max(len(cerveau.heredity), max_len)

    arbre = Noeud("racine")
    arbre.enfants[0] = []
    parents = {}
    for cerveau in cerveaux:
        while len(cerveau.heredity) < max_len:
            cerveau.heredity.append(0)
        new_noeud = Noeud(cerveau.id)
        arbre.enfants[0].append(new_noeud)
        parents[cerveau.id] = new_noeud

    for row in range(1, max_len, 1):
        for enfant in cerveaux:
            if enfant.heredity[row] != 0:
                new_noeud = Noeud(enfant.id)
                num_parent = enfant.heredity[row]

                # ajout de l'enfant
                if row in parents[num_parent].enfants.keys():
                    parents[num_parent].enfants[row].append(new_noeud)
                else:
                    parents[num_parent].enfants[row] = [new_noeud]

                # remplacement de son ancien emplacement en tant que parent
                # à partir de maintenant, tout ses enfants commencent ici et non à l'ancien noeud
                parents[enfant.id] = new_noeud

    return arbre


def getStrArbre(noeud: Noeud, prefixe: str = "", est_dernier: bool = True, est_racine: bool = True, epoque: int = None) -> str:
    """
    Génère une représentation textuelle élégante de l'arbre généalogique.
    """
    texte = ""

    # 1. Formatage du nœud courant
    if est_racine:
        texte += f"🌱 {noeud.num}\n"
    else:
        connecteur = "└── " if est_dernier else "├── "
        info_epoque = f"[Ep {epoque}] " if epoque is not None else ""
        texte += f"{prefixe}{connecteur}{info_epoque}{noeud.num}\n"

    # 2. Préparation du préfixe pour les enfants (pour l'indentation verticale)
    nouveau_prefixe = prefixe
    if not est_racine:
        nouveau_prefixe += "    " if est_dernier else "│   "

    # 3. Récupération et tri de tous les enfants
    # On les rassemble dans une liste pour savoir lequel est le tout dernier
    enfants_aplatis = []
    for ep in sorted(noeud.enfants.keys()):
        for enfant in noeud.enfants[ep]:
            enfants_aplatis.append((ep, enfant))

    # 4. Appels récursifs
    for i, (ep, enfant) in enumerate(enfants_aplatis):
        enfant_est_dernier = (i == len(enfants_aplatis) - 1)
        texte += getStrArbre(enfant, nouveau_prefixe, enfant_est_dernier, False, ep)

    return texte

