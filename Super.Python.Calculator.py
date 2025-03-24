# Super Python Calculator 
# By Mouton Binoclard
# Also known as a calculator for SAR tournaments

# Version 4.1

# ----------------------------------------------------------------------------

# The organization of functions and code was done by Mouton Binoclard.
# Most of the annotations and the matplotlib section were created by Deepseek AI (in French, of course, lol).

# ----------------------------------------------------------------------------

# IMPORTANT:
# This code requires the following libraries to run :

import os
import sys

import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import tkinter as tk
from tkinter import Listbox, MULTIPLE, messagebox

import json

from datetime import datetime

import warnings
warnings.simplefilter("ignore", UserWarning)

# ----------------------------------------------------------------------------

# NOW, HERE ARE SOME INSTRUCTIONS ON HOW TO USE THE CODE!

# ----------------------------------------------------------------------------

# 1. After extracting this code, do NOT change the folder structure as well as the names of the files and folders.
#    If you do, the code may not work properly.

# 2. To add a new round, simply copy the /getplayers data into a .txt file
#    and place it in the same folder as this script. The rounds will then be included in the scoring.

# 3. Be sure to NEVER use the SPC_ prefix for your round files.
#    Otherwise, the corresponding rounds may be excluded or even overwritten, and you could lose data.

#    (Rounds will be processed in alphabetical order, so naming the files 1.txt, 2.txt, etc., might be good idea.)

# ----------------------------------------------------------------------------

'ACTIVATE TEAMS'

# To enable team mode, set the following value to True. Otherwise, set it to False:
teams = False

# Every person will now have their kills synced with the team they're playing with.

# The first time you will the run code with the teams enabled, the code will ask you to create the teams with a wonderful graphical interface 
# They will be saved in a file named 'SPC___Teams.txt'

# If you want to change it, you can :
# - Manually change the id in the file
# - Delete the file and than start the code ato create the teams again

# ----------------------------------------------------------------------------

'MODIFY THE SCORING SYSTEM'

# To adjust the scoring system, update the function definitions in the Python preset file.
# When team mode is active, kills represent the total kills achieved by the player's team.

# Type the name of the file containing the scoring system you want to use:
# (The file must be in the SPC_scoring_presets folder.)

from SPC_scoring_presets.SPC_sp_spi import kill_points, placement_points, masterkill

# It must be something like SPC_scoring_presets.name_of_the_file_without_the_extension

# ----------------------------------------------------------------------------

'EXPORT THE TOP PLAYERS IN A TXT FILE'

# This line define how many players you want to put in the top file
nombre_de_joueurs_a_exporter = 5  # Number of players to include in the file.

# ----------------------------------------------------------------------------

'BAN PLAYERS'

# To ban players from the tournament and automatically adjust placements
# per round, add their IDs to the list below:

ID_banni_du_tournoi = []

# The list should have this form: ['53CEA3CB603F91EE', 'FEC13EBE7DA0943D', 'B4726A1348E0D88', ...]

# ----------------------------------------------------------------------------

'CHANGE THE NAME ON THE GRAPH'

# Here, you can change the tournament name that will appear on the graph.
nom_du_tournoi = "Mouton's simple scrims"

# Or you can add a logo to the graph by placing a file named "SPC_logo.png" in the same folder as this script
# and enabling the following line:
logo=False

# Size of the logo
zoom_logo=0.15

# If you want the date to show up on the graph, set the following value to True:
date=True

# ----------------------------------------------------------------------------

'CHANGE THE COLORS'

# You can change the colors of the graph by modifying the values in the file "SPC_colors_config.json".

color_scheme = "SPC_color_schemes/SPC_cs_v4.json"

# ----------------------------------------------------------------------------

# If you have any issues, feature requests, or you found a bug, feel free to contact me on Discord :D




# Start of the code

# ----------------------------------------------------------------------------

def charger_couleurs(fichier=color_scheme): # Charger les couleurs depuis le fichier JSON
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

# Charger les couleurs
couleurs = charger_couleurs()

