from tkinter import *
from sqlite3 import *
from random import randint

# COULEURS
FOND        = "#ffffff"
TEXTE       = "#1a1a1b"
CASE_VIDE   = "#ffffff"
BORDURE     = "#d3d6da"
VERT        = "#6aaa64"
ORANGE      = "#c9b458"
GRIS        = "#787c7e"
BOUTON      = "#6aaa64"
BOUTON_TEXT = "#ffffff"

# CONNEXION A LA BASE DE DONNEES
db = connect("wordle3.db")
curseur = db.cursor()

curseur.execute("""
    CREATE TABLE IF NOT EXISTS equipes (
        id_equipe INTEGER PRIMARY KEY,
        couleur   TEXT
    )
""")
curseur.execute("""
    CREATE TABLE IF NOT EXISTS joueurs (
        id_joueur    INTEGER PRIMARY KEY,
        pseudo       TEXT,
        mot_de_passe TEXT,
        id_equipe    INTEGER,
        score        INTEGER DEFAULT 0,
        FOREIGN KEY (id_equipe) REFERENCES equipes(id_equipe)
    )
""")
curseur.execute("""
    CREATE TABLE IF NOT EXISTS parties (
        id_partie         INTEGER PRIMARY KEY,
        id_joueur         INTEGER,
        mot               TEXT,
        coups_necessaires INTEGER,
        resultat          TEXT,
        FOREIGN KEY (id_joueur) REFERENCES joueurs(id_joueur)
    )
""")

curseur.execute("SELECT COUNT(*) FROM equipes")
if curseur.fetchone()[0] == 0:
    curseur.execute("INSERT INTO equipes (couleur) VALUES ('Rouge')")
    curseur.execute("INSERT INTO equipes (couleur) VALUES ('Bleu')")
db.commit()

# DONNEES DU JEU
liste_mots = [
    "animal", "aviron", "beurre", "brique", "canard",
    "cactus", "cheval", "cloche", "crayon", "eclair",
    "ecrire", "fleurs", "forage", "garage", "gauche",
    "glacer", "goutte", "jardin", "jouets", "lancer",
    "livres", "marche", "marine", "manger", "monter",
    "nature", "navire", "orange", "papier", "parler"
]

# ETAT DU JEU (variables globales)
etat = {
    "ligne"      : 0,
    "id_joueur"  : None,
    "tour_equipe": 1,
    "mot_secret" : liste_mots[randint(0, len(liste_mots) - 1)]
}

# CREATION DE LA FENETRE
fenetre = Tk()
fenetre.title("Wordle NSI")
fenetre.config(background=FOND)
fenetre.state("zoomed")
fenetre.iconbitmap('icone.ico')

# PAGES (frames)

# Page accueil
cadre_accueil = Frame(fenetre, bg=FOND)
cadre_accueil.pack(pady=80, expand=True)

label_titre      = Label(cadre_accueil, text="WORDLE",     font=("Arial", 48, "bold"), bg=FOND, fg=TEXTE)
label_sous_titre = Label(cadre_accueil, text="NSI Edition", font=("Arial", 14),        bg=FOND, fg=GRIS)
bouton_connexion  = Button(cadre_accueil, text="Se connecter", bg=BOUTON, fg=BOUTON_TEXT, font=("Arial", 13, "bold"), width=20, pady=10, relief="flat", cursor="hand2")
bouton_inscription = Button(cadre_accueil, text="S'inscrire",  bg=FOND,   fg=TEXTE,       font=("Arial", 13),         width=20, pady=10, relief="flat", cursor="hand2", highlightthickness=1, highlightbackground=BORDURE)
bouton_classement  = Button(cadre_accueil, text="Classement",  bg=FOND,   fg=TEXTE,       font=("Arial", 13),         width=20, pady=10, relief="flat", cursor="hand2", highlightthickness=1, highlightbackground=BORDURE)

label_titre.pack(pady=10)
label_sous_titre.pack()
bouton_connexion.pack(pady=8)
bouton_inscription.pack(pady=8)
bouton_classement.pack(pady=8)

# Page connexion
cadre_connexion = Frame(fenetre, bg=FOND)

