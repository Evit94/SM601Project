"""
Projet SM601 - Theorie des graphes
Algorithme de Floyd-Warshall : Recherche des chemins les plus courts
Annee 2025/2026 - Departement de Mathematiques
"""

import math
import sys
import os


# ============================================================================
#  Lecture du graphe depuis un fichier texte
# ============================================================================

def charger_graphe(numero_graphe):
    """
    Charge un graphe depuis un fichier texte.
    Format du fichier :
      Ligne 1 : nombre de sommets
      Ligne 2 : nombre d'arcs
      Lignes suivantes : extremite_initiale extremite_terminale valeur
    Retourne (n, matrice_adjacence) ou n est le nombre de sommets.
    """
    nom_fichier = f"graphe{numero_graphe}.txt"

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


# ============================================================================
#  Affichage d'une matrice
# ============================================================================

def afficher_matrice(matrice, n, titre="", est_matrice_predecesseurs=False):
    """
    Affiche une matrice de maniere lisible avec alignement des colonnes
    et identification des sommets.
    """
    if titre:
        print(f"\n{titre}")
        print("-" * len(titre))

    # Determiner la largeur maximale des cellules
    largeur = 4
    for i in range(n):
        for j in range(n):
            val = matrice[i][j]
            if val == math.inf:
                largeur = max(largeur, len("INF") + 1)
            elif est_matrice_predecesseurs and val == -1:
                largeur = max(largeur, len("-") + 1)
            else:
                largeur = max(largeur, len(str(val)) + 1)

    # En-tete des colonnes
    en_tete = " " * (largeur + 1) + "|"
    for j in range(n):
        en_tete += str(j).rjust(largeur)
    print(en_tete)

    # Ligne de separation
    separateur = "-" * (largeur + 1) + "+" + "-" * (n * largeur)
    print(separateur)

    # Lignes de la matrice
    for i in range(n):
        ligne = str(i).rjust(largeur) + " |"
        for j in range(n):
            val = matrice[i][j]
            if val == math.inf:
                ligne += "INF".rjust(largeur)
            elif est_matrice_predecesseurs and val == -1:
                ligne += "-".rjust(largeur)
            else:
                ligne += str(val).rjust(largeur)
        print(ligne)


# ============================================================================
#  Algorithme de Floyd-Warshall
# ============================================================================

