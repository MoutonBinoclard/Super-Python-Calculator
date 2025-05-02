import math

# ----------------------------------------------------------------------------

# Used for the PVP Arena Solo Tournament (https://discord.gg/KJk6HmV9hN)
# This scoring doesn't award any points for kills, but only for placement.

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        return 0
    
# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!
        
    else:
        if placement == 1:
            return 15
        elif placement == 2:
            return 12
        elif placement == 3:
            return 10
        elif 4 <= placement <= 6:
            return 9
        elif 7 <= placement <= 10:
            return 8
        elif 11 <= placement <= 15:
            return 7
        elif 16 <= placement <= 20:
            return 6
        elif 21 <= placement <= 25:
            return 5
        elif 26 <= placement <= 30:
            return 4
        elif 31 <= placement <= 40:
            return 3
        elif 41 <= placement <= 45:
            return 2
        else:
            return 1
        
# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 0
    else:
        return 0
