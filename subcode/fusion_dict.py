def create_fus_dict(base_dict, current_teams):
    fusion_dict = {}
    for team in current_teams:
        names = []
        for player_id in team :
            names.append(base_dict[player_id]['name'])
        team_name = names
        key = " & ".join(team)
        fusion_dict[key] = {
            'ids': team,
            'names': team_name,
            'score': 0,
            'rounds': []
        }
    return fusion_dict

def stats_to_fusion_one(fusion_dict, base_dict, fusion_id, team_mode, variable_team):
    """
    Find the best score for a given fusion dictionary ID.
    """
    rounds = []
    for round_number in range(len(base_dict[fusion_dict[fusion_id]['ids'][0]]['rounds'])):
        current_round_dict = {"score": 0, "placement": 0, "kills": 0, "masterkill": False, "number_of_players": 0}
        for team_id in fusion_dict[fusion_id]['ids']:
            current_placement = base_dict[team_id]['rounds'][round_number]['placement']
            current_number_of_players = base_dict[team_id]['rounds'][round_number]['number_of_players']
            
            if team_mode or variable_team:
                current_kills = base_dict[team_id]['rounds'][round_number]['team_kills']
                current_masterkill = base_dict[team_id]['rounds'][round_number]['masterkill_squad']

            else:
                current_kills = base_dict[team_id]['rounds'][round_number]['kills']
                current_masterkill = base_dict[team_id]['rounds'][round_number]['masterkill_solo']

            if current_placement >=1:
                if current_placement < current_round_dict['placement'] or current_round_dict['placement'] == 0:
                    current_round_dict['placement'] = current_placement
            if current_kills > current_round_dict['kills']:
                current_round_dict['kills'] = current_kills
            if current_masterkill:
                current_round_dict['masterkill'] = True       
            if current_number_of_players > current_round_dict['number_of_players']:
                current_round_dict['number_of_players'] = current_number_of_players

        rounds.append(current_round_dict)
    fusion_dict[fusion_id]['rounds'] = rounds
    return fusion_dict

def stats_to_fusion(fusion_dict, base_dict, team_mode, variable_team):
    """
    Apply stats_to_fusion_one to all entries in the fusion dictionary.
    """
    for fusion_id in fusion_dict:
        fusion_dict = stats_to_fusion_one(fusion_dict, base_dict, fusion_id, team_mode, variable_team)
    return fusion_dict

def add_scores_to_fusion_dict_every_round(fusion_dict, kill_fx, placement_fx, masterkill_fx):
    """
    Add scores to the fusion dictionary, not total, only round.
    """
    for keys in fusion_dict:
        index_round = 0
        for round_info in fusion_dict[keys]['rounds']:
            round_placement = round_info['placement']
            round_kills = round_info['kills']
            round_masterkill = round_info['masterkill']
            round_nb_players = round_info['number_of_players']

            round_score = kill_fx(round_placement, round_kills, round_nb_players) \
                + placement_fx(round_placement, round_kills, round_nb_players) \
                + masterkill_fx(round_masterkill, round_kills, round_nb_players)
            fusion_dict[keys]['rounds'][index_round]['score'] = round_score
            index_round += 1
    return fusion_dict

def add_scores_to_fusion_dict(fusion_dict, kill_fx, placement_fx, masterkill_fx):
    """
    Add total scores to the fusion dictionary.
    """
    fusion_dict = add_scores_to_fusion_dict_every_round(fusion_dict, kill_fx, placement_fx, masterkill_fx)
    for keys in fusion_dict:
        total_score = 0
        for round_info in fusion_dict[keys]['rounds']:
            total_score += round_info['score']
        fusion_dict[keys]['score'] = total_score
    return fusion_dict

def sort_fusion_dict(fusion_dict):
    """
    Sort the fusion dictionary by score in descending order.
    """
    sorted_fusion_dict = dict(sorted(fusion_dict.items(), key=lambda item: item[1]['score'], reverse=True))
    print("All rounds have been processed.")
    return sorted_fusion_dict