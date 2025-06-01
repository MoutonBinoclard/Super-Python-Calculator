import os

def export_light_leaderboard(leaderboard, filename):
    """
    Export a simple leaderboard to a file, with each player on a new line.

    """
    # Open the file in write mode with UTF-8 encoding
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Iterate over all players in the leaderboard
        for i, keys in enumerate(leaderboard):
            for player_data in leaderboard[keys][4]:
                username = player_data[0]
                final_score = player_data[1]
                file.write(f"{i + 1}. {username} - {final_score:.2f}pts\n")

def export_leaderboard_inline(leaderboard, filename):
    """
    Export a leaderboard as a single line in a file, with each player separated by " / ".
    """
    # Open the file in write mode with UTF-8 encoding
    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        inline_leaderboard = []
        # Iterate over all players in the leaderboard
        for i, keys in enumerate(leaderboard):
            for player_data in leaderboard[keys][4]:
                username = player_data[0]
                final_score = player_data[1]
                inline_leaderboard.append(f"{i + 1}. {username} - {final_score:.2f}pts")
        # Write the joined leaderboard to the file
        file.write(" / ".join(inline_leaderboard))
        file.write(" / ")

def export_detailed_leaderboard(leaderboard, filename):
    """
    Export a detailed leaderboard to a file, including per-round stats for each player.
    The leaderboard is expected to be a dict where each key is a player/team ID and each value is:
    [player_names, final_score, stats, rounds]
    """
    # Get the number of rounds from the first player
    # Get the number of rounds from the first entry in the leaderboard dict
    first_key = list(leaderboard.keys())[0]
    num_rounds = len(leaderboard[first_key][3])

    with open(os.path.join("SPC_exports", filename), 'w', encoding='utf-8') as file:
        # Write header
        header = "Placement\tPlayer\tScore\tNb Rounds\tPlacement Avg\tWins\tKills\tKill Avg\tMax Kill\tReal Score\t"
        for round_num in range(1, num_rounds + 1):
            header += f"Pts/Pos/Kill R{round_num}\t"
        header = header.rstrip('\t') + "\n"
        file.write(header)

        # Iterate over each player in the leaderboard
        for i, keys in enumerate(leaderboard):
            score = leaderboard[keys][2]
            for player_data in leaderboard[keys][4]:
                username = player_data[0]
                real_score = player_data[1]
                stats = player_data[4]
                nb_rounds = stats['nb_rounds']
                placement_avg = stats['placement_avg']
                wins = stats['nb_wins']
                kills = stats['nb_kills']
                kill_avg = stats['kill_avg']
                max_kill = stats['max_kill']
                
                # Write player data
                file.write(f"{i + 1}\t{username}\t{score:.2f}\t{nb_rounds}\t{placement_avg:.2f}\t{wins}\t{kills}\t{kill_avg:.2f}\t{max_kill}\t{real_score:.2f}\t")

                # Write round scores
                for round_num in range(num_rounds):
                    pts = player_data[2][round_num][0]
                    pos = player_data[2][round_num][1]
                    kill = player_data[2][round_num][2]

                    file.write(f"{pts:.2f}/{pos}/{kill}\t")
                # Remove the last tab and add a newline
                file.seek(file.tell() - 1)
                file.write("\n")