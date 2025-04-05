import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import numpy as np

from datetime import datetime

import os

from SPC_sub_codes.id_vers_nom import trouver_nom

# ----------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------

def exporter_graph(classement, nom_tr, cs, lg, lg_path, zoom, dt, fichiers_base):
    """
    Génère et exporte un graphique en barres empilées à partir du classement fourni.
    :param classement: dict -> Le classement des joueurs ou des équipes.
    """
    # Score max
    le_haut_du_graph = next(iter(classement.values()))[1]

    barres_couleurs = generer_degrade_4_couleurs(cs["gradient_color_1"], cs["gradient_color_2"], cs["gradient_color_3"], cs["gradient_color_4"], cs["chosen_number"])  # Augmenter le nombre de couleurs par trois
    # Créer un graphique en barres empilées avec un style personnalisé
    plt.figure(figsize=(12, 6), facecolor=cs["background_color"])  # Augmenter légèrement la largeur (de 10 à 12)
    ax = plt.gca()  # Obtenir l'axe actuel
    ax.set_facecolor(cs["background_color"])  # Fond pour l'arrière-plan du graphique
    # Pour stocker les handles de la légende
    legend_handles = []

    # Stocker les labels pour mise à jour après
    x_labels = []

    # Pour chaque joueur, empiler les scores de chaque manche
    for i, (playfab_id, data) in enumerate(classement.items()):
        pseudo, score_final, scores_manches = data

        # Utiliser uniquement le PlayFab ID comme label pour le moment
        unique_pseudo = playfab_id
        x_labels.append(playfab_id)  # Ajouter l'ID à la liste des labels

        bottom = 0  # Commencer à empiler à partir de 0
        for j, score in enumerate(scores_manches):
            bar = plt.bar(unique_pseudo, score, bottom=bottom, color=barres_couleurs[j % len(barres_couleurs)])
            bottom += score  # Mettre à jour la position de départ pour la prochaine manche

            # Ajouter un handle pour la légende (une seule fois par manche)
            if i == 0:  # On ne le fait que pour le premier joueur pour éviter les doublons
                legend_handles.append(bar[0])

        # Ajouter le score total en haut de la barre, en vertical et empiétant sur les colonnes
        plt.text(unique_pseudo, score_final + 0.03 * le_haut_du_graph, f"{score_final:.2f}", ha='center', va='bottom', color=cs["points_color"], fontsize=10, rotation=90)

    # Utiliser les graduations automatiques de Matplotlib pour les lignes horizontales
    y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in y_ticks:
        ax.axhline(y, color=cs["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)  # Ajouter une ligne horizontale à chaque graduation

    # Changer la couleur des ticks (graduations) et des noms des axes
    ax.tick_params(axis='x', which='both', colors=cs["x_ticks_color"])  # Couleur des ticks de l'axe X
    ax.xaxis.label.set_color(cs["x_label_color"])  # Couleur du label de l'axe X
    ax.tick_params(axis='y', which='both', colors=cs["y_ticks_color"])  # Couleur des ticks de l'axe Y
    ax.yaxis.label.set_color(cs["y_label_color"])  # Couleur du label de l'axe Y

    # Ajuster les bordures et les axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(cs["x_axis_color"])
    ax.spines['bottom'].set_color(cs["y_axis_color"])

    # Changer la couleur des labels des axes
    plt.xticks(rotation=45, ha='right', fontsize=8, color=cs["x_label_color"])
    plt.yticks(color=cs["y_label_color"])

    # Ajouter une légende
    labels = [f"Round {i+1}" for i in range(len(barres_couleurs))]  # Créer les labels pour chaque manche
    legend = plt.legend(legend_handles, labels, title_fontsize='large', fontsize='medium', facecolor=cs["background_color"], edgecolor=cs["legend_border_color"], labelcolor=cs["legend_text_color"])

    # Mettre à jour les labels des colonnes avec les vrais pseudos
    updated_labels = [trouver_nom(playfab_id, fichiers_base) for playfab_id in x_labels]
    ax.set_xticklabels(updated_labels)

    # Ajuster la mise en page
    plt.tight_layout()

    # Ajouter des marges à gauche et à droite pour plus de légèreté
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(nom_tr, fontdict={'color': cs["title_color"], 'fontsize': 16, 'weight': 'bold'}, pad=20)  # Gestion du titre

    if lg == True:

        # Charger le logo
        logo_image = plt.imread(lg_path)

        # Ajouter le logo à la place du titre
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom)  # Ajuster le zoom pour auto-scaling
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if dt == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', 
                fontdict={'color': cs["date_color"], 'fontsize': 8})

    # Enregistrer le graphique
    plt.savefig(os.path.join("SPC_exports", "SPC_Graphic.png"), dpi=600, facecolor=cs["background_color"])

