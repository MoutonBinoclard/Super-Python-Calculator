import os
from SPC_subcode.team_creation_interface import team_creation_interface

def check_if_launching_team_creation_interface(teams):
    """
    Check if the team creation interface should be launched.
    If :
    - the teams is True
    - and SPC_teams.txt does not exist
        Then 1
    
    If :
    - the teams is False
        Then 0

    If :
    - the teams is True
    - and SPC_teams.txt exists
        Then 2
    """
    
    if teams:
        if not os.path.exists("SPC_teams.txt"):
            return 1  # Launch the team creation interface
        else:
            return 2  # Do not launch the team creation interface, teams already exist
    else:
        return 0  # Do not launch the team creation interface, team mode is off
    

def creation_teams_files(dict_base, teams):
    """
    Create the teams files based on the base dictionary.
    If teams is True, launch the team creation interface.
    If SPC_teams.txt exists, load the teams from the file.
    """
    
    current_situation = check_if_launching_team_creation_interface(teams)

    if current_situation == 1:
        # Launch the team creation interface
        teams = team_creation_interface(dict_base)
        if teams is None:
            print("No teams created.")
            return
        # Save the teams to a file
        with open("SPC_teams.txt", "w", encoding="utf-8") as f:
            for team in teams:
                f.write(" ".join(team) + "\n")
    
    if current_situation == 0:
        # Create a file with all the id, one for each line
        with open("SPC_teams.txt", "w", encoding="utf-8") as f:
            for player_id in dict_base.keys():
                f.write(player_id + "\n")

def read_teams_file(teams_file_path='SPC_teams.txt'):
    """
    Read the teams file and return a list of teams.
    Each team is a list of player IDs.
    """
    teams = []
    try:
        with open(teams_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                team = line.strip().split()
                if team:  # Ensure the team is not empty
                    teams.append(team)
    except FileNotFoundError:
        print(f"File {teams_file_path} not found.")
    return teams

def creation_fusion_dict(current_dict, teams_file_path='SPC_teams.txt'):
    """
    Create a new dictionary that merges player
    This step only create the base dict
    Each key is the combined team ID for each player in the team.
    And each value associated is a list
    Firsts elements are :
    ['players names', score=0, [[score_round1, placement_round1], ...], [info_round1, ...], {'nb_rounds': 0, 'nb_wins': 0, 'nb_kills': 0, 'kill_avg': 0}]
    """

    current_teams= read_teams_file(teams_file_path)
    fusion_dict = {}
    for team in current_teams:
        team_id = " ".join(team)  # Combine player IDs to form a unique team ID
        fusion_dict[team_id] = []

        names = []
        ids_list =[]
        for id in team:
            names.append(current_dict[id][0])  # Get player names from the base dictionary
            ids_list.append(id)
        fusion_dict[team_id].append(ids_list)  # Add player IDs to the list
        fusion_dict[team_id].append(" & ".join(names))
        fusion_dict[team_id].append(0)
        fusion_dict[team_id].append([])
        fusion_dict[team_id].append([])
    return fusion_dict