from subcode.utilities import list_files

def find_most_probable_teams(dict_base, file_to_check = list_files(".txt", "SPC_")):
    """
    For each player, finds all other players they have played at least one game with.
    Returns a dict: {player_id: [list of player_ids they played with]}
    """
    number_of_players = len(dict_base)
    player_ids = list(dict_base.keys())
    id_to_index = {pid: idx for idx, pid in enumerate(player_ids)}
    played_with = {pid: set() for pid in player_ids}

    # Iterate through each file in the list
    for filename in file_to_check:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # Build a mapping from team_id to list of player_ids for this match
        team_to_players = {}
        for line in lines[1:]:
            columns = line.strip().split('\t')
            if len(columns) < 5:
                continue  # skip malformed lines
            player_id = columns[-5]
            team_id = columns[-4]
            if player_id == "-1" or team_id == "-1":
                continue  # skip invalid entries
            team_to_players.setdefault(team_id, []).append(player_id)
        # For each team, add all pairs to each other's set
        for players in team_to_players.values():
            for i in range(len(players)):
                for j in range(len(players)):
                    if i != j:
                        played_with[players[i]].add(players[j])

    # Convert sets to sorted lists for output
    result = {pid: sorted(list(ids)) for pid, ids in played_with.items() if ids}

    # Add any player_ids from dict_base that are missing in result with empty list
    for pid in dict_base:
        if pid not in result:
            result[pid] = []

    #print("Players and their teammates (at least one game together):")
    #for pid, teammates in result.items():
        #print(f"{pid}: {teammates}")

    return result