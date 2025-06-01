def add_data_player_to_fusion_dict(dict_fusion_to_complete, dict_base):
    """
    Add data from the base dictionary to the fusion dictionary.
    This function is used to make the fusion dictionnary complete
    with no need to re use the dict_base again.
    """
    for keys in dict_fusion_to_complete:
        for id_in_teams in dict_fusion_to_complete[keys][0]:
            dict_fusion_to_complete[keys][4].append(dict_base[id_in_teams])

    return dict_fusion_to_complete

def add_round_scores_to_fusion_dict(dict_without_rounds_scores):
    """
    Add the round scores to the fusion dictionary.
    This function is used to make the fusion dictionary complete
    
    For each entry, now index 3 is an empty list
    We need to fill it to make it like this
    {'PlayfabCombine' : [[ID1, ...], Names, Final_Score, [[score_round1, placement_round1], ...], [Full_dict_player1, ...], [round_score1, round_score2, ...]]}
    However, to find the round score, we need to take the highest value for this round among all players in the team.
    The same goes for the round placement.
    """
    
    for team in dict_without_rounds_scores:
        list_max_score_min_placement=[]
        for round_index in range(len(dict_without_rounds_scores[team][4][0][3])):
            max_score_min_placement = [0, 0]
            for ID_index in range(len(dict_without_rounds_scores[team][0])):
                round_score= dict_without_rounds_scores[team][4][ID_index][2][round_index][0]
                round_placement= dict_without_rounds_scores[team][4][ID_index][2][round_index][1]
                if round_score > max_score_min_placement[0]:
                    max_score_min_placement[0] = round_score
                if round_placement < max_score_min_placement[1] or (max_score_min_placement[1] == 0 and round_placement > 0):
                    max_score_min_placement[1] = round_placement
            list_max_score_min_placement.append(max_score_min_placement)
        dict_without_rounds_scores[team][3] = list_max_score_min_placement
    
    return dict_without_rounds_scores

def add_final_score_to_fusion_dict(dict_without_final_score):
    """
    Add the final score to the fusion dictionary.
    This function is used to make the fusion dictionary complete
    with no need to re use the dict_base again.
    """
    
    for team in dict_without_final_score:
        final_score = 0
        for round in dict_without_final_score[team][3]:
            final_score += round[0]
        dict_without_final_score[team][2] = final_score
    return dict_without_final_score

def sort_fusion_dict_by_score(dict_to_sort):
    """
    Sort the fusion dictionary by final score in descending order.
    """
    sorted_dict = dict(sorted(dict_to_sort.items(), key=lambda item: item[1][2], reverse=True))
    return sorted_dict