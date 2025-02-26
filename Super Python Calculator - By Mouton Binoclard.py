# Super Python Calculator - By Mouton Binoclard
# Also known as a calculator for SAR solo tournaments

# ----------------------------------------------------------------------------

# The organization of the functions and code was done by Mouton Binoclard
# Most of the annotations and the matplotlib section were created by Deepseek AI (in French, of course, lol)

# ----------------------------------------------------------------------------

# IMPORTANT:
# This code requires the matplotlib and numpy libraries.
# You may need to search how to install these, or you can download a program that includes everything you need.

# For example:
# Winpython64-3.10.11.0.exe from https://github.com/winpython/winpython/releases/tag/6.1.20230518final
# When installed, it contains IdleX, which can run the program without issues.

# ----------------------------------------------------------------------------

# NOW SOME INSTRUCTIONS ON HOW TO USE THE CODE!

# ----------------------------------------------------------------------------

# First, place this code in an empty folder to avoid any bugs.

# To add a new round, simply copy the /getplayers data into a .txt file
# and place it in the same folder as this script. The rounds will then be
# included in the scoring.

# (Rounds will be processed in alphabetical order, so naming
# the rounds 1.txt, 2.txt, etc., might be a good idea.)

# IMPORTANT: Do not name your round files with the following names:
# - classement_complet.txt
# - classement_partiel.txt
# - classement_top.txt
# Otherwise, the corresponding rounds may be excluded or even overwritten, and you could lose data.

# ----------------------------------------------------------------------------

'MODIFY THE SCORING SYSTEM'

# To modify the scoring system, change the return values of the functions
# kill_points, placement_points, and masterkill.

def kill_points(placement, kills, total_players):
    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        return 2 * kills

def placement_points(placement, kills, total_players):
    if placement == 0 or placement == -1:
        return 0  # This one either!

    if placement == 1:
        return 15
    if placement == 2:
        return 13
    if placement == 3:
        return 12
    if placement >= 4 and placement <= 5:
        return 10
    if placement >= 6 and placement <= 8:
        return 8
    if placement >= 9 and placement <= 10:
        return 6
    if placement >= 11 and placement <= 15:
        return 5
    if placement >= 16 and placement <= 20:
        return 3
    if placement >= 21 and placement <= 25:
        return 1
    else:
        return 0

def masterkill(presence_de_masterkill, total_players):
    if presence_de_masterkill:
        return 0
    else:
        return 0

# You can use the placement section to award points:
# For example, this line:
# if placement >= 4 and placement <= 5: return 10
# means that if the player's placement is between 4 and 5 (inclusive), award 10 points.

# Alternatively, you can use a function like this:
# else: return total_players * math.exp(0.1 * (1 - placement))
# This means you award the player:
# (number of players in the round) x exponential(0.1 x (1 - player's placement))

# The same applies to kill points, of course.

# The masterkill function is a boolean (True or False),
# so you can only change the value (x) for having the most kills in a round:
# else: return x

# ----------------------------------------------------------------------------

'EXPORT THE TOP PLAYERS IN A TXT FILE'

# If you want to display the current tournament leaders in your overlay,
# open the file "top_joueurs.txt" in OBS.

# If you want to add the ranking graph, open the file "classement.png" in OBS.

# These files are generated after running the script at least once with
# at least one round processed.

# You can change the number of players included in the file by modifying
# the value below:

nombre_de_joueurs_a_exporter = 5

# Be careful not to add more than the number of players.

# Also, when running the code, two other files will be created:
# classement_complet.txt and classement_partiel.txt
# classement_complet can be pasted directly into a spreadsheet; it contains a lot of info (KDA, number of wins, etc.)
# classement_partiel is a lighter version, so you can quickly preview the players' positions.

# ----------------------------------------------------------------------------

'BAN PLAYERS'

# To ban players from the tournament and automatically adjust placements
# per round, add their IDs to the list below:

