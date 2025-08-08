import math

# ----------------------------------------------------------------------------

desc = """What even is this ??????
Kill awards more if you die early
From the The H.A.M. Server (https://discord.gg/psVrUGeEdJ)"""

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        if 1 <= placement <= 10:
            return kills * 2
        elif 11 <= placement <= 20:
            return kills * 3
        elif 21 <= placement <= 30:
            return kills * 4
        elif 31 <= placement <= 40:
            return kills * 5
        elif 41 <= placement <= 50:
            return kills * 6
        elif 51 <= placement <= 64:
            return kills * 7
        else:
            return 0
    
# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!
    
    else:
        if placement == 1:
            return 25
        if placement == 2:
            return 23
        if placement == 3:
            return 21
        elif 4 <= placement <= 5:
            return 20
        elif 6 <= placement <= 7:
            return 19
        elif 8 <= placement <= 10:
            return 18
        elif 11 <= placement <= 12:
            return 17
        elif 13 <= placement <= 15:
            return 16
        elif 16 <= placement <= 18:
            return 15
        elif 19 <= placement <= 21:
            return 14
        elif 22 <= placement <= 24:
            return 13
        elif 25 <= placement <= 28:
            return 12
        elif 29 <= placement <= 32:
            return 11
        elif 33 <= placement <= 36:
            return 10
        elif 37 <= placement <= 40:
            return 9
        elif 41 <= placement <= 44:
            return 8
        elif 45 <= placement <= 48:
            return 7
        elif 49 <= placement <= 52:
            return 6
        elif 53 <= placement <= 56:
            return 5
        elif 57 <= placement <= 60:
            return 4
        elif 61 <= placement <= 64:
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