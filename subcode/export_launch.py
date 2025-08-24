from subcode.export_graph import *
from subcode.export_leaderboard import *
from subcode.export_spreadsheet import *
import os

def launch_exportations(fusion_dict, base_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date, enable_graph_export, enable_graph_placement_export, enable_spreadsheet_export, graphs_pixel_density, spreadsheet_pixel_density, logo_vertical_offset, enable_ties, ties_do_not_skip):
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
    os.makedirs("exports", exist_ok=True)
    
    export_full_csv(fusion_dict, base_dict, enable_ties, ties_do_not_skip)

    if enable_graph_placement_export:
        export_average_placement_graph(fusion_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date, graphs_pixel_density, logo_vertical_offset)
    
    if enable_graph_export:
        export_graph_leaderboard(fusion_dict, tournament_name, color_scheme, logo, logo_path, zoom_logo, date, graphs_pixel_density, logo_vertical_offset)
    
    if enable_spreadsheet_export :
        export_spreadsheet_from_csv("exports/leaderboard_full.csv", tournament_name, color_scheme, logo, logo_path, zoom_logo, date, spreadsheet_pixel_density)
    
    print("\nExportation finished !")