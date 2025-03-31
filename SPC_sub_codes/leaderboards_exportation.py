import os

from SPC_sub_codes.more_stats import nombre_de_parties_jouees, nombre_d_eliminations, calculer_kda, nombre_de_victoires

# ----------------------------------------------------------------------------

def exporter_top(classement_du_tournoi, filename, combien): # Fonction pour exporter les x premiers joueurs dans un fichier texte
    # classement_du_tournoi -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # filename -> str : 'letop.txt'
    # combien -> int : valeur

    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Parcourir les x premiers joueurs du classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            if i >= combien:  # On s'arrête après les cinq premiers
                break
            pseudo, score_final, _ = data
            # Écrire les informations du joueur dans le fichier
            file.write(f"{i + 1}. {score_final:.2f} -> {pseudo}\n")

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

def exporter_classement_partiel(classement_du_tournoi, filename): # Exporte un classement simple avec saut de ligne pour chaque joueur
    # classement_du_tournoi -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # filename -> str : 'classementpartiel.txt'

    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Parcourir tous les joueurs du classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            pseudo, score_final, scores_manches = data
            # Écrire les informations du joueur dans le fichier
            file.write(f"{i + 1}. {score_final:.2f} -> {pseudo}\n")

# ----------------------------------------------------------------------------

def exporter_classement_en_ligne(classement_du_tournoi, filename): # Exporte un classement simple en une ligne
    # classement_du_tournoi -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # filename -> str : 'classementligne.txt'

    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Créer une liste pour stocker les éléments du classement
        classement_en_ligne = []
        
        # Parcourir tous les joueurs du classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            pseudo, score_final, _ = data
            # Ajouter chaque joueur au format "X. joueur - XXpt /"
            classement_en_ligne.append(f"{i + 1}. {pseudo} - {score_final:.2f}pt")
        
        # Joindre tous les éléments avec " / " et ajouter un "/ " à la fin
        ligne_finale = " / ".join(classement_en_ligne) + " / "
        
        # Écrire la ligne finale dans le fichier
        file.write(ligne_finale)

# ----------------------------------------------------------------------------

def exporter_classement_complet(classement_du_tournoi, dict_ID, filename): # Exporte un classement detaillé dans un fichier
    # classement_du_tournoi -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # dict_ID -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # filename -> str : 'classementcomplet.txt'

    """
    Exporte le classement complet dans un fichier texte avec des informations détaillées pour chaque joueur :
    - Position
    - Nom du joueur
    - Points totaux
    - Nombre de victoires
    - Nombre de kills
    - Nombre de parties jouées
    - KDA
    - Points par round
    """
    
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Écrire l'en-tête du fichier
        file.write("Position\tNom du joueur\tPoints\tVictoires\tKills\tParties jouées\tKDA\tPoints par round\n")

        # Parcourir chaque joueur dans le classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            pseudo, score_final, scores_manches = data

            # Calculer les statistiques supplémentaires
            nb_victoires = nombre_de_victoires(dict_ID, playfab_id)
            nb_kills = nombre_d_eliminations(dict_ID, playfab_id)
            nb_parties = nombre_de_parties_jouees(dict_ID, playfab_id)
            kda = calculer_kda(dict_ID, playfab_id)

            # Écrire les informations du joueur dans le fichier
            file.write(f"{i + 1}\t{pseudo}\t{score_final:.2f}\t{nb_victoires}\t{nb_kills}\t{nb_parties}\t{kda:.2f}\t")

            # Écrire les points par round
            points_par_round = "\t".join(map(lambda x: f"{x:.2f}", scores_manches))
            file.write(f"{points_par_round}\n")