# Appliquer les couleurs
couleur_du_titre = couleurs["couleur_du_titre"]
couleur_date = couleurs["couleur_date"]
couleur_de_fond = couleurs["couleur_de_fond"]
couleur1 = couleurs["couleur1"]
couleur2 = couleurs["couleur2"]
couleur3 = couleurs["couleur3"]
couleur4 = couleurs["couleur4"]
nombre_choisi = couleurs["nombre_choisi"]
couleur_label_x = couleurs["couleur_label_x"]
couleur_label_y = couleurs["couleur_label_y"]
couleur_axe_x = couleurs["couleur_axe_x"]
couleur_axe_y = couleurs["couleur_axe_y"]
couleur_points = couleurs["couleur_points"]
couleur_contour_legende = couleurs["couleur_contour_legende"]
couleur_texte_legende = couleurs["couleur_texte_legende"]
couleur_fliers = couleurs["couleur_fliers"]
couleur_caps = couleurs["couleur_caps"]
couleur_whiskers = couleurs["couleur_whiskers"]
couleur_boxes_inside = couleurs["couleur_boxes_inside"]
couleur_boxes_outside = couleurs["couleur_boxes_outside"]
couleur_medians = couleurs["couleur_medians"]
couleur_moyenne = couleurs["couleur_moyenne"]
couleur_horizontales = couleurs["couleur_horizontales"]

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

def fichier_round_en_liste(fichier_du_round_1): # Prend un fichier de round et le transforme en liste
    # fichier_du_round_1 -> str : 'fichier1.txt' 

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
    liste_du_round=enlever_joueurs_liste_du_round(liste_du_round, ID_banni_du_tournoi)

    # Correction des positions des joueurs (mode team surtout)
    liste_du_round=MAJ_placement_en_teams(liste_du_round)

    return liste_du_round

"-----------------------------------------------------------------------------"

def nombre_de_joueur_dans_un_round(fichier_du_round_2): # Trouve le nombre de joueurs dans un fichier round
    # fichier_du_round_2 -> str : 'fichier1.txt'
 
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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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
                    # Ajouter les données à la liste du joueur
                    dictionnaire[playfab_id].append([placement, kills, total_joueurs, masterkill_ou_non, team, team_kill])
                    break
        else:
            # Si le joueur n'est pas dans la manche, ajouter [0, 0, 0, False, -1, 0]
            dictionnaire[playfab_id].append([0, 0, 0, False, -1, 0])  # Ajout de valeurs par défaut pour team et team_kill
    
    return dictionnaire # dict -> {'ID1' :[[placement, kills, nombre joueurs, masterkill ?, team, team kill],[,,,],...], ...}

"-----------------------------------------------------------------------------"

def trouver_nom(id_de_joueur): # Trouve un nom de joueur pour un ID donné
    # id_de_joueur -> str : 'ID'
    
    # Parcourir chaque fichier de round
    for filename in liste_fichiers_partie:
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

"-----------------------------------------------------------------------------"

# Ancien emplacement fonction kill et placement

"-----------------------------------------------------------------------------"

def score_final(manches_du_joueur): # Renvoi une liste de la forme [pt manche1, pt manche 2, etc...]
    # manche_du_joueurs -> list : [['ID1', placement, kill, nombre de joueur, masterkill ?, team, kill team], [], ...]

    # Liste pour stocker les scores de chaque manche
    scores_manches = []
    
    # Parcourir chaque manche
    for manche in manches_du_joueur:
        # Calculer le score de la manche avec la fonction score_manche
        score = score_manche(manche)
        scores_manches.append(score)
    
    return scores_manches

"-----------------------------------------------------------------------------"

def score_manche(information_de_manche): # Renvoi un score pour une manche donnée
    # information_de_manche -> list : ['ID1', placement, kill, nombre de joueur, masterkill ?, team, kill team]

    # Extraire les données de la manche
    placement, kills, nombre_de_joueurs, validite_mk, dans_quelle_team, kills_en_equipe = information_de_manche
    
    # Calculer les points de placement et de kills

    if teams==False :
        placement_pts = placement_points(placement, kills, nombre_de_joueurs)
        kill_pts = kill_points(placement, kills, nombre_de_joueurs)
        masterkill_pts=masterkill(validite_mk, nombre_de_joueurs)

    if teams==True:
        placement_pts = placement_points(placement, kills_en_equipe, nombre_de_joueurs)
        kill_pts = kill_points(placement, kills_en_equipe, nombre_de_joueurs)
        masterkill_pts=masterkill(validite_mk, nombre_de_joueurs)
    
    # Calculer le score total de la manche
    score_total = placement_pts + kill_pts + masterkill_pts
    
    return score_total # int -> score de la manche

"-----------------------------------------------------------------------------"

