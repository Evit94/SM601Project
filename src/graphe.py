"""
Chargement d'un graphe depuis un fichier texte.
SM601 - Theorie des graphes
"""

import math
import os


def charger_graphe(numero_graphe):
    """
    Charge un graphe depuis un fichier texte situe dans le dossier graphes/.
    Format du fichier :
      Ligne 1 : nombre de sommets
      Ligne 2 : nombre d'arcs
      Lignes suivantes : extremite_initiale extremite_terminale valeur
    Retourne (n, matrice_adjacence) ou n est le nombre de sommets.
    """
    nom_fichier = os.path.join("graphes", f"graphe{numero_graphe}.txt")

    if not os.path.exists(nom_fichier):
        print(f"Erreur : le fichier '{nom_fichier}' n'existe pas.")
        return None, None

    with open(nom_fichier, 'r') as f:
        lignes = f.read().strip().split('\n')

    # Ignorer les lignes vides et les commentaires (lignes commencant par #)
    lignes = [l.strip() for l in lignes if l.strip() and not l.strip().startswith('#')]

    n = int(lignes[0])       # nombre de sommets
    m = int(lignes[1])       # nombre d'arcs

    # Initialiser la matrice d'adjacence avec l'infini
    INF = math.inf
    matrice = [[INF] * n for _ in range(n)]

    # Diagonale a 0 (distance d'un sommet a lui-meme)
    for i in range(n):
        matrice[i][i] = 0

    # Lire les arcs
    for k in range(m):
        parties = lignes[2 + k].split()
        i = int(parties[0])
        j = int(parties[1])
        valeur = int(parties[2])
        matrice[i][j] = valeur

    return n, matrice
