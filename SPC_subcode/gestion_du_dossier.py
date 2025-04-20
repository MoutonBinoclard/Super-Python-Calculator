import os

# ----------------------------------------------------------------------------

def creer_dossier_export():  # Crée le dossier SPC_exports s'il n'existe pas
    if not os.path.exists("SPC_exports"):
        os.makedirs("SPC_exports")

# ----------------------------------------------------------------------------

def supprimer_fichier(fichier): #Supprime un fichier s'il existe.
    if os.path.exists(fichier):
        os.remove(fichier)

