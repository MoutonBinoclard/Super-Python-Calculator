import math

# ----------------------------------------------------------------------------

# Currently used for the scrims in the Double Trouble server (https://discord.gg/Bwe2mdGXp6)

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
        elif placement == 2:
            return 9
        elif placement == 3:
            return 8
        elif placement == 4:
            return 7
        elif 5 <= placement <= 6:
            return 6
        elif 7 <= placement <= 8:
            return 5
        elif 9 <= placement <= 10:
            return 4
        elif 11 <= placement <= 13:
            return 3
        elif 14 <= placement <= 16:
            return 2
        elif 17 <= placement <= 19:
            return 1
        else:
            return 0
        
# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 3
    else:
        return 0