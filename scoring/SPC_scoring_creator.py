import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
import importlib.util
import re
import sys  # <-- Add this

class IntervalManager(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Placement Points", padding=(6, 4), **kwargs)
        self.intervals = []
        self.interval_frames = []
        
        # Create scrollable container
        self.canvas = tk.Canvas(self, bg='#2d2d2d', highlightthickness=0, height=150)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.intervals_container = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.intervals_container, anchor="nw")
        
        # Bind mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.intervals_container.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.intervals_container.bind("<Configure>", self._on_frame_configure)
        
        self.add_btn = ttk.Button(self, text="+ Add Interval", command=self.add_interval, style='TButton')
        self.add_btn.pack(pady=4, anchor="w")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        # Update the canvas window width to match canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_frame_configure(self, event):
        # Update scroll region when frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_interval(self, start=1, end=1, points=0):
        frame = ttk.Frame(self.intervals_container)
        a_var = tk.IntVar(value=start)
        b_var = tk.IntVar(value=end)
        p_var = tk.IntVar(value=points)
        
        # Remove all font specifications to use default interface font
        ttk.Label(frame, text="From").pack(side=tk.LEFT)
        a_entry = ttk.Entry(frame, width=4, textvariable=a_var)
        a_entry.pack(side=tk.LEFT)
        
        ttk.Label(frame, text="to").pack(side=tk.LEFT)
        b_entry = ttk.Entry(frame, width=4, textvariable=b_var)
        b_entry.pack(side=tk.LEFT)
        
        ttk.Label(frame, text=":").pack(side=tk.LEFT)
        p_entry = ttk.Entry(frame, width=6, textvariable=p_var)
        p_entry.pack(side=tk.LEFT)
        
        ttk.Label(frame, text="points").pack(side=tk.LEFT)
        remove_btn = ttk.Button(frame, text="Remove", command=lambda: self.remove_interval(frame))
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind mouse wheel to child elements too
        for widget in frame.winfo_children():
            widget.bind("<MouseWheel>", self._on_mousewheel)
        frame.bind("<MouseWheel>", self._on_mousewheel)
        
        frame.pack(pady=2, fill=tk.X)
        self.interval_frames.append(frame)
        self.intervals.append((a_var, b_var, p_var))
        
        # Update scroll region after adding
        self.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def remove_interval(self, frame):
        idx = self.interval_frames.index(frame)
        frame.destroy()
        del self.interval_frames[idx]
        del self.intervals[idx]
        
        # Update scroll region after removing
        self.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def get_intervals(self):
        return [(a.get(), b.get(), p.get()) for a, b, p in self.intervals]

class PointsSection(ttk.LabelFrame):
    def __init__(self, master, name, var_label, **kwargs):
        super().__init__(master, text=name, padding=(6, 4), **kwargs)
        self.var = tk.IntVar(value=0)
        
        row = ttk.Frame(self)
        # Remove all font specifications to use default interface font
        ttk.Label(row, text=var_label).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.var, width=8).pack(side=tk.LEFT)
        ttk.Label(row, text="points").pack(side=tk.LEFT)
        row.pack(pady=2, anchor="w")

    def get_value(self):
        return self.var.get()

class ScoringCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scoring Creator")
        self.resizable(False, False)
        
        # Configure dark theme
        self.configure(bg='#2d2d2d')
        
        # Configure ttk styles for dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure dark theme colors - remove all font specifications
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabelframe', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TLabelframe.Label', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TLabel', background='#2d2d2d', foreground='#ffffff')
        self.style.configure('TButton', background='#404040', foreground='#ffffff')
        self.style.map('TButton', background=[('active', '#505050')])
        self.style.configure('TEntry', fieldbackground='#404040', foreground='#ffffff', bordercolor='#606060')
        self.style.configure('TCheckbutton', background='#2d2d2d', foreground='#ffffff')
        
        # Add custom style for green button - no font specification
        self.style.configure('Green.TButton', background='#2ecc40', foreground='#ffffff')
        self.style.map('Green.TButton', background=[('active', '#27ae60')])
        
        # Add custom style for blue button
        self.style.configure('Blue.TButton', background='#3498db', foreground='#ffffff')
        self.style.map('Blue.TButton', background=[('active', '#2980b9')])

        # Track if we're editing an existing file
        self.editing_file = None

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Scoring Name Section
        self.name_frame = ttk.LabelFrame(main_frame, text="Scoring Name")
        self.name_frame.pack(fill=tk.X, pady=8)
        self.name_var = tk.StringVar(value="standard_scoring")
        name_entry = ttk.Entry(self.name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(padx=6, pady=6, fill=tk.X)
        
        # Description Section
        self.desc_frame = ttk.LabelFrame(main_frame, text="Description")
        self.desc_frame.pack(fill=tk.X, pady=8)
        self.desc_text = tk.Text(self.desc_frame, height=3, width=30, bg='#404040', fg='#ffffff')
        self.desc_text.pack(padx=6, pady=6, fill=tk.X)
        self.desc_text.insert(tk.END, "Description of this scoring system")

        # Placement Points Section
        self.placement_section = IntervalManager(main_frame)
        self.placement_section.pack(fill=tk.X, pady=8)
        # Add default placement interval
        self.placement_section.add_interval(1, 1, 0)

        # Kill Points Section
        self.kill_section = PointsSection(main_frame, "Kill Points", "Points per Kill:")
        self.kill_section.pack(fill=tk.X, pady=8)

        # Masterkill Points Section
        self.masterkill_section = PointsSection(main_frame, "Masterkill Points", "Points per Masterkill:")
        self.masterkill_section.pack(fill=tk.X, pady=8)
        
        # Actions Section
        actions_frame = ttk.LabelFrame(main_frame, text="Actions")
        actions_frame.pack(fill=tk.X, pady=8)
        
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=tk.X, padx=6, pady=6)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        save_btn = ttk.Button(buttons_frame, text="Save Scoring", command=self.save_scoring, style='Green.TButton')
        save_btn.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10, columnspan=2)
        
        self.update_btn = ttk.Button(buttons_frame, text="Update Scoring", command=self.update_scoring, style='Blue.TButton')
        self.update_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        self.update_btn.grid_remove()  # Hide by default, only shown when editing
        
        # Callback to adjust save button width when update button visibility changes
        def on_update_visibility(event=None):
            if self.update_btn.winfo_viewable():
                save_btn.grid_configure(columnspan=1, padx=(10, 5))
            else:
                save_btn.grid_configure(columnspan=2, padx=(10, 10))
        
        # Bind to update button visibility changes
        self.update_btn.bind("<Visibility>", on_update_visibility)
        
        # Load Existing Scoring Section
        load_frame = ttk.LabelFrame(main_frame, text="Edit Existing Scoring")
        load_frame.pack(fill=tk.X, pady=8)
        
        load_btn = ttk.Button(load_frame, text="Load Scoring File", command=self.load_scoring)
        load_btn.pack(padx=6, pady=6, fill=tk.X)

    def save_scoring(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a scoring name")
            return
            
        # Sanitize the filename - replace spaces with underscores and remove special characters
        filename = ''.join(c if c.isalnum() or c == '_' else '_' for c in name.lower())
        if not filename.endswith('.py'):
            filename += '.py'
            
        description = self.desc_text.get("1.0", tk.END).strip()
        placement_intervals = self.placement_section.get_intervals()
        kill_points = self.kill_section.get_value()
        masterkill_points = self.masterkill_section.get_value()
        
        # Save scoring files in the same directory as this script
        scoring_dir = get_scoring_dir()
        file_path = os.path.join(scoring_dir, filename)
        
        # Check if file already exists
        if os.path.exists(file_path) and self.editing_file != file_path:
            response = messagebox.askyesno("File Exists", f"The file {filename} already exists. Do you want to overwrite it?")
            if not response:
                return
        
        # Generate the Python code for the scoring file
        code = self.generate_scoring_code(name, description, placement_intervals, kill_points, masterkill_points)
        
        try:
            with open(file_path, 'w') as f:
                f.write(code)
            messagebox.showinfo("Success", f"Scoring saved to:\n{file_path}")
            self.editing_file = None
            self.update_btn.grid_remove()  # Hide update button after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save scoring file: {str(e)}")
    
    def update_scoring(self):
        if not self.editing_file:
            messagebox.showerror("Error", "No file is currently being edited")
            return
        
        description = self.desc_text.get("1.0", tk.END).strip()
        placement_intervals = self.placement_section.get_intervals()
        kill_points = self.kill_section.get_value()
        masterkill_points = self.masterkill_section.get_value()
        
        # Get the name from the existing file path
        name = os.path.basename(self.editing_file)
        if name.endswith('.py'):
            name = name[:-3]
        
        # Generate the Python code for the scoring file
        code = self.generate_scoring_code(name, description, placement_intervals, kill_points, masterkill_points)
        
        try:
            with open(self.editing_file, 'w') as f:
                f.write(code)
            messagebox.showinfo("Success", f"Scoring updated at:\n{self.editing_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update scoring file: {str(e)}")
    
    def load_scoring(self):
        # Save scoring files in the same directory as this script
        scoring_dir = get_scoring_dir()
        
        # Get all .py files in the scoring directory
        scoring_files = []
        for file in os.listdir(scoring_dir):
            if file.endswith('.py'):
                file_path = os.path.join(scoring_dir, file)
                try:
                    # Check if this file was created with the scoring creator
                    spec = importlib.util.spec_from_file_location("module.name", file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'created_with_scoring') and module.created_with_scoring:
                        scoring_files.append((file, file_path))
                except Exception as e:
                    print(f"Error loading {file}: {e}")
        
        if not scoring_files:
            messagebox.showinfo("No Files", "No scoring files created with the scoring creator were found.")
            return
        
        # Create a dialog to select a file
        selection_window = tk.Toplevel(self)
        selection_window.title("Select Scoring File")
        selection_window.resizable(False, False)
        selection_window.configure(bg='#2d2d2d')
        selection_window.grab_set()  # Make the dialog modal
        
        ttk.Label(selection_window, text="Select a scoring file to edit:").pack(padx=10, pady=10)
        
        listbox = tk.Listbox(selection_window, bg='#404040', fg='#ffffff', selectbackground='#606060', height=10)
        listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        for file, _ in scoring_files:
            listbox.insert(tk.END, file)
        
        def on_select():
            if not listbox.curselection():
                messagebox.showerror("Error", "Please select a file")
                return
                
            idx = listbox.curselection()[0]
            selected_file, file_path = scoring_files[idx]
            self.load_scoring_from_file(file_path)
            selection_window.destroy()
        
        ttk.Button(selection_window, text="Edit Selected", command=on_select).pack(padx=10, pady=10)
    
    def load_scoring_from_file(self, file_path):
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the name from the file path
            name = os.path.basename(file_path)
            if name.endswith('.py'):
                name = name[:-3]
            self.name_var.set(name)
            
            # Load description
            if hasattr(module, 'desc'):
                self.desc_text.delete("1.0", tk.END)
                self.desc_text.insert(tk.END, module.desc)
            
            # Clear existing intervals
            for frame in self.placement_section.interval_frames[:]:
                self.placement_section.remove_interval(frame)
            
            # Extract placement intervals using regex
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Extract placement points intervals
            placement_pattern = r'if\s+(?:placement\s*==\s*(\d+)|(\d+)\s*<=\s*placement\s*<=\s*(\d+)):\s*\n\s*return\s*(\d+)'
            placement_matches = re.finditer(placement_pattern, code)
            
            for match in placement_matches:
                if match.group(1):  # Single value
                    start = end = int(match.group(1))
                else:  # Range
                    start = int(match.group(2))
                    end = int(match.group(3))
                points = int(match.group(4))
                self.placement_section.add_interval(start, end, points)
            
            # Extract kill points
            kill_pattern = r'return\s+kills\s*\*\s*(\d+)'
            kill_match = re.search(kill_pattern, code)
            if kill_match:
                self.kill_section.var.set(int(kill_match.group(1)))
            
            # Extract masterkill points
            masterkill_pattern = r'if\s+presence_de_masterkill:\s*\n\s*return\s*(\d+)'
            masterkill_match = re.search(masterkill_pattern, code)
            if masterkill_match:
                self.masterkill_section.var.set(int(masterkill_match.group(1)))
            
            # Set editing mode
            self.editing_file = file_path
            self.update_btn.grid()  # Show update button
            
            messagebox.showinfo("Success", f"Loaded scoring file: {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load scoring file: {str(e)}")

    def generate_scoring_code(self, name, description, placement_intervals, kill_points, masterkill_points):
        code = []
        code.append("import math\n")
        code.append("# ----------------------------------------------------------------------------\n")
        
        # Add name as a variable
        code.append(f"created_with_scoring = True")
        
        # Add description as a variable
        code.append("desc = \"\"\"" + description + "\"\"\"\n")
        
        code.append("# ----------------------------------------------------------------------------\n")
        
        # Generate kill_points function
        code.append("def kill_points(placement, kills, total_players):  # Define how kills award points")
        code.append("    # placement, kills, total_players -> int\n")
        code.append("    if placement == 0 or placement == -1:")
        code.append("        return 0  # DO NOT TOUCH, this line removes spectators and players who are not present!\n")
        code.append("    else:")
        code.append(f"        return kills * {kill_points}")
        code.append("    \n# ----------------------------------------------------------------------------\n")
        
        # Generate placement_points function
        code.append("def placement_points(placement, kills, total_players):  # Define how placement awards points")
        code.append("    # placement, kills, total_players -> int\n")
        code.append("    if placement == 0 or placement == -1:")
        code.append("        return 0  # This one either!\n")
        code.append("    else:")
        
        # Sort intervals by start position to make the code cleaner
        placement_intervals.sort(key=lambda x: x[0])
        
        if placement_intervals:
            for i, (start, end, points) in enumerate(placement_intervals):
                condition = f"placement == {start}" if start == end else f"{start} <= placement <= {end}"
                if i == 0:
                    code.append(f"        if {condition}:")
                else:
                    code.append(f"        elif {condition}:")
                code.append(f"            return {points}")
            code.append("        else:")
            code.append("            return 0")
        else:
            code.append("        return 0")
            
        code.append("        \n# ----------------------------------------------------------------------------\n")
        
        # Generate masterkill function
        code.append("def masterkill(presence_de_masterkill, kills, total_players):  # Define how many points the Masterkill awards")
        code.append("    # presence_de_masterkill -> bool")
        code.append("    # total_players -> int\n")
        code.append("    if presence_de_masterkill:")
        code.append(f"        return {masterkill_points}")
        code.append("    else:")
        code.append("        return 0")
        
        return "\n".join(code)

def get_scoring_dir():
    # Use the folder containing the EXE if frozen, else the script folder
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    app = ScoringCreatorApp()
    app.mainloop()
    app.mainloop()
    app.mainloop()
