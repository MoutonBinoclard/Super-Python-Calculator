def filter_score(dict_to_filter, min_score, max_score):
    """
    Filters the dictionary based on a score range.
    Usually to remove players without any points.
    
    If min_score is None, it will not filter on the lower bound.
    If max_score is None, it will not filter on the upper bound.

    boundaries are exclusive
    """
    filtered_dict = {}
    for player_id, player_data in dict_to_filter.items():
        score = player_data[1]  # Assuming the score is the second element in the list
        if (min_score is None or score > min_score) and (max_score is None or score < max_score):
            filtered_dict[player_id] = player_data
    return filtered_dict

def remove_full_time_spectators_or_non_players(dict_to_filter):
    """
    Removes players who are full-time spectators or not players from the dictionary.
    So it check if one placement at least is > 0.
    """
    filtered_dict = {}
    for player_id, player_data in dict_to_filter.items():
        # Check if the player has at least one placement greater than 0
        if any(round_info[0] > 0 for round_info in player_data[3]):
            filtered_dict[player_id] = player_data
    return filtered_dict