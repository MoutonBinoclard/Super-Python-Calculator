def export_full_csv(dict_fusion, dict_base):
    """
    Dict fusion is like this
    'team_id': {
        'score': 0,
        'name': 'team_name',
        'rounds': [
            {'placement': 1, 'kills': 10, 'masterkill': True, 'number_of_players': 100, 'score': 50},
            ...
        ]
    }
    Dict base is like this
    'team_id': {
        'name': 'player_name',
        'rounds': [
            {'placement': 1, 'kills': 10, 'masterkill_squad': True, 'number_of_players': 100},
            ...
        ]
    
        'nb_rounds': 5,
        'total_kills': 50,
        'total_wins': 2,
        'kill_avg': 10.0,
        'plac_avg': 2.0,
        'max_kill': 20
    }   

    export the full csv file with all the data
    """
    columns = ['ID_player',
               'Name',
               'Rank',
               'Score',
               'Rounds Played',
               'Total Kills',
               'Total Wins',
               'Kill Avg',
               'Plac Avg',
               'Max Kills',]
    
    # Find number of rounds
    num_rounds = len(dict_base[next(iter(dict_base))]['rounds'])
    for i in range(1, num_rounds + 1):
        columns.append(f'R{i} P')
        columns.append(f'R{i} K')
        columns.append(f'R{i} Mk')
        columns.append(f'R{i} NbPl')
        columns.append(f'R{i} S')
    

    rows = []
    placement_counter = 1  # Move outside the team loop for global placement

    for team_id, team_data in dict_fusion.items():
        for player_id in team_data['ids']:
            name = dict_base[player_id]['name']
            placement = placement_counter
            final_score = round(team_data['score'], 2)
            rounds_played = dict_base[player_id]['nb_rounds']
            total_kills = dict_base[player_id]['total_kills']
            total_wins = dict_base[player_id]['total_wins']
            kill_avg = round(dict_base[player_id]['kill_avg'], 2)
            plac_avg = round(dict_base[player_id]['plac_avg'], 2)
            max_kill = dict_base[player_id]['max_kill']
            row = [player_id, name, placement, final_score, rounds_played, total_kills, total_wins, kill_avg, plac_avg, max_kill]
            for round_info in team_data['rounds']:
                row.append(round_info['placement'])
                row.append(round_info['kills'])
                row.append(round_info.get('masterkill', False))  # Use .get for safety
                row.append(round_info['number_of_players'])
                row.append(round(round_info.get('score', 0), 2))
                
            rows.append(row)  # Collect the row
        placement_counter += 1  # Increment for each player

    # Write to CSV
    import csv

    with open('exports/leaderboard_full.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(rows)




