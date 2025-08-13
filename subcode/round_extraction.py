def extract_raw_data_from_round(round_file):
    """
    Extracts raw data from the round file.
    """

    dict_raw = {}

    with open(round_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines[1:]: # Skip header
        collumns = line.strip().split('\t')
        #print(collumns)
        pID = int(collumns[0])
        Player = collumns[1]
        PlayfabID = collumns[-5] # From end becasue name can make the thing glitch out
        SquadID = int(collumns[-4])
        TeamID = int(collumns[-3])
        Kills = int(collumns[-2])
        Placement = int(collumns[-1])

        dict_raw[PlayfabID] = {
            "playfab_id": PlayfabID,
            "pid": pID,
            "player": Player,
            "squad_id": SquadID,
            "team_id": TeamID,
            "kills": Kills,
            "placement": Placement
        }

    return dict_raw

def find_total_players_in_round(raw_dict):
    """
    Finds the total number of players in a round.
    """
    count = 0
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0 : count += 1
    return count

def find_total_squads_in_round(raw_dict):
    """
    Finds the total number of squads in a round.
    By counting the number of unique squad IDs
    """
    unique_squads = set()
    team_0_number = 0
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0:
            if raw_dict[keys]["squad_id"] == 0:
                team_0_number += 1
            else :
                unique_squads.add(raw_dict[keys]["squad_id"])
    return len(unique_squads) + team_0_number

def max_kills_in_round(raw_dict):
    """
    Finds the maximum number of kills in a round.
    """
    max_kills = 0
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0:
            if raw_dict[keys]["kills"] > max_kills:
                max_kills = raw_dict[keys]["kills"]
    return max_kills

def max_kills_by_squad_in_round(raw_dict):
    """
    Finds the maximum number of kills by a squad in a round.
    """
    squads_kills={}
    # Add the key to dict
    for keys in raw_dict:
        squads_kills[raw_dict[keys]["squad_id"]] = 0
    
    # Count the kills, if squad_id = 0, you do not add, you compare and take the highest
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0:
            squads_kills[raw_dict[keys]["squad_id"]] += raw_dict[keys]["kills"]

    # Return the max value in the dict
    return max(squads_kills.values()), squads_kills

def adjust_placement(raw_dict):
    list_placement = []
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0 and raw_dict[keys]["placement"] not in list_placement:
            list_placement.append(raw_dict[keys]["placement"])
    list_placement.sort()

    # Adjust placement for player with placement >0
    for keys in raw_dict:
        if raw_dict[keys]["placement"] > 0:
            raw_dict[keys]["placement"] = list_placement.index(raw_dict[keys]["placement"]) + 1
    
    return raw_dict
        

def add_round_to_base_dict(base_dict, file_name):
    dict_raw = adjust_placement(extract_raw_data_from_round(file_name))
    num_players = find_total_players_in_round(dict_raw)
    num_squads = find_total_squads_in_round(dict_raw)
    max_kills = max_kills_in_round(dict_raw)
    max_kills_by_squad, squads_kills = max_kills_by_squad_in_round(dict_raw)
    
    for player in base_dict:
        if player in dict_raw:
            dict_round_player = {
                "placement": dict_raw[player]["placement"],
                "squad_id": dict_raw[player]["squad_id"],
                "number_of_players": num_players,
                "number_of_squads": num_squads,
                "kills": dict_raw[player]["kills"],
                "team_kills": squads_kills[dict_raw[player]["squad_id"]],
                "masterkill_solo": (dict_raw[player]["kills"] == max_kills),
                "masterkill_squad": (squads_kills[dict_raw[player]["squad_id"]] == max_kills_by_squad)
            }
            base_dict[player]['rounds'].append(dict_round_player)
        else:
            dict_round_player = {
                "placement": 0,
                "squad_id": 0,
                "number_of_players": 0,
                "number_of_squads": 0,
                "kills": 0,
                "team_kills": 0,
                "masterkill_solo": False,
                "masterkill_squad": False
            }
            base_dict[player]['rounds'].append(dict_round_player)
    return base_dict
    

from subcode.utilities import list_files
def add_all_rounds_to_base_dict(base_dict):
    round_files = list_files(".txt", "SPC_")
    for round_file in round_files:
        base_dict = add_round_to_base_dict(base_dict, round_file)
    return base_dict