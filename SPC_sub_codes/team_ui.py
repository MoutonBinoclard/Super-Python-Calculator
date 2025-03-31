import tkinter as tk
from tkinter import Listbox, MULTIPLE, messagebox

# ----------------------------------------------------------------------------

def sauvegarder_equipes(equipes, fichier="SPC___teams.txt"): # Sauvergarde du fichier des équipes
    """Sauvegarde les équipes dans un fichier texte."""
    with open(fichier, "w", encoding="utf-8") as f:
        for equipe in equipes:
            f.write(" ".join(equipe) + "\n")

# ----------------------------------------------------------------------------

def interface_creation_equipe(liste_joueurs):

    # Variable pour stocker les équipes à retourner
    teams = []
    team_names_display = []  # Pour l'affichage des noms dans l'interface

    # Fonction pour créer une équipe
    def create_team():
        selected_indices = player_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aucun joueur sélectionné", "Veuillez sélectionner au moins un joueur.")
            return
        team_ids = []  # Pour stocker les ID des joueurs de l'équipe
        team_names = []  # Pour stocker les noms des joueurs de l'équipe
        for index in selected_indices[::-1]:  # Parcourir en sens inverse pour éviter les problèmes d'indexation
            player_id, player_name = liste_joueurs[index]
            team_ids.append(player_id)
            team_names.append(player_name)
            liste_joueurs.pop(index)
        teams.append(team_ids)  # On stocke les ID dans la liste des équipes
        team_names_display.append(team_names)  # On stocke les noms pour l'affichage
        update_listboxes()

    # Fonction pour dissoudre une équipe
    def dissolve_team():
        selected_indices = team_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Aucune équipe sélectionnée", "Veuillez sélectionner une équipe à dissoudre.")
            return
        for index in selected_indices[::-1]:  # Parcourir en sens inverse pour éviter les problèmes d'indexation
            team_ids = teams.pop(index)  # Récupérer les ID de l'équipe dissoute
            team_names = team_names_display.pop(index)  # Récupérer les noms de l'équipe dissoute
            # Réintégrer les joueurs dans la liste des joueurs disponibles
            for player_id, player_name in zip(team_ids, team_names):
                liste_joueurs.append([player_id, player_name])
        update_listboxes()

    # Fonction pour terminer et fermer la fenêtre
    def finish():
        root.quit()  # Ferme la boucle principale
        root.destroy()  # Détruit la fenêtre

    # Fonction pour mettre à jour les Listbox
    def update_listboxes():
        # Mettre à jour la liste des joueurs disponibles
        player_listbox.delete(0, tk.END)
        for player in liste_joueurs:
            player_listbox.insert(tk.END, player[1])

        # Mettre à jour la liste des équipes (en affichant les noms)
        team_listbox.delete(0, tk.END)
        for team_names in team_names_display:
            team_listbox.insert(tk.END, ', '.join(team_names))

    # Initialisation de la fenêtre Tkinter
    root = tk.Tk()
    root.title("Super Team Creator - From SPC")
    root.configure(bg='#191919')  # Fond sombre

    # Style des boutons
    button_style = {
        'bg': '#191919',  # Couleur de fond des boutons
        'fg': '#ecf0f1',  # Couleur du texte des boutons
        'font': ('Helvetica', 14),  # Police plus grande
        'relief': tk.RAISED,  # Bordure en relief
        'borderwidth': 2  # Épaisseur de la bordure
    }

    # Frame pour les Listbox et les Scrollbars
    listbox_frame = tk.Frame(root, bg='#191919')
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Listbox pour afficher les joueurs disponibles
    player_listbox = Listbox(
        listbox_frame,
        selectmode=MULTIPLE,
        bg='#191919',
        fg='#ecf0f1',
        font=('Helvetica', 14),
        width=30,
        height=15,
        selectbackground='#777777',  # Couleur de fond de la sélection (gris clair)
        selectforeground='#ecf0f1',  # Couleur du texte de la sélection (blanc)
        activestyle='none'  # Désactive le soulignement des éléments sélectionnés
    )
    player_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar pour la Listbox des joueurs
    player_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=player_listbox.yview)
    player_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    player_listbox.config(yscrollcommand=player_scrollbar.set)

    # Listbox pour afficher les équipes créées (noms des joueurs)
    team_listbox = Listbox(
        listbox_frame,
        selectmode=tk.SINGLE,
        bg='#191919',
        fg='#ecf0f1',
        font=('Helvetica', 14),
        width=30,
        height=15,
        selectbackground='#777777',  # Couleur de fond de la sélection (gris clair)
        selectforeground='#ecf0f1',  # Couleur du texte de la sélection (blanc)
        activestyle='none'  # Désactive le soulignement des éléments sélectionnés
    )
    team_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Scrollbar pour la Listbox des équipes
    team_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=team_listbox.yview)
    team_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    team_listbox.config(yscrollcommand=team_scrollbar.set)

    # Frame pour les boutons (disposés verticalement)
    button_frame = tk.Frame(root, bg='#191919')
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    # Boutons disposés verticalement
    create_team_button = tk.Button(button_frame, text="Create a team", command=create_team, **button_style)
    create_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)  # Bouton en haut, remplissage horizontal

    dissolve_team_button = tk.Button(button_frame, text="Dissolve a team", command=dissolve_team, **button_style)
    dissolve_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)  # Bouton en dessous, remplissage horizontal

    finish_button = tk.Button(button_frame, text="Finished !", command=finish, **button_style)
    finish_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)  # Bouton en bas, remplissage horizontal

    # Initialisation des Listbox
    update_listboxes()

    # Lancement de la boucle principale
    root.mainloop()

    # Sauvegarder puis retourner la liste des équipes après la fermeture de la fenêtre
    sauvegarder_equipes(teams)
    return teams