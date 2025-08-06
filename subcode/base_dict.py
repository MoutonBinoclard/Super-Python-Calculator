from subcode.utilities import list_files

def find_ids(file_to_check):
    """
    Return a list with every ID found in the giver files
    """
    id_list = []

    # Iterate through each file in the list
    for filename in file_to_check:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Iterate through each line in the file (skipping the header)
        for line in lines[1:]:
            columns = line.strip().split('\t')
            playfab_id = columns[-5]
            
            # If the PlayfabID is not already in the list, add it
            if playfab_id not in id_list:
                id_list.append(playfab_id)
    
    return id_list

def create_dict(list_id):
    """
    Create a dict, each entry is a key, the value associated is an empty dict
    """
    id_dict = {}
    
    # Iterate through each ID in the list
    for player_id in list_id:
        # Initialize an empty dictionary for each ID
        id_dict[player_id] = {
            'name': None,
            'rounds': [],
            'nb_rounds': 0,
            'total_kills': 0,
            'total_wins': 0,
            'kill_avg': 0.0,
            'plac_avg': 0.0,
            'max_kill': 0
        }
    
    return id_dict

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

def add_name_to_dict(dict_players, file_list):
    """
    Adds player names to the dict_players dictionary based on PlayfabID.
    """
    
    # Iterate through each player ID in the dictionary
    for player_id in dict_players.keys():
        # Find the player name using the find_name function
        player_name = find_name(player_id, file_list)
        
        # Add the player name to the dictionary
        dict_players[player_id]['name'] = player_name
    
    return dict_players

def create_start_dict():
    files = list_files('txt', 'SPC_')
    list_id = find_ids(files)
    dict_players = create_dict(list_id)
    dict_players = add_name_to_dict(dict_players, files)
    print(f"{len(dict_players)} players found in {len(files)} rounds.")
    return dict_players