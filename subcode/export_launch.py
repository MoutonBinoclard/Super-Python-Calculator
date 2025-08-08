from subcode.export_graph import *
from subcode.export_leaderboard import *
from subcode.export_spreadsheet import *

def launch_exportations(fusion_dict, base_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date):
    """
    Launches the exportation of the leaderboard graph.
    
    Parameters:
    - fusion_dict: The dictionary containing the team data.
    - tournament_name: The name of the tournament.
    - color_scheme: The color scheme to be used in the graph.
    - logo: Boolean indicating whether to show the logo.
    - logo_path: Path to the logo image.
    - zoom_logo: Boolean indicating whether to zoom the logo.
    - date: Boolean indicating whether to show the date.
    """
    
    # Export the leaderboard graph
    print("Starting exportation of the results... This may take longer than the rest of the program, be patient !")
    export_full_csv(fusion_dict, base_dict)
    
    export_average_placement_graph(fusion_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date)
    export_graph_leaderboard(fusion_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date)
    export_spreadsheet_from_csv_2("exports/leaderboard_full.csv", tournament_name, color_scheme, logo, logo_path, zoom_logo, date)
    print("\nExportation finished !")