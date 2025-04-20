import os

# ----------------------------------------------------------------------------

def exporter_un_joueur(classement_du_tournoi, filename, position): # Fonction pour exporter le joueur correspondant au classement donnée dans un fichier texte
    # classement_du_tournoi -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # filename -> str : 'classementjoueur.txt'
    # position -> int : valeur

    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Vérifier si la position demandée est valide
        if position > len(classement_du_tournoi):
            file.write("None")
            return
        
        # Récupérer le joueur à la position demandée
        joueur = list(classement_du_tournoi.items())[position - 1]
        playfab_id, data = joueur
        pseudo, score_final, _ = data
        
        # Écrire les informations du joueur dans le fichier avec le format "Joueur : Score / "
        file.write(f"{pseudo}  ")
        # file.write(f"{pseudo} : {score_final:.2f} / ")

# ----------------------------------------------------------------------------

def exporter_classement_partiel(leaderboard, filename):  # Exporte un classement simple avec saut de ligne pour chaque joueur
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Parcourir tous les joueurs du classement
        for i, (playfab_id, data) in enumerate(leaderboard.items()):
            pseudo = data[0]
            score_final = data[1]
            file.write(f"{i + 1}. {pseudo} - {score_final:.2f}pt\n")

# ----------------------------------------------------------------------------

def exporter_classement_en_ligne(leaderboard, filename):  # Exporte un classement simple en une ligne (nouvelle structure)
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        classement_en_ligne = []
        # Parcourir tous les joueurs du classement
        for i, (playfab_combine, data) in enumerate(leaderboard.items()):
            # data[3] est la liste des joueurs (pour les équipes/combine)
            pseudo = data[0]  # Prendre le pseudo du premier joueur de la liste
            score_final = data[1]  # Prendre le score final du joueur
            classement_en_ligne.append(f"{i + 1}. {pseudo} - {score_final:.2f}pt")
        # Joindre tous les éléments avec " / " et ajouter un "/ " à la fin
        ligne_finale = " / ".join(classement_en_ligne) + " / "
        file.write(ligne_finale)

# ----------------------------------------------------------------------------

def exporter_classement_complet(leaderboard, filename): # Exporte un classement detaillé dans un fichier
    # Trouver le nombre de rounds (manches) en regardant le premier joueur du leaderboard
    first_player_data = next(iter(leaderboard.values()))
    first_joueur = first_player_data[3][0]
    manches = first_joueur[3]
    nombre_de_rounds = len(manches)
    
    
    

    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Écrire l'en-tête du fichier
        # Générer dynamiquement l'en-tête pour chaque round
        entete = "Position\tNom du joueur\tScore Final\tVictoires\tNb Parties\tKills\tKDA\tScore Réel\t"
        for round_num in range(1, nombre_de_rounds + 1):
            entete += f"Pts/Pos/Kill R{round_num}\t"
        entete = entete.rstrip('\t') + "\n"
        file.write(entete)

        # Parcourir chaque joueur dans le classement
        for i, (playfab_combine, data) in enumerate(leaderboard.items()):
            
            for j in data[3]:
                pseudo = j[0]
                score_final = data[1]
                stats = j[2]
                manches = j[3]
                score_reel=j[1]

                nb_parties, nb_victoires, nb_kills, kda = stats

                #print(pseudo, score_final, nb_victoires, nb_parties, nb_kills, kda)

                # Écrire les informations du joueur dans le fichier
                file.write(f"{i + 1}\t{pseudo}\t{score_final:.2f}\t{nb_victoires}\t{nb_parties}\t{nb_kills}\t{kda:.2f}\t{score_reel:.2f}\t")

                # Récupérer les scores de chaque manche (nouvelle structure)
                scores_manches = [manche[0] for manche in manches]
                placements_manches = [manche[1][0] for manche in manches]
                kill_manches = [manche[1][1] for manche in manches]
                # Écrire les points, placements et kills par round
                round_details = []
                for score, placement, kill in zip(scores_manches, placements_manches, kill_manches):
                    round_details.append(f"{score:.2f} / {placement} / {kill}")
                file.write("\t".join(round_details) + "\n")


# {'ID_combine':[Nom des joueurs, score final, [[score manche 1, placement manche 1], ...], [[classement[ID1]], [classement [ID2]], ...]
# Forme du classement :
# {'ID1':[Nom du joueur, score final, [nb_partie_joué, nb_victoire, nb_kill, kda], [[score manche1, [placement, kill, nb_joueur, masterkill, team, team_kill]], [score manche2, ...}
