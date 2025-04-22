print("")
print("---------------------")
print("")


# Super Python Calculator 
# By Mouton Binoclard
# Also known as a calculator for SAR tournaments

# Version 5

# Automatically synced with github repository now :D

# ----------------------------------------------------------------------------

# The organization of functions and code was done by Mouton Binoclard.
# Most of the annotations and the matplotlib section were created by Deepseek AI (in French, of course, lol).

# ----------------------------------------------------------------------------

print("Launching SPC...")
print("")

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

from SPC_subcode.initialisation import trouver_id, lister_fichiers_repertoire
from SPC_subcode.round_en_liste import fichier_round_en_liste
from SPC_subcode.mise_a_jour_dico import maj_dictionnaire
from SPC_subcode.statistiques import ajouter_stats_globales, calculer_points_totaux, calculer_points_totaux_et_round
from SPC_subcode.exportation_des_resultats import exportation
from SPC_subcode.gestion_equipes import mise_en_place_teams, creation_classement_2

# Import de warning pour ignorer les avertissements de matplotlib
import warnings
warnings.simplefilter("ignore", UserWarning)

print("Libraries successfully loaded.")
print("")

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

print("Teams mode is set to", teams)
print("")

# ----------------------------------------------------------------------------

'MODIFY THE SCORING SYSTEM'

# To adjust the scoring system, update the function definitions in the Python preset file.
# When team mode is active, kills represent the total kills achieved by the player's team.

# Type the name of the file containing the scoring system you want to use:
# (The file must be in the SPC_scoring_presets folder.)

from SPC_scoring.spi import kill_points, placement_points, masterkill
import inspect

# It must be something like SPC_scoring_presets.name_of_the_file_without_the_extension

print("Scoring system loaded from file:", inspect.getfile(kill_points))
print("")

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

print("Banned players:", ID_banni_du_tournoi)
print("")

# ----------------------------------------------------------------------------

'CHANGE THE NAME ON THE GRAPH'

# Here, you can change the tournament name that will appear on the graph.
nom_du_tournoi = "SPC V5"

# Here you can specify if you want to add a logotype to the graph
logo=True

# This is where you can change the path to the logo file:
logo_path = "SPC_logo/spc_v5.png"

# Size of the logo
zoom_logo=0.20

# If you want the date to show up on the graph, set the following value to True:
date=True

print("Tournament name:", nom_du_tournoi)

print("Logo is set to", logo)
if logo :
    print("Logo path is:", logo_path)
    print("Logo zoom is set to", zoom_logo)

print("Date is set to", date)

print("")

# ----------------------------------------------------------------------------

'CHANGE THE STYLE'

# You can change the colors of the graph by modifying the values in the file "SPC_colors_config.json".
color_scheme = "SPC_color_schemes/v5.json"

# If you want to use a custom font, set the following value to True:
add_custom_fonts = True

# Put the font path here:
font_path = "SPC_fonts/FiraCode.ttf"

print("Color scheme loaded from file", color_scheme)
print("Custom font is set to", add_custom_fonts)
if add_custom_fonts:
    print("Font path is:", font_path)

print("")
print("---------------------")
print("")
# ----------------------------------------------------------------------------

# If you have any issues, feature requests, or you found a bug, feel free to contact me on Discord :D










# Start of the code

print("Loading fonts...")

if add_custom_fonts:
    # Charger la police personnalisée
    custom_font = fm.FontProperties(fname=font_path)
    # Appliquer la police globalement
    rcParams['font.family'] = custom_font.get_name()

else:
    # Réinitialiser la police à la valeur par défaut de Matplotlib
    rcParams['font.family'] = 'DejaVu Sans'  # Police par défaut de Matplotlib

# ----------------------------------------------------------------------------

print("Loading color scheme...")
print("")

def charger_couleurs(fichier=color_scheme): # Charger les couleurs depuis le fichier JSON
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)

# Charger les couleurs
couleurs = charger_couleurs()

# ----------------------------------------------------------------------------

print("Loading files...")

liste_fichiers_partie = lister_fichiers_repertoire(".txt", "SPC_") # On liste les fichiers de la partie
classement = trouver_id(liste_fichiers_partie) # On crée le dictionnaire avec les ID et les noms de joueurs

for fichier_de_manche in liste_fichiers_partie :
    classement=maj_dictionnaire(classement,fichier_round_en_liste(fichier_de_manche, ID_banni_du_tournoi))

print("Analyzing the following rounds:")
print(liste_fichiers_partie)
print("")
# ----------------------------------------------------------------------------


print("Calculating points...")

# Calcul points par manche

for joueur in classement:
    for manche in classement[joueur][3]:
        if not teams:
            pt_placement = placement_points(manche[1][0], manche[1][1], manche[1][2])
            pt_kill = kill_points(manche[1][0], manche[1][1], manche[1][2])
            pt_masterkill = masterkill(manche[1][3], manche[1][1], manche[1][2])
            pt_total = pt_placement + pt_kill + pt_masterkill

        if teams:
            pt_placement = placement_points(manche[1][0], manche[1][5], manche[1][2])
            pt_kill = kill_points(manche[1][0], manche[1][5], manche[1][2])
            pt_masterkill = masterkill(manche[1][6], manche[1][5], manche[1][2])
            pt_total = pt_placement + pt_kill + pt_masterkill

        manche[0] = pt_total

# ----------------------------------------------------------------------------


classement = calculer_points_totaux(classement)
classement = ajouter_stats_globales(classement)

print("Calulation done.")
print("")
print("---------------------")
print("")

teams_presentes = mise_en_place_teams(classement, teams, liste_fichiers_partie)


classement_2 = creation_classement_2(classement, teams_presentes)
classement_2 = calculer_points_totaux_et_round(classement_2)
classement_2 = dict(sorted(classement_2.items(), key=lambda item: item[1][1], reverse=True))

exportation(classement_2, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date)
print("DONE !")

# Forme du classement :
# {'ID1':[Nom du joueur, score final, [nb_partie_joué, nb_victoire, nb_kill, kda], [[score manche1, [placement, kill, nb_joueur, masterkill, team, team_kill]], [score manche2, ...}

# Forme du classement_2 :
# {'ID_combine':[Nom des joueurs, score final, [[score manche 1, placement manche 1], ...], [[classement[ID1]], [classement [ID2]], ...]