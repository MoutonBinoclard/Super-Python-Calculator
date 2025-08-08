import math

# ----------------------------------------------------------------------------

desc = """The Standardized Performance Index, my vision of a good scoring system
All the function take the number of players into account so a small lobby awards less than a big one
Currently in use on my server : https://discord.gg/Bm9WnUjdxR"""

# ----------------------------------------------------------------------------

def kill_points(placement, kills, total_players):  # Define how kills award points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!

    else:
        n=total_players
        ix=(n**0.6)*math.log(n**2)/(1.85)
        jx=1-math.exp(-2.5*kills/n)
        return ix*jx

# ----------------------------------------------------------------------------

def placement_points(placement, kills, total_players):  # Define how placement awards points
    # placement, kills, total_players -> int

    if placement == 0 or placement == -1:
        return 0  # This one either!

    else:
        n=total_players
        x=placement-1
        fx=1.5*n**0.5*math.exp(-2*x/5)
        gx=1.0*n**0.5*math.exp(-1*x/10)
        hx=1.0*n**0.5*(1-x/n)
        return fx+gx+hx

# ----------------------------------------------------------------------------

def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards
    # presence_de_masterkill -> bool
    # total_players -> int

    if presence_de_masterkill:
        return 0.20*total_players**0.6
    else:
        return 0