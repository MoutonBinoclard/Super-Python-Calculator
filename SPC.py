# Super Python Calculator 
# By Mouton Binoclard
# Also known as a calculator for SAR tournaments

# Version 5

# ----------------------------------------------------------------------------

print("Launching SPC...")
print("")

# IMPORTANT:
# Some libraries aren't shown here since they're only used in some sub-codes.
# If you have any issues, just install the missing libraries using pip.
# For example, if you get an error about "tkinter", just install it with pip:
# pip install tkinter

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

from SPC_scoring.pvp_arena_solo import kill_points, placement_points, masterkill

# ----------------------------------------------------------------------------

'BAN PLAYERS'

ID_banni_du_tournoi = []

# ----------------------------------------------------------------------------

'LOGO, NAME, DATE and FONT'

nom_du_tournoi = "PVP Arena Solo"

logo=True
logo_path = "SPC_logo/pvp_arena_solo.png"
zoom_logo=0.16

date=True

add_custom_fonts = True
font_path = "SPC_fonts/FiraCode.ttf"

# ----------------------------------------------------------------------------

'COLOR SCHEME'

color_scheme = "SPC_color_schemes/pvp_arena_solo.json"

# ----------------------------------------------------------------------------

# If you have any issues, feature requests, or you found a bug, feel free to contact me on Discord :D






#import inspect
#print("Scoring system loaded from file:", inspect.getfile(kill_points))
#print("")


# Start of the code

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