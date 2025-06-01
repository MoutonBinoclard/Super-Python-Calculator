# SPC Version 6
# Coded by Mouton Binoclard


'COLOR SCHEME'

color_scheme = "SPC_color_schemes/ascension_25.json"


import json

def load_settings(path="settings.json"):
    with open(path, "r") as f:
        settings = json.load(f)
    return (
        settings["team_mode"],
        settings["scoring_system"],
        settings["bonus"],
        settings["tournament_name"],
        settings["logo"],
        settings["logo_path"],
        settings["zoom_logo"],
        settings["date"],
        settings["add_custom_fonts"],
        settings["custom_font"],
        settings["color_scheme"]
    )

(
    team_mode,
    scoring_system,
    bonus,
    tournament_name,
    logo,
    logo_path,
    zoom_logo,
    date,
    add_custom_fonts,
    custom_font,
    color_scheme
) = load_settings()


import warnings
warnings.simplefilter("ignore", UserWarning)

from SPC_subcode.enabling_settings import *
from SPC_subcode.creation_of_base_dictionary import find_ids
from SPC_subcode.sync_dictionary_with_round import fully_update_base_dictionary
from SPC_subcode.list_files import list_files
from SPC_subcode.update_stats_for_players import update_stats_for_all_players
from SPC_subcode.score_calculation import calculate_score_for_everyone
from SPC_subcode.filtering_dictionary import filter_score, remove_full_time_spectators_or_non_players
from SPC_subcode.creation_dict_fusion import creation_teams_files, creation_fusion_dict
from SPC_subcode.finalization_fusion_dict import add_data_player_to_fusion_dict, add_round_scores_to_fusion_dict, add_final_score_to_fusion_dict, sort_fusion_dict_by_score
from SPC_subcode.results_exportation import starting_exportation_process



##############################################

# Enabling settings

kill_points, placement_points, masterkill = load_scoring_module(scoring_system)
color_scheme = load_colors(color_scheme)
custom_font_loader(add_custom_fonts, custom_font)

##############################################

# Creating the base dictionary
# It contains all the data extracted from the text files in the current directory
# After this step, the teams can be created

# Form of the dictionary:
# {'PlayfabID1': ['PlayerName1', Final_Score, [[score_round1, placement_round1], ...], [info_round1, ...], {'nb_rounds': 0, 'nb_wins': 0, 'nb_kills': 0, 'kill_avg': 0}],...}

# For of the info_round list :
# [placement, squad_id, number_of_players, number_of_squads, kills, team_kills, masterkill_solo, masterkill_squad]

dict_base = find_ids(list_files('.txt', 'SPC_'))
dict_base = fully_update_base_dictionary(dict_base, list_files('.txt', 'SPC_'))
dict_base = update_stats_for_all_players(dict_base)
dict_base = calculate_score_for_everyone(dict_base, team_mode, kill_points, placement_points, masterkill)
dict_base = filter_score(dict_base, None, None)
dict_base = remove_full_time_spectators_or_non_players(dict_base)

#print(dict_base)

##############################################

# Creating the final dictionary
# It contains the teams (even in solo mode)

# Form of the dictionary :
#{'PlayfabCombine' : [[ID1, ...], Names, Final_Score, [[score_round1, placement_round1], ...], [Full_dict_player1, ...]]}

creation_teams_files(dict_base, team_mode)
fusion_dict = creation_fusion_dict(dict_base)
fusion_dict = add_data_player_to_fusion_dict(fusion_dict, dict_base)
fusion_dict = add_round_scores_to_fusion_dict(fusion_dict)
fusion_dict = add_final_score_to_fusion_dict(fusion_dict)
fusion_dict = sort_fusion_dict_by_score(fusion_dict)


#print(fusion_dict)

##############################################

# Exporting ghaphs and results, etc ...
starting_exportation_process(fusion_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date, bonus)