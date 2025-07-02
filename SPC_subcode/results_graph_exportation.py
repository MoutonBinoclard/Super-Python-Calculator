import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from datetime import datetime
import os

def generate_gradient_colors(colors, num_colors):
    """
    Generate a gradient of colors interpolated between the given list of colors.

    Args:
        colors (list): List of color hex strings (e.g., ['#FF0000', '#00FF00']).
        num_colors (int): Number of colors to generate in the gradient.

    Returns:
        list: List of color hex strings representing the gradient.
    """
    # Convert hex colors to RGB
    rgb_colors = [to_rgb(color) for color in colors]

    # Create an array of values to interpolate between the colors
    t = np.linspace(0, len(rgb_colors) - 1, num_colors)

    # Linearly interpolate between the colors
    gradient = []
    for i in t:
        idx_low = int(np.floor(i))  # Lower index
        idx_high = min(idx_low + 1, len(rgb_colors) - 1)  # Upper index
        ratio = i - idx_low  # Ratio for interpolation

        # Interpolate between the two colors
        r = rgb_colors[idx_low][0] + (rgb_colors[idx_high][0] - rgb_colors[idx_low][0]) * ratio
        g = rgb_colors[idx_low][1] + (rgb_colors[idx_high][1] - rgb_colors[idx_low][1]) * ratio
        b = rgb_colors[idx_low][2] + (rgb_colors[idx_high][2] - rgb_colors[idx_low][2]) * ratio

        # Clip RGB values between 0 and 1
        r = max(0, min(1, r))
        g = max(0, min(1, g))
        b = max(0, min(1, b))

        # Convert the RGB color to hex and add to the list
        gradient.append(to_hex((r, g, b)))

    return gradient

