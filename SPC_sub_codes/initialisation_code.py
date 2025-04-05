import os

# ----------------------------------------------------------------------------

def lister_fichiers_repertoire(extension, prefix): # Trouve les fichiers à analyser dans le repertoire du code
    # extension -> str : ".txt"
    # prefix -> str : "SPC_"
    
    # Obtenir le répertoire courant
    repertoire_courant = os.getcwd()
    
    # Lister tous les fichiers dans le répertoire courant
    fichiers = os.listdir(repertoire_courant)
    
    # Filtrer les fichiers pour exclure ceux qui commencent par le préfixe
    fichiers_filtres = [
        fichier for fichier in fichiers
        if fichier.endswith(extension) and not fichier.startswith(prefix)
    ]
    
    return fichiers_filtres

# ----------------------------------------------------------------------------

def trouver_id(liste_de_fichier): # Créer un dictionnaire avec tout les ID présent au moins une fois
    # liste_de_fichier -> list : ['fichier1.txt',...]

    # Dictionnaire pour stocker les PlayfabID uniques avec des listes vides
    dict_des_id = {}

    # Parcourir chaque fichier dans la liste
    for filename in liste_de_fichier:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Parcourir chaque ligne du fichier (en ignorant l'en-tête)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            playfab_id = columns[-5]

            # Si le PlayfabID n'existe pas encore dans le dictionnaire, on l'ajoute avec une liste vide
            if playfab_id not in dict_des_id:
                dict_des_id[playfab_id] = []

    return dict_des_id