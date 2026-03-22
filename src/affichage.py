"""
Affichage terminal : matrices, chemins et menu interactif.
SM601 - Theorie des graphes
"""

import math
from src.graphe import charger_graphe
from src.algorithme import floyd_warshall, reconstruire_chemin


def afficher_matrice(matrice, n, titre="", est_matrice_predecesseurs=False):
    """
    Affiche une matrice de maniere lisible avec alignement des colonnes
    et identification des sommets.
    """
    if titre:
        print(f"\n{titre}")
        print("-" * len(titre))

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

    en_tete = " " * (largeur + 1) + "|"
    for j in range(n):
        en_tete += str(j).rjust(largeur)
    print(en_tete)

    separateur = "-" * (largeur + 1) + "+" + "-" * (n * largeur)
    print(separateur)

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


def boucle_chemins(L, P, n):
    """Interface interactive terminal pour afficher les chemins."""
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


def menu_principal():
    """Boucle principale terminal du programme."""
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

        print(f"\nChargement du graphe {numero}...")
        n, matrice = charger_graphe(numero)
        if n is None:
            continue

        print(f"Graphe charge avec succes : {n} sommets.")
        afficher_matrice(matrice, n, "Matrice d'adjacence du graphe (matrice des valeurs)")

        print("\n" + "=" * 60)
        print("  EXECUTION DE L'ALGORITHME DE FLOYD-WARSHALL")
        print("=" * 60)
        L, P, circuit_absorbant, _ = floyd_warshall(n, matrice)

        print("\n" + "=" * 60)
        if circuit_absorbant:
            print("  ATTENTION : Le graphe contient au moins un CIRCUIT ABSORBANT !")
            print("  Les distances minimales ne sont pas definies.")
            print("=" * 60)
            for i in range(n):
                if L[i][i] < 0:
                    print(f"  -> Circuit absorbant detecte passant par le sommet {i} (L[{i}][{i}] = {L[i][i]})")
        else:
            print("  Aucun circuit absorbant detecte.")
            print("=" * 60)
            afficher_matrice(L, n, "Matrice finale des distances minimales (L)")
            afficher_matrice(P, n, "Matrice finale des predecesseurs (P)", est_matrice_predecesseurs=True)
            boucle_chemins(L, P, n)