def export_leaderboard_graph(rankings, tournament_name, color_scheme, show_logo, logo_path, logo_zoom, show_date, has_bonus):
    """
    Export a stacked bar chart representing the leaderboard scores per player.

    Args:
        rankings (dict): Dictionary with player IDs as keys and values as [player_name, total_score, rounds].
                         rounds is a list of [round_score, ...] for each round.
        tournament_name (str): Title of the tournament to display.
        color_scheme (dict): Dictionary of color settings for the plot.
        show_logo (bool): Whether to display a logo on the plot.
        logo_path (str): Path to the logo image file.
        logo_zoom (float): Zoom factor for the logo.
        show_date (bool): Whether to display the current date on the plot.
        has_bonus (bool): Whether the last round is a bonus round (affects legend label).

    Returns:
        None. Saves the plot as "SPC_exports/graph_leaderboard.png".
    """
    # Determine the maximum score for y-axis scaling
    max_score = max([data[2] for data in rankings.values()]) if rankings else 0

    # Determine the number of rounds (from the first entry)
    num_rounds = max([len(data[3]) for data in rankings.values()]) if rankings else 0

    # Generate gradient colors for the bars
    bar_colors = generate_gradient_colors(color_scheme["gradient_colors"], num_rounds)

    plt.figure(figsize=(12, 6), facecolor=color_scheme["background_color"])
    ax = plt.gca()
    ax.set_facecolor(color_scheme["background_color"])
    legend_handles = []
    x_labels = []

    for i, (player_id, data) in enumerate(rankings.items()):
        total_score = data[2]
        rounds = data[3]  # List of rounds: [[round_score, ...], ...]

        unique_label = player_id
        x_labels.append(player_id)

        bottom = 0
        for j, round_info in enumerate(rounds):
            score = round_info[0]
            bar = plt.bar(unique_label, score, bottom=bottom, color=bar_colors[j % len(bar_colors)])
            bottom += score
            if i == 0:
                legend_handles.append(bar[0])

        plt.text(unique_label, total_score + 0.03 * max_score, f"{total_score:.2f}", ha='center', va='bottom',
                 color=color_scheme["points_color"], fontsize=8, rotation=90)

    y_ticks = ax.get_yticks()
    for y in y_ticks:
        ax.axhline(y, color=color_scheme["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)

    ax.tick_params(axis='x', which='both', colors=color_scheme["x_ticks_color"])
    ax.xaxis.label.set_color(color_scheme["x_label_color"])
    ax.tick_params(axis='y', which='both', colors=color_scheme["y_ticks_color"])
    ax.yaxis.label.set_color(color_scheme["y_label_color"])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(color_scheme["y_axis_color"])
    ax.spines['bottom'].set_color(color_scheme["x_axis_color"])

    plt.xticks(rotation=45, ha='right', fontsize=8, color=color_scheme["x_label_color"])
    plt.yticks(color=color_scheme["y_label_color"])

    legend_labels = [f"Round {i+1}" for i in range(num_rounds)]
    if has_bonus and legend_labels:
        legend_labels[-1] = "Bonus"
    legend = plt.legend(legend_handles, legend_labels, loc='upper right', title_fontsize='small', fontsize='x-small',
                        handleheight=0.8, handlelength=1, labelspacing=0.3, facecolor=color_scheme["background_color"],
                        edgecolor=color_scheme["legend_border_color"], labelcolor=color_scheme["legend_text_color"])

    updated_labels = [rankings[player_id][1] for player_id in x_labels]
    ax.set_xticklabels(updated_labels)
    ax.set_xlim(-1, len(x_labels) +0)

    plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)

    plt.title(tournament_name, fontdict={'color': color_scheme["title_color"], 'fontsize': 16, 'weight': 'bold'}, pad=20)

    if show_logo:
        logo_image = plt.imread(logo_path)
        ax = plt.gca()
        image_box = OffsetImage(logo_image, zoom=logo_zoom)
        annotation_box = AnnotationBbox(image_box, (0.5, 1.065), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if show_date:
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top',
                fontdict={'color': color_scheme["date_color"], 'fontsize': 8})

    plt.savefig(os.path.join("SPC_exports", "graph_leaderboard.png"), dpi=600, facecolor=color_scheme["background_color"])


def exporter_graph_placement_moyen(classement, nom_tr, cs, lg, lg_path, zoom, dt, bonus): 
    
    # Préparer les données pour le boxplot
    data = []
    labels = []
    
    for keys in classement:
        nom_joueur = classement[keys][1]
        classement_manche=[]
        for manche in classement[keys][3]:
            if manche[1] > 0 : classement_manche.append(manche[1])
        data.append(classement_manche)
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


    #for i in range(1,4):
    #    ax.axhline(i, color=cs["horizontal_lines_color"], linestyle=(0,(1,1)), linewidth=0.5, zorder=0)  # Ligne top 1

    ax.tick_params(axis='x', which='both', colors=cs["x_ticks_color"])  # Couleur des ticks de l'axe X
    ax.xaxis.label.set_color(cs["x_label_color"])  # Couleur du label de l'axe X
    ax.tick_params(axis='y', which='both', colors=cs["y_ticks_color"])  # Couleur des ticks de l'axe Y
    ax.yaxis.label.set_color(cs["y_label_color"])  # Couleur du label de l'axe Y

    # Inverser l'axe des ordonnées pour que le meilleur placement soit en haut
    ax.invert_yaxis()
    
    # Définir les ticks Y sur les entiers impairs uniquement
    placement_max = max([max(placements) for placements in data]) if data else 0
    ticks = list(range(1, int(placement_max) + 2, 2))  # 1, 3, 5, ...
    ax.set_yticks(ticks)

    #y_ticks = ax.get_yticks()  # Récupérer les positions des graduations sur l'axe Y
    for y in ticks:
        ax.axhline(y, color=cs["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)

    # Fixer la limite supérieure de l'axe Y à 0.5 et ajuster la limite inférieure
    placement_min = max([max(placements) for placements in data]) if data else 0
    ax.set_ylim(bottom=placement_min + 1, top=0.5)

    # Rotation des noms des joueurs pour une meilleure lisibilité avec une taille de police réduite
    plt.xticks(rotation=45, ha='right', fontsize=8, color=cs["x_label_color"])  # Correction de la couleur des ticks X
    plt.yticks(color=cs["y_label_color"])  # Correction de la couleur des ticks Y
    ax.set_xlim(0, len(labels) + 1)

    # Ajuster les bordures et les axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(cs["y_axis_color"])
    ax.spines['bottom'].set_color(cs["x_axis_color"])

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
    plt.savefig(os.path.join("SPC_exports", "graph_placement.png"), dpi=600, facecolor=cs["background_color"])
