from SPC_subcode.interface_creation_teams import interface_creation_equipe, charger_equipes
from SPC_subcode.recherche_nom import trouver_nom


def mise_en_place_teams(classement, teams, liste_fichiers_partie):
    # Standardise la mise en forme du classement, en equipe ou non
    if teams:

        liste_ID_joueurs = []
        for joueur in classement:
            liste_ID_joueurs.append([joueur, classement[joueur][0]])

        # Chargement des équipes existantes
        teams_presentes = charger_equipes()
        #print(teams_presentes)

        if teams_presentes is None:
            print("No team found. Creating teams...")
            teams_presentes = interface_creation_equipe(liste_ID_joueurs)

        else:
            print("Teams loaded from file:")
            for i, equipe in enumerate(teams_presentes):
                noms_joueurs = [trouver_nom(joueur_id, liste_fichiers_partie) for joueur_id in equipe]
                #print(f"Team {i + 1}: {equipe} ({', '.join(noms_joueurs)})")
                print(f"({', '.join(noms_joueurs)})")
        print("")
        print("---------------------")
        print("")

    elif not teams:
        teams_presentes = []
        for keys in classement:
            # On cherche le nom du joueur
            teams_presentes.append([keys])
    
    return teams_presentes

# ----------------------------------------------------------------------------

def creation_classement_2(classement, teams_presentes):
    classement_2 = {}
    for team in teams_presentes:
        id_combine = ''.join(str(id) for id in team)
        nom_des_joueurs = ", ".join(classement[id][0] for id in team)
        classement_2[id_combine] = [nom_des_joueurs, 0, [], []]
        for id in team :
            classement_2[id_combine][3].append(classement[id])
    return classement_2