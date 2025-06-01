def find_name(player_id, file_list):
    """
    Finds the player name for a given PlayfabID in the provided files.
    Returns the player name if found, otherwise returns "name no found".
    """
    
    # Iterate through each file in the list
    for filename in file_list:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Iterate through each line in the file (skipping the header)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            
            # If the PlayfabID matches, return the player name
            if columns[-5] == player_id:
                return columns[1]  # Player name is at index 1 (column "Player")
    
    # If the PlayfabID is not found, return None
    return "name not found"

def find_ids(file_to_check):
    """
    Creates a dictionary with all unique PlayfabIDs found at least once in the given files.
    The dictionary will have PlayfabIDs as keys and a list with the following structure as values:
    [player_name, final_score, score_per_round, round_stats_list, global_stats].
    """

    # Dictionary to store unique PlayfabIDs with empty lists
    id_dict = {}

    # Iterate through each file in the list
    for filename in file_to_check:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Iterate through each line in the file (skipping the header)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            playfab_id = columns[-5]

            # If the PlayfabID is not already in the dictionary, add it with an empty list
            if playfab_id not in id_dict:
                id_dict[playfab_id] = []

    for key in id_dict.keys():
        id_dict[key].append(find_name(key, file_to_check))  # Add the player name to the list
        id_dict[key].append(0)  # Final score initialized to 0
        id_dict[key].append([]) # Empty list for score for each round
        id_dict[key].append([])  # Empty list for stats for each round
        id_dict[key].append(
            {'nb_rounds': 0,'placement_avg': 0, 'nb_wins': 0, 'nb_kills': 0, 'kill_avg': 0, 'max_kill': 0}
            )  # Append the stats_players dictionary instead of an empty list

    return id_dict