def dictionnaire_finale(dictionnaire_des_infos_des_rounds): # Création du dicionnaire complet, (correspond au dict classement)
    # dictionnaire_des_infos_des_rounds -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}

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

    return dico_final # dict -> {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

"-----------------------------------------------------------------------------"

def tri_du_classement(dictionnaire_non_classé): # Tri un dictionnaire dans l'ordre décroissant des points
    # dictionnaire_non_classé -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

    # Trier le dictionnaire en fonction du score final (index 1 de la liste associée à chaque clé)
    classement_trié = dict(sorted(dictionnaire_non_classé.items(), key=lambda item: item[1][1], reverse=True))
    
    return classement_trié # dict -> {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

"-----------------------------------------------------------------------------"                

def creation_classement_team(classement_par_joueur_1, liste_de_teams):
    # classement_par_joueur_1 -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # liste_de_teams -> list : [['ID1', 'ID2'], ['ID3', 'ID4'], ...] (liste des équipes, chaque équipe est une liste de joueurs)

    # Dictionnaire pour stocker les informations des équipes
    classement_team = {}

    # Parcourir chaque équipe dans la liste des équipes
    for une_team in liste_de_teams:
        # Calculer les points par manche pour l'équipe en utilisant la fonction calcul_pt_par_manche_team
        team_id, team_data = calcul_pt_par_manche_team(classement_par_joueur_1, une_team)
        
        # Ajouter les informations de l'équipe au dictionnaire classement_team
        classement_team[team_id] = team_data

    # Trier le dictionnaire des équipes en fonction du score total (ordre décroissant)
    classement_team_trie = dict(sorted(classement_team.items(), key=lambda item: item[1][1], reverse=True))

    return classement_team_trie

"-----------------------------------------------------------------------------"

def calcul_pt_par_manche_team(classement_par_joueur_2, une_team):
    # classement_par_joueur_2 -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}
    # une_team -> list : ['ID1', 'ID2', ...] (liste des IDs des joueurs dans l'équipe)

    # Initialiser une liste pour stocker les points par manche pour l'équipe
    points_par_manche = []

    # Trouver le nombre de manches en prenant la longueur de la liste des scores d'un joueur
    nombre_de_manches = len(next(iter(classement_par_joueur_2.values()))[2])

    # Parcourir chaque manche
    for manche in range(nombre_de_manches):
        # Initialiser le score de la manche pour l'équipe
        score_manche_team = 0

        # Parcourir chaque joueur de l'équipe
        for joueur_id in une_team:
            if joueur_id in classement_par_joueur_2:
                # Récupérer les scores par manche du joueur
                scores_manches_joueur = classement_par_joueur_2[joueur_id][2]
                # Si le joueur a participé à cette manche (score > 0), ajouter son score à l'équipe
                if scores_manches_joueur[manche] > score_manche_team:
                    score_manche_team = scores_manches_joueur[manche]

        # Ajouter le score de la manche pour l'équipe à la liste
        points_par_manche.append(score_manche_team)

    # Calculer le score total de l'équipe (somme des scores de toutes les manches)
    score_total_team = sum(points_par_manche)

    # Retourner les informations de l'équipe sous la forme :
    # "ID1+ID2+..." : ["Nom du joueur 1 / Nom du joueur 2 / ...", score final, [score manche 1, score manche 2, ...]]
    noms_joueurs = " & ".join([classement_par_joueur_2[joueur_id][0] for joueur_id in une_team if joueur_id in classement_par_joueur_2])
    return f"{'+'.join(une_team)}", [noms_joueurs, score_total_team, points_par_manche]

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

def creer_dossier_export():  # Crée le dossier SPC_exports s'il n'existe pas
    if not os.path.exists("SPC_exports"):
        os.makedirs("SPC_exports")

creer_dossier_export()

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

"-----------------------------------------------------------------------------"

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

