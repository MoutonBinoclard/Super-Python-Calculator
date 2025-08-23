import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
import pathlib
import shutil
from datetime import datetime
import importlib.util
from PIL import Image, ImageTk


# =============================================================================
# CONSTANTS AND CONFIGURATION
# =============================================================================

INFORMATION_TEXT = """---------- Tournament Informations Section ----------

Show Date : Show the date of the tournament on the graph

Tournament Name : The name of the tournament (Will be displayed on the graph)

Event Host : The name of the event host (Just useful for saving the tournament to a folder)


---------- Scoring Section ----------

Scoring System : Choose how the points are calculated

Team mode : Let you score rounds with static teams

Auto team (Enable Team Mode) : Will try to automatically create teams (Please disable this for the final annoucement or check teams manually)

Variable team (Disable Team Mode and Auto Team) :  Let you score rounds for each player individually in squad events with not static teams (For a duo scrims for exemple)


---------- Web Section ----------

Title : The title of the web page

Ngrok Token : The token to use ngrok (Create an account on ngrok then go to https://dashboard.ngrok.com/get-started/your-authtoken to copy the token)


---------- Export Section ----------

Enable Graph Export : Export a picture with the score per player/team

Enable Graph Placement Export : Export a picture with stats about the placement of the players

Enable Spreadsheet Export : Export a spreadsheet with all the scores and stats (Takes a lot of time, maybe enable this only at the end)

Density (dpi) : The higher the dpi, the better the quality (First one is for graphs, second one for spreadsheet)


---------- Customization Section ----------

Add Custom Fonts : Enable custom fonts

Font weight : Choose the font weight (Bold, Light, Regular...)

Color Scheme : Let who choose what colors the exportations will use


---------- Logo Section ----------

Enable Logo : Enable a logo at the top of the graph instead of the tournament name

Logo file : Choose the logo file

Zoom Logo : Zoom the logo (0.150 is the original size). Use the zoom_150 logo file for a base if you want to create your own logo

Vertical Offset : Move the logo up or down


---------- Misc ----------

Game Saver Key : Ctrl + this key to save a round with round saver


---------- Actions ----------

Save tournament to folder : Saves all graph and round in a folder

Delete rounds : Deletes all rounds in the root folder (No turning back)

Save settings : Saves the current settings to settings.json

Delete matplotlib fontlist : Not for you to use !!!
"""

# Directory paths configuration
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
SPC_SCORING_DIR = os.path.join(BASE_DIR, "scoring")
SPC_LOGO_DIR = os.path.join(BASE_DIR, "logo")
SPC_COLOR_SCHEME_DIR = os.path.join(BASE_DIR, "color_schemes")
WINDOWS_FONTS_DIR = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')

