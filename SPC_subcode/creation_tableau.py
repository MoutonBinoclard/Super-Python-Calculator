import pandas as pd
import matplotlib.pyplot as plt


def creation_dictionnaire_tableau(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        if '\t' in first_line:
            items = first_line.split('\t')
        else:
            items = [first_line]
    dictionnaire = {}
    for item in items:
        dictionnaire[item] = []

    return dictionnaire

def remplir_dictionnaire_tableau(file_path, dictionnaire):
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # Ignore la première ligne
        for line in f:
            items = line.strip().split('\t')
            for i, item in enumerate(items):
                if i < len(dictionnaire):
                    dictionnaire[list(dictionnaire.keys())[i]].append(item)
    return dictionnaire


def creer_et_sauvegarder_tableau(file_path, output_path, cs, max_col_width=30):
    data = creation_dictionnaire_tableau(file_path)
    data = remplir_dictionnaire_tableau(file_path, data)

    df = pd.DataFrame(data)

    n_cols = len(df.columns)
    n_rows = len(df)

    # Définir les largeurs personnalisées pour chaque colonne
    default_col_width = 2
    small_col_width = 1  # moitié
    large_col_width = 4  # deux fois plus grande

    col_widths = []
    for i in range(n_cols):
        if i == 0:
            col_widths.append(small_col_width)
        elif i == 1:
            col_widths.append(large_col_width)
        elif 2 <= i <= 8:  # colonnes 3 à 9 incluses (indices 2 à 8)
            col_widths.append(default_col_width)
        else:
            col_widths.append(default_col_width)

    fig_width = max(8, sum(col_widths))
    row_height = 0.5
    fig_height = max(4, n_rows * row_height + 2)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')

    def truncate(val):
        return (val[:max_col_width] + '…') if isinstance(val, str) and len(val) > max_col_width else val

    truncated_values = [[truncate(val) for val in row] for row in df.values]
    truncated_columns = [truncate(col) for col in df.columns]

    table = ax.table(cellText=truncated_values, colLabels=truncated_columns, loc='center')

    fig.patch.set_facecolor(cs["background_color"])
    ax.set_facecolor(cs["background_color"])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    # Appliquer les largeurs de colonnes personnalisées
    for i, width in enumerate(col_widths):
        table.auto_set_column_width(i)
        for row in range(n_rows + 1):  # +1 pour l'en-tête
            cell = table[(row, i)]
            cell.set_width(width / sum(col_widths))

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor(cs["top_cells_color"])
            cell.set_text_props(color=cs["top_text_color"], weight='bold')
        else:
            cell.set_facecolor(cs["cells_color"])
            cell.set_text_props(color=cs["text_color"])
        cell.set_edgecolor(cs["grid_color"])

        # Centrer tout sur la colonne 2 (index 1)
        if col == 1:
            cell.set_text_props(ha='center', va='center')
        else:
            cell.set_text_props(ha='left', va='center')

    plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    plt.close()
