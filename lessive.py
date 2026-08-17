import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DOSSIER_PROGRAMME = Path(__file__).resolve().parent
FICHIER_SAUVEGARDE = DOSSIER_PROGRAMME / "lessive.json"

CAPACITE_PAR_DEFAUT = 6.0  # kg


# ============================================================
# POIDS DES VÊTEMENTS
# ============================================================

VETEMENTS = {
    "Chaussette": 50,
    "Sous-vêtement / boxer": 70,
    "Débardeur": 100,
    "T-shirt": 180,
    "T-shirt manches longues": 300,
    "Chemise": 250,
    "Short": 200,
    "Pantalon": 500,
    "Jean": 750,
    "Jogging": 350,
    "Pull léger": 350,
    "Pull épais / laine": 600,
    "Sweat": 400,
    "Hoodie": 600,
    "Veste légère": 500,
    "Veste épaisse": 800,
    "Manteau": 1000,
    "Pyjama": 250,
    "Serviette de bain": 500,
}


# ============================================================
# DONNEES
# ============================================================

linge = {}
capacite_machine = CAPACITE_PAR_DEFAUT


# ============================================================
# SAUVEGARDE / CHARGEMENT
# ============================================================

def charger_donnees():
    global linge, capacite_machine

    if not FICHIER_SAUVEGARDE.exists():
        linge = {}
        capacite_machine = CAPACITE_PAR_DEFAUT
        return

    try:
        with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as fichier:
            donnees = json.load(fichier)

        linge = donnees.get("linge", {})
        capacite_machine = donnees.get(
            "capacite_machine",
            CAPACITE_PAR_DEFAUT
        )

    except (json.JSONDecodeError, OSError, TypeError):
        linge = {}
        capacite_machine = CAPACITE_PAR_DEFAUT


def sauvegarder_donnees():
    donnees = {
        "capacite_machine": capacite_machine,
        "linge": linge
    }

    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as fichier:
        json.dump(
            donnees,
            fichier,
            ensure_ascii=False,
            indent=4
        )


# ============================================================
# CALCUL DU POIDS
# ============================================================

def poids_total():
    total = 0

    for vetement, quantite in linge.items():
        total += VETEMENTS[vetement] * quantite

    return total


# ============================================================
# CAPACITE DE LA MACHINE
# ============================================================

def changer_capacite():
    global capacite_machine

    texte = entree_capacite.get().replace(",", ".")

    try:
        nouvelle_capacite = float(texte)

    except ValueError:
        messagebox.showerror(
            "Erreur",
            "La capacité doit être un nombre.\n\n"
            "Exemple : 6 ou 7.5"
        )
        return

    if nouvelle_capacite <= 0:
        messagebox.showerror(
            "Erreur",
            "La capacité doit être supérieure à 0 kg."
        )
        return

    capacite_machine = nouvelle_capacite

    sauvegarder_donnees()
    mettre_a_jour_interface()


# ============================================================
# SUPPRIMER UNE UNITE
# ============================================================

def supprimer_un(vetement):
    if vetement not in linge:
        return

    linge[vetement] -= 1

    if linge[vetement] <= 0:
        del linge[vetement]

    sauvegarder_donnees()
    mettre_a_jour_interface()


# ============================================================
# SUPPRIMER TOUT UN TYPE
# ============================================================

def supprimer_tout(vetement):
    if vetement not in linge:
        return

    confirmation = messagebox.askyesno(
        "Supprimer",
        f"Supprimer tous les « {vetement} » ?"
    )

    if confirmation:
        del linge[vetement]

        sauvegarder_donnees()
        mettre_a_jour_interface()


# ============================================================
# AJOUTER UN VÊTEMENT
# ============================================================

def ajouter_vetement():

    vetement = combo_vetements.get()

    if not vetement:
        messagebox.showwarning(
            "Attention",
            "Choisis d'abord un vêtement."
        )
        return

    try:
        quantite = int(entree_quantite.get())

    except ValueError:
        messagebox.showwarning(
            "Attention",
            "La quantité doit être un nombre entier."
        )
        return

    if quantite <= 0:
        messagebox.showwarning(
            "Attention",
            "La quantité doit être supérieure à zéro."
        )
        return

    if vetement not in linge:
        linge[vetement] = 0

    linge[vetement] += quantite

    sauvegarder_donnees()
    mettre_a_jour_interface()

    entree_quantite.delete(0, tk.END)
    entree_quantite.insert(0, "1")


