def calculate_score_from_round(round, teams, kill_points, placement_points, masterkill):
    """
    Calculates the total score and placement for a given round.
    Args:
        round (list): A list containing round data. The indices used depend on whether teams mode is enabled.
        teams (bool): True if teams mode is enabled, False for solo mode.
    Returns:
        list: A list containing the total points for the round and the placement.
    """
    # Get the data needed to calculate the score
    if not teams: # Solo mode
        placement = round[0]
        kills = round[4]
        existence_masterkill= round[6]
        total_players = round[2]
    if teams:
        placement = round[0]
        kills = round[5]
        existence_masterkill = round[7]
        total_players = round[2]
    
    kills_pts = kill_points(placement, kills, total_players)
    placement_pts = placement_points(placement, kills, total_players)
    masterkill_pts = masterkill(existence_masterkill, kills, total_players)

    round_pts = kills_pts + placement_pts + masterkill_pts
    return [round_pts, placement, round[4]] # For stats, it's better to return the solo kills

def calculate_score_for_everyone(dict_base, teams, kill_points, placement_points, masterkill):
    """
    Calculates and updates the total score for each player in the given dictionary.
    For each player in `dict_base`, iterates through their rounds, calculates the score for each round
    using the `calculate_score_from_round` function, and appends the detailed round score to the player's
    record. The total score for all rounds is accumulated and updated in the player's data.
    """
    
    for player_id in dict_base:
        total_score = 0
        for round in dict_base[player_id][3]:
            calculated_round = calculate_score_from_round(round, teams, kill_points, placement_points, masterkill)
            total_score += calculated_round[0]
            dict_base[player_id][2].append(calculated_round)
        dict_base[player_id][1] = total_score
    
    return dict_base