import matplotlib.pyplot as plt
from datetime import datetime
import os
from matplotlib.colors import to_hex, to_rgb
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math

def generate_gradient_colors(colors, num_colors):
    # Convert hex colors to RGB
    rgb_colors = [to_rgb(color) for color in colors]

    # Handle edge case: only one color requested
    if num_colors <= 1:
        return [to_hex(rgb_colors[0])] if rgb_colors else []

    # Équivalent de np.linspace(start, end, num)
    t = [i * (len(rgb_colors) - 1) / (num_colors - 1) for i in range(num_colors)]

    # Linearly interpolate between the colors
    gradient = []
    for i in t:
        idx_low = math.floor(i)  # Lower index
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

        gradient.append(to_hex((r, g, b)))

    return gradient

def define_size_x_label(dict_fusion):
    number_columns = len(dict_fusion)
    max_player_team = 1
    for keys in dict_fusion :
        nb_players_in_team = len(dict_fusion[keys]['names'])
        if nb_players_in_team > max_player_team:
            max_player_team = nb_players_in_team
    
    if max_player_team == 1 :
        return 8
    
    if max_player_team == 2 and number_columns >= 20:
        return 5
    
    if max_player_team == 3 and number_columns < 13:
        return 5
    
    if max_player_team == 4 and number_columns >= 10:
        return 5
    
    else :
        return 8
    
    



def export_graph_leaderboard(dict_fusion, tournament_name, color_scheme, show_logo, logo_path, zoom_logo, show_date, graphs_pixel_density):
    """
    Exporte un graphique leaderboard à partir d'un dictionnaire fusionné.
    dict_fusion: {
        'id1 & id2': {
            'names': ['Nom joueur 1', 'Nom joueur 2', ...],
            'score': total_score,
            'rounds': [
                {'score': ..., 'placement': ..., ...},
                ...
            ]
        },
        ...
    }
    """
    # Récupérer le score maximal pour l'échelle Y
    max_score = max(team['score'] for team in dict_fusion.values()) if dict_fusion else 0

    # Nombre de manches
    num_rounds = len(next(iter(dict_fusion.values()))['rounds']) if dict_fusion else 0

    # Générer les couleurs du gradient pour chaque manche
    bar_colors = generate_gradient_colors(color_scheme["gradient_colors"], num_rounds)

    # Préparer le graphique
    plt.figure(figsize=(12, 6), facecolor=color_scheme["background_color"])
    ax = plt.gca()
    ax.set_facecolor(color_scheme["background_color"])

    legend_handles = []
    team_keys = list(dict_fusion.keys())

    # Affichage des barres empilées pour chaque équipe
    for team_idx, team_key in enumerate(team_keys):
        team_data = dict_fusion[team_key]
        team_name = team_data['names']
        total_score = team_data['score']
        rounds = team_data['rounds']

        bottom = 0
        for round_idx, round_info in enumerate(rounds):
            score = round_info['score']
            bar = plt.bar(team_idx, score, bottom=bottom, color=bar_colors[round_idx % len(bar_colors)])
            bottom += score
            if team_idx == 0:
                legend_handles.append(bar[0])

        # Afficher le score total au-dessus de la barre
        plt.text(team_idx, total_score + 0.03 * max_score, f"{total_score:.2f}", ha='center', va='bottom',
                 color=color_scheme["points_color"], fontsize=8, rotation=90)

    # Lignes horizontales pour l'échelle Y
    for y in ax.get_yticks():
        ax.axhline(y, color=color_scheme["horizontal_lines_color"], linestyle='--', linewidth=0.5, zorder=0)

    # Personnalisation des axes
    ax.tick_params(axis='x', which='both', colors=color_scheme["x_ticks_color"])
    ax.xaxis.label.set_color(color_scheme["x_label_color"])
    ax.tick_params(axis='y', which='both', colors=color_scheme["y_ticks_color"])
    ax.yaxis.label.set_color(color_scheme["y_label_color"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(color_scheme["y_axis_color"])
    ax.spines['bottom'].set_color(color_scheme["x_axis_color"])

    # Noms des équipes sur l'axe X
    team_names = ['\n'.join(dict_fusion[key]['names']) for key in team_keys]
    plt.xticks(range(len(team_names)), team_names, rotation=45, ha='right', fontsize=define_size_x_label(dict_fusion), color=color_scheme["x_label_color"])
    plt.yticks(color=color_scheme["y_label_color"])
    ax.set_xlim(-1, len(team_names))

    # Légende des manches
    legend_labels = [f"Round {i+1}" for i in range(num_rounds)]
    plt.legend(legend_handles, legend_labels, loc='upper right', title_fontsize='small', fontsize='x-small',
               handleheight=0.8, handlelength=1, labelspacing=0.3, facecolor=color_scheme["background_color"],
               edgecolor=color_scheme["legend_border_color"], labelcolor=color_scheme["legend_text_color"])

    # Mise en page et titre
    plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.85, top=0.82)
    plt.title(tournament_name, fontdict={'color': color_scheme["title_color"], 'fontsize': 16, 'weight': 'bold'}, pad=20)

    # Logo si demandé
    if show_logo:
        logo_image = plt.imread(logo_path)
        image_box = OffsetImage(logo_image, zoom=zoom_logo)
        annotation_box = AnnotationBbox(image_box, (0.5, 1.075), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    # Date si demandé
    if show_date:
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top',
                fontdict={'color': color_scheme["date_color"], 'fontsize': 8})

    # Créer le dossier d'export si besoin
    os.makedirs("exports", exist_ok=True)
    plt.savefig(os.path.join("exports", "graph_leaderboard.png"), dpi=graphs_pixel_density, facecolor=color_scheme["background_color"])
    plt.close()

def export_average_placement_graph(dict_fusion, nom_tr, cs, lg, lg_path, zoom, dt, graphs_pixel_density):
    """
    Exporte un graphique de placement moyen à partir d'un dictionnaire fusionné.
    dict_fusion: {
        'id1 & id2': {
            'names': ['Nom joueur 1', 'Nom joueur 2', ...],
            'rounds': [
                {'placement': ..., ...},
                ...
            ]
        },
        ...
    }
    """
    # Préparer les données
    data=[]
    labels = []

    for team_key, team_data in dict_fusion.items():
        name_player = team_data['names']
        placements = []
        for round in team_data['rounds']:
            if round['placement'] > 0:
                placements.append(round['placement'])
        data.append(placements)
        labels.append('\n'.join(name_player))

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
    plt.xticks(rotation=45, ha='right', fontsize=define_size_x_label(dict_fusion), color=cs["x_label_color"])  # Correction de la couleur des ticks X
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
        annotation_box = AnnotationBbox(image_box, (0.5, 1.075), xycoords='axes fraction', frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(annotation_box)
        ax.set_title("")

    if dt == True:
        # Ajouter la date du jour comme titre, mais descendre la position
        today_date = datetime.now().strftime("%d/%m/%Y")
        ax.text(0.5, 1.05, today_date, transform=ax.transAxes, ha='center', va='top', 
                fontdict={'color': cs["date_color"], 'fontsize': 8})

    # Enregistrer le graphique
    plt.savefig(os.path.join("exports", "graph_average_placement.png"), dpi=graphs_pixel_density, facecolor=cs["background_color"])