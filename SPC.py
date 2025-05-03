# Super Python Calculator 
# By Mouton Binoclard
# Also known as a calculator for SAR tournaments

# Version 5

# ----------------------------------------------------------------------------

from matplotlib import rcParams
from matplotlib import font_manager as fm
import json


from SPC_subcode.initialisation import trouver_id, lister_fichiers_repertoire
from SPC_subcode.round_en_liste import fichier_round_en_liste
from SPC_subcode.mise_a_jour_dico import maj_dictionnaire
from SPC_subcode.statistiques import ajouter_stats_globales, calculer_points_totaux, calculer_points_totaux_et_round
from SPC_subcode.exportation_des_resultats import exportation
from SPC_subcode.gestion_equipes import mise_en_place_teams, creation_classement_2

import warnings
warnings.simplefilter("ignore", UserWarning)


# ----------------------------------------------------------------------------

'SETTINGS'

# If you have any questions, feature requests, or you found a bug, feel free to contact me on Discord :D
# However, check the wiki first, it might be there already : https://github.com/MoutonBinoclard/Super-Python-Calculator/wiki

# ----------------------------------------------------------------------------

'ACTIVATE TEAMS'

teams = False

# ----------------------------------------------------------------------------

'MODIFY THE SCORING SYSTEM'

from SPC_scoring.spi import kill_points, placement_points, masterkill

# ----------------------------------------------------------------------------

'BAN PLAYERS'

ID_banni_du_tournoi = []

# ----------------------------------------------------------------------------

'LOGO, NAME, DATE and FONT'

nom_du_tournoi = "La Coupe du Pont du 1er Mai (Même si elle a lieu le 3 Mai)"

logo=False
logo_path = "SPC_logo/pvp_arena_solo.png"
zoom_logo=0.16

date=True

add_custom_fonts = True
custom_font = fm.FontProperties(fname=r"C:\Windows\Fonts\DINEngschriftStd.otf")

# ----------------------------------------------------------------------------

'COLOR SCHEME'

color_scheme = "SPC_color_schemes/blueprint.json"

# ----------------------------------------------------------------------------





# Start of the code

if add_custom_fonts:

    font_name=custom_font.get_name()
    rcParams['font.family'] = [font_name]

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