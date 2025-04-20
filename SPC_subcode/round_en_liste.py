def fichier_round_en_liste(fichier_du_round_1, banni): # Prend un fichier de round et le transforme en liste

    # Liste pour stocker les données du round
    liste_du_round = []
    
    # Nombre total de joueurs dans ce round
    total_joueurs = nombre_de_joueur_dans_un_round(fichier_du_round_1)
    # Maximum de kill dans la manche
    maximum=maximum_de_kill_dans_un_round(fichier_du_round_1)
    
    # Ouvrir le fichier et lire les lignes
    with open(fichier_du_round_1, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Parcourir chaque ligne du fichier (en ignorant l'en-tête)
    for line in lines[1:]:
        columns = line.strip().split('\t')

        # Extraire les données nécessaires
        playfab_id = columns[-5]
        placement = int(columns[-1])
        kills = int(columns[-2])
        mk=False
        if kills==maximum : mk=True
        team = int(columns[-4])
        

        # Ajouter les données du joueur à la liste du round
        liste_du_round.append([playfab_id, placement, kills, total_joueurs, mk, team])

    # Création de la nouvelle colonne avec les kills communs pour une team
    liste_du_round=sync_kill_equipe(liste_du_round, calcul_kill_par_equipe(liste_du_round))

    # On enleve les bannis
    liste_du_round=enlever_joueurs_liste_du_round(liste_du_round, banni)

    # Correction des positions des joueurs (mode team surtout)
    liste_du_round=MAJ_placement_en_teams(liste_du_round)

    # Ajout masterkill team
    liste_du_round=masterkill_team(liste_du_round)

    return liste_du_round

# ----------------------------------------------------------------------------

def nombre_de_joueur_dans_un_round(fichier_du_round_2): # Trouve le nombre de joueurs dans un fichier round

    with open(fichier_du_round_2, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # On ignore la première ligne (en-tête)
    joueurs = lines[1:]
    
    # On compte les joueurs dont le placement n'est pas -1
    nombre_joueurs = 0
    for joueur in joueurs:
        data = joueur.strip().split('\t')
        placement = int(data[-1])  # La dernière colonne est le placement
        if placement != -1:
            nombre_joueurs += 1
    
    return nombre_joueurs

# ----------------------------------------------------------------------------

def maximum_de_kill_dans_un_round(fichier_du_round_3): # Trouve le plus de kill fait par un joueur dans un round
    # fichier_du_round_3 -> str : 'fichier1.txt'

    with open(fichier_du_round_3, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # On ignore la première ligne (en-tête)
    joueurs = lines[1:]
    
    # On initialise la variable pour stocker le nombre maximum de kills
    max_kills = 0
    
    # On parcourt chaque joueur pour trouver le nombre maximum de kills
    for joueur in joueurs:
        data = joueur.strip().split('\t')
        kills = int(data[-2])  # L'avant-dernière colonne est le nombre de kills
        if kills > max_kills:
            max_kills = kills
    
    return max_kills

# ----------------------------------------------------------------------------

def sync_kill_equipe(liste_contenant_un_round_2, liste_de_kill_par_equipe): # Met les kills de l'equipe pour chaque joueurs
    nouvelle_liste = []
    
    for joueur in liste_contenant_un_round_2:
        team = joueur[5]  # Récupération de l'équipe
        if team==-1 or team==0: # Si team chelou, nombre de kill
            joueur.append(joueur[2])
        elif team in liste_de_kill_par_equipe:  # Vérifie que l'équipe est bien dans le dictionnaire
            joueur.append(liste_de_kill_par_equipe[team])  # Nouvelle colonne avec nombre de kill par l'équipe
        nouvelle_liste.append(joueur)  # Ajoute le joueur modifié à la nouvelle liste
    
    return nouvelle_liste

# ----------------------------------------------------------------------------

def enlever_joueurs_liste_du_round(liste_round_sans_analyse, liste_des_joueurs_a_enlever): # Enlève les joueurs banni et ajuste les positions des joueurs restants
    # liste_round_sans_analyse -> list : [['ID1', placement, kill, nombre de joueur, masterkill ?],...]
    # liste_des_joueurs_a_enlever -> list : ["ID_a_ban_1",...]

    # Liste pour stocker les positions des joueurs enlevés
    positions_enlevees = []

    # Parcourir la liste des joueurs à enlever
    for id_a_enlever in liste_des_joueurs_a_enlever:
        # Parcourir la liste des joueurs pour trouver et supprimer le joueur correspondant
        for joueur in liste_round_sans_analyse:
            if joueur[0] == id_a_enlever:  # L'ID est à l'index 0
                # Noter la position du joueur avant de le supprimer
                positions_enlevees.append(joueur[1])  # Le placement est à l'index 1
                # Supprimer le joueur de la liste
                liste_round_sans_analyse.remove(joueur)
                break  # Sortir de la boucle après avoir trouvé et supprimé le joueur

    # Ajuster les placements des autres joueurs en utilisant la fonction ajuster_les_positions_des_joueurs
    for position_trouvee in positions_enlevees:
        liste_round_sans_analyse = ajuster_les_positions_des_joueurs(liste_round_sans_analyse, position_trouvee)

    return liste_round_sans_analyse # list -> [['ID1', placement, kill, nombre de joueur, masterkill ?, team, kill team],...]

# ----------------------------------------------------------------------------

def ajuster_les_positions_des_joueurs(liste_apres_enlevement_du_joueur, position_de_ce_dernier): # Ajuste toute les postitions après un ban
    # liste_apres_enlevement_du_joueur -> list : [['ID1', placement, kill, nombre de joueur, masterkill ?, team, kill team],...]
    # position_de_ce_dernier -> int : position

    # Si la personne est spectatrice, on ne fait rien au nombre de joueurs
    if position_de_ce_dernier<=0:
        return liste_apres_enlevement_du_joueur
        
    # Parcourir chaque joueur dans la liste
    for joueur in liste_apres_enlevement_du_joueur:
        # Diminuer le total de joueurs de 1 pour chaque sous-liste
        joueur[3] -= 1  # Le total de joueurs est à l'index 3

        # Si le placement est strictement supérieur à la valeur donnée, diminuer le placement de 1
        if joueur[1] > position_de_ce_dernier:  # Le placement est à l'index 1
            joueur[1] -= 1

    return liste_apres_enlevement_du_joueur # list -> [['ID1', placement, kill, nombre de joueur, masterkill ?, team, kill team],...]

# ----------------------------------------------------------------------------

def calcul_kill_par_equipe(liste_contenant_un_round_1): # Calcul combien de kill pour chaque équipe puis les mets dans un dico
    # liste_contenant_un_round_1 -> list : [['ID1', placement, kill, nombre de joueur, masterkill ?, team], ...]
    dico = {}
    
    for info_dun_joueur in liste_contenant_un_round_1:
        la_team = info_dun_joueur[5]  # Récupération de l'équipe
        nb_kill = info_dun_joueur[2]  # Récupération du nombre de kills
        
        # Vérifier si l'équipe est déjà dans le dictionnaire
        if la_team in dico:
            dico[la_team] += nb_kill
        else:
            dico[la_team] = nb_kill
    
    return dico 

# ----------------------------------------------------------------------------

def MAJ_placement_en_teams(liste_contenant_un_round_3): # Ajuste les placements pour refléter les équipes

    # Retourne la liste avec les placements ajustés.
    # Ajuste les placements pour refléter les équipes :
    # - Tous les membres d'une même équipe obtiennent le même placement.
    # - Les placements sont réattribués consécutivement (1, 2, 3...) sans trous.
    # - Les joueurs ayant un placement -1 ou 0 sont ignorés.
    # liste_contenant_un_round : list -> [['ID', placement, kills, total_joueurs, masterkill, team, kill team], ...]
    
    # Dictionnaire pour stocker les joueurs par équipe
    equipes = {}

    # Grouper les joueurs par équipe (ignorer les teams 0 et -1)
    for joueur in liste_contenant_un_round_3:
        playfab_id, placement, kills, total_joueurs, mk, team, kill_team = joueur
        if team > 0 and placement > 0:  # On ignore les spectateurs et teams invalides
            if team not in equipes:
                equipes[team] = []
            equipes[team].append(joueur)

    # Trier les équipes selon leur meilleur placement (plus petit nombre = meilleur placement)
    equipes_triees = sorted(equipes.values(), key=lambda equipe: min(j[1] for j in equipe))

    # Réattribution des placements consécutifs
    nouveau_placement = 1
    for equipe in equipes_triees:
        for joueur in equipe:
            joueur[1] = nouveau_placement  # Donner le même placement à toute l'équipe
        nouveau_placement += 1  # Passer au placement suivant

    return liste_contenant_un_round_3

# ----------------------------------------------------------------------------

def masterkill_team(liste_contenant_un_round_4):
    # Calcule le nombre de masterkill (kill max) par équipe
    # On considère qu'un masterkill est quand le kill team est égal au max des kill team de toutes les équipes

    # Récupérer le kill team max parmi toutes les équipes (ignorer teams 0 et -1)
    kill_team_max = 0
    for joueur in liste_contenant_un_round_4:
        kill_team = joueur[6]
        if kill_team > kill_team_max:
            kill_team_max = kill_team


    for index in range(len(liste_contenant_un_round_4)):


        kill_team = liste_contenant_un_round_4[index][6]
        if kill_team == kill_team_max:
            liste_contenant_un_round_4[index].append(True)
        else:
            liste_contenant_un_round_4[index].append(False)

    return liste_contenant_un_round_4
