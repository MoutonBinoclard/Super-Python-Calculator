import math

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        return kills
"-----------------------------------------------------------------------------"

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!
    
    else:
        if placement == 1:
            return 10
        elif placement == 2:
            return 9
        elif placement == 3:
            return 8
        elif 4 <= placement <= 5:
            return 7
        elif 6 <= placement <= 7:
            return 6
        elif 8 <= placement <= 9:
            return 5
        elif 10 <= placement <= 11:
            return 4
        elif 12 <= placement <= 14:
            return 3
        elif 15 <= placement <= 18:
            return 2
        elif 19 <= placement <= 20:
            return 1
        else:
            return 0
"-----------------------------------------------------------------------------"

def masterkill(presence_de_masterkill, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 5
    else:
        return 0