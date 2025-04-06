# Super Python Calculator 
# By Mouton Binoclard
# Also known as a calculator for SAR tournaments

# Version 4.2

# Automatocally synced with github repository now :D

# ----------------------------------------------------------------------------

# The organization of functions and code was done by Mouton Binoclard.
# Most of the annotations and the matplotlib section were created by Deepseek AI (in French, of course, lol).

# ----------------------------------------------------------------------------

# IMPORTANT:
# Some libraries aren't shown here since they're only used in some sub-codes.
# If you have any issues, just install the missing libraries using pip.
# For example, if you get an error about "tkinter", just install it with pip:
# pip install tkinter

import os
import sys

from matplotlib import rcParams
from matplotlib import font_manager as fm

import json

# The next lines import functions from the sub-codes of the SPC folder, you don't need to download them.

# Import de l'initialisation du code (Recherche des fichiers et creation du dictionnaire des ids)
from SPC_sub_codes.initialisation_code import lister_fichiers_repertoire, trouver_id

# Import de l'interface graphique pour la création d'équipes
from SPC_sub_codes.team_ui import interface_creation_equipe, sauvegarder_equipes

# Import de la recherche d'un pseudo depuis un nom
from SPC_sub_codes.id_vers_nom import trouver_nom

# Import de la gestion du dossier du code (creer un dossier, supprimer un fichier)
from SPC_sub_codes.gestion_du_dossier import creer_dossier_export, supprimer_fichier

# Import des fonction d'exportation de classement
from SPC_sub_codes.leaderboards_exportation import exporter_top, exporter_un_joueur, exporter_classement_partiel, exporter_classement_en_ligne, exporter_classement_complet

# Import des fonctions d'exportation et de création de graphiques
from SPC_sub_codes.graphics_exportation import exporter_graph, exporter_graph_placement_moyen


# Import de warning pour ignorer les avertissements de matplotlib
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
nom_du_tournoi = "Scrims on Double Trouble server using SPI"

# Here you can specify if you want to add a logotype to the graph
logo=False

# This is where you can change the path to the logo file:
logo_path = "SPC_logo/SPC_lg_simple_scrims.png"

# Size of the logo
zoom_logo=0.15

# If you want the date to show up on the graph, set the following value to True:
date=True

# ----------------------------------------------------------------------------

'CHANGE THE STYLE'

# You can change the colors of the graph by modifying the values in the file "SPC_colors_config.json".
color_scheme = "SPC_color_schemes/SPC_cs_v5.json"

# If you want to use a custom font, set the following value to True:
add_custom_fonts = True

# Put the font path here:
font_path = "SPC_fonts/Rubik.ttf"

# ----------------------------------------------------------------------------

# If you have any issues, feature requests, or you found a bug, feel free to contact me on Discord :D








# Start of the code


# ----------------------------------------------------------------------------

if add_custom_fonts:
    # Charger la police personnalisée
    custom_font = fm.FontProperties(fname=font_path)
    # Appliquer la police globalement
    rcParams['font.family'] = custom_font.get_name()

else:
    # Réinitialiser la police à la valeur par défaut de Matplotlib
    rcParams['font.family'] = 'DejaVu Sans'  # Police par défaut de Matplotlib

# ----------------------------------------------------------------------------

def charger_couleurs(fichier=color_scheme): # Charger les couleurs depuis le fichier JSON
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

# Charger les couleurs
couleurs = charger_couleurs()

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

def dictionnaire_finale(dictionnaire_des_infos_des_rounds): # Création du dicionnaire complet, (correspond au dict classement)
    # dictionnaire_des_infos_des_rounds -> dict : {'ID1' :[[placement, kills, nombre joueurs, masterkill ?],[,,,],...], ...}

    # Dictionnaire final à retourner
    dico_final = {}
    
    # Parcourir chaque joueur dans le dictionnaire des rounds
    for playfab_id_joueur, manches in dictionnaire_des_infos_des_rounds.items():
        # Trouver le nom du joueur
        nom_joueur = trouver_nom(playfab_id_joueur, liste_fichiers_partie)
        
        # Calculer les scores des manches
        scores_manches = score_final(manches)
        
        # Calculer le score total (somme des scores des manches)
        score_total = sum(scores_manches)
        
        # Ajouter les informations au dictionnaire final
        dico_final[playfab_id_joueur] = [nom_joueur, score_total, scores_manches]

    return dico_final # dict -> {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

# ----------------------------------------------------------------------------

def tri_du_classement(dictionnaire_non_classé): # Tri un dictionnaire dans l'ordre décroissant des points
    # dictionnaire_non_classé -> dict : {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

    # Trier le dictionnaire en fonction du score final (index 1 de la liste associée à chaque clé)
    classement_trié = dict(sorted(dictionnaire_non_classé.items(), key=lambda item: item[1][1], reverse=True))
    
    return classement_trié # dict -> {'ID1':[Nom du joueur, score final, [score manche 1, ...]], ...}

# ----------------------------------------------------------------------------                

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

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

def charger_equipes(fichier="SPC___teams.txt"): # Chargement du fichier équipes du repertoire
    """Charge les équipes depuis un fichier texte s'il existe."""
    if os.path.exists(fichier):
        equipes = []
        with open(fichier, "r", encoding="utf-8") as f:
            for line in f:
                equipes.append(line.strip().split(" "))
        return equipes
    return None

# ----------------------------------------------------------------------------

creer_dossier_export()

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
    liste_des_joueurs = [[keys, trouver_nom(keys, liste_fichiers_partie)] for keys in dictionnaire_ID]
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
            noms_joueurs = [trouver_nom(joueur_id, liste_fichiers_partie) for joueur_id in equipe]
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
    exporter_graph(classement_equipe, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date, liste_fichiers_partie)
else:
    exporter_graph(classement, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date, liste_fichiers_partie)
    exporter_graph_placement_moyen(dictionnaire_ID, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date, liste_fichiers_partie)

print("")
print("Done !")
print("")