def export_txt_obs(dict_fusion, nombre_lignes):
    if len(dict_fusion) < nombre_lignes:
        nombre_lignes = len(dict_fusion)

    # Sort players by score (descending) and take top N
    sorted_players = sorted(dict_fusion.items(), key=lambda x: x[1]["score"], reverse=True)[:nombre_lignes]

    list_players_and_score=[]
    for playfab_id, player_data in sorted_players:
        name_player = player_data["names"][0]
        score_player = player_data["score"]
        valid_rounds = [round_data for round_data in player_data["rounds"] if round_data["placement"] >= 1]
        compteur_games = len(valid_rounds)
        compteur_win = sum(1 for round_data in valid_rounds if round_data["placement"] == 1)
        compteur_kill = sum(round_data["kills"] for round_data in player_data["rounds"])
        max_kill = 0
        placement_average = 0
        best_placement = 0
        if compteur_games > 0:
            placement_average = sum(round_data["placement"] for round_data in valid_rounds) / compteur_games
            best_placement = min(round_data["placement"] for round_data in valid_rounds)
        if player_data["rounds"]:
            max_kill = max(round_data["kills"] for round_data in player_data["rounds"])
        list_players_and_score.append([name_player, score_player, compteur_games, compteur_win, compteur_kill, placement_average, best_placement, max_kill])


    # Mettre dans un fichier texte avec la forme suivant
    """
    XX   NOM JOUEUR         SCORE   GAMES   WINS   KILLS   PLAC AVG   BEST   MAX K
    """

    # Le fichier sera mis dans le dossier "export" avec le nom "export_obs.txt"
    with open("exports/export_obs.txt", "w", encoding="utf-8") as f:
        compteur = 0
        for name_player, score_player, compteur_games, compteur_win, compteur_kill, placement_average, best_placement, max_kill in list_players_and_score:
            compteur += 1
            taille_nom = len(name_player)
            taillemax = 17
            if taille_nom > taillemax:
                name_player = name_player[:taillemax-3] + "..."
            f.write(f"{compteur:02}     {name_player:<17.17}    {score_player:05.1f}     {compteur_games:02}     {compteur_win:02}     {compteur_kill:02}     {placement_average:05.2f}     {best_placement:02}     {max_kill:02}\n")

        # Rajouter une ligne vide à la fin du fichier
        f.write("\n")


    