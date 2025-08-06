import math

# ----------------------------------------------------------------------------

# Used for the "Coupe de Pâques" tournament organized by Asphou
# On the SARFR server (https://discord.gg/4PcpcuTstA)

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        if kills == 0:
            return 0 # No kills, no points
        if kills == 1:
            return 1.5 # 1.5 points for the first kill
        if 2 <= kills <= 7:
            return (kills-1)*1 + 1.5 # 1.5 points for the first kill, then 1 point for each kill above 1
        if 8 <= kills:
            return 7.5 + 0.5*(kills-7) # 7.5 points for the first 7 kills, then 0.5 points for each kill above 7
        
# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!
    
    else:
        somme = 0
        if placement == 1:
            somme += 10
        elif placement == 2:
            somme += 6
        elif placement == 3:
            somme += 4
        elif 4 <= placement <= 8:
            somme += 2
        
        somme += 0.4*(total_players-placement)  # 0.4 points for each player below you in the ranking

        return somme
        
# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 3
    else:
        return 0
