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
            return 8
        elif placement == 3:
            return 7
        elif 4 <= placement <= 6:
            return 6
        elif 7 <= placement <= 9:
            return 5
        elif 10 <= placement <= 15:
            return 4
        elif 16 <= placement <= 20:
            return 3
        elif 21 <= placement <= 30:
            return 2
        else:
            return 1
        
# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 2
    else:
        return 0