ID_banni_du_tournoi = []

# The list should have this form: ['53CEA3CB603F91EE', 'FEC13EBE7DA0943D', 'B4726A1348E0D88', ...]

# ----------------------------------------------------------------------------

'CHANGE THE NAME ON THE GRAPH'

# Here, you can change the tournament name that will appear on the graph.
nom_du_tournoi = 'The name of your tourney'

# And here, you can change the color of the title
couleur_du_titre = '#ffffff'

# ----------------------------------------------------------------------------

'CHANGING THE "FLATS" COLORS'

# This line lets you change the background color of the picture
couleur_de_fond = '#111111'

# And this one lets you change the gradient of the columns

# Preset 1
# couleur1 = "#1c946a"
# couleur2 = "#312354"
# couleur3 = "#a62547"
# couleur4 = "#ffc75a"

# Preset 2
couleur1 = "#990000"
couleur2 = "#cacacb"
couleur3 = "#5c5f62"
couleur4 = "#2c363e"

# To fully define a gradient, you also need to specify how many colors there are in total (at the end, you'll have x colors)
nombre_choisi = 7

# ----------------------------------------------------------------------------

'CHANGING THE COLORS OF THE TICKS AND LABELS'

# You can change the color of the ticks and labels on the x-axis here
couleur_label_x = '#cacacb'

# Same for the y-axis
couleur_label_y = '#cacacb'

# ----------------------------------------------------------------------------

'CHANGING THE COLORS OF THE AXIS'

# Color of the x-axis
couleur_axe_x = '#939496'

# Color of the y-axis
couleur_axe_y = '#939496'

# ----------------------------------------------------------------------------

# If you have any issues, feature requests, or you found a bug, feel free to contact me on Discord :D















# Start of the code :


import os
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_hex, to_rgb


# Cette ligne enlève tout les warning, penser à l'enlever pour du debug
import warnings
warnings.simplefilter("ignore", UserWarning)


"-----------------------------------------------------------------------------"

def lister_fichiers_repertoire(extension, fichiers_a_exclure):
    """
    Liste tous les fichiers dans le répertoire courant avec une extension spécifiée,
    en excluant les fichiers donnés dans la liste `fichiers_a_exclure`.

    :param extension: L'extension des fichiers à lister (par exemple, ".txt").
    :param fichiers_a_exclure: Une liste de noms de fichiers à exclure.
    :return: Une liste des fichiers correspondants, excluant ceux spécifiés.
    """
    # Obtenir le répertoire courant
    repertoire_courant = os.getcwd()
    
    # Lister tous les fichiers dans le répertoire courant
    fichiers = os.listdir(repertoire_courant)
    
    # Filtrer les fichiers pour ne garder que ceux avec l'extension spécifiée et exclure les fichiers indiqués
    fichiers_filtres = [
        fichier for fichier in fichiers
        if fichier.endswith(extension) and fichier not in fichiers_a_exclure
    ]
    
    return fichiers_filtres

"-----------------------------------------------------------------------------"

