"""
Algorithme de Floyd-Warshall et reconstruction des chemins.
SM601 - Theorie des graphes
"""

import math


def floyd_warshall(n, matrice):
    """
    Execute l'algorithme de Floyd-Warshall.
    Retourne :
      - L : matrice des distances minimales
      - P : matrice des predecesseurs (pour reconstruire les chemins)
      - circuit_absorbant : booleen indiquant la presence d'un circuit absorbant
      - etapes : liste des etats intermediaires [(L_k, P_k)] pour k=0..n
    """
    INF = math.inf

    # Initialisation de L (matrice des distances) = copie de la matrice d'adjacence
    L = [row[:] for row in matrice]

    # Initialisation de P (matrice des predecesseurs)
    # P[i][j] = predecesseur de j sur le chemin de i a j
    # -1 signifie pas de chemin connu
    P = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and matrice[i][j] != INF:
                P[i][j] = i

    # Sauvegarder l'etat initial
    etapes = [([row[:] for row in L], [row[:] for row in P])]

    # Iterations de Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if L[i][k] != INF and L[k][j] != INF:
                    nouvelle_distance = L[i][k] + L[k][j]
                    if nouvelle_distance < L[i][j]:
                        L[i][j] = nouvelle_distance
                        P[i][j] = P[k][j]

        # Sauvegarder l'etat apres chaque iteration k
        etapes.append(([row[:] for row in L], [row[:] for row in P]))

    # Detection de circuit absorbant : si un element diagonal est negatif
    circuit_absorbant = any(L[i][i] < 0 for i in range(n))

    return L, P, circuit_absorbant, etapes


def reconstruire_chemin(P, depart, arrivee):
    """
    Reconstruit le chemin le plus court de 'depart' a 'arrivee'
    a partir de la matrice des predecesseurs P.
    Retourne la liste ordonnee des sommets du chemin, ou None si pas de chemin.
    """
    if P[depart][arrivee] == -1:
        return None

    chemin = [arrivee]
    courant = arrivee
    max_iter = len(P) + 1
    compteur = 0
    while courant != depart:
        courant = P[depart][courant]
        if courant == -1:
            return None
        chemin.append(courant)
        compteur += 1
        if compteur > max_iter:
            return None

    chemin.reverse()
    return chemin
