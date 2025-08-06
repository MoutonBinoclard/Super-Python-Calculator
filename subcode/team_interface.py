import tkinter as tk
from tkinter import Listbox, MULTIPLE, messagebox
import os

from subcode.find_mate import find_most_probable_teams

def creation_player_list(dict_base):
    """
    Convert the base dict to the good format so we can
    launch the team creation interface.
    """
    list_players = []
    for id in dict_base:
        current = [id, dict_base[id]['name']]
        list_players.append(current)
    return list_players

def save_teams(teams, file="SPC_teams.txt"):
    """
    Save the teams to a text file.
    """
    with open(file, "w", encoding="utf-8") as f:
        for team in teams:
            f.write(" ".join(team) + "\n")

def load_teams(file="SPC_teams.txt"):
    """
    Load teams from a text file if it exists.
    """
    if os.path.exists(file):
        teams = []
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                teams.append(line.strip().split(" "))
        return teams
    return None

def team_creation_interface(dict_base):
    """
    Launch the team creation interface for selecting and grouping players into teams.
    Returns the list of teams created.
    """
    probable_mate_for_each_player = find_most_probable_teams(dict_base)
    player_list = creation_player_list(dict_base)  # Convert the base dictionary to a player list
    teams = []
    team_names_display = []

    # Function to create a team
    def create_team():
        selected_indices = player_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No player selected", "Please select at least one player.")
            return
        team_ids = []
        team_names = []
        for index in sorted(selected_indices, reverse=True):
            player_id, player_name = player_list[index]
            team_ids.append(player_id)
            team_names.append(player_name)
            player_list.pop(index)
        teams.append(team_ids)
        team_names_display.append(team_names)
        update_listboxes()

    # Function to dissolve a team
    def dissolve_team():
        selected_indices = team_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No team selected", "Please select a team to dissolve.")
            return
        for index in sorted(selected_indices, reverse=True):
            team_ids = teams.pop(index)
            team_names = team_names_display.pop(index)
            for player_id, player_name in zip(team_ids, team_names):
                player_list.append([player_id, player_name])
        update_listboxes()

    def finish():
        root.quit()
        root.destroy()

    def update_listboxes():
        player_listbox.delete(0, tk.END)
        for player in player_list:
            player_listbox.insert(tk.END, player[1])
        team_listbox.delete(0, tk.END)
        for team_names in team_names_display:
            team_listbox.insert(tk.END, ', '.join(team_names))
        highlight_probable_mates()

    def highlight_probable_mates(event=None):
        # Remove all custom tags/colors first
        for i in range(len(player_list)):
            player_listbox.itemconfig(i, {'bg': '#191919', 'fg': '#ecf0f1'})
        selected_indices = player_listbox.curselection()
        if not selected_indices:
            return
        # Collect all probable mates from selected players
        probable_ids = set()
        for idx in selected_indices:
            player_id = player_list[idx][0]
            probable_ids.update(probable_mate_for_each_player.get(player_id, []))
        # Highlight probable mates
        for i, (pid, _) in enumerate(player_list):
            if pid in probable_ids and i not in selected_indices:
                player_listbox.itemconfig(i, {'bg': '#a94442', 'fg': '#fff'})  # reddish bg

    root = tk.Tk()
    root.title("Super Team Creator - From SPC")
    root.configure(bg='#191919')

    button_style = {
        'bg': '#191919',
        'fg': '#ecf0f1',
        'font': ('Helvetica', 14),
        'relief': tk.RAISED,
        'borderwidth': 2
    }

    listbox_frame = tk.Frame(root, bg='#191919')
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    player_listbox = Listbox(
        listbox_frame,
        selectmode=MULTIPLE,
        bg='#191919',
        fg='#ecf0f1',
        font=('Helvetica', 14),
        width=30,
        height=15,
        selectbackground='#777777',
        selectforeground='#ecf0f1',
        activestyle='none'
    )
    player_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    player_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=player_listbox.yview)
    player_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    player_listbox.config(yscrollcommand=player_scrollbar.set)

    team_listbox = Listbox(
        listbox_frame,
        selectmode=tk.SINGLE,
        bg='#191919',
        fg='#ecf0f1',
        font=('Helvetica', 14),
        width=30,
        height=15,
        selectbackground='#777777',
        selectforeground='#ecf0f1',
        activestyle='none'
    )
    team_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    team_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=team_listbox.yview)
    team_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    team_listbox.config(yscrollcommand=team_scrollbar.set)

    button_frame = tk.Frame(root, bg='#191919')
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    create_team_button = tk.Button(button_frame, text="Create a team", command=create_team, **button_style)
    create_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    dissolve_team_button = tk.Button(button_frame, text="Dissolve a team", command=dissolve_team, **button_style)
    dissolve_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    finish_button = tk.Button(button_frame, text="Finished !", command=finish, **button_style)
    finish_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    update_listboxes()

    # Bind selection event to highlight probable mates
    player_listbox.bind('<<ListboxSelect>>', highlight_probable_mates)

    root.mainloop()

    save_teams(teams)
    return teams
