import importlib
import json
from matplotlib import rcParams
from matplotlib import font_manager as fm

def load_scoring_module(module_name):
    """
    Dynamically imports a scoring module from the 'SPC_scoring' package and retrieves its scoring attributes.
    """
    scoring_module = importlib.import_module(f"SPC_scoring.{module_name}")
    return scoring_module.kill_points, scoring_module.placement_points, scoring_module.masterkill

def load_colors(fichier): # Charger les couleurs depuis le fichier JSON
    """
    Loads color data from a JSON file.
    """
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)
    
def custom_font_loader(add_custom_fonts, custom_font, font_weight):
    """
    Loads a custom font into Matplotlib's configuration or resets to the default font.
    Parameters:
        add_custom_fonts (bool): If True, sets the font family to the provided custom font.
        custom_font (object): An object representing the custom font, expected to have a get_name() method.
    Behavior:
        - If add_custom_fonts is True, updates Matplotlib's rcParams to use the custom font.
        - If add_custom_fonts is False, resets the font family to Matplotlib's default ('DejaVu Sans').
    """
    # Map font weights to matplotlib-compatible values
    weight_mapping = {
        'thin': 100,
        'ultralight': 200,
        'light': 300,
        'regular': 400,
        'normal': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700,
        'ultrabold': 800,
        'heavy': 900,
        'black': 900
    }
    
    custom_font = fm.FontProperties(fname=custom_font)

    if add_custom_fonts:

        font_name=custom_font.get_name()
        rcParams['font.family'] = [font_name]
        print(font_name)
        # Convert font weight to matplotlib-compatible value
        matplotlib_weight = weight_mapping.get(font_weight.lower(), 400)
        rcParams['font.weight'] = matplotlib_weight
    else:
        # Réinitialiser la police à la valeur par défaut de Matplotlib
        rcParams['font.family'] = 'DejaVu Sans'  # Police par défaut de Matplotlib
        rcParams['font.weight'] = 'normal'

# -----------------------------------------------------------------------------
# Notes:
# - rcParams['font.family'] expects a font family name, not a file path.
# - If the font is not installed system-wide, Matplotlib will not find it by name.
# - To use a font from a file (not installed), register it with:
#     fm.fontManager.addfont(path_to_font)
#   and then use its family name in rcParams.
# - custom_font should be a string path to the font file (e.g., "SPC_fonts/myfont.ttf").
# -----------------------------------------------------------------------------

