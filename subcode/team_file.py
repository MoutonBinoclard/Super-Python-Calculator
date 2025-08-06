from subcode.team_interface import team_creation_interface
import os
from subcode.find_mate import find_most_probable_teams

def create_teams_file_when_solo(dict_base):
    """
    Create a file SPC_teams.txt with all player IDs, one per line.
    This is used when the team mode is off.
    """
    with open("SPC_teams.txt", "w", encoding="utf-8") as f:
        for player_id in dict_base.keys():
            f.write(player_id + "\n")

def creation_team_file_with_auto_team(dict_base):
    probable_team = find_most_probable_teams(dict_base)
    written_teams = set()
    with open("SPC_teams.txt", "w", encoding="utf-8") as f:
        for player_id, teammates in probable_team.items():
            # Build the team as a set (player + teammates)
            team_set = frozenset([player_id] + [mate for mate in teammates if mate != player_id])
            if not team_set or team_set in written_teams:
                continue
            written_teams.add(team_set)
            f.write(" ".join(sorted(team_set)) + "\n")

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

def team_file_creation(dict_base, team_mode, auto_team):
    """
    Create the SPC_teams.txt file based on the team mode.
    """
    if team_mode :
        if auto_team:
            creation_team_file_with_auto_team(dict_base)
        elif not os.path.exists("SPC_teams.txt"): # If no team file exists
            teams = team_creation_interface(dict_base)  # Launch the team creation interface
            with open("SPC_teams.txt", "w", encoding="utf-8") as f:
                for team in teams:
                    f.write(" ".join(team) + "\n")
    else :
        create_teams_file_when_solo(dict_base)

def load_teams(dict_base, team_mode, auto_team):
    """
    First create files, then return the list of teams.
    """
    team_file_creation(dict_base, team_mode, auto_team)
    return read_teams_file('SPC_teams.txt')