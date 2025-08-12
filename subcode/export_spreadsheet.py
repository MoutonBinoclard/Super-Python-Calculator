import csv
import matplotlib.pyplot as plt
import os

def export_spreadsheet_from_csv(csv_path, tournament_name, cs, logo, logo_path, zoom_logo, date, spreadsheet_pixel_density):
    """
    Export a spreadsheet (png format) from a CSV file with color scheme applied.
    No margin: the table fills the entire image.
    """

    # Read the CSV file into headers and rows
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        raise ValueError("CSV file is empty")

    headers = data[0]
    rows = data[1:]

    # Fixed dimensions, no margin
    row_height = 0.3  # Fixed height per row in inches
    col_width = 0.8   # Fixed width per column in inches
    
    fig_height = (len(rows) + 1) * row_height  # +1 for header
    fig_width = len(headers) * col_width
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=rows, colLabels=headers, 
                    bbox=[0, 0, 1, 1], cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    
    # Uniform cell height
    cellDict = table.get_celld()
    cell_height = 1.0 / (len(rows) + 1)
    
    for i in range(len(rows) + 1):
        for j in range(len(headers)):
            cellDict[(i, j)].set_height(cell_height)
    
    # Uniform column widths
    table.auto_set_column_width(col=list(range(len(headers))))
    
    # Apply color scheme
    for i in range(len(headers)):
        # Headers
        table[(0, i)].set_facecolor(cs["top_cells_color"])
        table[(0, i)].set_text_props(color=cs["top_text_color"])
        table[(0, i)].set_edgecolor(cs["grid_color"])
        
        # Data
        for j in range(len(rows)):
            table[(j+1, i)].set_facecolor(cs["cells_color"])
            table[(j+1, i)].set_text_props(color=cs["text_color"])
            table[(j+1, i)].set_edgecolor(cs["grid_color"])
    
    # Save image
    plt.savefig(
        os.path.join("exports", "spreadsheet.png"),
        dpi=spreadsheet_pixel_density,
        facecolor=cs["background_color"],
        pad_inches=0
    )
    plt.close()
