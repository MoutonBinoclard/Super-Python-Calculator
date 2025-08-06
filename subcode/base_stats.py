def extract_stats_from_rounds(list_rounds):
    """
    Extract statistics from rounds
    """
    
    # Extract the number of rounds played
    count_rounds = 0
    for round_dict in list_rounds:
        if round_dict['placement'] >= 1:
            count_rounds += 1

    # Calculate total kills
    total_kills = 0  # Changé de tot_kills à total_kills
    for round_dict in list_rounds:
        total_kills += round_dict['kills']  # Utilise total_kills au lieu de tot_kills
    
    # Calculate total wins
    total_wins = 0  # Changé de tot_wins à total_wins
    for round_dict in list_rounds:
        if round_dict['placement'] == 1:
            total_wins += 1  # Utilise total_wins au lieu de tot_wins
    
    # Calculate average kills
    kill_average = 0.0
    if count_rounds > 0:
        kill_average = total_kills / count_rounds

    # Calculate average placement
    placement_average = 0.0
    if count_rounds > 0:
        placement_average = sum(round_dict['placement'] for round_dict in list_rounds) / count_rounds
    
    # Find max kills
    max_kill = 0
    for round_dict in list_rounds:
        if round_dict['kills'] > max_kill:
            max_kill = round_dict['kills']

    return {
        'nb_rounds_st': count_rounds,
        'nb_wins_st': total_wins,
        'nb_kills_st': total_kills,
        'kill_avg_st': kill_average,
        'plac_avg_st': placement_average,
        'max_kill_st': max_kill
    }

def add_stats_for_every_id(base_dict):
    """
    Add statistics for every player in the base dictionary.
    """
    for player_id in base_dict:
        list_rounds = base_dict[player_id]['rounds']
        stats = extract_stats_from_rounds(list_rounds)
        
        base_dict[player_id]['nb_rounds'] = stats['nb_rounds_st']
        base_dict[player_id]['total_kills'] = stats['nb_kills_st']
        base_dict[player_id]['total_wins'] = stats['nb_wins_st']
        base_dict[player_id]['kill_avg'] = stats['kill_avg_st']
        base_dict[player_id]['plac_avg'] = stats['plac_avg_st']
        base_dict[player_id]['max_kill'] = stats['max_kill_st']

    return base_dict