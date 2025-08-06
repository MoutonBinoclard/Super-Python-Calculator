import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
import pathlib
import shutil
from datetime import datetime

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
        self.geometry("380x750")  # Increased height to accommodate taller listbox
        
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
        
        self.settings = load_settings()
        self.scoring_systems = load_scoring_systems()
        self.logo_names, self.logo_files = load_logo_files()
        self.logo_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("logo", f).replace("\\", "/")
            for f in self.logo_files
        }
        self.color_names, self.color_files = load_color_schemes()
        self.color_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("color_schemes", f).replace("\\", "/")
            for f in self.color_files
        }
        self.font_families = load_font_families()
        self.create_widgets()

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

    def create_widgets(self):
        row = 0

        # --- Header Section ---
        header_frame = ttk.LabelFrame(self, text="Tournament Informations")
        header_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
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
        row += 1
        # --- End Header Section ---

        # --- Scoring Section ---
        scoring_frame = ttk.LabelFrame(self, text="Scoring")
        scoring_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        scoring_row = 0

        ttk.Label(scoring_frame, text="Scoring System:").grid(row=scoring_row, column=0, sticky="w")
        self.scoring_var = tk.StringVar(value=self.settings.get("scoring_system", self.scoring_systems[0] if self.scoring_systems else ""))
        ttk.OptionMenu(scoring_frame, self.scoring_var, self.scoring_var.get(), *self.scoring_systems).grid(row=scoring_row, column=1, sticky="ew")
        scoring_row += 1

        self.team_mode_var = tk.BooleanVar(value=self.settings.get("team_mode", False))
        ttk.Checkbutton(scoring_frame, text="Team Mode", variable=self.team_mode_var).grid(row=scoring_row, column=0, sticky="w")
        scoring_row += 1

        self.auto_team_var = tk.BooleanVar(value=self.settings.get("auto_team", False))
        ttk.Checkbutton(scoring_frame, text="Auto Team", variable=self.auto_team_var).grid(row=scoring_row, column=0, sticky="w")
        scoring_row += 1

        scoring_frame.columnconfigure(1, weight=1)
        row += 1
        # --- End Scoring Section ---

        # --- Customization Section ---
        customization_frame = ttk.LabelFrame(self, text="Customization")
        customization_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
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
        
        # Create listbox with scrollbar (increased height to 8 lines)
        self.font_family_listbox = tk.Listbox(font_frame, height=8, bg='#404040', fg='#ffffff', 
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
        ttk.OptionMenu(customization_frame, self.color_scheme_var, self.color_scheme_var.get(), *self.color_names).grid(row=customization_row, column=1, sticky="ew")
        customization_row += 1

        customization_frame.columnconfigure(1, weight=1)
        row += 1
        # --- End Customization Section ---

        # --- Logo Section ---
        logo_frame = ttk.LabelFrame(self, text="Logo")
        logo_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
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
        ttk.OptionMenu(logo_frame, self.logo_file_var, self.logo_file_var.get(), *self.logo_names).grid(row=logo_row, column=1, sticky="ew")
        logo_row += 1

        ttk.Label(logo_frame, text="Zoom Logo:").grid(row=logo_row, column=0, sticky="w")
        self.zoom_logo_var = tk.DoubleVar(value=self.settings.get("zoom_logo", 1.0))
        # Configure Scale widget for dark theme
        zoom_scale = tk.Scale(logo_frame, variable=self.zoom_logo_var, from_=0.01, to=0.3, resolution=0.005, orient="horizontal",
                             bg='#404040', fg='#ffffff', activebackground='#505050', highlightbackground='#2d2d2d', troughcolor='#606060')
        zoom_scale.grid(row=logo_row, column=1, sticky="ew")
        logo_row += 1

        logo_frame.columnconfigure(1, weight=1)
        row += 1
        # --- End Logo Section ---

        # --- Manage Tournament Section ---
        row += 1
        save_tournament_frame = ttk.LabelFrame(self, text="Manage Tournament")
        save_tournament_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Button(save_tournament_frame, text="Save Tournament to Folder", command=self.save_tournament).grid(row=0, column=0, sticky="ew", pady=5)
        ttk.Button(save_tournament_frame, text="DELETE ROUNDS", command=self.delete_rounds).grid(row=0, column=1, sticky="ew", pady=5)

        # Save button
        row += 1
        ttk.Button(self, text="Save", command=self.save).grid(row=row, column=0, columnspan=1, pady=10, sticky="ew")
        # Button to delete fontlist files
        ttk.Button(self, text="Delete matplotlib fontlist", command=delete_fontlist_files).grid(row=row, column=1, columnspan=1, pady=10, sticky="ew")

        # Make columns expand
        self.columnconfigure(1, weight=1)

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
