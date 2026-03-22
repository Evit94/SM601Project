"""
Interface graphique pour l'algorithme de Floyd-Warshall
SM601 - Theorie des graphes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import os

# Importer les fonctions algorithmiques
from src.graphe import charger_graphe
from src.algorithme import floyd_warshall, reconstruire_chemin


# ============================================================================
#  Couleurs et styles
# ============================================================================

COULEURS = {
    "bg_principal": "#1e1e2e",
    "bg_card": "#2a2a3e",
    "bg_header": "#12122a",
    "accent": "#7c6af7",
    "accent_hover": "#9d8fff",
    "texte": "#e0e0f0",
    "texte_secondaire": "#9090b0",
    "inf": "#ff6b6b",
    "negatif": "#ffa94d",
    "zero": "#74c0fc",
    "positif": "#69db7c",
    "danger": "#ff4444",
    "succes": "#51cf66",
    "btn_graphe": "#2d2d4e",
    "btn_graphe_hover": "#3d3d6e",
    "separateur": "#3a3a5c",
}

POLICE_MONO = ("Courier New", 11)
POLICE_TITRE = ("Helvetica", 18, "bold")
POLICE_SOUS_TITRE = ("Helvetica", 13)
POLICE_BTN = ("Helvetica", 11, "bold")
POLICE_LABEL = ("Helvetica", 11)


# ============================================================================
#  Classe principale de l'interface
# ============================================================================

class FloydWarshallGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Floyd-Warshall — SM601 Theorie des graphes")
        self.configure(bg=COULEURS["bg_principal"])
        self.resizable(True, True)
        self.geometry("1100x750")
        self.minsize(900, 600)

        # Donnees courantes
        self.numero_graphe = None
        self.n = None
        self.matrice_adj = None
        self.L_final = None
        self.P_final = None
        self.circuit_absorbant = False
        self.etapes = []          # liste de (L_k, P_k) pour k=0..n
        self.index_etape = 0

        # Conteneur principal
        self.container = tk.Frame(self, bg=COULEURS["bg_principal"])
        self.container.pack(fill="both", expand=True)

        self._afficher_selection()

    # -------------------------------------------------------------------------
    #  Frame 1 : Sélection du graphe
    # -------------------------------------------------------------------------

    def _afficher_selection(self):
        """Affiche l'écran de sélection du graphe."""
        self._vider_container()

        # En-tête
        header = tk.Frame(self.container, bg=COULEURS["bg_header"], pady=30)
        header.pack(fill="x")

        tk.Label(
            header,
            text="ALGORITHME DE FLOYD-WARSHALL",
            font=POLICE_TITRE,
            bg=COULEURS["bg_header"],
            fg=COULEURS["accent"],
        ).pack()
        tk.Label(
            header,
            text="Recherche des chemins les plus courts  —  SM601 Theorie des graphes",
            font=POLICE_SOUS_TITRE,
            bg=COULEURS["bg_header"],
            fg=COULEURS["texte_secondaire"],
        ).pack(pady=(4, 0))

        # Corps
        corps = tk.Frame(self.container, bg=COULEURS["bg_principal"], pady=30)
        corps.pack(fill="both", expand=True)

        tk.Label(
            corps,
            text="Selectionnez un graphe a analyser",
            font=POLICE_SOUS_TITRE,
            bg=COULEURS["bg_principal"],
            fg=COULEURS["texte"],
        ).pack(pady=(0, 20))

        # Grille de boutons 5+5+3
        grille = tk.Frame(corps, bg=COULEURS["bg_principal"])
        grille.pack()

        for idx in range(13):
            num = idx + 1
            fichier = os.path.join("graphes", f"graphe{num}.txt")
            existe = os.path.exists(fichier)
            col = idx % 5
            row = idx // 5

            btn = tk.Button(
                grille,
                text=f"Graphe {num}",
                font=POLICE_BTN,
                bg=COULEURS["btn_graphe"] if existe else COULEURS["separateur"],
                fg=COULEURS["texte"] if existe else COULEURS["texte_secondaire"],
                activebackground=COULEURS["btn_graphe_hover"],
                activeforeground=COULEURS["texte"],
                relief="flat",
                width=14,
                height=2,
                cursor="hand2" if existe else "arrow",
                state="normal" if existe else "disabled",
                command=lambda n=num: self._charger_graphe(n),
            )
            btn.grid(row=row, column=col, padx=8, pady=8)

            if existe:
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COULEURS["btn_graphe_hover"]))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=COULEURS["btn_graphe"]))

        # Bouton quitter
        tk.Button(
            corps,
            text="Quitter",
            font=POLICE_BTN,
            bg=COULEURS["danger"],
            fg="white",
            activebackground="#cc0000",
            activeforeground="white",
            relief="flat",
            width=12,
            height=1,
            cursor="hand2",
            command=self.destroy,
        ).pack(pady=30)

    # -------------------------------------------------------------------------
    #  Chargement et exécution de l'algorithme
    # -------------------------------------------------------------------------

    def _charger_graphe(self, numero):
        """Charge le graphe et exécute Floyd-Warshall."""
        n, matrice = charger_graphe(numero)
        if n is None:
            messagebox.showerror("Erreur", f"Le fichier graphe{numero}.txt est introuvable.")
            return

        self.numero_graphe = numero
        self.n = n
        self.matrice_adj = matrice

        L, P, circuit_absorbant, etapes = floyd_warshall(n, matrice)
        self.L_final = L
        self.P_final = P
        self.circuit_absorbant = circuit_absorbant
        self.etapes = etapes
        self.index_etape = 0

        self._afficher_resultats()

    # -------------------------------------------------------------------------
    #  Frame 2 : Résultats (onglets)
    # -------------------------------------------------------------------------

    def _afficher_resultats(self):
        """Affiche l'écran des résultats avec onglets."""
        self._vider_container()

        # En-tête
        header = tk.Frame(self.container, bg=COULEURS["bg_header"], pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Graphe {self.numero_graphe}  —  {self.n} sommet(s)",
            font=POLICE_TITRE,
            bg=COULEURS["bg_header"],
            fg=COULEURS["accent"],
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="← Retour",
            font=POLICE_BTN,
            bg=COULEURS["btn_graphe"],
            fg=COULEURS["texte"],
            activebackground=COULEURS["btn_graphe_hover"],
            activeforeground=COULEURS["texte"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self._afficher_selection,
        ).pack(side="right", padx=20)

        # Notebook
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TNotebook",
            background=COULEURS["bg_principal"],
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background=COULEURS["btn_graphe"],
            foreground=COULEURS["texte"],
            padding=(14, 6),
            font=POLICE_BTN,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COULEURS["accent"])],
            foreground=[("selected", "white")],
        )

        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Onglet 1 : Matrice d'adjacence
        frame_adj = self._creer_frame_onglet()
        self.notebook.add(frame_adj, text="  Matrice d'adjacence  ")
        self._remplir_onglet_adjacence(frame_adj)

        # Onglet 2 : Itérations
        frame_iter = self._creer_frame_onglet()
        self.notebook.add(frame_iter, text="  Iterations  ")
        self._remplir_onglet_iterations(frame_iter)

        # Onglet 3 : Résultat final
        frame_final = self._creer_frame_onglet()
        self.notebook.add(frame_final, text="  Resultat final  ")
        self._remplir_onglet_final(frame_final)

        # Onglet 4 : Chemins
        frame_chemins = self._creer_frame_onglet()
        self.notebook.add(frame_chemins, text="  Chemins  ")
        self._remplir_onglet_chemins(frame_chemins)

    # -------------------------------------------------------------------------
    #  Onglet 1 — Matrice d'adjacence
    # -------------------------------------------------------------------------

    def _remplir_onglet_adjacence(self, frame):
        tk.Label(
            frame,
            text="Matrice d'adjacence du graphe",
            font=POLICE_SOUS_TITRE,
            bg=COULEURS["bg_card"],
            fg=COULEURS["texte"],
        ).pack(pady=(12, 4))

        zone = tk.Frame(frame, bg=COULEURS["bg_card"])
        zone.pack(fill="both", expand=True, padx=20, pady=10)
        self._afficher_matrice_widget(zone, self.matrice_adj, self.n, est_predecesseurs=False)

    # -------------------------------------------------------------------------
    #  Onglet 2 — Itérations
    # -------------------------------------------------------------------------

    def _remplir_onglet_iterations(self, frame):
        """Onglet avec navigation entre les étapes k."""
        n_etapes = len(self.etapes)  # = n+1

        # Barre de navigation
        nav = tk.Frame(frame, bg=COULEURS["bg_card"], pady=8)
        nav.pack(fill="x")

        self.lbl_etape = tk.Label(
            nav,
            text="",
            font=POLICE_SOUS_TITRE,
            bg=COULEURS["bg_card"],
            fg=COULEURS["texte"],
            width=30,
        )
        self.lbl_etape.pack(side="left", padx=20)

        btn_suiv = tk.Button(
            nav,
            text="Suivant →",
            font=POLICE_BTN,
            bg=COULEURS["accent"],
            fg="white",
            activebackground=COULEURS["accent_hover"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self._changer_etape(1),
        )
        btn_suiv.pack(side="right", padx=10)

        btn_prec = tk.Button(
            nav,
            text="← Precedent",
            font=POLICE_BTN,
            bg=COULEURS["btn_graphe"],
            fg=COULEURS["texte"],
            activebackground=COULEURS["btn_graphe_hover"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self._changer_etape(-1),
        )
        btn_prec.pack(side="right", padx=2)

        # Zone d'affichage des deux matrices côte à côte
        self.frame_iter_contenu = tk.Frame(frame, bg=COULEURS["bg_card"])
        self.frame_iter_contenu.pack(fill="both", expand=True, padx=10, pady=4)

        self._afficher_etape()

    def _changer_etape(self, delta):
        n_etapes = len(self.etapes)
        self.index_etape = (self.index_etape + delta) % n_etapes
        self._afficher_etape()

    def _afficher_etape(self):
        """Met à jour l'affichage de l'étape courante."""
        for w in self.frame_iter_contenu.winfo_children():
            w.destroy()

        k = self.index_etape
        L_k, P_k = self.etapes[k]

        if k == 0:
            titre = "Etat initial  —  L(0) et P(0)"
        else:
            titre = f"Apres iteration k={k-1}  —  L({k}) et P({k})"

        self.lbl_etape.configure(text=titre)

        # Deux colonnes
        col_L = tk.LabelFrame(
            self.frame_iter_contenu,
            text=f"  L({k}) — Distances  ",
            font=POLICE_LABEL,
            bg=COULEURS["bg_card"],
            fg=COULEURS["texte"],
            bd=1,
            relief="groove",
        )
        col_L.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=4)
        self._afficher_matrice_widget(col_L, L_k, self.n, est_predecesseurs=False)

        col_P = tk.LabelFrame(
            self.frame_iter_contenu,
            text=f"  P({k}) — Predecesseurs  ",
            font=POLICE_LABEL,
            bg=COULEURS["bg_card"],
            fg=COULEURS["texte"],
            bd=1,
            relief="groove",
        )
        col_P.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=4)
        self._afficher_matrice_widget(col_P, P_k, self.n, est_predecesseurs=True)

    # -------------------------------------------------------------------------
    #  Onglet 3 — Résultat final
    # -------------------------------------------------------------------------

    def _remplir_onglet_final(self, frame):
        if self.circuit_absorbant:
            # Alerte circuit absorbant
            alerte = tk.Frame(frame, bg="#3a1010", pady=16)
            alerte.pack(fill="x", padx=20, pady=10)
            tk.Label(
                alerte,
                text="⚠  CIRCUIT ABSORBANT DETECTE",
                font=("Helvetica", 14, "bold"),
                bg="#3a1010",
                fg=COULEURS["danger"],
            ).pack()
            tk.Label(
                alerte,
                text="Les distances minimales ne sont pas definies pour ce graphe.",
                font=POLICE_LABEL,
                bg="#3a1010",
                fg=COULEURS["texte"],
            ).pack(pady=(4, 0))

            detail = tk.Label(
                alerte,
                text="",
                font=POLICE_MONO,
                bg="#3a1010",
                fg=COULEURS["negatif"],
                justify="left",
            )
            lignes = []
            for i in range(self.n):
                if self.L_final[i][i] < 0:
                    lignes.append(f"  Sommet {i}  :  L[{i}][{i}] = {self.L_final[i][i]}")
            detail.configure(text="\n".join(lignes))
            detail.pack(pady=(8, 0))
        else:
            tk.Label(
                frame,
                text="✓  Aucun circuit absorbant detecte",
                font=("Helvetica", 12, "bold"),
                bg=COULEURS["bg_card"],
                fg=COULEURS["succes"],
            ).pack(pady=(12, 4))

            # Deux colonnes
            zone = tk.Frame(frame, bg=COULEURS["bg_card"])
            zone.pack(fill="both", expand=True, padx=10, pady=4)

            col_L = tk.LabelFrame(
                zone,
                text="  L — Matrice des distances minimales  ",
                font=POLICE_LABEL,
                bg=COULEURS["bg_card"],
                fg=COULEURS["texte"],
                bd=1,
                relief="groove",
            )
            col_L.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=4)
            self._afficher_matrice_widget(col_L, self.L_final, self.n, est_predecesseurs=False)

            col_P = tk.LabelFrame(
                zone,
                text="  P — Matrice des predecesseurs  ",
                font=POLICE_LABEL,
                bg=COULEURS["bg_card"],
                fg=COULEURS["texte"],
                bd=1,
                relief="groove",
            )
            col_P.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=4)
            self._afficher_matrice_widget(col_P, self.P_final, self.n, est_predecesseurs=True)

    # -------------------------------------------------------------------------
    #  Onglet 4 — Chemins
    # -------------------------------------------------------------------------

    def _remplir_onglet_chemins(self, frame):
        if self.circuit_absorbant:
            tk.Label(
                frame,
                text="Chemins non disponibles : circuit absorbant detecte.",
                font=POLICE_LABEL,
                bg=COULEURS["bg_card"],
                fg=COULEURS["danger"],
            ).pack(pady=40)
            return

        # Formulaire
        formulaire = tk.Frame(frame, bg=COULEURS["bg_card"], pady=14)
        formulaire.pack(fill="x", padx=20)

        tk.Label(formulaire, text="Sommet de depart :", font=POLICE_LABEL,
                 bg=COULEURS["bg_card"], fg=COULEURS["texte"]).grid(row=0, column=0, padx=8, pady=4, sticky="e")
        self.entry_depart = tk.Entry(formulaire, font=POLICE_MONO, width=6,
                                     bg=COULEURS["bg_header"], fg=COULEURS["texte"],
                                     insertbackground=COULEURS["texte"], relief="flat", bd=4)
        self.entry_depart.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(formulaire, text="Sommet d'arrivee :", font=POLICE_LABEL,
                 bg=COULEURS["bg_card"], fg=COULEURS["texte"]).grid(row=0, column=2, padx=8, pady=4, sticky="e")
        self.entry_arrivee = tk.Entry(formulaire, font=POLICE_MONO, width=6,
                                      bg=COULEURS["bg_header"], fg=COULEURS["texte"],
                                      insertbackground=COULEURS["texte"], relief="flat", bd=4)
        self.entry_arrivee.grid(row=0, column=3, padx=8, pady=4)

        tk.Button(
            formulaire,
            text="Chemin specifique",
            font=POLICE_BTN,
            bg=COULEURS["accent"],
            fg="white",
            activebackground=COULEURS["accent_hover"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self._afficher_chemin_specifique,
        ).grid(row=0, column=4, padx=14, pady=4)

        tk.Button(
            formulaire,
            text="Tous les chemins",
            font=POLICE_BTN,
            bg=COULEURS["btn_graphe"],
            fg=COULEURS["texte"],
            activebackground=COULEURS["btn_graphe_hover"],
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self._afficher_tous_chemins,
        ).grid(row=0, column=5, padx=6, pady=4)

        # Zone de résultat scrollable
        result_frame = tk.Frame(frame, bg=COULEURS["bg_card"])
        result_frame.pack(fill="both", expand=True, padx=20, pady=(4, 10))

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_chemins = tk.Text(
            result_frame,
            font=POLICE_MONO,
            bg=COULEURS["bg_header"],
            fg=COULEURS["texte"],
            insertbackground=COULEURS["texte"],
            relief="flat",
            bd=6,
            state="disabled",
            yscrollcommand=scrollbar.set,
            wrap="word",
        )
        self.text_chemins.pack(fill="both", expand=True)
        scrollbar.config(command=self.text_chemins.yview)

        # Tags couleur
        self.text_chemins.tag_configure("chemin", foreground=COULEURS["positif"])
        self.text_chemins.tag_configure("distance", foreground=COULEURS["accent"])
        self.text_chemins.tag_configure("absent", foreground=COULEURS["texte_secondaire"])
        self.text_chemins.tag_configure("titre", foreground=COULEURS["accent_hover"],
                                        font=("Helvetica", 11, "bold"))
        self.text_chemins.tag_configure("erreur", foreground=COULEURS["danger"])

    def _ecrire_chemin(self, depart, arrivee):
        """Retourne les lignes décrivant le chemin de depart à arrivee."""
        lignes = []
        if depart == arrivee:
            lignes.append((f"  {depart} → {arrivee}  :  distance = 0\n", "chemin"))
            return lignes

        dist = self.L_final[depart][arrivee]
        if dist == math.inf:
            lignes.append((f"  {depart} → {arrivee}  :  pas de chemin\n", "absent"))
            return lignes

        chemin = reconstruire_chemin(self.P_final, depart, arrivee)
        if chemin is None:
            lignes.append((f"  {depart} → {arrivee}  :  pas de chemin\n", "absent"))
            return lignes

        chemin_str = " → ".join(str(s) for s in chemin)
        lignes.append((f"  {depart} → {arrivee}  :  {chemin_str}", "chemin"))
        lignes.append((f"   (distance = {dist})\n", "distance"))
        return lignes

    def _afficher_chemin_specifique(self):
        try:
            d = int(self.entry_depart.get())
            a = int(self.entry_arrivee.get())
        except ValueError:
            self._ecrire_zone_chemins([("Erreur : veuillez saisir des entiers valides.\n", "erreur")])
            return

        if not (0 <= d < self.n and 0 <= a < self.n):
            self._ecrire_zone_chemins([
                (f"Erreur : les sommets doivent etre entre 0 et {self.n - 1}.\n", "erreur")
            ])
            return

        lignes = [("Chemin le plus court :\n", "titre")]
        lignes += self._ecrire_chemin(d, a)
        self._ecrire_zone_chemins(lignes)

    def _afficher_tous_chemins(self):
        lignes = [("Tous les chemins les plus courts :\n\n", "titre")]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    lignes += self._ecrire_chemin(i, j)
        self._ecrire_zone_chemins(lignes)

    def _ecrire_zone_chemins(self, lignes):
        """Écrit les lignes dans la zone de texte des chemins."""
        self.text_chemins.configure(state="normal")
        self.text_chemins.delete("1.0", "end")
        for texte, tag in lignes:
            self.text_chemins.insert("end", texte, tag)
        self.text_chemins.configure(state="disabled")

    # -------------------------------------------------------------------------
    #  Widget matrice générique
    # -------------------------------------------------------------------------

    def _afficher_matrice_widget(self, parent, matrice, n, est_predecesseurs=False):
        """Crée un widget Text affichant la matrice avec couleurs."""
        frame = tk.Frame(parent, bg=COULEURS["bg_card"])
        frame.pack(fill="both", expand=True, padx=6, pady=6)

        # Scrollbars
        sx = tk.Scrollbar(frame, orient="horizontal")
        sx.pack(side="bottom", fill="x")
        sy = tk.Scrollbar(frame, orient="vertical")
        sy.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            font=POLICE_MONO,
            bg=COULEURS["bg_header"],
            fg=COULEURS["texte"],
            relief="flat",
            bd=4,
            state="normal",
            wrap="none",
            xscrollcommand=sx.set,
            yscrollcommand=sy.set,
        )
        text.pack(fill="both", expand=True)
        sx.config(command=text.xview)
        sy.config(command=text.yview)

        # Tags
        text.tag_configure("inf", foreground=COULEURS["inf"])
        text.tag_configure("negatif", foreground=COULEURS["negatif"])
        text.tag_configure("zero", foreground=COULEURS["zero"])
        text.tag_configure("positif", foreground=COULEURS["positif"])
        text.tag_configure("header", foreground=COULEURS["accent"], font=("Courier New", 11, "bold"))
        text.tag_configure("sep", foreground=COULEURS["separateur"])
        text.tag_configure("dash", foreground=COULEURS["texte_secondaire"])

        INF = math.inf
        largeur = 5
        for i in range(n):
            for j in range(n):
                val = matrice[i][j]
                if val == INF:
                    largeur = max(largeur, len("INF") + 2)
                elif est_predecesseurs and val == -1:
                    largeur = max(largeur, 3)
                else:
                    largeur = max(largeur, len(str(int(val) if val != INF else val)) + 2)

        # En-tête colonnes
        en_tete = " " * (largeur + 1) + "|"
        for j in range(n):
            en_tete += str(j).rjust(largeur)
        text.insert("end", en_tete + "\n", "header")

        # Séparateur
        sep = "-" * (largeur + 1) + "+" + "-" * (n * largeur) + "\n"
        text.insert("end", sep, "sep")

        # Lignes
        for i in range(n):
            # Numéro de ligne
            text.insert("end", str(i).rjust(largeur) + " |", "header")
            for j in range(n):
                val = matrice[i][j]
                if val == INF:
                    cell = "INF".rjust(largeur)
                    text.insert("end", cell, "inf")
                elif est_predecesseurs and val == -1:
                    cell = "-".rjust(largeur)
                    text.insert("end", cell, "dash")
                else:
                    v = int(val) if isinstance(val, float) and val == int(val) else val
                    cell = str(v).rjust(largeur)
                    if v < 0:
                        text.insert("end", cell, "negatif")
                    elif v == 0:
                        text.insert("end", cell, "zero")
                    else:
                        text.insert("end", cell, "positif")
            text.insert("end", "\n")

        text.configure(state="disabled")

    # -------------------------------------------------------------------------
    #  Utilitaires
    # -------------------------------------------------------------------------

    def _creer_frame_onglet(self):
        """Retourne un Frame stylisé pour un onglet."""
        f = tk.Frame(self.notebook, bg=COULEURS["bg_card"])
        return f

    def _vider_container(self):
        """Supprime tous les widgets du conteneur principal."""
        for widget in self.container.winfo_children():
            widget.destroy()


# ============================================================================
#  Point d'entrée
# ============================================================================

def main():
    app = FloydWarshallGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
