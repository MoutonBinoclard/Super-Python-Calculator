import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
import pathlib
import shutil
from datetime import datetime
import importlib.util
from PIL import Image, ImageTk  # Add PIL import for image handling

informations = """Save tournament to folder : Saves all graph and round in a folder
Delete rounds : Deletes all rounds in the root folder (No turning back)
Save settings : Saves the current settings to settings.json
Delete matplotlib fontlist : If the fonts doesnt work, this might help"""

# Determine if running as a PyInstaller executable
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Executable's directory
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Script's directory

SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
SPC_SCORING_DIR = os.path.join(BASE_DIR, "scoring")
SPC_LOGO_DIR = os.path.join(BASE_DIR, "logo")
SPC_COLOR_SCHEME_DIR = os.path.join(BASE_DIR, "color_schemes")

WINDOWS_FONTS_DIR = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')

def load_settings():
    # Valeurs par défaut si settings.json n'existe pas
    default_settings = {
        "date": False,
        "tournament_name": "",
        "event_host": "",
        "scoring_system": "",
        "team_mode": False,
        "auto_team": False,
        "add_custom_fonts": False,
        "custom_font": "",
        "font_weight": "Regular",
        "color_scheme": "",
        "logo": False,
        "logo_path": "",
        "zoom_logo": 1.0
    }
    if not os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4)
        return default_settings
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

def load_scoring_systems():
    # List all files in SPC_scoring directory, remove extension
    if os.path.isdir(SPC_SCORING_DIR):
        files = os.listdir(SPC_SCORING_DIR)
        scoring_names = [os.path.splitext(f)[0] for f in files if os.path.isfile(os.path.join(SPC_SCORING_DIR, f))]
        return sorted(scoring_names)
    return []

def get_scoring_description(scoring_name):
    """Load the description from a scoring system module."""
    if not scoring_name:
        return ""
    
    try:
        # Construct the file path
        file_path = os.path.join(SPC_SCORING_DIR, f"{scoring_name}.py")
        if not os.path.exists(file_path):
            return "Description not available"
        
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location(f"scoring_{scoring_name}", file_path)
        if spec is None or spec.loader is None:
            return "Failed to load scoring system"
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the description variable
        if hasattr(module, 'desc'):
            return module.desc
        else:
            return "No description available"
    
    except Exception as e:
        return f"Error loading description: {str(e)}"

def load_logo_files():
    # List all files in SPC_logo directory, remove extension
    if os.path.isdir(SPC_LOGO_DIR):
        files = os.listdir(SPC_LOGO_DIR)
        logo_files = [f for f in files if os.path.isfile(os.path.join(SPC_LOGO_DIR, f))]
        logo_names = [os.path.splitext(f)[0] for f in logo_files]
        return sorted(logo_names), logo_files
    return [], []

def load_color_schemes():
    # List all .json files in SPC_color_schemes directory, remove extension
    if os.path.isdir(SPC_COLOR_SCHEME_DIR):
        files = os.listdir(SPC_COLOR_SCHEME_DIR)
        color_files = [f for f in files if os.path.isfile(os.path.join(SPC_COLOR_SCHEME_DIR, f)) and f.lower().endswith('.json')]
        color_names = [os.path.splitext(f)[0] for f in color_files]
        return sorted(color_names), color_files
    return [], []

def get_matplotlib_config_dir():
    # Use matplotlib's logic if available, else fallback to user home
    try:
        import matplotlib
        return matplotlib.get_configdir()
    except Exception:
        # Fallback: ~/.matplotlib or platform equivalent
        return os.path.join(os.path.expanduser("~"), ".matplotlib")

def delete_fontlist_files():
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

def get_font_weights(font_path):
    """Extract available font weights from a font file."""
    if not font_path or not os.path.isfile(font_path):
        return []
    
    try:
        # Try to use fontTools if available
        from fontTools.ttLib import TTFont
        font = TTFont(font_path)
        
        # Get the name table
        name_table = font['name']
        weights = set()
        
        # Look for subfamily names (ID 2) which often contain weight info
        for record in name_table.names:
            if record.nameID == 2:  # Subfamily name
                subfamily = record.toUnicode() if hasattr(record, 'toUnicode') else str(record)
                weights.add(subfamily)
        
        font.close()
        return sorted(list(weights)) if weights else ["Regular"]
        
    except ImportError:
        # Fallback: return common weight names if fontTools not available
        return ["Regular", "Bold", "Light", "Medium", "Thin", "Black"]
    except Exception:
        # If font parsing fails, return basic options
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

class SettingsEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings Editor")
        # Remove fixed geometry - we'll calculate it automatically
        
        # Dark theme configuration
        self.configure(bg='#2d2d2d')
        
        # Configure ttk styles for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure dark theme colors
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabelframe', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TLabelframe.Label', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TLabel', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TButton', background='#404040', foreground='#ffffff')
        self.style.map('TButton', background=[('active', '#505050')])
        self.style.configure('TEntry', fieldbackground='#404040', foreground='#ffffff', bordercolor='#606060')
        self.style.configure('TCheckbutton', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TMenubutton', background='#404040', foreground='#ffffff', arrowcolor='#ffffff')
        self.style.map('TMenubutton', background=[('active', '#505050')])
        
        # Add custom style for green button
        self.style.configure('Green.TButton', background='#2ecc40', foreground='#ffffff')
        self.style.map('Green.TButton', background=[('active', '#27ae60')])

        self.settings = load_settings()
        self.scoring_systems = load_scoring_systems()
        self.logo_names, self.logo_files = load_logo_files()
        self.logo_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("logo", f).replace("\\", "/")
            for f in self.logo_files
        }
        self.logo_name_to_file = {
            os.path.splitext(f)[0]: f
            for f in self.logo_files
        }
        # Logo preview image reference
        self.logo_image = None
        self.color_names, self.color_files = load_color_schemes()
        self.color_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("color_schemes", f).replace("\\", "/")
            for f in self.color_files
        }
        self.font_families = load_font_families()
        self.create_widgets()
        
        # After creating widgets, adjust window size automatically
        self.adjust_window_size()

    def adjust_window_size(self):
        """Calculate and set the optimal window size based on content"""
        # Update the window to calculate widget sizes
        self.update_idletasks()
        
        # Get the required width and height
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        # Set minimum size constraints
        self.minsize(650, 550)
        
        # Center the window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the window size and position
        self.geometry(f"{width}x{height}+{x}+{y}")

    def update_font_weights(self, *args):
        """Update the font weight dropdown based on selected font family."""
        # Get selected family from listbox
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

    def load_logo_preview(self, logo_name):
        """Load and resize the selected logo for preview"""
        try:
            # Clear previous image reference
            self.logo_image = None
            
            # If no logo selected or preview not enabled, show blank
            if not logo_name or not self.logo_names:
                self.logo_preview_label.config(image='', text="No logo available")
                return
                
            # Get the file path
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
            max_width, max_height = 150, 100
            
            # Calculate resize ratio
            width_ratio = max_width / width if width > max_width else 1
            height_ratio = max_height / height if height > max_height else 1
            ratio = min(width_ratio, height_ratio)
            
            # Apply resize if needed
            if ratio < 1:
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Update the label
            self.logo_preview_label.config(image=photo, text='')
            
            # Keep a reference to prevent garbage collection
            self.logo_image = photo
            
        except Exception as e:
            self.logo_preview_label.config(image='', text=f"Error: {str(e)}")
            print(f"Error loading logo: {e}")

    def update_logo_preview(self, *args):
        """Update the logo preview when selection changes"""
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
            # Clear preview if not found
            for widget in self.color_preview_frame.winfo_children():
                widget.destroy()
            # Clear color list
            for widget in self.color_list_frame.winfo_children():
                widget.destroy()
            return
            
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
        for widget in self.color_preview_frame.winfo_children():
            widget.destroy()
        
        # Fixed-width approach for color blocks
        max_colors = 8  # Maximum number of colors we want to support in the display
        
        # Create a container frame with fixed width
        color_container = tk.Frame(self.color_preview_frame, bg='#2d2d2d')
        color_container.pack(fill=tk.X, expand=True)
        
        # Background color always gets a fixed proportion (about 25-30% of width)
        bg_frame = tk.Frame(color_container, width=80, height=30)
        bg_frame.pack(side=tk.LEFT, padx=2, pady=2)
        bg_frame.pack_propagate(False)  # Prevent frame from resizing
        
        # Background color label
        bg_label = tk.Label(
            bg_frame, 
            text="Background", 
            bg=bg_color, 
            fg="#fff" if bg_color.lower() != "#fff" else "#000"
        )
        bg_label.pack(fill=tk.BOTH, expand=True)
        
        # Calculate width for gradient colors (all equal)
        num_gradients = len(gradient_colors)
        if num_gradients > 0:
            # Create a frame to hold all gradient colors with equal spacing
            gradients_frame = tk.Frame(color_container, bg='#2d2d2d')
            gradients_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
            
            # Each gradient color gets equal width
            for idx, color in enumerate(gradient_colors):
                # Create fixed-width frame for each color
                color_frame = tk.Frame(gradients_frame, width=30, height=30)
                color_frame.pack(side=tk.LEFT, padx=1, fill=tk.Y)
                color_frame.pack_propagate(False)
                
                # Add the color label
                color_label = tk.Label(
                    color_frame, 
                    text=f"G{idx+1}", 
                    bg=color, 
                    fg="#fff" if color.lower() != "#fff" else "#000"
                )
                color_label.pack(fill=tk.BOTH, expand=True)
        
        # --- New horizontal color list with color squares ---
        # Clear previous color list widgets
        for widget in self.color_list_frame.winfo_children():
            widget.destroy()

        # Set a fixed, smaller width for the canvas (e.g., 260px)
        canvas_width = 260
        canvas = tk.Canvas(self.color_list_frame, width=canvas_width, height=60, bg='#2d2d2d', highlightthickness=0)
        h_scroll = tk.Scrollbar(self.color_list_frame, orient=tk.HORIZONTAL, command=canvas.xview, bg='#404040', troughcolor='#606060')
        canvas.configure(xscrollcommand=h_scroll.set)
        canvas.pack(side=tk.TOP, fill=tk.X, expand=False)  # expand=False keeps it at fixed width
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        color_row_frame = tk.Frame(canvas, bg='#2d2d2d')
        canvas.create_window((0,0), window=color_row_frame, anchor='nw')

        # Gather all colors to display: background + gradients + other keys
        color_items = []
        # Always show background_color first
        color_items.append(('background_color', bg_color))
        # Show gradient colors
        for i, color in enumerate(gradient_colors):
            color_items.append((f'gradient_{i+1}', color))
        # Show other color keys (excluding background and gradients)
        for key, value in color_data.items():
            if key not in ['background_color', 'gradient_colors']:
                if isinstance(value, str) and (value.startswith("#") or value.lower() == "none"):
                    color_items.append((key, value))

        # Create color squares side by side
        for idx, (key, value) in enumerate(color_items):
            col_frame = tk.Frame(color_row_frame, width=40, height=50, bg='#2d2d2d')
            col_frame.pack(side=tk.LEFT, padx=4, pady=2)
            col_frame.pack_propagate(False)

            # Color square
            square = tk.Label(col_frame, width=2, height=1, bg=value, relief='solid', borderwidth=1)
            square.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(2,0))
            # Color key label
            label = tk.Label(col_frame, text=key, bg='#2d2d2d', fg='#fff', font=('Arial', 8))
            label.pack(side=tk.TOP, fill=tk.X, expand=False, pady=(2,0))
            # Hex code label
            hex_label = tk.Label(col_frame, text=value, bg='#2d2d2d', fg='#aaa', font=('Arial', 7))
            hex_label.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Update scroll region
        color_row_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def create_widgets(self):
        # Create main container frames for left and right columns
        left_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)
        
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Configure weight for the columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        # --- LEFT COLUMN ---
        left_row = 0

        # --- Header Section ---
        header_frame = ttk.LabelFrame(left_frame, text="Tournament Informations")
        header_frame.grid(row=left_row, column=0, sticky="ew", padx=5, pady=5)
        header_row = 0

        self.date_var = tk.BooleanVar(value=self.settings.get("date", False))
        ttk.Checkbutton(header_frame, text="Show Date", variable=self.date_var).grid(row=header_row, column=0, sticky="w")
        header_row += 1

        ttk.Label(header_frame, text="Tournament Name:").grid(row=header_row, column=0, sticky="w")
        self.tournament_var = tk.StringVar(value=self.settings.get("tournament_name", ""))
        ttk.Entry(header_frame, textvariable=self.tournament_var).grid(row=header_row, column=1, sticky="ew")
        header_row += 1

        # Event host section
        ttk.Label(header_frame, text="Event Host:").grid(row=header_row, column=0, sticky="w")
        self.event_host_var = tk.StringVar(value=self.settings.get("event_host", ""))
        ttk.Entry(header_frame, textvariable=self.event_host_var).grid(row=header_row, column=1, sticky="ew")
        header_row += 1

        header_frame.columnconfigure(1, weight=1)
        left_row += 1
        # --- End Header Section ---

        # --- Scoring Section ---
        scoring_frame = ttk.LabelFrame(left_frame, text="Scoring")
        scoring_frame.grid(row=left_row, column=0, sticky="ew", padx=5, pady=5)
        scoring_row = 0

        ttk.Label(scoring_frame, text="Scoring System:").grid(row=scoring_row, column=0, sticky="w")
        self.scoring_var = tk.StringVar(value=self.settings.get("scoring_system", self.scoring_systems[0] if self.scoring_systems else ""))
        scoring_menu = ttk.OptionMenu(scoring_frame, self.scoring_var, self.scoring_var.get(), *self.scoring_systems)
        scoring_menu.grid(row=scoring_row, column=1, sticky="ew")
        # Add trace to update description when scoring system changes
        self.scoring_var.trace_add("write", self.update_scoring_description)
        scoring_row += 1

        # Add description text area
        ttk.Label(scoring_frame, text="Description:").grid(row=scoring_row, column=0, sticky="nw", pady=(5,0))
        scoring_row += 1
        
        # Text widget for description with scrollbar
        desc_frame = tk.Frame(scoring_frame, bg='#2d2d2d')
        desc_frame.grid(row=scoring_row, column=0, columnspan=2, sticky="ew", pady=(0,5))
        
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
        self.scoring_desc_text.config(state=tk.DISABLED)  # Make read-only
        
        scoring_row += 1

        self.team_mode_var = tk.BooleanVar(value=self.settings.get("team_mode", False))
        ttk.Checkbutton(scoring_frame, text="Team Mode", variable=self.team_mode_var).grid(row=scoring_row, column=0, sticky="w")
        scoring_row += 1

        self.auto_team_var = tk.BooleanVar(value=self.settings.get("auto_team", False))
        ttk.Checkbutton(scoring_frame, text="Auto Team", variable=self.auto_team_var).grid(row=scoring_row, column=0, sticky="w")
        scoring_row += 1

        scoring_frame.columnconfigure(1, weight=1)
        left_row += 1
        # --- End Scoring Section ---

        # --- Customization Section (LEFT) ---
        customization_frame = ttk.LabelFrame(left_frame, text="Customization")
        customization_frame.grid(row=left_row, column=0, sticky="ew", padx=5, pady=5)
        # Configure the customization frame to expand horizontally
        customization_frame.columnconfigure(0, weight=0)  # Label column
        customization_frame.columnconfigure(1, weight=1)  # Content column
        customization_row = 0

        self.add_custom_fonts_var = tk.BooleanVar(value=self.settings.get("add_custom_fonts", False))
        ttk.Checkbutton(customization_frame, text="Add Custom Fonts", variable=self.add_custom_fonts_var).grid(row=customization_row, column=0, sticky="w", columnspan=2)
        customization_row += 1

        # Selected font display
        self.selected_font_var = tk.StringVar()
        selected_font_label = ttk.Label(customization_frame, textvariable=self.selected_font_var, 
                                       foreground='#00ff00', font=('Arial', 9, 'bold'))
        selected_font_label.grid(row=customization_row, column=0, columnspan=2, sticky="w", pady=(0, 5))
        customization_row += 1

        # Font family scrollable listbox
        ttk.Label(customization_frame, text="Font Family:").grid(row=customization_row, column=0, sticky="nw")
        
        # Create frame for listbox and scrollbar
        font_frame = tk.Frame(customization_frame, bg='#2d2d2d')
        font_frame.grid(row=customization_row, column=1, sticky="ew", pady=2)
        
        # Extract current family from settings
        current_font_path = self.settings.get("custom_font", "")
        current_family = ""
        if current_font_path:
            current_filename = os.path.basename(current_font_path)
            base_name = os.path.splitext(current_filename)[0]
            if '-' in base_name:
                current_family = base_name.rsplit('-', 1)[0]
            else:
                current_family = base_name
        
        family_names = sorted(self.font_families.keys())
        if not family_names:
            family_names = ["No fonts found"]
        
        # Create listbox with scrollbar (reduced height to 6 lines to save vertical space)
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
        
        # Select current family and update display
        if current_family in family_names:
            index = family_names.index(current_family)
            self.font_family_listbox.selection_set(index)
            self.font_family_listbox.see(index)
            self.selected_font_var.set(f"Selected: {current_family}")
        elif family_names:
            self.font_family_listbox.selection_set(0)
            self.selected_font_var.set(f"Selected: {family_names[0]}")
        
        customization_row += 1

        # Font weight dropdown
        ttk.Label(customization_frame, text="Font Weight:").grid(row=customization_row, column=0, sticky="w")
        self.font_weight_var = tk.StringVar(value=self.settings.get("font_weight", "Regular"))
        
        # Get initial weights for selected family
        if self.font_family_listbox.curselection():
            selected_family = self.font_family_listbox.get(self.font_family_listbox.curselection()[0])
            initial_weights = get_font_weights_from_family(self.font_families, selected_family)
        else:
            initial_weights = ["Regular"]
            
        if not initial_weights:
            initial_weights = ["Regular"]
        self.font_weight_menu = ttk.OptionMenu(customization_frame, self.font_weight_var, self.font_weight_var.get(), *initial_weights)
        self.font_weight_menu.grid(row=customization_row, column=1, sticky="ew")
        customization_row += 1

        # Bind font family selection changes to update weights
        if family_names != ["No fonts found"]:
            self.font_family_listbox.bind('<<ListboxSelect>>', self.update_font_weights)

        # Color scheme dropdown
        ttk.Label(customization_frame, text="Color Scheme:").grid(row=customization_row, column=0, sticky="w")
        current_color_path = self.settings.get("color_scheme", "")
        current_color_name = os.path.splitext(os.path.basename(current_color_path))[0] if current_color_path else ""
        self.color_scheme_var = tk.StringVar(value=current_color_name if current_color_name in self.color_names else (self.color_names[0] if self.color_names else ""))
        color_dropdown = ttk.OptionMenu(customization_frame, self.color_scheme_var, self.color_scheme_var.get(), *self.color_names)
        color_dropdown.grid(row=customization_row, column=1, sticky="ew")
        customization_row += 1

        # --- Color scheme preview zone ---
        ttk.Label(customization_frame, text="Preview:").grid(row=customization_row, column=0, sticky="nw", pady=(5, 0))
        customization_row += 1
        
        self.color_preview_frame = tk.Frame(customization_frame, bg='#2d2d2d')
        self.color_preview_frame.grid(row=customization_row, column=0, columnspan=2, sticky="ew", pady=(2, 5))
        customization_row += 1
        
        # --- Color list section ---
        ttk.Label(customization_frame, text="Colors:").grid(row=customization_row, column=0, sticky="nw", pady=(2, 0))
        customization_row += 1
        
        # Create frame for color list canvas with horizontal scrollbar
        self.color_list_frame = tk.Frame(customization_frame, bg='#2d2d2d')
        self.color_list_frame.grid(row=customization_row, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        customization_row += 1

        # Configure left_frame to expand horizontally
        left_frame.columnconfigure(0, weight=1)

        # Initialize the color preview and list
        self.update_color_preview()
        self.color_scheme_var.trace_add("write", self.update_color_preview)
        # --- End color scheme preview zone ---

        # --- RIGHT COLUMN ---
        right_row = 0
        
        # --- Logo Section (RIGHT) ---
        logo_frame = ttk.LabelFrame(right_frame, text="Logo")
        logo_frame.grid(row=right_row, column=0, sticky="ew", padx=5, pady=5)
        logo_row = 0

        self.logo_var = tk.BooleanVar(value=self.settings.get("logo", False))
        ttk.Checkbutton(logo_frame, text="Enable Logo", variable=self.logo_var).grid(row=logo_row, column=0, sticky="w")
        logo_row += 1

        # Logo file dropdown
        ttk.Label(logo_frame, text="Logo File:").grid(row=logo_row, column=0, sticky="w")
        # Get current logo path and extract the filename without extension
        current_logo_path = self.settings.get("logo_path", "")
        current_logo_name = os.path.splitext(os.path.basename(current_logo_path))[0] if current_logo_path else ""
        self.logo_file_var = tk.StringVar(value=current_logo_name if current_logo_name in self.logo_names else (self.logo_names[0] if self.logo_names else ""))
        
        # Create dropdown menu for logo selection
        logo_menu = ttk.OptionMenu(logo_frame, self.logo_file_var, self.logo_file_var.get(), *self.logo_names, 
                                 command=lambda _: self.update_logo_preview())
        logo_menu.grid(row=logo_row, column=1, sticky="ew")
        logo_row += 1

        # Logo preview label on the right side
        ttk.Label(logo_frame, text="Preview:").grid(row=logo_row, column=0, sticky="nw", pady=5)
        # Frame to contain the logo preview with fixed size
        preview_frame = tk.Frame(logo_frame, width=150, height=100, bg='#404040', bd=1, relief=tk.SUNKEN)
        preview_frame.grid(row=logo_row, column=1, sticky="w", pady=5)
        preview_frame.pack_propagate(False)  # Prevent frame from resizing to fit content
        
        # Label to show the logo image
        self.logo_preview_label = tk.Label(preview_frame, bg='#404040', fg='#ffffff', 
                                         text="No logo selected", font=('Arial', 9),
                                         anchor='center', justify='center')
        self.logo_preview_label.pack(fill=tk.BOTH, expand=True)
        
        # Load initial preview
        self.load_logo_preview(self.logo_file_var.get())
        logo_row += 1

        ttk.Label(logo_frame, text="Zoom Logo:").grid(row=logo_row, column=0, sticky="w")
        self.zoom_logo_var = tk.DoubleVar(value=self.settings.get("zoom_logo", 1.0))
        # Configure Scale widget for dark theme
        zoom_scale = tk.Scale(logo_frame, variable=self.zoom_logo_var, from_=0.01, to=0.3, resolution=0.005, orient="horizontal",
                             bg='#404040', fg='#ffffff', activebackground='#505050', highlightbackground='#2d2d2d', troughcolor='#606060')
        zoom_scale.grid(row=logo_row, column=1, sticky="ew")
        logo_row += 1

        logo_frame.columnconfigure(1, weight=1)
        right_row += 1
        # --- End Logo Section (RIGHT) ---

        # --- Manage Tournament Section (RIGHT) ---
        save_tournament_frame = ttk.LabelFrame(right_frame, text="Manage Tournament")
        save_tournament_frame.grid(row=right_row, column=0, sticky="ew", padx=5, pady=5)
        # Configure columns to expand equally
        save_tournament_frame.columnconfigure(0, weight=1)
        save_tournament_frame.columnconfigure(1, weight=1)
        # Centered and same size buttons
        btn_save = ttk.Button(save_tournament_frame, text="Save Tournament to Folder", command=self.save_tournament)
        btn_delete = ttk.Button(save_tournament_frame, text="DELETE ROUNDS", command=self.delete_rounds)
        btn_save.grid(row=0, column=0, sticky="ew", padx=(10,5), pady=10)
        btn_delete.grid(row=0, column=1, sticky="ew", padx=(5,10), pady=10)
        right_row += 1
        # --- End Manage Tournament Section (RIGHT) ---

        # --- Actions Section (RIGHT) ---
        actions_frame = ttk.LabelFrame(right_frame, text="Actions")
        actions_frame.grid(row=right_row, column=0, sticky="ew", padx=5, pady=5)
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        
        # Swap button positions and add padding to match Manage Tournament
        # "Delete matplotlib fontlist" on left, "Save Settings" on right
        ttk.Button(
            actions_frame, 
            text="Delete matplotlib fontlist", 
            command=delete_fontlist_files
        ).grid(row=0, column=0, sticky="ew", padx=(10,5), pady=10)
        ttk.Button(
            actions_frame, 
            text="Save Settings", 
            command=self.save, 
            style='Green.TButton'
        ).grid(row=0, column=1, sticky="ew", padx=(5,10), pady=10)
        right_row += 1
        # --- End Actions Section (RIGHT) ---

        # --- Informations Section (RIGHT) ---
        info_frame = ttk.LabelFrame(right_frame, text="Informations")
        info_frame.grid(row=right_row, column=0, sticky="ew", padx=5, pady=5)
        info_frame.columnconfigure(0, weight=1)
        
        # Create frame for text widget and scrollbar
        info_text_frame = tk.Frame(info_frame, bg='#2d2d2d')
        info_text_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        info_text_frame.columnconfigure(0, weight=1)
        
        # Text widget for informations with scrollbar
        info_text = tk.Text(info_text_frame, height=7, width=40, wrap=tk.WORD,
                           bg='#404040', fg='#ffffff', font=('Arial', 9),
                           relief='solid', borderwidth=1)
        info_scrollbar = tk.Scrollbar(info_text_frame, bg='#404040', troughcolor='#606060',
                                     activebackground='#505050')
        
        info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        info_text.config(yscrollcommand=info_scrollbar.set)
        info_scrollbar.config(command=info_text.yview)
        
        # Insert the informations text and make read-only
        info_text.insert(tk.END, informations)
        info_text.config(state=tk.DISABLED)
        
        right_row += 1
        # --- End Informations Section (RIGHT) ---

    def save_tournament(self):
        # Ask user for destination directory
        dest_dir = filedialog.askdirectory(title="Select folder to save tournament")
        if not dest_dir:
            return

        # Get tournament name and event host from settings.json
        tournament_name = self.settings.get("tournament_name", "").strip()
        event_host = self.settings.get("event_host", "").strip()
        date_str = datetime.now().strftime("%Y_%m_%d")
        folder_name = f"{date_str} - {tournament_name} - {event_host}"
        save_path = os.path.join(dest_dir, folder_name)

        try:
            os.makedirs(save_path, exist_ok=True)
            files_copied = 0

            # Copy all files from SPC_exports (including subfolders)
            exports_dir = os.path.join(BASE_DIR, "exports")
            if os.path.isdir(exports_dir):
                for root, dirs, files in os.walk(exports_dir):
                    for fname in files:
                        src = os.path.join(root, fname)
                        rel_path = os.path.relpath(src, exports_dir)
                        dest = os.path.join(save_path, rel_path)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy2(src, dest)
                        files_copied += 1

            # Copy all .txt files from root (BASE_DIR)
            for fname in os.listdir(BASE_DIR):
                if fname.lower().endswith(".txt"):
                    src = os.path.join(BASE_DIR, fname)
                    if os.path.isfile(src):
                        shutil.copy2(src, save_path)
                        files_copied += 1

            messagebox.showinfo("Success", f"Tournament saved to:\n{save_path}\n{files_copied} files copied.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tournament: {e}")

    def delete_rounds(self):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "This will delete ALL .txt files in the root folder.\nAre you sure you want to continue?"
        )
        if not confirm:
            return

        # Delete all .txt files from the root (BASE_DIR)
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
        if deleted:
            messagebox.showinfo("Success", f"Deleted: {', '.join(deleted)}")
        elif not errors:
            messagebox.showinfo("Info", "No .txt files found.")
        if errors:
            messagebox.showerror("Error", "\n".join(errors))

    def save(self):
        self.settings["team_mode"] = self.team_mode_var.get()
        self.settings["auto_team"] = self.auto_team_var.get()
        # Save logo_path as full path using selected logo name
        selected_logo_name = self.logo_file_var.get()
        self.settings["logo_path"] = self.logo_name_to_path.get(selected_logo_name, "")
        self.settings["zoom_logo"] = self.zoom_logo_var.get()
        self.settings["logo"] = self.logo_var.get()
        # Save color_scheme as full path using selected color scheme name
        selected_color_name = self.color_scheme_var.get()
        self.settings["color_scheme"] = self.color_name_to_path.get(selected_color_name, "")
        self.settings["add_custom_fonts"] = self.add_custom_fonts_var.get()
        # Construct font path from family and weight
        selection = self.font_family_listbox.curselection()
        if selection:
            selected_family = self.font_family_listbox.get(selection[0])
            selected_weight = self.font_weight_var.get()
            font_path = get_font_path_from_family_weight(self.font_families, selected_family, selected_weight)
            self.settings["custom_font"] = font_path
        self.settings["font_weight"] = self.font_weight_var.get()
        self.settings["date"] = self.date_var.get()
        self.settings["scoring_system"] = self.scoring_var.get()
        self.settings["tournament_name"] = self.tournament_var.get()
        self.settings["event_host"] = self.event_host_var.get()
        try:
            save_settings(self.settings)
            messagebox.showinfo("Success", "Settings saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

if __name__ == "__main__":
    app = SettingsEditor()
    app.mainloop()
