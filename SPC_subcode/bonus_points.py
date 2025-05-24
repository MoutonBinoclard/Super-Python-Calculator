
def ajuster_bonus_interface(liste_indice_points):
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.title("Ajuster les points bonus")

    entries = []

    # En-têtes
    tk.Label(root, text="Nom").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(root, text="Points bonus").grid(row=0, column=1, padx=10, pady=5)

    # Affichage des noms et champs d'entrée pour les points bonus
    for i, (id_, nom, pt_bonus) in enumerate(liste_indice_points):
        tk.Label(root, text=nom).grid(row=i+1, column=0, padx=10, pady=2)
        entry = tk.Entry(root, width=5)
        entry.insert(0, str(pt_bonus))
        entry.grid(row=i+1, column=1, padx=10, pady=2)
        entries.append(entry)

    result = []

    def valider():
        for idx, entry in enumerate(entries):
            try:
                val = int(entry.get())
            except ValueError:
                val = 0
            # Met à jour la liste avec la nouvelle valeur
            liste_indice_points[idx][2] = val
        result.extend(liste_indice_points)
        root.destroy()

    bouton = tk.Button(root, text="Valider", command=valider)
    bouton.grid(row=len(liste_indice_points)+1, column=0, columnspan=2, pady=10)

    root.mainloop()
    return result

def ajout_bonus_valeur(leaderboard3):
    liste_indice_points = []
    for keys in leaderboard3:
        liste_indice_points.append([keys, leaderboard3[keys][0], 0])
    
    liste_indice_points=ajuster_bonus_interface(liste_indice_points)

    return liste_indice_points

def ajout_bonus(leaderboard2):
    listes_bonus = ajout_bonus_valeur(leaderboard2)

    for keys in leaderboard2:
        leaderboard2[keys][2].append([0,0])

    for ID, nom, pt_bonus in listes_bonus:
        leaderboard2[ID][2][-1][0] = pt_bonus

    return leaderboard2