# ============================================================
# LESSIVE FAITE
# ============================================================

def lessive_faite():

    if not linge:
        messagebox.showinfo(
            "Lessive",
            "Il n'y a actuellement aucun linge enregistré."
        )
        return

    confirmation = messagebox.askyesno(
        "Lessive faite",
        "As-tu vraiment fait ta lessive ?\n\n"
        "Tout le linge enregistré sera supprimé."
    )

    if confirmation:
        linge.clear()

        sauvegarder_donnees()
        mettre_a_jour_interface()


# ============================================================
# MISE A JOUR DE L'INTERFACE
# ============================================================

def mettre_a_jour_interface():

    total = poids_total()

    poids_kg = total / 1000

    capacite_grammes = capacite_machine * 1000

    pourcentage = (total / capacite_grammes) * 100

    # --------------------------------------------------------
    # POIDS
    # --------------------------------------------------------

    label_poids.config(
        text=f"{poids_kg:.2f} kg / {capacite_machine:.2f} kg"
    )

    # --------------------------------------------------------
    # POURCENTAGE
    # --------------------------------------------------------

    label_pourcentage.config(
        text=f"{pourcentage:.1f} %"
    )

    # --------------------------------------------------------
    # BARRE
    # --------------------------------------------------------

    barre["value"] = min(pourcentage, 100)

    # --------------------------------------------------------
    # STATUT
    # --------------------------------------------------------

    if pourcentage >= 100:

        label_statut.config(
            text="🔴 LESSIVE À FAIRE — CAPACITÉ ATTEINTE !",
            foreground="red"
        )

    elif pourcentage >= 90:

        label_statut.config(
            text="🟠 PRESQUE PLEIN — PRÉPARE TA LESSIVE",
            foreground="orange"
        )

    elif pourcentage >= 75:

        label_statut.config(
            text="🟡 Tu peux encore ajouter du linge",
            foreground="#CC9900"
        )

    else:

        label_statut.config(
            text="🟢 OK — tu peux continuer",
            foreground="green"
        )

    # --------------------------------------------------------
    # RECREATION DE LA LISTE
    # --------------------------------------------------------

    for widget in cadre_liste.winfo_children():
        widget.destroy()

    # En-têtes
    tk.Label(
        cadre_liste,
        text="Vêtement",
        font=("Arial", 11, "bold"),
        width=25,
        anchor="w"
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Label(
        cadre_liste,
        text="Quantité",
        font=("Arial", 11, "bold"),
        width=10
    ).grid(row=0, column=1, padx=5)

    tk.Label(
        cadre_liste,
        text="Poids",
        font=("Arial", 11, "bold"),
        width=12
    ).grid(row=0, column=2, padx=5)

    tk.Label(
        cadre_liste,
        text="Actions",
        font=("Arial", 11, "bold"),
        width=22
    ).grid(row=0, column=3, padx=5)

    # --------------------------------------------------------
    # VÊTEMENTS
    # --------------------------------------------------------

    for ligne, (vetement, quantite) in enumerate(
        linge.items(),
        start=1
    ):

        poids = VETEMENTS[vetement] * quantite

        # Nom
        tk.Label(
            cadre_liste,
            text=vetement,
            width=25,
            anchor="w"
        ).grid(
            row=ligne,
            column=0,
            padx=5,
            pady=3
        )

        # Quantité
        tk.Label(
            cadre_liste,
            text=str(quantite),
            width=10
        ).grid(
            row=ligne,
            column=1,
            padx=5
        )

        # Poids
        tk.Label(
            cadre_liste,
            text=f"{poids} g",
            width=12
        ).grid(
            row=ligne,
            column=2,
            padx=5
        )

        # Cadre des boutons
        cadre_actions = tk.Frame(cadre_liste)

        cadre_actions.grid(
            row=ligne,
            column=3,
            padx=5
        )

        # Bouton -1
        bouton_moins = tk.Button(
            cadre_actions,
            text="− 1",
            width=6,
            command=lambda v=vetement: supprimer_un(v)
        )

        bouton_moins.pack(
            side="left",
            padx=2
        )

        # Bouton supprimer tout
        bouton_supprimer = tk.Button(
            cadre_actions,
            text="Supprimer",
            width=9,
            command=lambda v=vetement: supprimer_tout(v)
        )

        bouton_supprimer.pack(
            side="left",
            padx=2
        )


# ============================================================
# FENETRE
# ============================================================

fenetre = tk.Tk()

fenetre.title("Gestionnaire de lessive")

fenetre.geometry("750x650")

fenetre.minsize(700, 600)


# ============================================================
# CHARGEMENT
# ============================================================

charger_donnees()


# ============================================================
# TITRE
# ============================================================

titre = tk.Label(
    fenetre,
    text="Gestionnaire de lessive",
    font=("Arial", 24, "bold")
)

titre.pack(pady=20)


# ============================================================
# CAPACITE
# ============================================================

cadre_capacite = tk.Frame(fenetre)

cadre_capacite.pack(pady=5)


tk.Label(
    cadre_capacite,
    text="Capacité de la machine :",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=5
)


entree_capacite = tk.Entry(
    cadre_capacite,
    width=8
)

entree_capacite.grid(
    row=0,
    column=1,
    padx=5
)

entree_capacite.insert(
    0,
    str(capacite_machine)
)


tk.Label(
    cadre_capacite,
    text="kg",
    font=("Arial", 12)
).grid(
    row=0,
    column=2,
    padx=5
)


bouton_capacite = tk.Button(
    cadre_capacite,
    text="Enregistrer",
    command=changer_capacite
)

bouton_capacite.grid(
    row=0,
    column=3,
    padx=10
)


# ============================================================
# POIDS
# ============================================================

label_poids = tk.Label(
    fenetre,
    text="0.00 kg / 6.00 kg",
    font=("Arial", 20, "bold")
)

label_poids.pack(pady=10)


# ============================================================
# POURCENTAGE
# ============================================================

label_pourcentage = tk.Label(
    fenetre,
    text="0.0 %",
    font=("Arial", 16)
)

label_pourcentage.pack()


# ============================================================
# BARRE DE PROGRESSION
# ============================================================

barre = ttk.Progressbar(
    fenetre,
    orient="horizontal",
    length=600,
    mode="determinate"
)

barre.pack(pady=10)


# ============================================================
# STATUT
# ============================================================

label_statut = tk.Label(
    fenetre,
    text="",
    font=("Arial", 14, "bold")
)

label_statut.pack(pady=10)


# ============================================================
# AJOUT
# ============================================================

cadre_ajout = tk.Frame(fenetre)

cadre_ajout.pack(pady=15)


tk.Label(
    cadre_ajout,
    text="Vêtement :",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=5
)


combo_vetements = ttk.Combobox(
    cadre_ajout,
    values=list(VETEMENTS.keys()),
    state="readonly",
    width=25
)

combo_vetements.grid(
    row=0,
    column=1,
    padx=5
)

combo_vetements.current(0)


tk.Label(
    cadre_ajout,
    text="Quantité :",
    font=("Arial", 12)
).grid(
    row=0,
    column=2,
    padx=5
)


entree_quantite = tk.Entry(
    cadre_ajout,
    width=5
)

entree_quantite.grid(
    row=0,
    column=3,
    padx=5
)

entree_quantite.insert(
    0,
    "1"
)


bouton_ajouter = tk.Button(
    cadre_ajout,
    text="Ajouter",
    command=ajouter_vetement
)

bouton_ajouter.grid(
    row=0,
    column=4,
    padx=10
)


# ============================================================
# LISTE DES VETEMENTS
# ============================================================

cadre_liste = tk.Frame(
    fenetre,
    relief="groove",
    borderwidth=1
)

cadre_liste.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


# ============================================================
# LESSIVE FAITE
# ============================================================

bouton_lessive = tk.Button(
    fenetre,
    text="🧺 Lessive faite",
    command=lessive_faite,
    font=("Arial", 12, "bold")
)

bouton_lessive.pack(
    pady=15
)


# ============================================================
# INITIALISATION
# ============================================================

mettre_a_jour_interface()


# ============================================================
# LANCEMENT
# ============================================================

fenetre.mainloop()