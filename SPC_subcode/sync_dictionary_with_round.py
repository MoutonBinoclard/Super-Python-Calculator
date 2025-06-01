from SPC_subcode.data_extraction_from_single_round import extract_data_from_round_file

def fully_update_base_dictionary(dictionnary_to_fully_update, file_list):
    """
    Fully updates the base dictionary with data extracted from all round files.
    The function will iterate through each file in the file_list and update the base dictionary
    with the data extracted from each round file.
    """
    
    for round_file in file_list:
        # Extract data from the current round file
        data_from_round = extract_data_from_round_file(round_file)
        
        # Update the base dictionary with the extracted data
        update_base_dictionary(dictionnary_to_fully_update, data_from_round)

    return dictionnary_to_fully_update

def update_base_dictionary(dictionary_to_update, data_from_round):
    """
    Updates the base dictionary with data extracted from a round file.
    If no data is found for a PlayfabID, the entry will be a default list:
    so instead of
    [placement, squad_id, number_of_players, number_of_squads, kills, team_kills, masterkill_solo, masterkill_squad]
    it will be
    [0, 0, 0, 0, 0, 0, False, False].
    """

    for player_id in dictionary_to_update.keys():
        if player_id in data_from_round:
            # If data is found for the PlayfabID, update the entry with the data from the round
            dictionary_to_update[player_id][3].append(data_from_round[player_id])
        else:
            # If no data is found for the PlayfabID, append a default list
            dictionary_to_update[player_id][3].append([0, 0, 0, 0, 0, 0, False, False])

    return dictionary_to_update