label_titre_connexion   = Label(cadre_connexion, text="Connexion",    font=("Arial", 24, "bold"), bg=FOND, fg=TEXTE)
label_tour              = Label(cadre_connexion, text="",             font=("Arial", 13, "bold"), bg=FOND, fg=BOUTON)
label_pseudo            = Label(cadre_connexion, text="Pseudo",       font=("Arial", 11),         bg=FOND, fg=TEXTE)
entree_pseudo           = Entry(cadre_connexion, font=("Arial", 13),  width=24, relief="solid", bd=1)
label_mdp               = Label(cadre_connexion, text="Mot de passe", font=("Arial", 11),         bg=FOND, fg=TEXTE)
entree_mdp              = Entry(cadre_connexion, font=("Arial", 13),  width=24, relief="solid", bd=1, show="*")
bouton_valider_connexion = Button(cadre_connexion, text="Valider",    bg=BOUTON, fg=BOUTON_TEXT, font=("Arial", 12, "bold"), width=20, pady=8, relief="flat", cursor="hand2")
label_message_connexion  = Label(cadre_connexion, text="",            font=("Arial", 10), bg=FOND, fg="red")
bouton_retour_connexion  = Button(cadre_connexion, text="← Retour",   bg=FOND, fg=GRIS,  font=("Arial", 10), relief="flat", cursor="hand2")

label_titre_connexion.pack(pady=20)
label_tour.pack(pady=6)
label_pseudo.pack()
entree_pseudo.pack(pady=6)
label_mdp.pack()
entree_mdp.pack(pady=6)
bouton_valider_connexion.pack(pady=10)
label_message_connexion.pack()
bouton_retour_connexion.pack(pady=10)

# Page inscription
cadre_inscription = Frame(fenetre, bg=FOND)

equipe_var = IntVar()

label_titre_inscription   = Label(cadre_inscription, text="Inscription",    font=("Arial", 24, "bold"), bg=FOND, fg=TEXTE)
label_pseudo_inscription  = Label(cadre_inscription, text="Pseudo",         font=("Arial", 11),         bg=FOND, fg=TEXTE)
entree_pseudo_inscription = Entry(cadre_inscription, font=("Arial", 13),    width=24, relief="solid", bd=1)
label_mdp_inscription     = Label(cadre_inscription, text="Mot de passe",   font=("Arial", 11),         bg=FOND, fg=TEXTE)
entree_mdp_inscription    = Entry(cadre_inscription, font=("Arial", 13),    width=24, relief="solid", bd=1, show="*")
label_equipe              = Label(cadre_inscription, text="Choisis ton équipe :", font=("Arial", 11),   bg=FOND, fg=TEXTE)
radio_rouge               = Radiobutton(cadre_inscription, text="Rouge", variable=equipe_var, value=1,  bg=FOND, font=("Arial", 11), cursor="hand2")
radio_bleu                = Radiobutton(cadre_inscription, text="Bleu",  variable=equipe_var, value=2,  bg=FOND, font=("Arial", 11), cursor="hand2")
bouton_valider_inscription = Button(cadre_inscription, text="S'inscrire",   bg=BOUTON, fg=BOUTON_TEXT, font=("Arial", 12, "bold"), width=20, pady=8, relief="flat", cursor="hand2")
label_message_inscription  = Label(cadre_inscription, text="",             font=("Arial", 10), bg=FOND, fg="red")
bouton_retour_inscription  = Button(cadre_inscription, text="← Retour",    bg=FOND, fg=GRIS,  font=("Arial", 10), relief="flat", cursor="hand2")

label_titre_inscription.pack(pady=20)
label_pseudo_inscription.pack()
entree_pseudo_inscription.pack(pady=6)
label_mdp_inscription.pack()
entree_mdp_inscription.pack(pady=6)
label_equipe.pack(pady=6)
radio_rouge.pack()
radio_bleu.pack()
bouton_valider_inscription.pack(pady=10)
label_message_inscription.pack()
bouton_retour_inscription.pack(pady=10)

# Page jeu
cadre_jeu     = Frame(fenetre, bg=FOND)
cadre_grille  = Frame(cadre_jeu,  bg=FOND)

label_info    = Label(cadre_jeu, text="Devine le mot de 6 lettres", font=("Arial", 13), bg=FOND, fg=TEXTE)
entree_mot    = Entry(cadre_jeu, font=("Arial", 16), width=14, relief="solid", bd=1, justify="center")
bouton_jouer  = Button(cadre_jeu, text="Proposer", bg=BOUTON, fg=BOUTON_TEXT, font=("Arial", 12, "bold"), width=16, pady=8, relief="flat", cursor="hand2")