# Default settings configuration
DEFAULT_SETTINGS = {
    "date": True,
    "tournament_name": "Test Tournament",
    "event_host": "Guest",
    "scoring_system": "spi",
    "team_mode": False,
    "auto_team": False,
    "add_custom_fonts": False,
    "custom_font": "",
    "font_weight": "Regular",
    "color_scheme": "",
    "logo": False,
    "logo_path": "",
    "zoom_logo": 1.0,
    "enable_graph_export": True,
    "enable_graph_placement_export": True,
    "enable_spreadsheet_export": True,
    "activate_game_saver_key": "m",
    "logo_vertical_offset": 0.0,
    "title_web": "SPC V7 - Live Tournament Leaderboard",
    "auth_token": ""
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_settings():
    """Load settings from JSON file or create default settings if file doesn't exist."""
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        return DEFAULT_SETTINGS.copy()
    
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    """Save settings to JSON file."""
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def load_scoring_systems():
    """Load available scoring systems from the scoring directory."""
    if not os.path.isdir(SPC_SCORING_DIR):
        return []
        
    files = os.listdir(SPC_SCORING_DIR)
    scoring_names = [
        os.path.splitext(f)[0]
        for f in files
        if os.path.isfile(os.path.join(SPC_SCORING_DIR, f))
        and not f.startswith("SPC_")
    ]
    return sorted(scoring_names)


def get_scoring_description(scoring_name):
    """Load the description from a scoring system module."""
    if not scoring_name:
        return ""
    
    try:
        file_path = os.path.join(SPC_SCORING_DIR, f"{scoring_name}.py")
        if not os.path.exists(file_path):
            return "Description not available"
        
        spec = importlib.util.spec_from_file_location(f"scoring_{scoring_name}", file_path)
        if spec is None or spec.loader is None:
            return "Failed to load scoring system"
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return getattr(module, 'desc', "No description available")
    
    except Exception as e:
        return f"Error loading description: {str(e)}"


def load_logo_files():
    """Load available logo files from the logo directory."""
    if not os.path.isdir(SPC_LOGO_DIR):
        return [], []
        
    files = os.listdir(SPC_LOGO_DIR)
    logo_files = [f for f in files if os.path.isfile(os.path.join(SPC_LOGO_DIR, f))]
    logo_names = [os.path.splitext(f)[0] for f in logo_files]
    return sorted(logo_names), logo_files


def load_color_schemes():
    """Load available color schemes from the color schemes directory."""
    if not os.path.isdir(SPC_COLOR_SCHEME_DIR):
        return [], []
        
    files = os.listdir(SPC_COLOR_SCHEME_DIR)
    color_files = [
        f for f in files
        if os.path.isfile(os.path.join(SPC_COLOR_SCHEME_DIR, f))
        and f.lower().endswith('.json')
        and not f.startswith("SPC_")
    ]
    color_names = [os.path.splitext(f)[0] for f in color_files]
    return sorted(color_names), color_files


def get_matplotlib_config_dir():
    """Get matplotlib configuration directory."""
    try:
        import matplotlib
        return matplotlib.get_configdir()
    except Exception:
        return os.path.join(os.path.expanduser("~"), ".matplotlib")


def delete_fontlist_files():
    """Delete matplotlib fontlist cache files."""
    config_dir = get_matplotlib_config_dir()
    if not os.path.isdir(config_dir):
        messagebox.showinfo("Info", f"No matplotlib config directory found at:\n{config_dir}")
        return
        
    deleted = []
    for fname in os.listdir(config_dir):
        if fname.startswith("fontlist"):
            try:
                os.remove(os.path.join(config_dir, fname))
                deleted.append(fname)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete {fname}: {e}")
                return
                
    if deleted:
        messagebox.showinfo("Success", f"Deleted: {', '.join(deleted)}")
    else:
        messagebox.showinfo("Info", "No fontlist files found.")


# =============================================================================
# FONT HANDLING FUNCTIONS
# =============================================================================

def get_font_weights(font_path):
    """Extract available font weights from a font file."""
    if not font_path or not os.path.isfile(font_path):
        return []
    
    try:
        from fontTools.ttLib import TTFont
        font = TTFont(font_path)
        
        name_table = font['name']
        weights = set()
        
        # Look for subfamily names (ID 2) which often contain weight info
        for record in name_table.names:
            if record.nameID == 2:
                subfamily = record.toUnicode() if hasattr(record, 'toUnicode') else str(record)
                weights.add(subfamily)
        
        font.close()
        return sorted(list(weights)) if weights else ["Regular"]
        
    except ImportError:
        # Fallback: return common weight names if fontTools not available
        return ["Regular", "Bold", "Light", "Medium", "Thin", "Black"]
    except Exception:
        return ["Regular", "Bold"]


def load_font_families():
    """Load font families from Windows Fonts directory."""
    if not os.path.isdir(WINDOWS_FONTS_DIR):
        return {}
    
    font_families = {}
    for fname in os.listdir(WINDOWS_FONTS_DIR):
        if fname.lower().endswith(('.ttf', '.otf')):
            # Extract family name from filename (assuming format: FamilyName-Weight.ttf)
            base_name = os.path.splitext(fname)[0]
            if '-' in base_name:
                family, weight = base_name.rsplit('-', 1)
            else:
                family, weight = base_name, "Regular"
            
            if family not in font_families:
                font_families[family] = []
            font_families[family].append({
                'weight': weight,
                'file': fname,
                'path': os.path.join(WINDOWS_FONTS_DIR, fname)
            })
    
    # Sort weights for each family
    for family in font_families:
        font_families[family].sort(key=lambda x: x['weight'])
    
    return font_families


def get_font_weights_from_family(font_families, family_name):
    """Get available weights for a specific font family."""
    if family_name in font_families:
        return [font['weight'] for font in font_families[family_name]]
    return ["Regular"]


def get_font_path_from_family_weight(font_families, family_name, weight):
    """Get the full font path from family name and weight."""
    if family_name in font_families:
        for font in font_families[family_name]:
            if font['weight'] == weight:
                return font['path']
    return ""


# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================

class SettingsEditor(tk.Tk):
    """Main settings editor application window."""
    
    def __init__(self):
        super().__init__()
        self.title("Settings Editor")
        self.configure(bg='#2d2d2d')
        self.resizable(False, False)
        
        # Initialize data
        self.settings = load_settings()
        self.scoring_systems = load_scoring_systems()
        self.logo_names, self.logo_files = load_logo_files()
        self.color_names, self.color_files = load_color_schemes()
        self.font_families = load_font_families()
        
        # Create name-to-path mappings
        self._create_file_mappings()
        
        # Logo preview image reference
        self.logo_image = None
        
        # Setup UI
        self._setup_styles()
        self.create_widgets()
        self.adjust_window_size()

    def _create_file_mappings(self):
        """Create mappings between display names and file paths."""
        self.logo_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("logo", f).replace("\\", "/")
            for f in self.logo_files
        }
        self.logo_name_to_file = {
            os.path.splitext(f)[0]: f
            for f in self.logo_files
        }
        self.color_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("color_schemes", f).replace("\\", "/")
            for f in self.color_files
        }

    def _setup_styles(self):
        """Configure ttk styles for dark theme."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Dark theme colors
        style_config = {
            'TFrame': {'background': '#2d2d2d'},
            'TLabelframe': {'background': '#2d2d2d', 'foreground': '#ffffff'},
            'TLabelframe.Label': {'background': '#2d2d2d', 'foreground': '#ffffff'},
            'TLabel': {'background': '#2d2d2d', 'foreground': '#ffffff'},
            'TButton': {'background': '#404040', 'foreground': '#ffffff'},
            'TEntry': {'fieldbackground': '#404040', 'foreground': '#ffffff', 'bordercolor': '#606060'},
            'TCheckbutton': {'background': '#2d2d2d', 'foreground': '#ffffff'},
            'TMenubutton': {'background': '#404040', 'foreground': '#ffffff', 'arrowcolor': '#ffffff'},
            'Green.TButton': {'background': '#2ecc40', 'foreground': '#ffffff'}
        }
        
        for style_name, config in style_config.items():
            self.style.configure(style_name, **config)
        
        # Button hover effects
        self.style.map('TButton', background=[('active', '#505050')])
        self.style.map('TMenubutton', background=[('active', '#505050')])
        self.style.map('Green.TButton', background=[('active', '#27ae60')])

    def adjust_window_size(self):
        """Calculate and set the optimal window size based on content."""
        self.update_idletasks()
        
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        self.minsize(900, 550)
        
        # Center the window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")


    # =============================================================================
    # EVENT HANDLERS AND UPDATES
    # =============================================================================

    def update_font_weights(self, *args):
        """Update the font weight dropdown based on selected font family."""
        selection = self.font_family_listbox.curselection()
        if not selection:
            return
            
        family_name = self.font_family_listbox.get(selection[0])
        if family_name == "No fonts found":
            return
        
        # Update the selected font display
        self.selected_font_var.set(f"Selected: {family_name}")
            
        weights = get_font_weights_from_family(self.font_families, family_name)
        
        # Update the option menu
        menu = self.font_weight_menu['menu']
        menu.delete(0, 'end')
        
        for weight in weights:
            menu.add_command(label=weight, command=tk._setit(self.font_weight_var, weight))
        
        # Set default value if current value is not in new weights
        current_weight = self.font_weight_var.get()
        if current_weight not in weights and weights:
            self.font_weight_var.set(weights[0])

    def update_scoring_description(self, *args):
        """Update the description text when scoring system is changed."""
        selected_scoring = self.scoring_var.get()
        description = get_scoring_description(selected_scoring)
        self.scoring_desc_text.config(state=tk.NORMAL)
        self.scoring_desc_text.delete(1.0, tk.END)
        self.scoring_desc_text.insert(tk.END, description)
        self.scoring_desc_text.config(state=tk.DISABLED)

    def update_logo_preview(self, *args):
        """Update the logo preview when selection changes."""
        selected_logo = self.logo_file_var.get()
        self.load_logo_preview(selected_logo)

    def update_color_preview(self, *args):
        """Update the color scheme preview zone."""
        selected_color_name = self.color_scheme_var.get()
        color_file = None
        for name, file in zip(self.color_names, self.color_files):
            if name == selected_color_name:
                color_file = file
                break
                
        if not color_file:
            self._clear_color_preview()
            return
            
        self._display_color_preview(color_file)

    def _clear_color_preview(self):
        """Clear the color preview displays."""
        for widget in self.color_preview_frame.winfo_children():
            widget.destroy()
        for widget in self.color_list_frame.winfo_children():
            widget.destroy()

    def _display_color_preview(self, color_file):
        """Display color preview for the selected color scheme."""
        color_path = os.path.join(SPC_COLOR_SCHEME_DIR, color_file)
        try:
            with open(color_path, "r", encoding="utf-8") as f:
                color_data = json.load(f)
            bg_color = color_data.get("background_color", "#222")
            gradient_colors = color_data.get("gradient_colors", [])
        except Exception:
            bg_color = "#222"
            gradient_colors = []
            color_data = {}

        # Clear previous preview
        self._clear_color_preview()
        
        # Create main color preview
        self._create_main_color_preview(bg_color, gradient_colors)
        
        # Create detailed color list
        self._create_detailed_color_list(color_data, bg_color, gradient_colors)

    def _create_main_color_preview(self, bg_color, gradient_colors):
        """Create the main color preview with background and gradient colors."""
        color_container = tk.Frame(self.color_preview_frame, bg='#2d2d2d')
        color_container.pack(fill=tk.X, expand=True)
        
        # Background color (fixed proportion)
        bg_frame = tk.Frame(color_container, width=80, height=30)
        bg_frame.pack(side=tk.LEFT, padx=2, pady=2)
        bg_frame.pack_propagate(False)
        
        bg_label = tk.Label(
            bg_frame, 
            text="Background", 
            bg=bg_color, 
            fg="#fff" if bg_color.lower() != "#fff" else "#000"
        )
        bg_label.pack(fill=tk.BOTH, expand=True)
        
        # Gradient colors
        if gradient_colors:
            gradients_frame = tk.Frame(color_container, bg='#2d2d2d')
            gradients_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            for idx, color in enumerate(gradient_colors):
                color_frame = tk.Frame(gradients_frame, width=30, height=30)
                color_frame.pack(side=tk.LEFT, padx=1, fill=tk.Y)
                color_frame.pack_propagate(False)
                
                color_label = tk.Label(
                    color_frame, 
                    text=f"G{idx+1}", 
                    bg=color, 
                    fg="#fff" if color.lower() != "#fff" else "#000"
                )
                color_label.pack(fill=tk.BOTH, expand=True)

    def _create_detailed_color_list(self, color_data, bg_color, gradient_colors):
        """Create detailed horizontal scrollable color list."""
        canvas_width = 260
        canvas = tk.Canvas(self.color_list_frame, width=canvas_width, height=60, 
                          bg='#2d2d2d', highlightthickness=0)
        h_scroll = tk.Scrollbar(self.color_list_frame, orient=tk.HORIZONTAL, 
                               command=canvas.xview, bg='#404040', troughcolor='#606060')
        canvas.configure(xscrollcommand=h_scroll.set)
        canvas.pack(side=tk.TOP, fill=tk.X, expand=False)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        color_row_frame = tk.Frame(canvas, bg='#2d2d2d')
        canvas.create_window((0,0), window=color_row_frame, anchor='nw')

        # Gather all colors to display
        color_items = [('background_color', bg_color)]
        for i, color in enumerate(gradient_colors):
            color_items.append((f'gradient_{i+1}', color))
        for key, value in color_data.items():
            if key not in ['background_color', 'gradient_colors']:
                if isinstance(value, str) and (value.startswith("#") or value.lower() == "none"):
                    color_items.append((key, value))

        # Create color squares
        for idx, (key, value) in enumerate(color_items):
            self._create_color_square(color_row_frame, key, value)

        # Update scroll region
        color_row_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def _create_color_square(self, parent, key, value):
        """Create a single color square with label."""
        col_frame = tk.Frame(parent, width=40, height=50, bg='#2d2d2d')
        col_frame.pack(side=tk.LEFT, padx=4, pady=2)
        col_frame.pack_propagate(False)

        is_none = isinstance(value, str) and value.lower() == "none"
        display_color = "#2d2d2d" if is_none else value

        if is_none:
            # Canvas for diagonal line
            square_canvas = tk.Canvas(col_frame, width=32, height=18, bg=display_color, 
                                    highlightthickness=0, bd=0)
            square_canvas.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(2,0))
            square_canvas.create_line(2, 2, 30, 16, fill="#888", width=2)
        else:
            # Color square
            square = tk.Label(col_frame, width=2, height=1, bg=display_color, 
                            relief='solid', borderwidth=1)
            square.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(2,0))

        # Labels
        label = tk.Label(col_frame, text=key, bg='#2d2d2d', fg='#fff', font=('Arial', 8))
        label.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(2,0))
        
        hex_label = tk.Label(col_frame, text=value, bg='#2d2d2d', fg='#aaa', font=('Arial', 7))
        hex_label.pack(side=tk.TOP, fill=tk.X, expand=False)

    def load_logo_preview(self, logo_name):
        """Load and resize the selected logo for preview."""
        try:
            # Clear previous image reference
            self.logo_image = None
            
            if not logo_name or not self.logo_names:
                self.logo_preview_label.config(image='', text="No logo available")
                return
                
            logo_file = self.logo_name_to_file.get(logo_name)
            if not logo_file:
                self.logo_preview_label.config(image='', text="Logo file not found")
                return
                
            logo_path = os.path.join(SPC_LOGO_DIR, logo_file)
            if not os.path.isfile(logo_path):
                self.logo_preview_label.config(image='', text="Logo file not found")
                return
                
            # Open and resize the image
            img = Image.open(logo_path)
            
            # Calculate resize ratio maintaining aspect ratio
            width, height = img.size
            max_width, max_height = 150, 75
            
            width_ratio = max_width / width if width > max_width else 1
            height_ratio = max_height / height if height > max_height else 1
            ratio = min(width_ratio, height_ratio)
            
            if ratio < 1:
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(img)
            
            self.logo_preview_label.config(image=photo, text='')
            self.logo_image = photo  # Keep reference to prevent garbage collection
            
        except Exception as e:
            self.logo_preview_label.config(image='', text=f"Error: {str(e)}")
            print(f"Error loading logo: {e}")


    # =============================================================================
    # WIDGET CREATION METHODS
    # =============================================================================

    def create_widgets(self):
        """Create and layout all widgets in the application."""
        # Create main container frames for three columns
        self.col1_frame = ttk.Frame(self)
        self.col2_frame = ttk.Frame(self)
        self.col3_frame = ttk.Frame(self)
        
        self.col1_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.col2_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.col3_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Configure equal weight for all columns
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_columnconfigure(1, weight=1, uniform="column")
        self.grid_columnconfigure(2, weight=1, uniform="column")
        self.rowconfigure(0, weight=1)
        
        # Configure column frames
        for frame in [self.col1_frame, self.col2_frame, self.col3_frame]:
            frame.columnconfigure(0, weight=1)
        self.col3_frame.rowconfigure(2, weight=1)  # Info section expandable
        
        # Create sections
        self._create_column1_widgets()
        self._create_column2_widgets()
        self._create_column3_widgets()

    def _create_column1_widgets(self):
        """Create widgets for the first column (Tournament, Scoring, Web, Export)."""
        row = 0
        
        # Tournament Information Section
        self._create_tournament_section(self.col1_frame, row)
        row += 1
        
        # Scoring Section
        self._create_scoring_section(self.col1_frame, row)
        row += 1
        
        # Web Section
        self._create_web_section(self.col1_frame, row)
        row += 1
        
        # Export Section
        self._create_export_section(self.col1_frame, row)

    def _create_tournament_section(self, parent, row):
        """Create the Tournament Information section."""
        frame = ttk.LabelFrame(parent, text="Tournament Informations")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Date checkbox
        self.date_var = tk.BooleanVar(value=self.settings.get("date", False))
        ttk.Checkbutton(frame, text="Show Date", variable=self.date_var).grid(
            row=current_row, column=0, sticky="w"
        )
        current_row += 1

        # Tournament name
        ttk.Label(frame, text="Tournament Name:").grid(row=current_row, column=0, sticky="w")
        self.tournament_var = tk.StringVar(value=self.settings.get("tournament_name", ""))
        ttk.Entry(frame, textvariable=self.tournament_var).grid(
            row=current_row, column=1, sticky="ew"
        )
        current_row += 1

        # Event host
        ttk.Label(frame, text="Event Host:").grid(row=current_row, column=0, sticky="w")
        self.event_host_var = tk.StringVar(value=self.settings.get("event_host", ""))
        ttk.Entry(frame, textvariable=self.event_host_var).grid(
            row=current_row, column=1, sticky="ew"
        )

    def _create_scoring_section(self, parent, row):
        """Create the Scoring section."""
        frame = ttk.LabelFrame(parent, text="Scoring")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Scoring system dropdown
        ttk.Label(frame, text="Scoring System:").grid(row=current_row, column=0, sticky="w")
        self.scoring_var = tk.StringVar(value=self.settings.get(
            "scoring_system", self.scoring_systems[0] if self.scoring_systems else ""
        ))
        scoring_menu = ttk.OptionMenu(frame, self.scoring_var, self.scoring_var.get(), *self.scoring_systems)
        scoring_menu.grid(row=current_row, column=1, sticky="ew")
        self.scoring_var.trace_add("write", self.update_scoring_description)
        current_row += 1

        # Description area
        ttk.Label(frame, text="Description:").grid(row=current_row, column=0, sticky="nw", pady=(5,0))
        current_row += 1
        
        desc_frame = tk.Frame(frame, bg='#2d2d2d')
        desc_frame.grid(row=current_row, column=0, columnspan=2, sticky="ew", pady=(0,5))
        
        self.scoring_desc_text = tk.Text(desc_frame, height=4, width=40, wrap=tk.WORD,
                                        bg='#404040', fg='#ffffff', font=('Arial', 9),
                                        relief='solid', borderwidth=1)
        scrollbar_desc = tk.Scrollbar(desc_frame, bg='#404040', troughcolor='#606060',
                                    activebackground='#505050')
        
        self.scoring_desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_desc.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scoring_desc_text.config(yscrollcommand=scrollbar_desc.set)
        scrollbar_desc.config(command=self.scoring_desc_text.yview)
        
        # Load initial description
        initial_description = get_scoring_description(self.scoring_var.get())
        self.scoring_desc_text.insert(tk.END, initial_description)
        self.scoring_desc_text.config(state=tk.DISABLED)
        current_row += 1

        # Team mode checkboxes
        self.team_mode_var = tk.BooleanVar(value=self.settings.get("team_mode", False))
        ttk.Checkbutton(frame, text="Team Mode", variable=self.team_mode_var).grid(
            row=current_row, column=0, sticky="w"
        )
        current_row += 1

        self.auto_team_var = tk.BooleanVar(value=self.settings.get("auto_team", False))
        ttk.Checkbutton(frame, text="Auto Team", variable=self.auto_team_var).grid(
            row=current_row, column=0, sticky="w"
        )
        current_row += 1
        
        self.variable_team_var = tk.BooleanVar(value=self.settings.get("variable_team", False))
        ttk.Checkbutton(frame, text="Variable Team", variable=self.variable_team_var).grid(
            row=current_row, column=0, sticky="w"
        )

    def _create_web_section(self, parent, row):
        """Create the Web section."""
        frame = ttk.LabelFrame(parent, text="Web")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(0, weight=0)  # Label column
        frame.columnconfigure(1, weight=1)  # Content column
        
        current_row = 0
        
        # Web title
        ttk.Label(frame, text="Title:").grid(row=current_row, column=0, sticky="w")
        self.title_web_var = tk.StringVar(value=self.settings.get(
            "title_web", "SPC V7 - Live Tournament Leaderboard"
        ))
        ttk.Entry(frame, textvariable=self.title_web_var).grid(
            row=current_row, column=1, sticky="ew", pady=2
        )
        current_row += 1
        
        # Auth token
        ttk.Label(frame, text="Ngrok Token:").grid(row=current_row, column=0, sticky="w")
        self.auth_token_var = tk.StringVar(value=self.settings.get("auth_token", ""))
        ttk.Entry(frame, textvariable=self.auth_token_var).grid(
            row=current_row, column=1, sticky="ew", pady=2
        )
        current_row += 1
        
        # Information note
        web_note = ttk.Label(
            frame,
            text="Go to https://dashboard.ngrok.com/get-started/your-authtoken to copy the token",
            font=('Arial', 8, 'italic'),
            foreground='#aaaaaa',
            background='#2d2d2d',
            wraplength=260,
            justify='left'
        )
        web_note.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=5, pady=(0,8))

    def _create_export_section(self, parent, row):
        """Create the Export section."""
        frame = ttk.LabelFrame(parent, text="Export")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        current_row = 0

        # Initialize export variables
        self.enable_graph_export_var = tk.BooleanVar(value=self.settings.get("enable_graph_export", True))
        self.enable_graph_placement_export_var = tk.BooleanVar(value=self.settings.get("enable_graph_placement_export", True))
        self.enable_spreadsheet_export_var = tk.BooleanVar(value=self.settings.get("enable_spreadsheet_export", True))

        # Graph export with density setting
        ttk.Checkbutton(frame, text="Enable Graph Export", variable=self.enable_graph_export_var).grid(
            row=current_row, column=0, sticky="w"
        )
        
        graph_density_frame = tk.Frame(frame, bg='#2d2d2d')
        graph_density_frame.grid(row=current_row, column=1, sticky="ew", padx=5)
        ttk.Label(graph_density_frame, text="Density (dpi):").pack(side=tk.LEFT, padx=(0,5))
        self.graph_pixel_density_var = tk.StringVar(value=str(self.settings.get("graphs_pixel_density", 600)))
        ttk.Entry(graph_density_frame, textvariable=self.graph_pixel_density_var, width=5).pack(side=tk.LEFT)
        current_row += 1
        
        # Graph placement export
        ttk.Checkbutton(frame, text="Enable Graph Placement Export", 
                       variable=self.enable_graph_placement_export_var).grid(
            row=current_row, column=0, sticky="w"
        )
        current_row += 1
        
        # Spreadsheet export with density setting
        ttk.Checkbutton(frame, text="Enable Spreadsheet Export", 
                       variable=self.enable_spreadsheet_export_var).grid(
            row=current_row, column=0, sticky="w"
        )
        
        sheet_density_frame = tk.Frame(frame, bg='#2d2d2d')
        sheet_density_frame.grid(row=current_row, column=1, sticky="ew", padx=5)
        ttk.Label(sheet_density_frame, text="Density (dpi):").pack(side=tk.LEFT, padx=(0,5))
        self.spreadsheet_pixel_density_var = tk.StringVar(value=str(self.settings.get("spreadsheet_pixel_density", 150)))
        ttk.Entry(sheet_density_frame, textvariable=self.spreadsheet_pixel_density_var, width=5).pack(side=tk.LEFT)
        current_row += 1

        # Warning text
        warning_label = ttk.Label(
            frame,
            text="Exporting leaderboard (as a picture) can significantly increase load time.\nIt is recommended to enable this only after the final round.",
            foreground="#ffcc00",
            font=('Arial', 8, 'italic'),
            background='#2d2d2d',
            wraplength=260,
            justify='left'
        )
        warning_label.grid(row=current_row, column=0, columnspan=2, sticky="w", padx=(5,0), pady=(0,8))

    def _create_column2_widgets(self):
        """Create widgets for the second column (Customization, Logo)."""
        row = 0
        
        # Customization Section
        self._create_customization_section(self.col2_frame, row)
        row += 1
        
        # Logo Section
        self._create_logo_section(self.col2_frame, row)

    def _create_column3_widgets(self):
        """Create widgets for the third column (Misc, Actions, Information)."""
        row = 0
        
        # Misc Section
        self._create_misc_section(self.col3_frame, row)
        row += 1
        
        # Actions Section
        self._create_actions_section(self.col3_frame, row)
        row += 1
        
        # Information Section
        self._create_information_section(self.col3_frame, row)


    # =============================================================================
    # SECTION CREATION METHODS (CONTINUED)
    # =============================================================================

    def _create_customization_section(self, parent, row):
        """Create the Customization section."""
        frame = ttk.LabelFrame(parent, text="Customization")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(0, weight=0)  # Label column
        frame.columnconfigure(1, weight=1)  # Content column
        
        current_row = 0

        # Custom fonts checkbox
        self.add_custom_fonts_var = tk.BooleanVar(value=self.settings.get("add_custom_fonts", False))
        ttk.Checkbutton(frame, text="Add Custom Fonts", variable=self.add_custom_fonts_var).grid(
            row=current_row, column=0, sticky="w", columnspan=2
        )
        current_row += 1

        # Selected font display
        self.selected_font_var = tk.StringVar()
        selected_font_label = ttk.Label(frame, textvariable=self.selected_font_var, 
                                       foreground='#00ff00', font=('Arial', 9, 'bold'))
        selected_font_label.grid(row=current_row, column=0, columnspan=2, sticky="w", pady=(0, 5))
        current_row += 1

        # Font family listbox
        self._create_font_selection(frame, current_row)
        current_row += 1

        # Font weight dropdown
        ttk.Label(frame, text="Font Weight:").grid(row=current_row, column=0, sticky="w")
        self.font_weight_var = tk.StringVar(value=self.settings.get("font_weight", "Regular"))
        
        # Get initial weights for selected family
        if hasattr(self, 'font_family_listbox') and self.font_family_listbox.curselection():
            selected_family = self.font_family_listbox.get(self.font_family_listbox.curselection()[0])
            initial_weights = get_font_weights_from_family(self.font_families, selected_family)
        else:
            initial_weights = ["Regular"]
            
        if not initial_weights:
            initial_weights = ["Regular"]
            
        self.font_weight_menu = ttk.OptionMenu(frame, self.font_weight_var, 
                                             self.font_weight_var.get(), *initial_weights)
        self.font_weight_menu.grid(row=current_row, column=1, sticky="ew")
        current_row += 1

        # Color scheme dropdown
        ttk.Label(frame, text="Color Scheme:").grid(row=current_row, column=0, sticky="w")
        current_color_path = self.settings.get("color_scheme", "")
        current_color_name = os.path.splitext(os.path.basename(current_color_path))[0] if current_color_path else ""
        self.color_scheme_var = tk.StringVar(value=current_color_name if current_color_name in self.color_names else (self.color_names[0] if self.color_names else ""))
        color_dropdown = ttk.OptionMenu(frame, self.color_scheme_var, self.color_scheme_var.get(), *self.color_names)
        color_dropdown.grid(row=current_row, column=1, sticky="ew")
        current_row += 1

        # Color preview section
        self._create_color_preview_section(frame, current_row)

        # Initialize the color preview and list
        self.update_color_preview()
        self.color_scheme_var.trace_add("write", self.update_color_preview)

    def _create_font_selection(self, parent, row):
        """Create the font family selection widgets."""
        ttk.Label(parent, text="Font Family:").grid(row=row, column=0, sticky="nw")
        
        # Create frame for listbox and scrollbar
        font_frame = tk.Frame(parent, bg='#2d2d2d')
        font_frame.grid(row=row, column=1, sticky="ew", pady=2)
        
        # Extract current family from settings
        current_font_path = self.settings.get("custom_font", "")
        current_family = self._extract_font_family_from_path(current_font_path)
        
        family_names = sorted(self.font_families.keys())
        if not family_names:
            family_names = ["No fonts found"]
        
        # Create listbox with scrollbar
        self.font_family_listbox = tk.Listbox(font_frame, height=6, bg='#404040', fg='#ffffff', 
                                             selectbackground='#505050', selectforeground='#ffffff',
                                             borderwidth=1, relief='solid', font=('Arial', 9))
        scrollbar_font = tk.Scrollbar(font_frame, bg='#404040', troughcolor='#606060', 
                                     activebackground='#505050')
        
        self.font_family_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_font.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure scrollbar
        self.font_family_listbox.config(yscrollcommand=scrollbar_font.set)
        scrollbar_font.config(command=self.font_family_listbox.yview)
        
        # Populate listbox
        for family in family_names:
            self.font_family_listbox.insert(tk.END, family)
        
        # Select current family
        if current_family in family_names:
            index = family_names.index(current_family)
            self.font_family_listbox.selection_set(index)
            self.font_family_listbox.see(index)
            self.selected_font_var.set(f"Selected: {current_family}")
        elif family_names:
            self.font_family_listbox.selection_set(0)
            self.selected_font_var.set(f"Selected: {family_names[0]}")
        
        # Bind font family selection changes
        if family_names != ["No fonts found"]:
            self.font_family_listbox.bind('<<ListboxSelect>>', self.update_font_weights)

    def _extract_font_family_from_path(self, font_path):
        """Extract font family name from font path."""
        if not font_path:
            return ""
            
        current_filename = os.path.basename(font_path)
        base_name = os.path.splitext(current_filename)[0]
        if '-' in base_name:
            return base_name.rsplit('-', 1)[0]
        else:
            return base_name

    def _create_color_preview_section(self, parent, row):
        """Create the color preview section."""
        # Preview label and frame
        ttk.Label(parent, text="Preview:").grid(row=row, column=0, sticky="nw", pady=(5, 0))
        row += 1
        
        self.color_preview_frame = tk.Frame(parent, bg='#2d2d2d')
        self.color_preview_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(2, 5))
        row += 1
        
        # Color list section
        ttk.Label(parent, text="Colors:").grid(row=row, column=0, sticky="nw", pady=(2, 0))
        row += 1
        
        self.color_list_frame = tk.Frame(parent, bg='#2d2d2d')
        self.color_list_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 8))

    def _create_logo_section(self, parent, row):
        """Create the Logo section."""
        frame = ttk.LabelFrame(parent, text="Logo")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        current_row = 0

        # Enable logo checkbox
        self.logo_var = tk.BooleanVar(value=self.settings.get("logo", False))
        ttk.Checkbutton(frame, text="Enable Logo", variable=self.logo_var).grid(
            row=current_row, column=0, sticky="w"
        )
        current_row += 1

        # Logo file dropdown
        ttk.Label(frame, text="Logo File:").grid(row=current_row, column=0, sticky="w")
        current_logo_path = self.settings.get("logo_path", "")
        current_logo_name = os.path.splitext(os.path.basename(current_logo_path))[0] if current_logo_path else ""
        self.logo_file_var = tk.StringVar(value=current_logo_name if current_logo_name in self.logo_names else (self.logo_names[0] if self.logo_names else ""))
        
        logo_menu = ttk.OptionMenu(frame, self.logo_file_var, self.logo_file_var.get(), *self.logo_names, 
                                 command=lambda _: self.update_logo_preview())
        logo_menu.grid(row=current_row, column=1, sticky="ew")
        current_row += 1

        # Logo preview
        self._create_logo_preview(frame, current_row)
        current_row += 1

        # Zoom slider
        ttk.Label(frame, text="Zoom Logo:").grid(row=current_row, column=0, sticky="w")
        self.zoom_logo_var = tk.DoubleVar(value=self.settings.get("zoom_logo", 1.0))
        zoom_scale = tk.Scale(frame, variable=self.zoom_logo_var, from_=0.01, to=0.3, 
                             resolution=0.005, orient="horizontal",
                             bg='#404040', fg='#ffffff', activebackground='#505050', 
                             highlightbackground='#2d2d2d', troughcolor='#606060')
        zoom_scale.grid(row=current_row, column=1, sticky="ew")
        current_row += 1
        
        # Vertical offset slider
        ttk.Label(frame, text="Vertical Offset:").grid(row=current_row, column=0, sticky="w")
        self.logo_vertical_offset_var = tk.DoubleVar(value=self.settings.get("logo_vertical_offset", 0.0))
        vertical_offset_scale = tk.Scale(frame, variable=self.logo_vertical_offset_var, 
                                       from_=-0.2, to=0.2, resolution=0.01, orient="horizontal",
                                       bg='#404040', fg='#ffffff', activebackground='#505050', 
                                       highlightbackground='#2d2d2d', troughcolor='#606060')
        vertical_offset_scale.grid(row=current_row, column=1, sticky="ew")

    def _create_logo_preview(self, parent, row):
        """Create the logo preview widget."""
        ttk.Label(parent, text="Preview:").grid(row=row, column=0, sticky="nw", pady=5)
        
        # Frame to contain the logo preview with fixed size
        preview_frame = tk.Frame(parent, width=150, height=80, bg='#404040', bd=1, relief=tk.SUNKEN)
        preview_frame.grid(row=row, column=1, sticky="w", pady=5)
        preview_frame.pack_propagate(False)
        
        # Label to show the logo image
        self.logo_preview_label = tk.Label(preview_frame, bg='#404040', fg='#ffffff', 
                                         text="No logo selected", font=('Arial', 9),
                                         anchor='center', justify='center')
        self.logo_preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Load initial preview
        self.load_logo_preview(self.logo_file_var.get())

    def _create_misc_section(self, parent, row):
        """Create the Misc section."""
        frame = ttk.LabelFrame(parent, text="Misc")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        current_row = 0

        # Game saver key setting
        ttk.Label(frame, text="Game Saver Key:").grid(row=current_row, column=0, sticky="w", padx=(5,0))
        self.game_saver_key_var = tk.StringVar(value=self.settings.get("activate_game_saver_key", "m"))
        key_entry = ttk.Entry(frame, textvariable=self.game_saver_key_var, width=5)
        key_entry.grid(row=current_row, column=1, sticky="w", padx=5, pady=5)
        
        # Explanatory note
        note_label = ttk.Label(
            frame,
            text="The game will be saved using Ctrl + the key you specify above",
            font=('Arial', 8, 'italic'),
            background='#2d2d2d',
            wraplength=260,
            justify='left'
        )
        note_label.grid(row=current_row+1, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

    def _create_actions_section(self, parent, row):
        """Create the Actions section."""
        frame = ttk.LabelFrame(parent, text="Actions")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # Create a 2x2 grid of buttons
        buttons = [
            ("Save Tournament to Folder", self.save_tournament, 0, 0),
            ("DELETE ROUNDS", self.delete_rounds, 0, 1),
            ("Delete matplotlib fontlist", delete_fontlist_files, 1, 0),
            ("Save Settings", self.save, 1, 1, 'Green.TButton')
        ]
        
        for button_data in buttons:
            text, command, btn_row, btn_col = button_data[:4]
            style = button_data[4] if len(button_data) > 4 else None
            
            btn = ttk.Button(frame, text=text, command=command)
            if style:
                btn.configure(style=style)
                
            btn.grid(row=btn_row, column=btn_col, sticky="ew", 
                    padx=(10,5) if btn_col == 0 else (5,10), 
                    pady=(10,5) if btn_row == 0 else (5,10))

    def _create_information_section(self, parent, row):
        """Create the Information section."""
        frame = ttk.LabelFrame(parent, text="Informations")
        frame.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Create frame for text widget and scrollbar
        info_text_frame = tk.Frame(frame, bg='#2d2d2d')
        info_text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        info_text_frame.columnconfigure(0, weight=1)
        info_text_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        info_text = tk.Text(info_text_frame, width=40, wrap=tk.WORD,
                           bg='#404040', fg='#ffffff', font=('Arial', 9),
                           relief='solid', borderwidth=1)
        info_scrollbar = tk.Scrollbar(info_text_frame, bg='#404040', troughcolor='#606060',
                                     activebackground='#505050')
        
        info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        info_text.config(yscrollcommand=info_scrollbar.set)
        info_scrollbar.config(command=info_text.yview)
        
        # Insert the information text and make read-only
        info_text.insert(tk.END, INFORMATION_TEXT)
        info_text.config(state=tk.DISABLED)


    # =============================================================================
    # ACTION METHODS
    # =============================================================================
    def save_tournament(self):
        """Save tournament data to a folder chosen by the user."""
        # Ask user for destination directory
        dest_dir = filedialog.askdirectory(title="Select folder to save tournament")
        if not dest_dir:
            return

        # Create folder name from tournament data
        tournament_name = self.settings.get("tournament_name", "").strip()
        event_host = self.settings.get("event_host", "").strip()
        date_str = datetime.now().strftime("%Y_%m_%d")
        folder_name = f"{date_str} - {tournament_name} - {event_host}"
        save_path = os.path.join(dest_dir, folder_name)

        try:
            os.makedirs(save_path, exist_ok=True)
            files_copied = 0

            # Copy all files from exports directory
            exports_dir = os.path.join(BASE_DIR, "exports")
            if os.path.isdir(exports_dir):
                files_copied += self._copy_directory_contents(exports_dir, save_path)

            # Copy all .txt files from root directory
            files_copied += self._copy_txt_files_from_root(save_path)

            messagebox.showinfo("Success", f"Tournament saved to:\n{save_path}\n{files_copied} files copied.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tournament: {e}")

    def _copy_directory_contents(self, source_dir, dest_dir):
        """Copy all contents from source directory to destination directory."""
        files_copied = 0
        for root, dirs, files in os.walk(source_dir):
            for fname in files:
                src = os.path.join(root, fname)
                rel_path = os.path.relpath(src, source_dir)
                dest = os.path.join(dest_dir, rel_path)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                files_copied += 1
        return files_copied

    def _copy_txt_files_from_root(self, dest_dir):
        """Copy all .txt files from the root directory."""
        files_copied = 0
        for fname in os.listdir(BASE_DIR):
            if fname.lower().endswith(".txt"):
                src = os.path.join(BASE_DIR, fname)
                if os.path.isfile(src):
                    shutil.copy2(src, dest_dir)
                    files_copied += 1
        return files_copied

    def delete_rounds(self):
        """Delete all .txt files from the root directory after confirmation."""
        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "This will delete ALL .txt files in the root folder.\nAre you sure you want to continue?"
        )
        if not confirm:
            return

        deleted = []
        errors = []
        
        for fname in os.listdir(BASE_DIR):
            if fname.lower().endswith(".txt"):
                path = os.path.join(BASE_DIR, fname)
                try:
                    os.remove(path)
                    deleted.append(fname)
                except Exception as e:
                    errors.append(f"{fname}: {e}")
        
        # Show results
        if deleted:
            messagebox.showinfo("Success", f"Deleted: {', '.join(deleted)}")
        elif not errors:
            messagebox.showinfo("Info", "No .txt files found.")
        if errors:
            messagebox.showerror("Error", "\n".join(errors))

    def save(self):
        """Save all current settings to the settings file."""
        # Update settings with current values
        settings_mapping = {
            "team_mode": self.team_mode_var.get(),
            "auto_team": self.auto_team_var.get(), 
            "variable_team": self.variable_team_var.get(),
            "logo": self.logo_var.get(),
            "zoom_logo": self.zoom_logo_var.get(),
            "logo_vertical_offset": self.logo_vertical_offset_var.get(),
            "add_custom_fonts": self.add_custom_fonts_var.get(),
            "font_weight": self.font_weight_var.get(),
            "date": self.date_var.get(),
            "scoring_system": self.scoring_var.get(),
            "tournament_name": self.tournament_var.get(),
            "event_host": self.event_host_var.get(),
            "enable_graph_export": self.enable_graph_export_var.get(),
            "enable_graph_placement_export": self.enable_graph_placement_export_var.get(),
            "enable_spreadsheet_export": self.enable_spreadsheet_export_var.get(),
            "activate_game_saver_key": self.game_saver_key_var.get(),
            "title_web": self.title_web_var.get(),
            "auth_token": self.auth_token_var.get()
        }

        # Update all settings
        for key, value in settings_mapping.items():
            self.settings[key] = value

        # Handle special cases that need processing
        self._save_special_settings()

        try:
            save_settings(self.settings)
            messagebox.showinfo("Success", "Settings saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _save_special_settings(self):
        """Handle special settings that need additional processing."""
        # Save logo path from selected logo name
        selected_logo_name = self.logo_file_var.get()
        self.settings["logo_path"] = self.logo_name_to_path.get(selected_logo_name, "")
        
        # Save color scheme path from selected color scheme name
        selected_color_name = self.color_scheme_var.get()
        self.settings["color_scheme"] = self.color_name_to_path.get(selected_color_name, "")
        
        # Save font path from family and weight selection
        selection = self.font_family_listbox.curselection()
        if selection:
            selected_family = self.font_family_listbox.get(selection[0])
            selected_weight = self.font_weight_var.get()
            font_path = get_font_path_from_family_weight(self.font_families, selected_family, selected_weight)
            self.settings["custom_font"] = font_path
        
        # Save pixel density settings with validation
        try:
            self.settings["graphs_pixel_density"] = int(self.graph_pixel_density_var.get())
        except ValueError:
            self.settings["graphs_pixel_density"] = 600  # Default
            
        try:
            self.settings["spreadsheet_pixel_density"] = int(self.spreadsheet_pixel_density_var.get())
        except ValueError:
            self.settings["spreadsheet_pixel_density"] = 150  # Default


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    app = SettingsEditor()
    app.mainloop()
