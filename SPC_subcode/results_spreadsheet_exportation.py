import pandas as pd
import matplotlib.pyplot as plt
import os

def export_spreadsheet(final_dict_sorted, tournament_name, cs, logo, logo_path, zoom_logo, date, bonus):
    """
    Export a spreadsheet (png format) with the results of the tournament.3
    for each entry in the final_dict_sorted dictionary, it creates a row in the spreadsheet.
    How to access the data
    for each key,
    take the last entrie of the list = dict for player
    format
    {'PlayfabID1': ['PlayerName1', Final_Score, [[score_round1, placement_round1], ...], [info_round1, ...], {'nb_rounds': 0, 'nb_wins': 0, 'nb_kills': 0, 'kill_avg': 0}],...}
    """
    all_players_data = []
    for index, entries in enumerate(final_dict_sorted):
        for player_index in range(len(final_dict_sorted[entries][-1])):
            info_player = (final_dict_sorted[entries][-1][player_index])
            
            # Score and placement
            placement = index + 1
            name = info_player[0]
            final_score = round(info_player[1], 2)

            # Some stats
            nb_rounds = info_player[-1]['nb_rounds']
            placement_avg = round(info_player[-1]['placement_avg'], 2)
            nb_wins = info_player[-1]['nb_wins']
            nb_kills = info_player[-1]['nb_kills']
            kill_avg = round(info_player[-1]['kill_avg'], 2)
            max_kill = info_player[-1]['max_kill']

            info_each_round = []
            # with this form [[points, placement,kills],...]
            # index correspond to the round number
            for round_data in info_player[2]:
                score = round(round_data[0], 2)
                placement_round = round_data[1]
                kills = round_data[2]
                liste = [score, placement_round, kills]
                info_each_round.append(liste)
            
            # Create a dictionary for the player
            player_data = {
                'Name': name,
                'Final Score': final_score,
                'Placement': placement,
                'Rounds Played': nb_rounds,
                'Average Placement': placement_avg,
                'Wins': nb_wins,
                'Kills': nb_kills,
                'Average Kills': kill_avg,
                'Max Kills': max_kill
            }
            
            # Ajouter les données de chaque round
            for round_index, round_data in enumerate(info_each_round, 1):
                if len(round_data) >= 3:  # Points, placement, kills
                    points = round_data[0]
                    placement = round_data[1]
                    kills = round_data[2] if len(round_data) > 2 else 0
                    player_data[f'Round {round_index}'] = f"{points} - P{placement} - K{kills}"
            
            all_players_data.append(player_data)

    df = pd.DataFrame(all_players_data)

    # Afficher et sauvegarder le tableau en image PNG avec dimensions optimisées
    fig_height = len(df) * 0.25 + 0.6  # Hauteur réduite
    fig_width = len(df.columns) * 1.1  # Largeur réduite
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(df.columns))))
    
    # Appliquer les couleurs du schéma
    for i in range(len(df.columns)):
        # En-têtes (première ligne)
        table[(0, i)].set_facecolor(cs["top_cells_color"])
        table[(0, i)].set_text_props(color=cs["top_text_color"])
        table[(0, i)].set_edgecolor(cs["grid_color"])
        
        # Cellules de données
        for j in range(len(df)):
            table[(j+1, i)].set_facecolor(cs["cells_color"])
            table[(j+1, i)].set_text_props(color=cs["text_color"])
            table[(j+1, i)].set_edgecolor(cs["grid_color"])
    
    # Marges ultra serrées autour du tableau
    plt.subplots_adjust(left=0.05, right=0.05, top=0.05, bottom=0.05)

    filename = f"{tournament_name}_results.png"
    plt.savefig(
        os.path.join("SPC_exports", "spreadsheet.png"),
        dpi=600,
        facecolor=cs["background_color"],
        pad_inches=0.1  # Add some padding to ensure borders are visible
    )
    #print(f"Image du tableau sauvegardée sous : {filename}")
    #return filename