def trouver_id(liste_de_fichier): # A partir d'une liste de fichier de la forme ['fichier1.txt','','',...]

    # Dictionnaire pour stocker les PlayfabID uniques avec des listes vides
    dict_des_id = {}

    # Parcourir chaque fichier dans la liste
    for filename in liste_de_fichier:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Parcourir chaque ligne du fichier (en ignorant l'en-tête)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            playfab_id = columns[2]

            # Si le PlayfabID n'existe pas encore dans le dictionnaire, on l'ajoute avec une liste vide
            if playfab_id not in dict_des_id:
                dict_des_id[playfab_id] = []
    
    return dict_des_id

"-----------------------------------------------------------------------------"

def nombre_de_joueur_dans_un_round(fichier_du_round_2):
    
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

"-----------------------------------------------------------------------------"

def maximum_de_kill_dans_un_round(fichier_du_round_3):
    
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

"-----------------------------------------------------------------------------"

def enlever_joueurs_liste_du_round(liste_round_sans_analyse, liste_des_joueurs_a_enlever):
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
    return liste_round_sans_analyse

"-----------------------------------------------------------------------------"

def ajuster_les_positions_des_joueurs(liste_apres_enlevement_du_joueur, position_de_ce_dernier):

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
    return liste_apres_enlevement_du_joueur

"-----------------------------------------------------------------------------"

def fichier_round_en_liste(fichier_du_round_1):
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
        playfab_id = columns[2]
        placement = int(columns[6])
        kills = int(columns[5])
        mk=False
        if kills==maximum : mk=True

        # Ajouter les données du joueur à la liste du round
        liste_du_round.append([playfab_id, placement, kills, total_joueurs, mk])

    liste_du_round=enlever_joueurs_liste_du_round(liste_du_round, ID_banni_du_tournoi)
    
    return liste_du_round

"-----------------------------------------------------------------------------"

def maj_dictionnaire(dictionnaire, manche):
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
                    masterkill_ou_non = joueur[4]  # Ajout de la quatrième valeur
                    # Ajouter les données à la liste du joueur
                    dictionnaire[playfab_id].append([placement, kills, total_joueurs, masterkill_ou_non])
                    break
        else:
            # Si le joueur n'est pas dans la manche, ajouter [0, 0, 0, False]
            dictionnaire[playfab_id].append([0, 0, 0, False])  # Ajout de False comme quatrième valeur
    
    return dictionnaire

"-----------------------------------------------------------------------------"

def trouver_nom(id_de_joueur):
    # Parcourir chaque fichier de round
    for filename in liste_fichiers_partie:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Parcourir chaque ligne du fichier (en ignorant l'en-tête)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            
            # Si le PlayfabID correspond, retourner le nom du joueur
            if columns[2] == id_de_joueur:
                return columns[1]  # Le nom du joueur est à l'index 1 (colonne "Player")
    
    # Si le PlayfabID n'est pas trouvé, retourner None ou un message d'erreur
    return None

"-----------------------------------------------------------------------------"
"-----------------------------------------------------------------------------"

# Ancien emplacement des fonctions kill placement et masterkill

"-----------------------------------------------------------------------------"
"-----------------------------------------------------------------------------"

def score_manche(information_de_manche): #[placement,nombre de kill,nombre de joueur,masterkill ou non]
    # Extraire les données de la manche
    placement, kills, nombre_de_joueurs, validite_mk = information_de_manche
    
    # Calculer les points de placement et de kills
    placement_pts = placement_points(placement, kills, nombre_de_joueurs)
    kill_pts = kill_points(placement, kills, nombre_de_joueurs)
    masterkill_pts=masterkill(validite_mk, nombre_de_joueurs)
    
    # Calculer le score total de la manche
    score_total = placement_pts + kill_pts + masterkill_pts
    
    return score_total

"-----------------------------------------------------------------------------"

def score_final(manches_du_joueurs): # Renvoi une liste de la forme [pt manche1, pt manche 2, etc...]
    # Liste pour stocker les scores de chaque manche
    scores_manches = []
    
    # Parcourir chaque manche
    for manche in manches_du_joueurs:
        # Calculer le score de la manche avec la fonction score_manche
        score = score_manche(manche)
        scores_manches.append(score)
    
    return scores_manches

"-----------------------------------------------------------------------------"

def dictionnaire_finale(dictionnaire_des_infos_des_rounds):
    # Dictionnaire final à retourner
    dico_final = {}
    
    # Parcourir chaque joueur dans le dictionnaire des rounds
    for playfab_id_joueur, manches in dictionnaire_des_infos_des_rounds.items():
        # Trouver le nom du joueur
        nom_joueur = trouver_nom(playfab_id_joueur)
        
        # Calculer les scores des manches
        scores_manches = score_final(manches)
        
        # Calculer le score total (somme des scores des manches)
        score_total = sum(scores_manches)
        
        # Ajouter les informations au dictionnaire final
        dico_final[playfab_id_joueur] = [nom_joueur, score_total, scores_manches]
    
    return dico_final

"-----------------------------------------------------------------------------"

def tri_du_classement(dictionnaire_non_classé):
    # Trier le dictionnaire en fonction du score final (index 1 de la liste associée à chaque clé)
    classement_trié = dict(sorted(dictionnaire_non_classé.items(), key=lambda item: item[1][1], reverse=True))
    
    return classement_trié

"-----------------------------------------------------------------------------"

def nombre_de_parties_jouees(dictionnaire_ID, playfab_id):
    """
    Calcule le nombre de parties jouées par un joueur spécifique.
    Une partie est considérée comme jouée si le placement est strictement positif.

    :param dictionnaire_ID: Le dictionnaire contenant les données des joueurs et leurs placements.
    :param playfab_id: L'ID du joueur pour lequel on veut calculer le nombre de parties jouées.
    :return: Le nombre de parties jouées par le joueur.
    """
    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a joué aucune partie

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Compter le nombre de parties où le placement est strictement positif
    nb_parties = sum(1 for manche in manches if manche[0] > 0)

    return nb_parties

"-----------------------------------------------------------------------------"

def nombre_d_eliminations(dictionnaire_ID, playfab_id):
    """
    Calcule le nombre total de kills (éliminations) d'un joueur spécifique.

    :param dictionnaire_ID: Le dictionnaire contenant les données des joueurs et leurs kills.
    :param playfab_id: L'ID du joueur pour lequel on veut calculer le nombre de kills.
    :return: Le nombre total de kills du joueur.
    """
    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a fait aucun kill

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Calculer le nombre total de kills
    total_kills = sum(manche[1] for manche in manches if manche[0] > 0)

    return total_kills

"-----------------------------------------------------------------------------"

def calculer_kda(dictionnaire_ID, playfab_id):
    """
    Calcule le KDA (Kills / Nombre de parties jouées) d'un joueur spécifique.

    :param dictionnaire_ID: Le dictionnaire contenant les données des joueurs.
    :param playfab_id: L'ID du joueur pour lequel on veut calculer le KDA.
    :return: Le KDA du joueur (float). Si le joueur n'a joué aucune partie, retourne 0.
    """
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

"-----------------------------------------------------------------------------"

def nombre_de_victoires(dictionnaire_ID, playfab_id):
    """
    Calcule le nombre de victoires d'un joueur spécifique.
    Une victoire est comptée lorsque le placement est égal à 1.

    :param dictionnaire_ID: Le dictionnaire contenant les données des joueurs et leurs placements.
    :param playfab_id: L'ID du joueur pour lequel on veut calculer le nombre de victoires.
    :return: Le nombre de victoires du joueur.
    """
    # Vérifier si le joueur existe dans le dictionnaire
    if playfab_id not in dictionnaire_ID:
        return 0  # Si le joueur n'existe pas, il n'a aucune victoire

    # Récupérer les manches du joueur
    manches = dictionnaire_ID[playfab_id]

    # Compter le nombre de victoires (placement == 1)
    nb_victoires = sum(1 for manche in manches if manche[0] == 1)

    return nb_victoires

"-----------------------------------------------------------------------------"

# Fonction pour exporter les combien premiers joueurs dans un fichier texte
def exporter_top(classement_du_tournoi, filename, combien):
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(filename, 'w', encoding='utf-8') as file:
        # Parcourir les cinq premiers joueurs du classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            if i >= combien:  # On s'arrête après les cinq premiers
                break
            pseudo, score_final, _ = data
            # Écrire les informations du joueur dans le fichier
            file.write(f"{i + 1}. {score_final:.2f} -> {pseudo}\n")

"-----------------------------------------------------------------------------"

# Fonction pour exporter le classement avec les points seulement
def exporter_classement_partiel(classement_du_tournoi, filename):
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(filename, 'w', encoding='utf-8') as file:
        # Parcourir tous les joueurs du classement
        for i, (playfab_id, data) in enumerate(classement_du_tournoi.items()):
            pseudo, score_final, scores_manches = data
            # Écrire les informations du joueur dans le fichier
            file.write(f"{i + 1}. {score_final:.2f} -> {pseudo}\n")

"-----------------------------------------------------------------------------"

def exporter_classement_complet(classement_du_tournoi, dict_ID, filename):
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

    :param classement_du_tournoi: Le classement des joueurs (dictionnaire trié).
    :param dictionnaire_ID: Le dictionnaire contenant les données des joueurs.
    :param filename: Le nom du fichier de sortie.
    """
    # Ouvrir le fichier en mode écriture avec l'encodage UTF-8
    with open(filename, 'w', encoding='utf-8') as file:
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

"-----------------------------------------------------------------------------"
"-----------------------------------------------------------------------------"

liste_fichiers_partie=(lister_fichiers_repertoire(".txt",["classement_top.txt","classement_partiel.txt","classement_complet.txt"]))

dictionnaire_ID=trouver_id(liste_fichiers_partie)

# Enlever les banni du dictionnaire d'ID
for ID_ban in ID_banni_du_tournoi:
    dictionnaire_ID.pop(ID_ban)

for fichier_de_manche in liste_fichiers_partie :
    dictionnaire_ID=maj_dictionnaire(dictionnaire_ID,fichier_round_en_liste(fichier_de_manche))
#print(dictionnaire_ID)

classement=tri_du_classement(dictionnaire_finale(dictionnaire_ID))
#print(classement)

# Export des fichiers textes
exporter_top(classement, 'classement_top.txt',nombre_de_joueurs_a_exporter)
exporter_classement_partiel(classement, 'classement_partiel.txt')
exporter_classement_complet(classement, dictionnaire_ID, 'classement_complet.txt')

'''
for i in classement:
    joueur=classement[i][0]
    score=classement[i][1]
    print(str(score)+" : "+str(joueur))

print('')
'''


















"-----------------------------------------------------------------------------"

def generer_degrade_4_couleurs(couleur1, couleur2, couleur3, couleur4, nombre_de_couleurs): #Couleur sous le format #xxxxxx et nombre de couleur 7 modulo 3+

    # Convertir les couleurs hexadécimales en RGB
    rgb1 = to_rgb(couleur1)
    rgb2 = to_rgb(couleur2)
    rgb3 = to_rgb(couleur3)
    rgb4 = to_rgb(couleur4)

    # Créer un tableau de valeurs pour interpoler entre les couleurs
    t = np.linspace(0, 1, nombre_de_couleurs)

    # Interpoler linéairement entre les quatre couleurs
    degrade = []
    for i in t:
        if i <= 0.333:
            # Interpolation entre couleur1 et couleur2
            r = rgb1[0] + (rgb2[0] - rgb1[0]) * (i * 3)
            g = rgb1[1] + (rgb2[1] - rgb1[1]) * (i * 3)
            b = rgb1[2] + (rgb2[2] - rgb1[2]) * (i * 3)
        elif i <= 0.666:
            # Interpolation entre couleur2 et couleur3
            r = rgb2[0] + (rgb3[0] - rgb2[0]) * ((i - 0.333) * 3)
            g = rgb2[1] + (rgb3[1] - rgb2[1]) * ((i - 0.333) * 3)
            b = rgb2[2] + (rgb3[2] - rgb2[2]) * ((i - 0.333) * 3)
        else:
            # Interpolation entre couleur3 et couleur4
            r = rgb3[0] + (rgb4[0] - rgb3[0]) * ((i - 0.666) * 3)
            g = rgb3[1] + (rgb4[1] - rgb3[1]) * ((i - 0.666) * 3)
            b = rgb3[2] + (rgb4[2] - rgb3[2]) * ((i - 0.666) * 3)
        
        # Clipper les valeurs RGB entre 0 et 1
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))
        
        # Convertir la couleur RGB en hexadécimal et l'ajouter à la liste
        degrade.append(to_hex((r, g, b)))

    return degrade

"-----------------------------------------------------------------------------"

# Score max
le_haut_du_graph = next(iter(classement.values()))[1]

barres_couleurs = generer_degrade_4_couleurs(couleur1, couleur2, couleur3, couleur4, nombre_choisi) # Augmenter le nombre de couleurs par trois
# Créer un graphique en barres empilées avec un style personnalisé
plt.figure(figsize=(10, 6), facecolor=couleur_de_fond)  # Fond pour la figure
ax = plt.gca()  # Obtenir l'axe actuel
ax.set_facecolor(couleur_de_fond)  # Fond pour l'arrière-plan du graphique

# Pour stocker les handles de la légende
legend_handles = []

# Pour chaque joueur, empiler les scores de chaque manche
for i, (playfab_id, data) in enumerate(classement.items()):
    pseudo, score_final, scores_manches = data
    bottom = 0  # Commencer à empiler à partir de 0
    for j, score in enumerate(scores_manches):
        bar = plt.bar(pseudo, score, bottom=bottom, color=barres_couleurs[j % len(barres_couleurs)])
        bottom += score  # Mettre à jour la position de départ pour la prochaine manche

        # Ajouter un handle pour la légende (une seule fois par manche)
        if i == 0:  # On ne le fait que pour le premier joueur pour éviter les doublons
            legend_handles.append(bar[0])

    # Ajouter le score total en haut de la barre, en vertical et empiétant sur les colonnes
    plt.text(pseudo, score_final + 0.03*le_haut_du_graph, f"{score_final:.2f}", ha='center', va='bottom', color='white', fontsize=10, rotation=90)

# Personnaliser les axes et les labels
# plt.xlabel('Joueurs', color='white')  # Texte en blanc
# plt.ylabel('Score Final', color='white')  # Texte en blanc
plt.title(nom_du_tournoi, fontdict={'color': couleur_du_titre})  # Gestion du titre

# Changer la couleur des ticks (graduations) et des labels des axes
ax.tick_params(axis='x', colors=couleur_label_x)  # Couleur des ticks et labels de l'axe X
ax.tick_params(axis='y', colors=couleur_label_y)  # Couleur des ticks et labels de l'axe Y

# Changer la couleur des bordures du graphique
for spine in ax.spines.values():
    spine.set_edgecolor('white')  # Bordures en blanc

# Définir la couleur des axes X et Y
ax.spines['bottom'].set_color(couleur_axe_x) # Axe X en blanc
ax.spines['left'].set_color(couleur_axe_y)   # Axe Y en blanc

# Désactiver les bordures du haut et de la droite
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Garder les bordures gauche et basse visibles
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Rotation des noms des joueurs pour une meilleure lisibilité
plt.xticks(rotation=45, ha='right')

# Ajouter une légende
labels = [f"Manche {i+1}" for i in range(len(barres_couleurs))]  # Créer les labels pour chaque manche
plt.legend(legend_handles, labels, title_fontsize='large', fontsize='medium', facecolor=couleur_de_fond, edgecolor='white', labelcolor='white')

# Ajuster la mise en page
plt.tight_layout()

# Afficher le graphique
#plt.show()

# Ajuster la mise en page
plt.tight_layout()

# Enregistrer le graphique
plt.savefig("classement.png", dpi=600, bbox_inches='tight', facecolor=couleur_de_fond)
print("Graphique enregistré sous 'classement.png'")

