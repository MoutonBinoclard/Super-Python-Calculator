def find_nb_rounds(player_entry_from_dict_base):
    """
    Counts the number of rounds played by a player.
    :param player_entry_from_dict_base):: List containing player data.
    :return: Number of rounds played by the player.
    """
    
    count = 0
    for round in player_entry_from_dict_base[3]:
        if round[0] > 0 :
            count += 1
    return count

def find_nb_wins(player_entry_from_dict_base):
    """
    Counts the number of wins for a player.
    :param player_entry_from_dict_base: List containing player data.
    :return: Number of wins for the player.
    """
    
    count = 0
    for round in player_entry_from_dict_base[3]:
        if round[0] == 1:
            count += 1
    return count

def find_nb_kills(player_entry_from_dict_base):
    """
    Counts the total number of kills for a player.
    :param player_entry_from_dict_base: List containing player data.
    :return: Total number of kills for the player.
    """
    
    count = 0
    for round in player_entry_from_dict_base[3]:
        count += round[4]
    return count

def find_kill_avg(player_entry_from_dict_base):
    """
    Calculates the average number of kills per round for a player.
    :param player_entry_from_dict_base: List containing player data.
    :return: Average number of kills per round for the player.
    """
    
    nb_rounds = find_nb_rounds(player_entry_from_dict_base)
    if nb_rounds == 0:
        return 0
    return find_nb_kills(player_entry_from_dict_base) / nb_rounds

def find_max_kills(player_entry_from_dict_base):
    """
    Finds the maximum number of kills made by a player in a single round.
    :param player_entry_from_dict_base: List containing player data.
    :return: Maximum number of kills made by the player in a single round.
    """
    
    max_kills = 0
    for round in player_entry_from_dict_base[3]:
        if round[4] > max_kills:
            max_kills = round[4]
    return max_kills

def find_placement_avg(player_entry_from_dict_base):
    """
    Calculates the average placement for a player across all rounds.
    :param player_entry_from_dict_base: List containing player data.
    :return: Average placement for the player.
    """
    
    total_placement = 0
    nb_rounds = find_nb_rounds(player_entry_from_dict_base)
    
    if nb_rounds == 0:
        return 0
    
    for round in player_entry_from_dict_base[3]:
        if round[0]>0:
            total_placement += round[0]
    
    return total_placement / nb_rounds

def update_stats_for_a_player(player_entry_from_dict_base):
    """
    Updates the statistics for a player in the base dictionary.
    :param player_entry_from_dict_base: List containing player data.
    :return: Updated player entry with statistics.
    """
    
    player_entry_from_dict_base[4]['nb_rounds'] = find_nb_rounds(player_entry_from_dict_base)
    player_entry_from_dict_base[4]['placement_avg'] = find_placement_avg(player_entry_from_dict_base)
    player_entry_from_dict_base[4]['nb_wins'] = find_nb_wins(player_entry_from_dict_base)
    player_entry_from_dict_base[4]['nb_kills'] = find_nb_kills(player_entry_from_dict_base)
    player_entry_from_dict_base[4]['kill_avg'] = find_kill_avg(player_entry_from_dict_base)
    player_entry_from_dict_base[4]['max_kill'] = find_max_kills(player_entry_from_dict_base)
    
    return player_entry_from_dict_base

def update_stats_for_all_players(dict_base):
    """
    Updates the statistics for all players in the base dictionary.
    :param dict_base: Dictionary containing player data.
    :return: Updated base dictionary with player statistics.
    """
    
    for player_id, player_entry in dict_base.items():
        dict_base[player_id] = update_stats_for_a_player(player_entry)
    
    return dict_base