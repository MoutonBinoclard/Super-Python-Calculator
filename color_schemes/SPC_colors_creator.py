import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import json
import os
import sys

class ColorSection(ttk.LabelFrame):
    def __init__(self, master, name, color_var, **kwargs):
        super().__init__(master, text=name, padding=(6, 4), **kwargs)
        self.color_var = color_var
        
        row = ttk.Frame(self)
        self.color_button = tk.Button(row, bg=color_var.get(), width=3, 
                                     command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)
        
        self.entry = ttk.Entry(row, textvariable=color_var, width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<KeyRelease>", self.update_button_color)
        
        row.pack(pady=2, anchor="w")

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_var.get())
        if color[1]:
            self.color_var.set(color[1])
            self.color_button.config(bg=color[1])
            # Force update of the UI to immediately show the color change
            self.update_idletasks()

    def update_button_color(self, event=None):
        try:
            self.color_button.config(bg=self.color_var.get())
        except tk.TclError:
            pass  # Invalid color format in entry

class GradientSection(ttk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Gradient Colors", padding=(6, 4), **kwargs)
        self.colors = []
        self.color_frames = []
        
        # Create scrollable container
        self.canvas = tk.Canvas(self, bg='#2d2d2d', highlightthickness=0, height=150)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.colors_container = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.colors_container, anchor="nw")
        
        # Bind mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.colors_container.bind("<MouseWheel>", self._on_mousewheel)
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.colors_container.bind("<Configure>", self._on_frame_configure)
        
        self.add_btn = ttk.Button(self, text="+ Add Color", command=self.add_color, style='TButton')
        self.add_btn.pack(pady=4, anchor="w")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        # Update the canvas window width to match canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_frame_configure(self, event):
        # Update scroll region when frame size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_color(self, color="#74a998"):
        frame = ttk.Frame(self.colors_container)
        color_var = tk.StringVar(value=color)
        
        color_button = tk.Button(frame, bg=color_var.get(), width=3, 
                                command=lambda v=color_var: self.choose_color(v))
        color_button.pack(side=tk.LEFT, padx=5)
        
        entry = ttk.Entry(frame, textvariable=color_var, width=10)
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind("<KeyRelease>", lambda e, b=color_button, v=color_var: self.update_button_color(b, v))
        
        remove_btn = ttk.Button(frame, text="Remove", 
                               command=lambda f=frame, v=color_var: self.remove_color(f, v))
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind mouse wheel to child elements
        for widget in frame.winfo_children():
            widget.bind("<MouseWheel>", self._on_mousewheel)
        frame.bind("<MouseWheel>", self._on_mousewheel)
        
        frame.pack(pady=2, fill=tk.X)
        self.color_frames.append(frame)
        self.colors.append(color_var)
        
        # Update scroll region after adding
        self.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def choose_color(self, color_var):
        color = colorchooser.askcolor(initialcolor=color_var.get())
        if color[1]:
            color_var.set(color[1])
            # Find the button associated with this color_var and update it
            for frame in self.color_frames:
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Button) and widget.cget("width") == 3:
                        # Update button if it's in the same frame as our color_var
                        for child in frame.winfo_children():
                            if isinstance(child, ttk.Entry) and child.cget("textvariable") == str(color_var):
                                widget.config(bg=color[1])
                                # Force update to immediately show the color change
                                widget.update_idletasks()
                                break
            
            # Force update of the UI
            self.update_idletasks()

    def update_button_color(self, button, color_var):
        try:
            button.config(bg=color_var.get())
        except tk.TclError:
            pass  # Invalid color format

    def remove_color(self, frame, color_var):
        if len(self.colors) <= 1:
            messagebox.showinfo("Info", "You need at least one gradient color")
            return
            
        idx = self.color_frames.index(frame)
        frame.destroy()
        del self.color_frames[idx]
        del self.colors[idx]
        
        # Update scroll region after removing
        self.after_idle(lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def get_colors(self):
        return [color.get() for color in self.colors]

class ColorSchemeCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color Scheme Creator")
        self.resizable(False, False)
        
        # Configure dark theme
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
        
        # Add custom style for green button
        self.style.configure('Green.TButton', background='#2ecc40', foreground='#ffffff')
        self.style.map('Green.TButton', background=[('active', '#27ae60')])
        
        # Add custom style for blue button
        self.style.configure('Blue.TButton', background='#3498db', foreground='#ffffff')
        self.style.map('Blue.TButton', background=[('active', '#2980b9')])

        # Track if we're editing an existing file
        self.editing_file = None

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Scheme Name Section
        self.name_frame = ttk.LabelFrame(main_frame, text="Color Scheme Name")
        self.name_frame.pack(fill=tk.X, pady=8)
        self.name_var = tk.StringVar(value="my_color_scheme")
        name_entry = ttk.Entry(self.name_frame, textvariable=self.name_var, width=30)
        name_entry.pack(padx=6, pady=6, fill=tk.X)
        
        # Create a notebook for color categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=8)
        
        # Main Colors Tab
        main_colors_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_colors_frame, text="Main Colors")
        
        # Create two columns for color sections
        left_column = ttk.Frame(main_colors_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_column = ttk.Frame(main_colors_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Background color
        self.bg_color = tk.StringVar(value="#5b6369")
        self.bg_section = ColorSection(left_column, "Background Color", self.bg_color)
        self.bg_section.pack(fill=tk.X, pady=4)
        
        # Title colors
        self.title_color = tk.StringVar(value="#ffffff")
        self.title_section = ColorSection(left_column, "Title Color", self.title_color)
        self.title_section.pack(fill=tk.X, pady=4)
        
        self.date_color = tk.StringVar(value="#929ccd")
        self.date_section = ColorSection(left_column, "Date Color", self.date_color)
        self.date_section.pack(fill=tk.X, pady=4)
        
        self.points_color = tk.StringVar(value="#ac8fb3")
        self.points_section = ColorSection(right_column, "Points Color", self.points_color)
        self.points_section.pack(fill=tk.X, pady=4)
        
        # Legend colors
        self.legend_border_color = tk.StringVar(value="#74a998")
        self.legend_border_section = ColorSection(right_column, "Legend Border Color", self.legend_border_color)
        self.legend_border_section.pack(fill=tk.X, pady=4)
        
        self.legend_text_color = tk.StringVar(value="#74a998")
        self.legend_text_section = ColorSection(right_column, "Legend Text Color", self.legend_text_color)
        self.legend_text_section.pack(fill=tk.X, pady=4)
        
        # Gradient colors - full width at bottom
        self.gradient_section = GradientSection(main_colors_frame)
        self.gradient_section.pack(fill=tk.X, pady=4)
        self.gradient_section.add_color("#74a998")
        self.gradient_section.add_color("#929ccd")
        self.gradient_section.add_color("#ac8fb3")
        
        # Axis Tab
        axis_frame = ttk.Frame(self.notebook)
        self.notebook.add(axis_frame, text="Axis Colors")
        
        # Create two columns for axis tab
        axis_left = ttk.Frame(axis_frame)
        axis_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        axis_right = ttk.Frame(axis_frame)
        axis_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # X and Y label colors
        self.x_label_color = tk.StringVar(value="#ac8fb3")
        self.x_label_section = ColorSection(axis_left, "X Label Color", self.x_label_color)
        self.x_label_section.pack(fill=tk.X, pady=4)
        
        self.y_label_color = tk.StringVar(value="#ac8fb3")
        self.y_label_section = ColorSection(axis_left, "Y Label Color", self.y_label_color)
        self.y_label_section.pack(fill=tk.X, pady=4)
        
        # X and Y axis colors
        self.x_axis_color = tk.StringVar(value="#74a998")
        self.x_axis_section = ColorSection(axis_left, "X Axis Color", self.x_axis_color)
        self.x_axis_section.pack(fill=tk.X, pady=4)
        
        self.y_axis_color = tk.StringVar(value="#74a998")
        self.y_axis_section = ColorSection(axis_right, "Y Axis Color", self.y_axis_color)
        self.y_axis_section.pack(fill=tk.X, pady=4)
        
        # Ticks colors
        self.x_ticks_color = tk.StringVar(value="#74a998")
        self.x_ticks_section = ColorSection(axis_right, "X Ticks Color", self.x_ticks_color)
        self.x_ticks_section.pack(fill=tk.X, pady=4)
        
        self.y_ticks_color = tk.StringVar(value="#74a998")
        self.y_ticks_section = ColorSection(axis_right, "Y Ticks Color", self.y_ticks_color)
        self.y_ticks_section.pack(fill=tk.X, pady=4)
        
        self.horizontal_lines_color = tk.StringVar(value="#e7e9f7")
        self.horizontal_lines_section = ColorSection(axis_left, "Horizontal Lines Color", self.horizontal_lines_color)
        self.horizontal_lines_section.pack(fill=tk.X, pady=4)
        
        # Box Plot Tab
        boxplot_frame = ttk.Frame(self.notebook)
        self.notebook.add(boxplot_frame, text="Box Plot")
        
        # Create two columns for boxplot tab
        box_left = ttk.Frame(boxplot_frame)
        box_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        box_right = ttk.Frame(boxplot_frame)
        box_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.fliers_color = tk.StringVar(value="#ac8fb3")
        self.fliers_section = ColorSection(box_left, "Fliers Color", self.fliers_color)
        self.fliers_section.pack(fill=tk.X, pady=4)
        
        self.caps_color = tk.StringVar(value="#929ccd")
        self.caps_section = ColorSection(box_left, "Caps Color", self.caps_color)
        self.caps_section.pack(fill=tk.X, pady=4)
        
        self.whiskers_color = tk.StringVar(value="#929ccd")
        self.whiskers_section = ColorSection(box_left, "Whiskers Color", self.whiskers_color)
        self.whiskers_section.pack(fill=tk.X, pady=4)
        
        self.medians_color = tk.StringVar(value="#ac8fb3")
        self.medians_section = ColorSection(box_right, "Medians Color", self.medians_color)
        self.medians_section.pack(fill=tk.X, pady=4)
        
        self.mean_color = tk.StringVar(value="#ac8fb3")
        self.mean_section = ColorSection(box_right, "Mean Color", self.mean_color)
        self.mean_section.pack(fill=tk.X, pady=4)
        
        self.boxes_inside_color = tk.StringVar(value="#5b6369")
        self.boxes_inside_section = ColorSection(box_right, "Boxes Inside Color", self.boxes_inside_color)
        self.boxes_inside_section.pack(fill=tk.X, pady=4)
        
        self.boxes_outside_color = tk.StringVar(value="#929ccd")
        self.boxes_outside_section = ColorSection(box_left, "Boxes Outside Color", self.boxes_outside_color)
        self.boxes_outside_section.pack(fill=tk.X, pady=4)
        
        # Table Tab
        table_frame = ttk.Frame(self.notebook)
        self.notebook.add(table_frame, text="Table Colors")
        
        # Create two columns for table tab
        table_left = ttk.Frame(table_frame)
        table_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        table_right = ttk.Frame(table_frame)
        table_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.grid_color = tk.StringVar(value="#929ccd")
        self.grid_section = ColorSection(table_left, "Grid Color", self.grid_color)
        self.grid_section.pack(fill=tk.X, pady=4)
        
        self.top_cells_color = tk.StringVar(value="#929ccd")
        self.top_cells_section = ColorSection(table_left, "Top Cells Color", self.top_cells_color)
        self.top_cells_section.pack(fill=tk.X, pady=4)
        
        self.cells_color = tk.StringVar(value="#5b6369")
        self.cells_section = ColorSection(table_right, "Cells Color", self.cells_color)
        self.cells_section.pack(fill=tk.X, pady=4)
        
        self.top_text_color = tk.StringVar(value="#ffffff")
        self.top_text_section = ColorSection(table_right, "Top Text Color", self.top_text_color)
        self.top_text_section.pack(fill=tk.X, pady=4)
        
        self.text_color = tk.StringVar(value="#e7e9f7")
        self.text_section = ColorSection(table_left, "Text Color", self.text_color)
        self.text_section.pack(fill=tk.X, pady=4)
        
        # Actions Section - Keep this as a full-width section
        actions_frame = ttk.LabelFrame(main_frame, text="Actions")
        actions_frame.pack(fill=tk.X, pady=8)
        
        buttons_frame = ttk.Frame(actions_frame)
        buttons_frame.pack(fill=tk.X, padx=6, pady=6)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        save_btn = ttk.Button(buttons_frame, text="Save Color Scheme", command=self.save_color_scheme, style='Green.TButton')
        save_btn.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10, columnspan=2)
        
        self.update_btn = ttk.Button(buttons_frame, text="Update Color Scheme", command=self.update_color_scheme, style='Blue.TButton')
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
        
        # Load Existing Color Scheme Section
        load_frame = ttk.LabelFrame(main_frame, text="Edit Existing Color Scheme")
        load_frame.pack(fill=tk.X, pady=8)
        
        load_btn = ttk.Button(load_frame, text="Load Color Scheme File", command=self.load_color_scheme)
        load_btn.pack(padx=6, pady=6, fill=tk.X)

    def save_color_scheme(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a color scheme name")
            return
            
        # Sanitize the filename - replace spaces with underscores and remove special characters
        filename = ''.join(c if c.isalnum() or c == '_' else '_' for c in name.lower())
        if not filename.endswith('.json'):
            filename += '.json'
            
        # Save color scheme files in the same directory as this script
        colors_dir = get_colors_dir()
        file_path = os.path.join(colors_dir, filename)
        
        # Check if file already exists
        if os.path.exists(file_path) and self.editing_file != file_path:
            response = messagebox.askyesno("File Exists", f"The file {filename} already exists. Do you want to overwrite it?")
            if not response:
                return
        
        # Generate the JSON for the color scheme file
        scheme_data = self.get_color_scheme_data()
        
        try:
            with open(file_path, 'w') as f:
                json.dump(scheme_data, f, indent=4)
            messagebox.showinfo("Success", f"Color scheme saved to:\n{file_path}")
            self.editing_file = None
            self.update_btn.grid_remove()  # Hide update button after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save color scheme file: {str(e)}")
    
    def update_color_scheme(self):
        if not self.editing_file:
            messagebox.showerror("Error", "No file is currently being edited")
            return
        
        # Generate the JSON for the color scheme file
        scheme_data = self.get_color_scheme_data()
        
        try:
            with open(self.editing_file, 'w') as f:
                json.dump(scheme_data, f, indent=4)
            messagebox.showinfo("Success", f"Color scheme updated at:\n{self.editing_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update color scheme file: {str(e)}")
    
    def load_color_scheme(self):
        # Color scheme files are in the same directory as this script
        colors_dir = get_colors_dir()
        
        # Get all .json files in the colors directory
        filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(
            initialdir=colors_dir,
            title="Select Color Scheme File",
            filetypes=filetypes
        )
        
        if not file_path:
            return
            
        self.load_color_scheme_from_file(file_path)
    
    def load_color_scheme_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                scheme_data = json.load(f)
            
            # Get the name from the file path
            name = os.path.basename(file_path)
            if name.endswith('.json'):
                name = name[:-5]
            self.name_var.set(name)
            
            # Load all colors from the scheme data
            self.set_color_values(scheme_data)
            
            # Set editing mode
            self.editing_file = file_path
            self.update_btn.grid()  # Show update button
            
            messagebox.showinfo("Success", f"Loaded color scheme file: {name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load color scheme file: {str(e)}")
    
    def get_color_scheme_data(self):
        # Create dictionary with all color values
        return {
            "background_color": self.bg_color.get(),
            
            "title_color": self.title_color.get(),
            "date_color": self.date_color.get(),
            "points_color": self.points_color.get(),
            
            "legend_border_color": self.legend_border_color.get(),
            "legend_text_color": self.legend_text_color.get(),
            
            "gradient_colors": self.gradient_section.get_colors(),
            
            "x_label_color": self.x_label_color.get(),
            "y_label_color": self.y_label_color.get(),
            
            "x_axis_color": self.x_axis_color.get(),
            "y_axis_color": self.y_axis_color.get(),
            
            "x_ticks_color": self.x_ticks_color.get(),
            "y_ticks_color": self.y_ticks_color.get(),
            
            "horizontal_lines_color": self.horizontal_lines_color.get(),
            
            "fliers_color": self.fliers_color.get(),
            "caps_color": self.caps_color.get(),
            "whiskers_color": self.whiskers_color.get(),
            "medians_color": self.medians_color.get(),
            "mean_color": self.mean_color.get(),
            
            "boxes_inside_color": self.boxes_inside_color.get(),
            "boxes_outside_color": self.boxes_outside_color.get(),
            
            "grid_color": self.grid_color.get(),
            "top_cells_color": self.top_cells_color.get(),
            "cells_color": self.cells_color.get(),
            "top_text_color": self.top_text_color.get(),
            "text_color": self.text_color.get()
        }
    
    def set_color_values(self, scheme_data):
        # Helper function to safely set a color variable and update button
        def set_color(var, key, section=None):
            if key in scheme_data:
                var.set(scheme_data[key])
                # Update button color if section is provided
                if section and hasattr(section, 'color_button'):
                    try:
                        section.color_button.config(bg=scheme_data[key])
                    except tk.TclError:
                        pass  # Invalid color format
        
        # Set all the color variables and update buttons
        set_color(self.bg_color, "background_color", self.bg_section)
        
        set_color(self.title_color, "title_color", self.title_section)
        set_color(self.date_color, "date_color", self.date_section)
        set_color(self.points_color, "points_color", self.points_section)
        
        set_color(self.legend_border_color, "legend_border_color", self.legend_border_section)
        set_color(self.legend_text_color, "legend_text_color", self.legend_text_section)
        
        # Handle gradient colors list
        if "gradient_colors" in scheme_data and isinstance(scheme_data["gradient_colors"], list) and scheme_data["gradient_colors"]:
            # Temporarily store colors to add
            colors_to_add = scheme_data["gradient_colors"]
            
            # Keep at least one color to avoid the "You need at least one gradient color" message
            # First update the first color rather than removing it
            if self.gradient_section.colors:
                first_color = self.gradient_section.colors[0]
                if colors_to_add:
                    first_color.set(colors_to_add[0])
                    self.gradient_section.update_button_color(
                        self.gradient_section.color_frames[0].winfo_children()[0], 
                        first_color
                    )
                    colors_to_add = colors_to_add[1:]  # Remove the first color as it's already set
                
                # Remove any extra color frames (keeping the first one)
                for frame in self.gradient_section.color_frames[1:]:
                    idx = self.gradient_section.color_frames.index(frame)
                    frame.destroy()
                    # Don't call remove_color as that would trigger the warning
                
                # Clean up the lists but keep the first element
                self.gradient_section.color_frames = self.gradient_section.color_frames[:1]
                self.gradient_section.colors = self.gradient_section.colors[:1]
                
                # Add remaining colors
                for color in colors_to_add:
                    self.gradient_section.add_color(color)
            else:
                # If somehow there are no colors at all, add all from the file
                for color in colors_to_add:
                    self.gradient_section.add_color(color)
        
        set_color(self.x_label_color, "x_label_color", self.x_label_section)
        set_color(self.y_label_color, "y_label_color", self.y_label_section)
        
        set_color(self.x_axis_color, "x_axis_color", self.x_axis_section)
        set_color(self.y_axis_color, "y_axis_color", self.y_axis_section)
        
        set_color(self.x_ticks_color, "x_ticks_color", self.x_ticks_section)
        set_color(self.y_ticks_color, "y_ticks_color", self.y_ticks_section)
        
        set_color(self.horizontal_lines_color, "horizontal_lines_color", self.horizontal_lines_section)
        
        set_color(self.fliers_color, "fliers_color", self.fliers_section)
        set_color(self.caps_color, "caps_color", self.caps_section)
        set_color(self.whiskers_color, "whiskers_color", self.whiskers_section)
        set_color(self.medians_color, "medians_color", self.medians_section)
        set_color(self.mean_color, "mean_color", self.mean_section)
        
        set_color(self.boxes_inside_color, "boxes_inside_color", self.boxes_inside_section)
        set_color(self.boxes_outside_color, "boxes_outside_color", self.boxes_outside_section)
        
        set_color(self.grid_color, "grid_color", self.grid_section)
        set_color(self.top_cells_color, "top_cells_color", self.top_cells_section)
        set_color(self.cells_color, "cells_color", self.cells_section)
        set_color(self.top_text_color, "top_text_color", self.top_text_section)
        set_color(self.text_color, "text_color", self.text_section)
        
        # Force update of the UI
        self.update_idletasks()

def get_colors_dir():
    # Use the folder containing the EXE if frozen, else the script folder
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    app = ColorSchemeCreatorApp()
    app.mainloop()
