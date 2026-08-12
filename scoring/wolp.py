import math

# ----------------------------------------------------------------------------

created_with_scoring = True
desc = """Description of this scoring system"""

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        return kills * 5
    
# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!

    else:
        if placement == 1:
            return 22
        elif placement == 2:
            return 18
        elif placement == 3:
            return 15
        elif placement == 4:
            return 13
        elif placement == 5:
            return 11
        elif 6 <= placement <= 10:
            return 8
        elif 11 <= placement <= 15:
            return 6
        elif 16 <= placement <= 20:
            return 4
        elif 21 <= placement <= 30:
            return 2
        elif 31 <= placement <= 64:
            return 1
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