def exporter_graph(classement):  # Génère le graph du classement à partir d'un dico classement
    """
    Génère et exporte un graphique en barres empilées à partir du classement fourni.
    :param classement: dict -> Le classement des joueurs ou des équipes.
    """
    # Score max
    le_haut_du_graph = next(iter(classement.values()))[1]

    barres_couleurs = generer_degrade_4_couleurs(couleur1, couleur2, couleur3, couleur4, nombre_choisi) # Augmenter le nombre de couleurs par trois
    # Créer un graphique en barres empilées avec un style personnalisé
    plt.figure(figsize=(12, 6), facecolor=couleur_de_fond)  # Augmenter légèrement la largeur (de 10 à 12)
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
        plt.text(pseudo, score_final + 0.03*le_haut_du_graph, f"{score_final:.2f}", ha='center', va='bottom', color=couleur_points, fontsize=10, rotation=90)

    # Utiliser les graduations automatiques de Matplotlib pour les lignes horizontales
    y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in y_ticks:
        ax.axhline(y, color=couleur_horizontales, linestyle='--', linewidth=0.5, zorder=0)  # Ajouter une ligne horizontale à chaque graduation

    # Changer la couleur des ticks (graduations) et des labels des axes
    ax.tick_params(axis='x', which='both', colors=couleur_axe_x)  # Couleur des ticks de l'axe X
    ax.xaxis.label.set_color(couleur_label_x)  # Couleur du label de l'axe X
    ax.tick_params(axis='y', which='both', colors=couleur_axe_y)  # Couleur des ticks de l'axe Y
    ax.yaxis.label.set_color(couleur_label_y)  # Couleur du label de l'axe Y

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

    # Rotation des noms des joueurs pour une meilleure lisibilité avec une taille de police réduite
    plt.xticks(rotation=45, ha='right', fontsize=8, color=couleur_label_x)  # Correction de la couleur des ticks X
    plt.yticks(color=couleur_label_y)  # Correction de la couleur des ticks Y

    # Ajouter une légende
    labels = [f"Round {i+1}" for i in range(len(barres_couleurs))]  # Créer les labels pour chaque manche
    legend = plt.legend(legend_handles, labels, title_fontsize='large', fontsize='medium', facecolor=couleur_de_fond, edgecolor=couleur_contour_legende, labelcolor=couleur_texte_legende)

    # Ajuster la mise en page
    plt.tight_layout()

    # Ajouter des marges à gauche et à droite pour plus de légèreté
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(nom_du_tournoi, fontdict={'color': couleur_du_titre, 'fontsize': 16, 'style': 'italic', 'weight': 'bold'}, pad=20)  # Gestion du titre

    if logo == True:

        # Charger le logo
        logo_path = "SPC_logo.png"
        logo_image = plt.imread(logo_path)

        # Ajouter le logo à la place du titre
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom=zoom_logo)  # Ajuster le zoom pour auto-scaling
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if date == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', 
                fontdict={'color': couleur_date, 'fontsize': 8, 'style': 'italic'})

    # Afficher le graphiques
    #plt.show()

    # Ajuster la mise en page
    #plt.tight_layout()

    # Enregistrer le graphique
    plt.savefig(os.path.join("SPC_exports", "SPC_Graphic.png"), dpi=600, facecolor=couleur_de_fond)


