def trouver_nom(id_de_joueur, liste_fichiers): # Trouve un nom de joueur pour un ID donné
    # id_de_joueur -> str : 'ID'
    
    # Parcourir chaque fichier de round
    for filename in liste_fichiers:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Parcourir chaque ligne du fichier (en ignorant l'en-tête)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            
            # Si le PlayfabID correspond, retourner le nom du joueur
            if columns[-5] == id_de_joueur:
                return columns[1]  # Le nom du joueur est à l'index 1 (colonne "Player")
    
    # Si le PlayfabID n'est pas trouvé, retourner None ou un message d'erreur
    return None