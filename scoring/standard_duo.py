import math

# ----------------------------------------------------------------------------

# This is the recommendation for scoring a DUO tournament that are mentioned
# in the Event Format Doc. You can check it here: https://docs.google.com/document/d/16QC3gHi54TgKgCmIGTbVwdj4uO_kf-zB0mxx-yl7Rdo/edit?usp=sharing

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        return kills
    
# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!
    
    else:
        if placement == 1:
            return 10
        elif 2 <= placement <= 3:
            return 7
        elif 4 <= placement <= 9:
            return 5
        elif 10 <= placement <= 15:
            return 3
        else:
            return 0
        
# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 0
    else:
        return 0