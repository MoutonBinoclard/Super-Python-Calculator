def nombre_de_parties_jouees(leaderboard, ID): # Trouve combien de partie à un joué un joueur donné

    # Vérifier si le joueur existe dans le dictionnaire
    if ID not in leaderboard:
        return 0  # Si le joueur n'existe pas, il n'a joué aucune partie

    # Récupérer les manches du joueur
    manches = leaderboard[ID][3]

    # Compter le nombre de parties où le placement est strictement positif
    nb_parties = 0
    for manche in manches:
        if manche[1][0] > 0:
            nb_parties += 1
    
    return nb_parties

# ----------------------------------------------------------------------------

def nombre_d_eliminations(leaderboard, ID): # Trouve le nombre de kill d'un joueur sur toutes les games jouées par ce dernier


    # Vérifier si le joueur existe dans le dictionnaire
    if ID not in leaderboard:
        return 0  # Si le joueur n'existe pas, il n'a fait aucun kill

    # Récupérer les manches du joueur
    manches = leaderboard[ID][3]

    # Calculer le nombre total de kills
    total_kills = 0
    for manche in manches:
        if manche[1][0] > 0:  # On ne compte que les manches où le placement est positif
            total_kills += manche[1][1]  # Ajoute le nombre de kills de cette manche

    return total_kills

# ----------------------------------------------------------------------------

def calculer_kda(leaderboard, ID): # Calcul le KDA d'un joueur sur toutes les games jouées par ce dernier


    # Calculer le nombre de parties jouées
    nb_parties = nombre_de_parties_jouees(leaderboard, ID)

    # Si le joueur n'a joué aucune partie, son KDA est 0
    if nb_parties == 0:
        return 0.0

    # Calculer le nombre total de kills
    total_kills = nombre_d_eliminations(leaderboard, ID)

    # Calculer le KDA
    kda = total_kills / nb_parties

    return kda

# ----------------------------------------------------------------------------

def nombre_de_victoires(leaderboard, ID): # Calcul le nombre de top 1 d'un joueur sur toutes les games jouées par ce dernier

    # Vérifier si le joueur existe dans le dictionnaire
    if ID not in leaderboard:
        return 0  # Si le joueur n'existe pas, il n'a aucune victoire

    # Récupérer les manches du joueur
    manches = leaderboard[ID][3]

    # Compter le nombre de victoires (placement == 1)
    nb_victoires = 0
    for manche in manches:
        if manche[1][0] == 1:
            nb_victoires += 1

    return nb_victoires

# ----------------------------------------------------------------------------

def calculer_points_totaux(classement):
    # Calcul points totaux

    for joueur in classement:
        somme = 0
        for manche in classement[joueur][3]:
            somme += manche[0]
        classement[joueur][1] = somme
    
    return classement

# ----------------------------------------------------------------------------

def ajouter_stats_globales(classement):
    # Ajout de stats globales
        
    for joueur in classement:
        classement[joueur][2].append(nombre_de_parties_jouees(classement, joueur))
        classement[joueur][2].append(nombre_de_victoires(classement, joueur))
        classement[joueur][2].append(nombre_d_eliminations(classement, joueur))
        classement[joueur][2].append(calculer_kda(classement, joueur))
    
    return classement

# ----------------------------------------------------------------------------

def calculer_points_totaux_et_round(leaderboard2):
    # classement2: {'ID_combine':[Nom, score final, [[score manche 1, placement manche 1], ...], [[classement[ID1]], [classement[ID2]], ...]]}
    for ID in leaderboard2:
        nombre_de_manches = len(leaderboard2[ID][3][0][3])
        for i in range(nombre_de_manches):
            scoremax = 0
            placementmin = 0
            for joueur in leaderboard2[ID][3]:
                if joueur[3][i][0] > scoremax:
                    scoremax = joueur[3][i][0]
                if joueur[3][i][1][0] < placementmin or placementmin == 0:
                    placementmin = joueur[3][i][1][0]
            leaderboard2[ID][2].append([scoremax, placementmin])
    
    # calcul du score final
    for ID in leaderboard2:
        somme = 0
        for manche in leaderboard2[ID][2]:
            somme += manche[0]
        leaderboard2[ID][1] = somme
    
    return leaderboard2
