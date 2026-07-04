def export_txt_obs(dict_fusion, nombre_top):

    if len(dict_fusion) < nombre_top:
        return

    # Sort players by score (descending) and take top N
    sorted_players = sorted(dict_fusion.items(), key=lambda x: x[1]["score"], reverse=True)[:nombre_top]
    
    list_players_and_score=[]
    for playfab_id, player_data in sorted_players:
        name_player = player_data["names"][0]
        score_player = player_data["score"]
        list_players_and_score.append([name_player, score_player])

    # Design du truc avec des caracteres
    # █▓▒░

    # Le plus grand score à ███████ (7) puis ▓▒░ à la fin


    # On ouvre un fichier txt pour écrire le résultat

    with open("SPC_resultats.txt", "w", encoding="utf-8") as f:
        max_score = max(score for _, score in list_players_and_score)

        for player_score in list_players_and_score:
            name, score = player_score
            bar_length = int((score / max_score) * 10)  # Scale to a maximum of 15 characters
            bar = '█' * bar_length + '▓▒░'

            # On ecrit maintenant de la forme
            # Score (XX.XX) - Nom [7 caractere, on reduit si trop long, on met des espace si trop cours] [On met la bar]
            f.write(f"{score:.2f} - {name[:7]:<7} {bar}\n")

    