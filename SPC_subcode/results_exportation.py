import os
from SPC_subcode.results_text_exportation import *
from SPC_subcode.results_graph_exportation import *

def creation_export_folder():
    """
    If the folder SPC_exports does not exist, create it.
    """
    if not os.path.exists("SPC_exports"):
        os.makedirs("SPC_exports")

def starting_exportation_process(final_dict_sorted, tournament_name, colors, logo, logo_path, zoom_logo, date, bonus):
    """
    Start the exportation process by creating the export folder and exporting the results.
    """
    creation_export_folder()

    export_light_leaderboard(final_dict_sorted, "compact_leaderboard.txt")
    export_leaderboard_inline(final_dict_sorted, "inline_leaderboard.txt")
    export_detailed_leaderboard(final_dict_sorted, "detailed_leaderboard.txt")

    export_leaderboard_graph(final_dict_sorted, tournament_name, colors, logo, logo_path, zoom_logo, date, bonus)
    exporter_graph_placement_moyen(final_dict_sorted, tournament_name, colors, logo, logo_path, zoom_logo, date, bonus)
                

