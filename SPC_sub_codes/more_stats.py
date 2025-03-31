def nombre_de_parties_jouees(dictionnaire_ID, playfab_id): # Trouve combien de partie à un joué un joueur donné
    # dictionnaire_ID -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # playfab_id -> str : 'ID1'
    
    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a joué aucune partie

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Compter le nombre de parties où le placement est strictement positif
    nb_parties = sum(1 for manche in manches if manche[0] > 0)

    return nb_parties

# ----------------------------------------------------------------------------

def nombre_d_eliminations(dictionnaire_ID, playfab_id): # Trouve le nombre de kill d'un joueur sur toutes les games jouées par ce dernier
    # dictionnaire_ID -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # playfab_id -> str : 'ID1'

    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a fait aucun kill

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Calculer le nombre total de kills
    total_kills = sum(manche[1] for manche in manches if manche[0] > 0)

    return total_kills

# ----------------------------------------------------------------------------

def calculer_kda(dictionnaire_ID, playfab_id): # Calcul le KDA d'un joueur sur toutes les games jouées par ce dernier
    # dictionnaire_ID -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # playfab_id -> str : 'ID1'

    # Calculer le nombre de parties jouées
    nb_parties = nombre_de_parties_jouees(dictionnaire_ID, playfab_id)

    # Si le joueur n'a joué aucune partie, son KDA est 0
    if nb_parties == 0:
        return 0.0

    # Calculer le nombre total de kills
    total_kills = nombre_d_eliminations(dictionnaire_ID, playfab_id)

    # Calculer le KDA
    kda = total_kills / nb_parties

    return kda

# ----------------------------------------------------------------------------

def nombre_de_victoires(dictionnaire_ID, playfab_id): # Calcul le nombre de top 1 d'un joueur sur toutes les games jouées par ce dernier
    # dictionnaire_ID -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}
    # playfab_id -> str : 'ID1'

    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a aucune victoire

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Compter le nombre de victoires (placement == 1)
    nb_victoires = sum(1 for manche in manches if manche[0] == 1)

    return nb_victoires