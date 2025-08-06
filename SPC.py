# Small utilitie to better see a dictionary
from subcode.utilities import show_entries_from_base_dict, show_entries_from_fusion_dict

# Remove warnings
import warnings
warnings.simplefilter("ignore", UserWarning)

# Loading the parameters
from subcode.enabling_settings import load_settings
(
    team_mode,
    scoring_system,
    tournament_name,
    logo,
    logo_path,
    zoom_logo,
    date,
    add_custom_fonts,
    custom_font,
    font_weight,
    color_scheme,
    auto_team,
) = load_settings()


# Load the scoring system
from subcode.enabling_settings import load_scoring_module
kill_points, placement_points, masterkill = load_scoring_module(scoring_system)

# Load the color scheme
from subcode.enabling_settings import load_colors
color_scheme = load_colors(color_scheme)

# Load the custom
from subcode.enabling_settings import custom_font_loader
custom_font_loader(add_custom_fonts, custom_font, font_weight)

# Base dictionary creation
from subcode.base_dict import create_start_dict
base_dict = create_start_dict()

# Adding rounds to the base dictionary
from subcode.round_extraction import add_all_rounds_to_base_dict
base_dict = add_all_rounds_to_base_dict(base_dict)

# Adding statistics to the base dictionary
from subcode.base_stats import add_stats_for_every_id
base_dict = add_stats_for_every_id(base_dict)

# Creation of the teams
from subcode.team_file import load_teams
current_teams = load_teams(base_dict, team_mode, auto_team)

# Creation fusion dict
from subcode.fusion_dict import create_fus_dict
fusion_dict = (create_fus_dict(base_dict, current_teams))

# Adding stats to the fusion dict
from subcode.fusion_dict import stats_to_fusion
fusion_dict = stats_to_fusion(fusion_dict, base_dict, team_mode)

# Adding scores to the fusion dict
from subcode.fusion_dict import add_scores_to_fusion_dict
fusion_dict = add_scores_to_fusion_dict(fusion_dict, kill_points, placement_points, masterkill)

# Remove non-player
from subcode.filter_dict import remove_non_player
fusion_dict = remove_non_player(fusion_dict)

# Sort by score, descending order
from subcode.fusion_dict import sort_fusion_dict
fusion_dict = sort_fusion_dict(fusion_dict)

show_entries_from_base_dict(base_dict)
# All the calculations are done

from subcode.export_launch import launch_exportations
launch_exportations(
    fusion_dict,
    base_dict,
    tournament_name,
    color_scheme,
    logo,
    logo_path,
    zoom_logo,
    date
)