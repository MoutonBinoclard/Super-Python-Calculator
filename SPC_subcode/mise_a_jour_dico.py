def maj_dictionnaire(dictionnaire, manche): # Met à jour le dictionnaire des ID avec une manche
    # dictionnaire -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # manche -> list : [['ID1', placement, kill, nombre de joueur, masterkill ?],...]
    
    # Créer un ensemble des PlayfabID présents dans la manche
    id_dans_manche = set([joueur[0] for joueur in manche])

    # Parcourir tous les PlayfabID du dictionnaire
    for playfab_id in dictionnaire:
        # Vérifier si le PlayfabID est présent dans la manche
        if playfab_id in id_dans_manche:
            # Trouver les données du joueur dans la manche
            for joueur in manche:
                if joueur[0] == playfab_id:
                    placement = joueur[1]
                    kills = joueur[2]
                    total_joueurs = joueur[3]
                    masterkill_ou_non = joueur[4] # Ajout de la quatrième valeur
                    team = joueur[5]
                    team_kill = joueur[6]
                    masterkill_team = joueur[7]
                    # Ajouter les données à la liste du joueur
                    dictionnaire[playfab_id][3].append([0,[placement, kills, total_joueurs, masterkill_ou_non, team, team_kill, masterkill_team]]) # Zero pour l'ajout du score de la manche a priori
                    break
        else:
            # Si le joueur n'est pas dans la manche, ajouter [0, 0, 0, False, -1, 0]
            dictionnaire[playfab_id][3].append([0,[0, 0, 0, False, -1, 0, False]])  # Ajout de valeurs par défaut pour team et team_kill
    
    return dictionnaire # dict -> {'ID1' :[[placement, kills, nombre joueurs, masterkill ?, team, team kill],[,,,],...], ...}
