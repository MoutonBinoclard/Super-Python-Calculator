import pandas as pd
import matplotlib.pyplot as plt
import os

def export_spreadsheet_from_csv_2(csv_path, tournament_name, cs, logo, logo_path, zoom_logo, date):
    """
    Export a spreadsheet (png format) from a CSV file with color scheme applied.
    No margin: the table fills the entire image.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import os

    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Fixed dimensions, no margin
    row_height = 0.3  # Fixed height per row in inches
    col_width = 0.8   # Fixed width per column in inches
    
    fig_height = (len(df) + 1) * row_height  # +1 for header
    fig_width = len(df.columns) * col_width
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    
    # bbox fills the entire figure: [left, bottom, width, height] = [0, 0, 1, 1]
    table = ax.table(cellText=df.values, colLabels=df.columns, 
                    bbox=[0, 0, 1, 1], cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    
    # Set uniform cell dimensions
    cellDict = table.get_celld()
    cell_height = 1.0 / (len(df) + 1)  # Uniform height for all cells
    
    for i in range(len(df) + 1):  # +1 for header row
        for j in range(len(df.columns)):
            cellDict[(i, j)].set_height(cell_height)
    
    # Manual column width adjustment - uniform widths
    table.auto_set_column_width(col=list(range(len(df.columns))))
    
    # Apply color scheme
    for i in range(len(df.columns)):
        # Headers (first row)
        table[(0, i)].set_facecolor(cs["top_cells_color"])
        table[(0, i)].set_text_props(color=cs["top_text_color"])
        table[(0, i)].set_edgecolor(cs["grid_color"])
        
        # Data cells
        for j in range(len(df)):
            table[(j+1, i)].set_facecolor(cs["cells_color"])
            table[(j+1, i)].set_text_props(color=cs["text_color"])
            table[(j+1, i)].set_edgecolor(cs["grid_color"])
    
    # Save the image
    plt.savefig(
        os.path.join("exports", "spreadsheet.png"),
        dpi=150,
        facecolor=cs["background_color"],
        pad_inches=0
    )
    plt.close()  # Close the figure