label_info.pack(pady=10)
cadre_grille.pack()

for l in range(6):
    for col in range(6):
        case_vide = Label(cadre_grille, width=4, height=2, bg=CASE_VIDE, font=("Arial", 22, "bold"), relief="solid", bd=1)
        case_vide.grid(row=l, column=col, padx=4, pady=4)

entree_mot.pack(pady=14)
bouton_jouer.pack()

# Page classement
cadre_classement = Frame(fenetre, bg=FOND)
cadre_tableau    = Frame(cadre_classement, bg=FOND)

label_titre_classement  = Label(cadre_classement, text="Classement", font=("Arial", 24, "bold"), bg=FOND, fg=TEXTE)
bouton_retour_classement = Button(cadre_classement, text="← Retour", bg=FOND, fg=GRIS, font=("Arial", 10), relief="flat", cursor="hand2")

label_titre_classement.pack(pady=20)
cadre_tableau.pack()
bouton_retour_classement.pack(pady=20)

# navigation entre les pages
def afficher_accueil():
    cadre_connexion.pack_forget()
    cadre_inscription.pack_forget()
    cadre_classement.pack_forget()
    cadre_jeu.pack_forget()
    cadre_accueil.pack(pady=40, expand=True)

def afficher_connexion():
    cadre_accueil.pack_forget()
    couleur = "Rouge" if etat["tour_equipe"] == 1 else "Bleu"
    label_tour.config(text=f"Tour de l'équipe {couleur} !")
    cadre_connexion.pack(pady=40)

def afficher_inscription():
    cadre_accueil.pack_forget()
    cadre_inscription.pack(pady=40)

def afficher_jeu():
    cadre_connexion.pack_forget()
    cadre_jeu.pack(pady=20)

def afficher_classement():
    cadre_accueil.pack_forget()
    rafraichir_classement()
    cadre_classement.pack(pady=40)

# VALIDATION DES FORMULAIRES
def valider_inscription():
    pseudo = entree_pseudo_inscription.get()
    mdp    = entree_mdp_inscription.get()
    equipe = equipe_var.get()

    if pseudo == "" or mdp == "":
        label_message_inscription.config(text="Remplis tous les champs !")
        return
    if equipe == 0:
        label_message_inscription.config(text="Choisis une équipe !")
        return

    curseur.execute("SELECT pseudo FROM joueurs WHERE pseudo = ?", (pseudo,))
    if curseur.fetchone() is not None:
        label_message_inscription.config(text="Pseudo déjà utilisé !")
        return

    curseur.execute(
        "INSERT INTO joueurs (pseudo, mot_de_passe, id_equipe) VALUES (?, ?, ?)",
        (pseudo, mdp, equipe)
    )
    db.commit()
    label_message_inscription.config(text="Compte créé ! Tu peux te connecter.", fg="green")

def valider_connexion():
    pseudo = entree_pseudo.get()
    mdp    = entree_mdp.get()

    if pseudo == "" or mdp == "":
        label_message_connexion.config(text="Remplis tous les champs !")
        return

    curseur.execute(
        "SELECT id_joueur, id_equipe FROM joueurs WHERE pseudo = ? AND mot_de_passe = ?",
        (pseudo, mdp)
    )
    joueur = curseur.fetchone()

    if joueur is None:
        label_message_connexion.config(text="Pseudo ou mot de passe incorrect !")
        return
    if joueur[1] != etat["tour_equipe"]:
        couleur = "Rouge" if etat["tour_equipe"] == 1 else "Bleu"
        label_message_connexion.config(text=f"C'est le tour de l'équipe {couleur} !")
        return

    etat["id_joueur"] = joueur[0]
    afficher_jeu()

