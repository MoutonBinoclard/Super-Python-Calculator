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


def creer_et_sauvegarder_tableau(file_path, output_path, max_col_width=30):
    data = creation_dictionnaire_tableau(file_path)
    data = remplir_dictionnaire_tableau(file_path, data)
    print(data)

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.axis('off')

    def truncate(val):
        return (val[:max_col_width] + '…') if isinstance(val, str) and len(val) > max_col_width else val

    truncated_values = [[truncate(val) for val in row] for row in df.values]
    truncated_columns = [truncate(col) for col in df.columns]

    table = ax.table(cellText=truncated_values, colLabels=truncated_columns, loc='center')

    fig.patch.set_facecolor('#222222')
    ax.set_facecolor('#222222')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 2)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#333333')
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor('#222222')
            cell.set_text_props(color='white')
        cell.set_edgecolor('#444444')

    plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
    plt.close()
