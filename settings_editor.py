import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
import pathlib
import shutil

# Dynamically determine base directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
SPC_SCORING_DIR = os.path.join(BASE_DIR, "SPC_scoring")
SPC_LOGO_DIR = os.path.join(BASE_DIR, "SPC_logo")
SPC_COLOR_SCHEME_DIR = os.path.join(BASE_DIR, "SPC_color_schemes")

def load_settings():
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
    # List all files in SPC_color_schemes directory, remove extension
    if os.path.isdir(SPC_COLOR_SCHEME_DIR):
        files = os.listdir(SPC_COLOR_SCHEME_DIR)
        color_files = [f for f in files if os.path.isfile(os.path.join(SPC_COLOR_SCHEME_DIR, f))]
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

class SettingsEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings Editor")
        self.geometry("400x450")
        self.settings = load_settings()
        self.scoring_systems = load_scoring_systems()
        self.logo_names, self.logo_files = load_logo_files()
        self.logo_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("SPC_logo", f).replace("\\", "/")
            for f in self.logo_files
        }
        self.color_names, self.color_files = load_color_schemes()
        self.color_name_to_path = {
            os.path.splitext(f)[0]: os.path.join("SPC_color_schemes", f).replace("\\", "/")
            for f in self.color_files
        }
        self.create_widgets()

    def create_widgets(self):
        row = 0

        # --- Header Section ---
        header_frame = ttk.LabelFrame(self, text="Header")
        header_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        header_row = 0

        self.date_var = tk.BooleanVar(value=self.settings.get("date", False))
        ttk.Checkbutton(header_frame, text="Show Date", variable=self.date_var).grid(row=header_row, column=0, sticky="w")
        header_row += 1

        ttk.Label(header_frame, text="Tournament Name:").grid(row=header_row, column=0, sticky="w")
        self.tournament_var = tk.StringVar(value=self.settings.get("tournament_name", ""))
        ttk.Entry(header_frame, textvariable=self.tournament_var).grid(row=header_row, column=1, sticky="ew")
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

        self.bonus_var = tk.BooleanVar(value=self.settings.get("bonus", False))
        ttk.Checkbutton(scoring_frame, text="Bonus", variable=self.bonus_var).grid(row=scoring_row, column=0, sticky="w")
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

        ttk.Label(customization_frame, text="Custom Font:").grid(row=customization_row, column=0, sticky="w")
        self.custom_font_var = tk.StringVar(value=self.settings.get("custom_font", ""))
        ttk.Entry(customization_frame, textvariable=self.custom_font_var).grid(row=customization_row, column=1, sticky="ew")
        customization_row += 1

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
        tk.Scale(logo_frame, variable=self.zoom_logo_var, from_=0.1, to=0.7, resolution=0.01, orient="horizontal").grid(row=logo_row, column=1, sticky="ew")
        logo_row += 1

        logo_frame.columnconfigure(1, weight=1)
        row += 1
        # --- End Logo Section ---

        # Save button
        ttk.Button(self, text="Save", command=self.save).grid(row=row, column=0, columnspan=1, pady=10, sticky="ew")
        # Button to delete fontlist files
        ttk.Button(self, text="Delete matplotlib fontlist", command=delete_fontlist_files).grid(row=row, column=1, columnspan=1, pady=10, sticky="ew")

        # Make columns expand
        self.columnconfigure(1, weight=1)

    def save(self):
        self.settings["team_mode"] = self.team_mode_var.get()
        self.settings["bonus"] = self.bonus_var.get()
        # Save logo_path as full path using selected logo name
        selected_logo_name = self.logo_file_var.get()
        self.settings["logo_path"] = self.logo_name_to_path.get(selected_logo_name, "")
        self.settings["zoom_logo"] = self.zoom_logo_var.get()
        self.settings["logo"] = self.logo_var.get()
        # Save color_scheme as full path using selected color scheme name
        selected_color_name = self.color_scheme_var.get()
        self.settings["color_scheme"] = self.color_name_to_path.get(selected_color_name, "")
        self.settings["add_custom_fonts"] = self.add_custom_fonts_var.get()
        self.settings["custom_font"] = self.custom_font_var.get()
        self.settings["date"] = self.date_var.get()
        self.settings["scoring_system"] = self.scoring_var.get()
        self.settings["tournament_name"] = self.tournament_var.get()
        try:
            save_settings(self.settings)
            messagebox.showinfo("Success", "Settings saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

if __name__ == "__main__":
    app = SettingsEditor()
    app.mainloop()
