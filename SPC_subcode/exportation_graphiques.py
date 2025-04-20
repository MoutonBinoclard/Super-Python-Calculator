import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import numpy as np

from datetime import datetime

import os

# ----------------------------------------------------------------------------

def generer_degrade_couleurs(couleurs, nombre_de_couleurs):

    # Convertir les couleurs hexadécimales en RGB
    rgb_couleurs = [to_rgb(couleur) for couleur in couleurs]

    # Créer un tableau de valeurs pour interpoler entre les couleurs
    t = np.linspace(0, len(rgb_couleurs) - 1, nombre_de_couleurs)

    # Interpoler linéairement entre les couleurs
    degrade = []
    for i in t:
        idx_inf = int(np.floor(i))  # Index inférieur
        idx_sup = min(idx_inf + 1, len(rgb_couleurs) - 1)  # Index supérieur
        ratio = i - idx_inf  # Ratio pour l'interpolation

        # Interpolation entre les deux couleurs
        r = rgb_couleurs[idx_inf][0] + (rgb_couleurs[idx_sup][0] - rgb_couleurs[idx_inf][0]) * ratio
        g = rgb_couleurs[idx_inf][1] + (rgb_couleurs[idx_sup][1] - rgb_couleurs[idx_inf][1]) * ratio
        b = rgb_couleurs[idx_inf][2] + (rgb_couleurs[idx_sup][2] - rgb_couleurs[idx_inf][2]) * ratio

        # Clipper les valeurs RGB entre 0 et 1
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))

        # Convertir la couleur RGB en hexadécimal et l'ajouter à la liste
        degrade.append(to_hex((r, g, b)))

    return degrade

# ----------------------------------------------------------------------------

def exporter_graph(classement, nom_tr, cs, lg, lg_path, zoom, dt):

    # Score max
    le_haut_du_graph = max([data[1] for data in classement.values()]) if classement else 0

    # Nombre de manches (on prend la première entrée pour déterminer le nombre de manches)
    nb_manches = max([len(data[2]) for data in classement.values()]) if classement else 0

    barres_couleurs = generer_degrade_couleurs(cs["gradient_colors"], nb_manches)

    plt.figure(figsize=(12, 6), facecolor=cs["background_color"])
    ax = plt.gca()
    ax.set_facecolor(cs["background_color"])
    legend_handles = []
    x_labels = []

    for i, (playfab_id, data) in enumerate(classement.items()):
        pseudo = data[0]
        score_final = data[1]
        manches = data[2]  # Liste des manches : [[score manche, [infos...]], ...]

        unique_pseudo = playfab_id
        x_labels.append(playfab_id)

        bottom = 0
        for j, manche in enumerate(manches):
            score = manche[0]
            bar = plt.bar(unique_pseudo, score, bottom=bottom, color=barres_couleurs[j % len(barres_couleurs)])
            bottom += score
            if i == 0:
                legend_handles.append(bar[0])

        plt.text(unique_pseudo, score_final + 0.03 * le_haut_du_graph, f"{score_final:.2f}", ha='center', va='bottom', color=cs["points_color"], fontsize=8, rotation=90)

    y_ticks = ax.get_yticks()
    for y in y_ticks:
        ax.axhline(y, color=cs["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)

    ax.tick_params(axis='x', which='both', colors=cs["x_ticks_color"])
    ax.xaxis.label.set_color(cs["x_label_color"])
    ax.tick_params(axis='y', which='both', colors=cs["y_ticks_color"])
    ax.yaxis.label.set_color(cs["y_label_color"])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(cs["x_axis_color"])
    ax.spines['bottom'].set_color(cs["y_axis_color"])

    plt.xticks(rotation=45, ha='right', fontsize=8, color=cs["x_label_color"])
    plt.yticks(color=cs["y_label_color"])

    labels = [f"Manche {i+1}" for i in range(nb_manches)]
    legend = plt.legend(legend_handles, labels, loc='upper right', title_fontsize='small', fontsize='x-small',
                        handleheight=0.8, handlelength=1, labelspacing=0.3, facecolor=cs["background_color"],
                        edgecolor=cs["legend_border_color"], labelcolor=cs["legend_text_color"])


    updated_labels = [classement[playfab_id][0] for playfab_id in x_labels]
    ax.set_xticklabels(updated_labels)

    plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(nom_tr, fontdict={'color': cs["title_color"], 'fontsize': 16, 'weight': 'bold'}, pad=20)

    if lg:
        logo_image = plt.imread(lg_path)
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom=zoom)
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if dt:
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top',
                fontdict={'color': cs["date_color"], 'fontsize': 8})

    plt.savefig(os.path.join("SPC_exports", "SPC_Graphic.png"), dpi=600, facecolor=cs["background_color"])

# ----------------------------------------------------------------------------

def exporter_graph_placement_moyen(classement, nom_tr, cs, lg, lg_path, zoom, dt): 

    # Préparer les données pour le boxplot
    data = []
    labels = []
    
    for joueur_id, joueur_data in classement.items():
        nom_joueur = joueur_data[0]
        manches = joueur_data[3]
        placements = [manche[1][0] for manche in manches if manche[0] > 0]  # Ignorer les placements 0 et -1
        if placements:
            data.append(placements)
            labels.append(nom_joueur)  # Utiliser le nom du joueur ou l'ID si le nom est introuvable

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

    #for i in range(1,4):
    #    ax.axhline(i, color=cs["horizontal_lines_color"], linestyle=(0,(1,1)), linewidth=0.5, zorder=0)  # Ligne top 1

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
        image_box = OffsetImage(logo_image, zoom=zoom)  # Ajuster le zoom pour auto-scaling
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
