def find_total_players_in_round(round_file):
    """
    Finds the total number of players in a round file.
    :param round_file: Path to the round file.
    :return: Total number of players in the round.
    """
    
    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    count = 0
    for line in lines[1:]:
        columns = line.strip().split('\t')
        if int(columns[-1]) >= 1:
            count += 1 # Count only players with placement greater than zero
    return count

def find_total_squads_in_round(round_file):
    """
    Finds the total number of squads in a round file.
    :param round_file: Path to the round file.
    :return: Total number of squads in the round.
    """
    
    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    squads = set()
    count_player_team_minus_one = 0
    for line in lines[1:]:
        columns = line.strip().split('\t')
        squad_id = int(columns[-4])
        placement = int(columns[-1])
        if squad_id != -1 and placement > 0:  # Exclude players without a squad and with placement <= 0
            squads.add(squad_id)
        elif squad_id == -1 and placement > 0:  # Count players without a squad
            count_player_team_minus_one += 1
    return len(squads) + count_player_team_minus_one

def find_total_kill_for_a_squad(round_file, squad_id):
    """
    Finds the total number of kills made by a specific squad in a round file.
    :param round_file: Path to the round file.
    :param squad_id: ID of the squad to check.
    :return: Total number of kills made by the squad.
    """

    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    total_kills = 0
    for line in lines[1:]:
        columns = line.strip().split('\t')
        if int(columns[-4]) == squad_id:  # Check if the player belongs to the specified squad
            kills = int(columns[-2])
            total_kills += kills
    return total_kills

def find_max_kills_in_round(round_file):
    """
    Finds the maximum number of kills made by a player in a round file.
    :param round_file: Path to the round file.
    :return: Maximum number of kills in the round.
    """
    
    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    max_kills = 0
    for line in lines[1:]:
        columns = line.strip().split('\t')
        kills = int(columns[-2])
        if kills > max_kills:
            max_kills = kills
    return max_kills

def find_max_kills_by_a_squad_in_round(round_file):
    """
    Finds the maximum number of kills made by a squad in a round file.
    :param round_file: Path to the round file.
    :return: Maximum number of kills made by a squad in the round.
    """
    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    squads_kills = {}
    for line in lines[1:]:
        columns = line.strip().split('\t')
        squad_id = int(columns[-4])
        kills = int(columns[-2])

        if squad_id <= 0:
            continue  # Ignore players without a squad

        if squad_id not in squads_kills:
            squads_kills[squad_id] = 0
        squads_kills[squad_id] += kills

    squads_kills["max_for_solo"] = find_max_kills_in_round(round_file)
    return max(squads_kills.values(), default=0)

def adjust_placement(dict_round):
    """
    Adjusts placement so it reflect the position in the round.
    Only really useful for the team mode.
    """
    list_placement = [] # List with all the current placements possible
    for id in dict_round:
        if dict_round[id][0] not in list_placement and dict_round[id][0] > 0:
            list_placement.append(dict_round[id][0])
    
    # Sort the placements
    list_placement.sort()

    # Replace the placement (>0) in the dictionnary by the index+1 in the list
    for id in dict_round:
        if dict_round[id][0] > 0:
            dict_round[id][0] = list_placement.index(dict_round[id][0]) + 1
    
    return dict_round

def extract_data_from_round_file(round_file):
    """
    Extracts data from a round file and returns a list with player statistics with the following structure:
    {'id': [placement, squad_id, number of players, number_of_squads, kills, team_kills, masterkill_solo, masterkill_squad], ...}
    """
    
    dict_round = {}

    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip the header line
    players_data = {}
    for line in lines[1:]:
        columns = line.strip().split('\t')
        
        # Extract necessary data
        playfab_id = columns[-5]
        placement = int(columns[-1])
        squad_id = int(columns[-4])
        number_of_players = find_total_players_in_round(round_file)
        number_of_squads = find_total_squads_in_round(round_file)
        kills = int(columns[-2])
        if squad_id == -1:
            team_kills = kills
        else :
            team_kills = find_total_kill_for_a_squad(round_file, squad_id)
        masterkill_solo = (kills == find_max_kills_in_round(round_file))
        masterkill_squad = (team_kills == find_max_kills_by_a_squad_in_round(round_file))

        # Store the data in the dictionary
        dict_round[playfab_id] = [
            placement, squad_id, number_of_players, number_of_squads,
            kills, team_kills, masterkill_solo, masterkill_squad
        ]

    dict_round = adjust_placement(dict_round)
    return dict_round