"-----------------------------------------------------------------------------"
def exporter_graph_placement_moyen(dict_ID): 
    """
    Génère un graphique en boxplot pour visualiser les placements moyens des joueurs.
    :param dict_ID: dict -> {'ID1': [[placement, kills, nombre joueurs, masterkill ?, team, team kill], ...], ...}
    """
    # Préparer les données pour le boxplot
    data = []
    labels = []
    
    for playfab_id, manches in dict_ID.items():
        placements = [manche[0] for manche in manches if manche[0] > 0]  # Ignorer les placements 0 et -1
        if placements:
            data.append(placements)
            labels.append(trouver_nom(playfab_id))  # Utiliser le nom du joueur ou l'ID si le nom est introuvable

    # Créer le graphique
    plt.figure(figsize=(12, 6), facecolor=couleur_de_fond)
    ax = plt.gca()
    ax.set_facecolor(couleur_de_fond)

    # Générer le boxplot
    box = plt.boxplot(data, patch_artist=True, tick_labels=labels, vert=True, showmeans=True)

    # Personnaliser les couleurs des boxplots
    for patch in box['boxes']:
        patch.set(facecolor=couleur_boxes_inside, edgecolor=couleur_boxes_outside)
    for whisker in box['whiskers']:
        whisker.set(color=couleur_whiskers)
    for cap in box['caps']:
        cap.set(color=couleur_caps)
    for median in box['medians']:
        median.set(color=couleur_medians, linewidth=1)  # Réduire l'épaisseur des médianes
        median.set_xdata([median.get_xdata()[0] - 0.15, median.get_xdata()[1] + 0.15])  # Étendre la médiane au-delà de la box
    for flier in box['fliers']:
        flier.set(marker='x', markerfacecolor=couleur_fliers, markeredgecolor=couleur_fliers, alpha=1)
    for mean in box['means']:
        mean.set(marker= "o", markerfacecolor="none", markeredgecolor=couleur_moyenne, alpha=1, markersize=5)

    # Utiliser les graduations automatiques de Matplotlib pour les lignes horizontales
    y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in y_ticks:
        ax.axhline(y, color=couleur_horizontales, linestyle='--', linewidth=0.5, zorder=0)  # Ajouter une ligne horizontale à chaque graduation

    for i in range(1,4):
        ax.axhline(i, color=couleur_horizontales, linestyle=(0,(1,1)), linewidth=0.5, zorder=0)  # Ligne top 1

    ax.tick_params(axis='x', which='both', colors=couleur_axe_x)  # Couleur des ticks de l'axe X
    ax.xaxis.label.set_color(couleur_label_x)  # Couleur du label de l'axe X
    ax.tick_params(axis='y', which='both', colors=couleur_axe_y)  # Couleur des ticks de l'axe Y
    ax.yaxis.label.set_color(couleur_label_y)  # Couleur du label de l'axe Y

    # Ajouter des titres et labels
    #plt.title("Placement moyen des joueurs", color=couleur_du_titre, fontsize=14)
    #plt.ylabel("Placement (1 = Meilleur)", color=couleur_label_y)
    #plt.xlabel("Joueurs", color=couleur_label_x)

    # Inverser l'axe des ordonnées pour que le meilleur placement soit en haut
    ax.invert_yaxis()

    # Fixer la limite supérieure de l'axe Y à 0.5 et ajuster la limite inférieure
    placement_min = max([max(placements) for placements in data]) if data else 0
    ax.set_ylim(bottom=placement_min + 1, top=0.5)

    # Rotation des noms des joueurs pour une meilleure lisibilité avec une taille de police réduite
    plt.xticks(rotation=45, ha='right', fontsize=8, color=couleur_label_x)  # Correction de la couleur des ticks X
    plt.yticks(color=couleur_label_y)  # Correction de la couleur des ticks Y

    # Ajuster les bordures et les axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(couleur_axe_y)
    ax.spines['bottom'].set_color(couleur_axe_x)

    # Ajuster la mise en page
    plt.tight_layout()

    # Ajouter des marges à gauche et à droite pour plus de légèreté
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(nom_du_tournoi, fontdict={'color': couleur_du_titre, 'fontsize': 16, 'style': 'italic', 'weight': 'bold'}, pad=20)  # Gestion du titre

    if logo == True:

        # Charger le logo
        logo_path = "SPC_logo.png"
        logo_image = plt.imread(logo_path)

        # Ajouter le logo au graphique
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom=zoom_logo)  # Ajuster le zoom pour auto-scaling
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if date == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', 
                fontdict={'color': couleur_date, 'fontsize': 8, 'style': 'italic'})

    # Enregistrer le graphique
    plt.savefig(os.path.join("SPC_exports", "SPC_Placement_Boxplot.png"), dpi=600, facecolor=couleur_de_fond)

"-----------------------------------------------------------------------------"

def afficher_joueurs(liste_des_joueurs): # Affiche toute les joueurs présent dans un dico adapté
    for index, joueur in enumerate(liste_des_joueurs):
        print(f"{index}: {joueur[1]}")

"-----------------------------------------------------------------------------"

def sauvegarder_equipes(equipes, fichier="SPC___teams.txt"): # Sauvergarde du fichier des équipes
    """Sauvegarde les équipes dans un fichier texte."""
    with open(fichier, "w", encoding="utf-8") as f:
        for equipe in equipes:
            f.write(" ".join(equipe) + "\n")

"-----------------------------------------------------------------------------"

def charger_equipes(fichier="SPC___teams.txt"): # Chargement du fichier équipes du repertoire
    """Charge les équipes depuis un fichier texte s'il existe."""
    if os.path.exists(fichier):
        equipes = []
        with open(fichier, "r", encoding="utf-8") as f:
            for line in f:
                equipes.append(line.strip().split(" "))
        return equipes
    return None

"-----------------------------------------------------------------------------"