def floyd_warshall(n, matrice):
    """
    Execute l'algorithme de Floyd-Warshall.
    Retourne :
      - L : matrice des distances minimales
      - P : matrice des predecesseurs (pour reconstruire les chemins)
      - circuit_absorbant : booleen indiquant la presence d'un circuit absorbant
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

    # Affichage de l'etat initial
    afficher_matrice(L, n, "L(0) - Matrice des distances initiale")
    afficher_matrice(P, n, "P(0) - Matrice des predecesseurs initiale", est_matrice_predecesseurs=True)

    # Iterations de Floyd-Warshall
    for k in range(n):
        print(f"\n{'='*60}")
        print(f"  Iteration k = {k} (sommet intermediaire : {k})")
        print(f"{'='*60}")

        for i in range(n):
            for j in range(n):
                if L[i][k] != INF and L[k][j] != INF:
                    nouvelle_distance = L[i][k] + L[k][j]
                    if nouvelle_distance < L[i][j]:
                        L[i][j] = nouvelle_distance
                        P[i][j] = P[k][j]

        afficher_matrice(L, n, f"L({k+1}) - Matrice des distances apres passage par {k}")
        afficher_matrice(P, n, f"P({k+1}) - Matrice des predecesseurs apres passage par {k}", est_matrice_predecesseurs=True)

    # Detection de circuit absorbant : si un element diagonal est negatif
    circuit_absorbant = False
    for i in range(n):
        if L[i][i] < 0:
            circuit_absorbant = True
            break

    return L, P, circuit_absorbant


# ============================================================================
#  Reconstruction d'un chemin
# ============================================================================

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
    # Securite : limiter les iterations pour eviter boucle infinie
    max_iter = len(P) + 1
    compteur = 0
    while courant != depart:
        courant = P[depart][courant]
        if courant == -1:
            return None
        chemin.append(courant)
        compteur += 1
        if compteur > max_iter:
            return None  # Probleme detecte

    chemin.reverse()
    return chemin


def afficher_chemin(L, P, n, depart, arrivee):
    """Affiche le chemin le plus court entre deux sommets."""
    if depart < 0 or depart >= n or arrivee < 0 or arrivee >= n:
        print(f"Erreur : sommets invalides. Les sommets vont de 0 a {n-1}.")
        return

    if depart == arrivee:
        print(f"Chemin de {depart} a {arrivee} : {depart} (distance = 0)")
        return

    if L[depart][arrivee] == math.inf:
        print(f"Il n'existe pas de chemin de {depart} a {arrivee}.")
        return

    chemin = reconstruire_chemin(P, depart, arrivee)
    if chemin is None:
        print(f"Il n'existe pas de chemin de {depart} a {arrivee}.")
        return

    chemin_str = " -> ".join(str(s) for s in chemin)
    print(f"Chemin de {depart} a {arrivee} : {chemin_str}")
    print(f"Distance minimale : {L[depart][arrivee]}")


def afficher_tous_les_chemins(L, P, n):
    """Affiche tous les chemins les plus courts entre toutes les paires de sommets."""
    print("\n" + "=" * 60)
    print("  TOUS LES CHEMINS DE VALEURS MINIMALES")
    print("=" * 60)
    for i in range(n):
        for j in range(n):
            if i != j:
                afficher_chemin(L, P, n, i, j)
    print()


# ============================================================================
#  Boucle d'interface pour les chemins
# ============================================================================

def boucle_chemins(L, P, n):
    """Interface interactive pour afficher les chemins."""
    while True:
        print("\n--- Menu des chemins ---")
        print("1. Afficher un chemin specifique")
        print("2. Afficher tous les chemins")
        print("3. Retourner au menu principal")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            try:
                depart = int(input(f"Sommet de depart (0 a {n-1}) : "))
                arrivee = int(input(f"Sommet d'arrivee (0 a {n-1}) : "))
                print()
                afficher_chemin(L, P, n, depart, arrivee)
            except ValueError:
                print("Erreur : veuillez entrer des nombres entiers.")
        elif choix == "2":
            afficher_tous_les_chemins(L, P, n)
        elif choix == "3":
            break
        else:
            print("Choix invalide.")


# ============================================================================
#  Boucle principale
# ============================================================================

def menu_principal():
    """Boucle principale du programme."""
    print("=" * 60)
    print("  ALGORITHME DE FLOYD-WARSHALL")
    print("  Recherche des chemins les plus courts")
    print("  SM601 - Theorie des graphes")
    print("=" * 60)

    while True:
        print("\n--- Menu Principal ---")
        print("Entrez le numero du graphe a analyser (ex: 1 pour graphe1.txt)")
        print("Entrez 0 pour quitter.")
        choix = input("Votre choix : ").strip()

        if choix == "0":
            print("Au revoir !")
            break

        try:
            numero = int(choix)
        except ValueError:
            print("Erreur : veuillez entrer un nombre entier.")
            continue

        # (1) & (2) Charger le graphe
        print(f"\nChargement du graphe {numero}...")
        n, matrice = charger_graphe(numero)
        if n is None:
            continue

        print(f"Graphe charge avec succes : {n} sommets.")

        # (3) Le graphe est en memoire, on n'accede plus au fichier

        # (4) Affichage du graphe sous forme matricielle
        afficher_matrice(matrice, n, "Matrice d'adjacence du graphe (matrice des valeurs)")

        # (5) Execution de l'algorithme de Floyd-Warshall
        print("\n" + "=" * 60)
        print("  EXECUTION DE L'ALGORITHME DE FLOYD-WARSHALL")
        print("=" * 60)
        L, P, circuit_absorbant = floyd_warshall(n, matrice)

        # (6) Detection de circuit absorbant
        print("\n" + "=" * 60)
        if circuit_absorbant:
            print("  ATTENTION : Le graphe contient au moins un CIRCUIT ABSORBANT !")
            print("  Les distances minimales ne sont pas definies.")
            print("=" * 60)
            # On affiche quand meme les diagonales negatives
            for i in range(n):
                if L[i][i] < 0:
                    print(f"  -> Circuit absorbant detecte passant par le sommet {i} (L[{i}][{i}] = {L[i][i]})")
        else:
            print("  Aucun circuit absorbant detecte.")
            print("=" * 60)

            # Affichage des matrices finales
            afficher_matrice(L, n, "Matrice finale des distances minimales (L)")
            afficher_matrice(P, n, "Matrice finale des predecesseurs (P)", est_matrice_predecesseurs=True)

            # (7) Affichage des chemins
            boucle_chemins(L, P, n)


# ============================================================================
#  Point d'entree
# ============================================================================

if __name__ == "__main__":
    menu_principal()