def jouer():
    proposition = entree_mot.get().lower()

    if len(proposition) != 6:
        label_info.config(text="Le mot doit faire 6 lettres !")
        return

    for i in range(6):
        if proposition[i] == etat["mot_secret"][i]:
            couleur = VERT
        elif proposition[i] in etat["mot_secret"]:
            couleur = ORANGE
        else:
            couleur = GRIS

        case = Label(cadre_grille,
            text=proposition[i].upper(),
            width=4, height=2,
            bg=couleur, fg=BOUTON_TEXT,
            font=("Arial", 22, "bold"),
            relief="flat"
        )
        case.grid(row=etat["ligne"], column=i, padx=4, pady=4)

    etat["ligne"] += 1
    entree_mot.delete(0, END)

    if proposition == etat["mot_secret"]:
        label_info.config(text="Bravo, tu as trouvé !", fg=VERT)
        bouton_jouer.config(state="disabled")
        curseur.execute(
            "INSERT INTO parties (id_joueur, mot, coups_necessaires, resultat) VALUES (?, ?, ?, ?)",
            (etat["id_joueur"], etat["mot_secret"], etat["ligne"], "victoire")
        )
        curseur.execute(
            "UPDATE joueurs SET score = score + 1 WHERE id_joueur = ?",
            (etat["id_joueur"],)
        )
        db.commit()
        fenetre.after(3000, changer_tour)
        return

    if etat["ligne"] == 6:
        label_info.config(text="Perdu ! Le mot était : " + etat["mot_secret"].upper(), fg=GRIS)
        bouton_jouer.config(state="disabled")
        curseur.execute(
            "INSERT INTO parties (id_joueur, mot, coups_necessaires, resultat) VALUES (?, ?, ?, ?)",
            (etat["id_joueur"], etat["mot_secret"], etat["ligne"], "defaite")
        )
        db.commit()
        fenetre.after(3000, changer_tour)

def changer_tour():
    etat["tour_equipe"] = 2 if etat["tour_equipe"] == 1 else 1
    etat["mot_secret"]  = liste_mots[randint(0, len(liste_mots) - 1)]
    etat["ligne"]       = 0
    etat["id_joueur"]   = None

    for widget in cadre_grille.winfo_children():
        widget.destroy()
    for l in range(6):
        for col in range(6):
            case_vide = Label(cadre_grille, width=4, height=2, bg=CASE_VIDE, font=("Arial", 22, "bold"), relief="solid", bd=1)
            case_vide.grid(row=l, column=col, padx=4, pady=4)

    bouton_jouer.config(state="normal")
    label_info.config(text="Devine le mot de 6 lettres", fg=TEXTE)
    entree_mot.delete(0, END)
    afficher_accueil()

def rafraichir_classement():
    for widget in cadre_tableau.winfo_children():
        widget.destroy()

    curseur.execute("""
        SELECT e.couleur, SUM(j.score)
        FROM joueurs j
        JOIN equipes e ON j.id_equipe = e.id_equipe
        GROUP BY e.id_equipe
        ORDER BY SUM(j.score) DESC
    """)
    equipes_resultats = curseur.fetchall()

    ligne_affichage = 0
    for couleur, score_equipe in equipes_resultats:
        Label(cadre_tableau, text=f"Equipe {couleur} — {score_equipe} pts", font=("Arial", 13, "bold"), bg=FOND).grid(row=ligne_affichage, column=0, columnspan=2, pady=8, sticky="w")
        ligne_affichage += 1

        Label(cadre_tableau, text="Pseudo",    font=("Arial", 11, "italic"), bg=FOND, width=15).grid(row=ligne_affichage, column=0, padx=20)
        Label(cadre_tableau, text="Victoires", font=("Arial", 11, "italic"), bg=FOND, width=10).grid(row=ligne_affichage, column=1)
        ligne_affichage += 1

        curseur.execute("""
            SELECT j.pseudo, j.score
            FROM joueurs j
            JOIN equipes e ON j.id_equipe = e.id_equipe
            WHERE e.couleur = ?
            ORDER BY j.score DESC
        """, (couleur,))

        for pseudo, score in curseur.fetchall():
            Label(cadre_tableau, text=pseudo, font=("Arial", 11), bg=FOND).grid(row=ligne_affichage, column=0, padx=20)
            Label(cadre_tableau, text=score,  font=("Arial", 11), bg=FOND).grid(row=ligne_affichage, column=1)
            ligne_affichage += 1

# ASSIGNATION DES FONCTIONS AUX BOUTONS
bouton_connexion.config(command=afficher_connexion)
bouton_inscription.config(command=afficher_inscription)
bouton_classement.config(command=afficher_classement)
bouton_valider_connexion.config(command=valider_connexion)
bouton_retour_connexion.config(command=afficher_accueil)
bouton_valider_inscription.config(command=valider_inscription)
bouton_retour_inscription.config(command=afficher_accueil)
bouton_jouer.config(command=jouer)
bouton_retour_classement.config(command=afficher_accueil)

# LANCEMENT DE LA FENETRE
fenetre.mainloop()