def creer_equipe(liste_des_joueurs): # FX NON UTILISÉE Interface dans le shell pour creer les équipes
    """Crée les équipes de manière interactive et les sauvegarde."""
    equipes = []
    while True:
        afficher_joueurs(liste_des_joueurs)
        print("Enter the player indexes to form a team (separated by spaces), or press Enter to finish:")
        selection = input().strip()
        if selection == "":
            break
        try:
            indices = list(map(int, selection.split()))
            equipe = [liste_des_joueurs[i][0] for i in indices]
            equipes.append(equipe)
            for i in sorted(indices, reverse=True):
                del liste_des_joueurs[i]
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid indexes.")
    sauvegarder_equipes(equipes)
    return equipes

"-----------------------------------------------------------------------------"

def supprimer_fichier(fichier): #Supprime un fichier s'il existe.
    if os.path.exists(fichier):
        os.remove(fichier)

"-----------------------------------------------------------------------------"

def interface_creation_equipe(liste_joueurs):
    """
    Fonction pour créer une interface Tkinter permettant de créer et dissoudre des équipes.
    :param liste_joueurs: list -> Une liste de joueurs sous la forme [['ID1', 'Nom1'], ['ID2', 'Nom2'], ...]
    :return: list -> Une liste des équipes créées sous la forme [[ID1, ID2], [ID3, ID4], ...]
    """
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

"-----------------------------------------------------------------------------"
"-----------------------------------------------------------------------------"
"-----------------------------------------------------------------------------"
print("")

# Recherche des fichiers à analyser
liste_fichiers_partie=(lister_fichiers_repertoire(".txt","SPC_"))

if liste_fichiers_partie==[]:
    print("No round were found, stopping the code...")
    sys.exit()
    
print("Calculating data from the following files :")
print(liste_fichiers_partie)
print("")

# Creation du dictionnaire
dictionnaire_ID=trouver_id(liste_fichiers_partie)


if teams:
    # Créer une liste des joueurs avec leurs ID et noms
    liste_des_joueurs = [[keys, trouver_nom(keys)] for keys in dictionnaire_ID]
    #print(liste_des_joueurs)

    # Chargement des équipes existantes
    teams_presentes = charger_equipes()
    #print(teams_presentes)


    if teams_presentes is None:
        print("No team found. Creating teams...")
        teams_presentes = interface_creation_equipe(liste_des_joueurs)

    else:
        print("Teams loaded from file:")
        for i, equipe in enumerate(teams_presentes):
            noms_joueurs = [trouver_nom(joueur_id) for joueur_id in equipe]
            print(f"Team {i + 1}: {equipe} ({', '.join(noms_joueurs)})")

    print("")

# Mise à jour du dictionnaire des parties
for fichier_de_manche in liste_fichiers_partie :
    dictionnaire_ID=maj_dictionnaire(dictionnaire_ID,fichier_round_en_liste(fichier_de_manche))

# Impression du classement
print("Creating leaderboard...")
classement=tri_du_classement(dictionnaire_finale(dictionnaire_ID))

# Export des fichiers textes si teams
if teams:
    print("Exporting files...")
    classement_equipe=creation_classement_team(classement, teams_presentes)
    exporter_top(classement_equipe, 'SPC_top_players.txt',nombre_de_joueurs_a_exporter)
    exporter_classement_partiel(classement_equipe, 'SPC_classement_partiel.txt')
    exporter_classement_en_ligne(classement_equipe, 'SPC_classement_en_ligne.txt')
    supprimer_fichier('SPC_classement_complet.txt') # Classement complet pour les teams pas encore dispo
    exporter_un_joueur(classement_equipe, 'SPC_top1.txt',1)
    exporter_un_joueur(classement_equipe, 'SPC_top2.txt',2)
    exporter_un_joueur(classement_equipe, 'SPC_top3.txt',3)


# Export des fichiers textes si solo
if not teams:
    print("Exporting files...")
    exporter_top(classement, 'SPC_top_players.txt',nombre_de_joueurs_a_exporter)
    exporter_classement_partiel(classement, 'SPC_classement_partiel.txt')
    exporter_classement_en_ligne(classement, 'SPC_classement_en_ligne.txt')
    exporter_classement_complet(classement, dictionnaire_ID, 'SPC_classement_complet.txt')
    exporter_un_joueur(classement, 'SPC_top1.txt',1)
    exporter_un_joueur(classement, 'SPC_top2.txt',2)
    exporter_un_joueur(classement, 'SPC_top3.txt',3)


print("Generating graph...")
print("")

if teams:
    exporter_graph(classement_equipe)
else:
    exporter_graph(classement)
    exporter_graph_placement_moyen(dictionnaire_ID)



print("")
print("Done !")
print("")