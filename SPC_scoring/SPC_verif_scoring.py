from sar_weeklies import placement_points, kill_points, masterkill
import numpy as np
import plotly.graph_objects as go




def matrice_points(joueur):
    matrice = np.zeros((64, 64))
    for i in range(64):
        for j in range(64):
            matrice[i][j] = placement_points(i+1, j, joueur) + kill_points(i+1, j, joueur)

    return matrice


j30=matrice_points(64)
print(j30)

fig = go.Figure(data=[go.Surface(z=j30)])
fig.update_layout(title='ok boomer', scene=dict(
    xaxis_title='Kills',
    yaxis_title='Placement',
    zaxis_title='Points'
))
fig.show()