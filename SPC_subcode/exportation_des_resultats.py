from SPC_subcode.exportation_classement import exporter_classement_complet, exporter_classement_partiel
from SPC_subcode.exportation_graphiques import exporter_graph, exporter_graph_placement_moyen
from SPC_subcode.gestion_du_dossier import creer_dossier_export

# ----------------------------------------------------------------------------

def exportation(classement, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date):

    print("leaderboard exportation in progress...")
    creer_dossier_export()
    #exporter_classement_partiel(classement, "classement_partiel.txt")
    exporter_classement_complet(classement, "classement_complet.txt")
    print("leaderbaord exportation done")
    print("")    
    
    print("graphs exportation in progress...")
    exporter_graph(classement, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date)
    #exporter_graph_placement_moyen(classement, nom_du_tournoi, couleurs, logo, logo_path, zoom_logo, date)
    print("graphs exportation done")
    print("")
    