# ----------------------------------------------------------------------------

def exporter_graph_placement_moyen(dict_ID, nom_tr, cs, lg, lg_path, zoom, dt, fichiers_base): 
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
            labels.append(trouver_nom(playfab_id, fichiers_base))  # Utiliser le nom du joueur ou l'ID si le nom est introuvable

    # Créer le graphique
    plt.figure(figsize=(12, 6), facecolor=cs["background_color"])
    ax = plt.gca()
    ax.set_facecolor(cs["background_color"])

    # Générer le boxplot
    box = plt.boxplot(data, patch_artist=True, tick_labels=labels, vert=True, showmeans=True)

    # Personnaliser les couleurs des boxplots
    for patch in box['boxes']:
        patch.set(facecolor=cs["boxes_inside_color"], edgecolor=cs["boxes_outside_color"])
    for whisker in box['whiskers']:
        whisker.set(color=cs["whiskers_color"])
    for cap in box['caps']:
        cap.set(color=cs["caps_color"])
    for median in box['medians']:
        median.set(color=cs["medians_color"], linewidth=1)  # Réduire l'épaisseur des médianes
        median.set_xdata([median.get_xdata()[0] - 0.15, median.get_xdata()[1] + 0.15])  # Étendre la médiane au-delà de la box
    for flier in box['fliers']:
        flier.set(marker='x', markerfacecolor=cs["fliers_color"], markeredgecolor=cs["fliers_color"], alpha=1)
    for mean in box['means']:
        mean.set(marker= "o", markerfacecolor="none", markeredgecolor=cs["mean_color"], alpha=1, markersize=5)

    # Utiliser les graduations automatiques de Matplotlib pour les lignes horizontales
    y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in y_ticks:
        ax.axhline(y, color=cs["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)  # Ajouter une ligne horizontale à chaque graduation

    for i in range(1,4):
        ax.axhline(i, color=cs["horizontal_lines_color"], linestyle=(0,(1,1)), linewidth=0.5, zorder=0)  # Ligne top 1

    ax.tick_params(axis='x', which='both', colors=cs["x_ticks_color"])  # Couleur des ticks de l'axe X
    ax.xaxis.label.set_color(cs["x_label_color"])  # Couleur du label de l'axe X
    ax.tick_params(axis='y', which='both', colors=cs["y_ticks_color"])  # Couleur des ticks de l'axe Y
    ax.yaxis.label.set_color(cs["y_label_color"])  # Couleur du label de l'axe Y

    # Inverser l'axe des ordonnées pour que le meilleur placement soit en haut
    ax.invert_yaxis()

    # Fixer la limite supérieure de l'axe Y à 0.5 et ajuster la limite inférieure
    placement_min = max([max(placements) for placements in data]) if data else 0
    ax.set_ylim(bottom=placement_min + 1, top=0.5)

    # Rotation des noms des joueurs pour une meilleure lisibilité avec une taille de police réduite
    plt.xticks(rotation=45, ha='right', fontsize=8, color=cs["x_label_color"])  # Correction de la couleur des ticks X
    plt.yticks(color=cs["y_label_color"])  # Correction de la couleur des ticks Y

    # Ajuster les bordures et les axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(cs["x_axis_color"])
    ax.spines['bottom'].set_color(cs["y_axis_color"])

    # Ajuster la mise en page
    plt.tight_layout()

    # Ajouter des marges à gauche et à droite pour plus de légèreté
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(nom_tr, fontdict={'color': cs["title_color"], 'fontsize': 16, 'weight': 'bold'}, pad=20)  # Gestion du titre

    if lg == True:

        # Charger le logo
        logo_image = plt.imread(lg_path)

        # Ajouter le logo au graphique
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom)  # Ajuster le zoom pour auto-scaling
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if dt == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', 
                fontdict={'color': cs["date_color"], 'fontsize': 8})

    # Enregistrer le graphique
    plt.savefig(os.path.join("SPC_exports", "SPC_Placement_Boxplot.png"), dpi=600, facecolor=cs["background_color"])
