import tkinter as tk
from tkinter import Listbox, MULTIPLE, messagebox
import os

def creation_player_list(dict_base):
    """
    Create a list of players from the base dictionary.
    Returns a list of tuples (PlayfabID, PlayerName).
    """
    player_list = []
    for playfab_id, player_info in dict_base.items():
        player_name = player_info[0]
        player_list.append([playfab_id, player_name])
    return player_list

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
    player_list = creation_player_list(dict_base)  # Convert the base dictionary to a player list
    # Variable to store the teams to return
    teams = []
    team_names_display = []  # For displaying team member names in the interface

    # Function to create a team
    def create_team():
        """
        Create a team from selected players.
        """
        selected_indices = player_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No player selected", "Please select at least one player.")
            return
        team_ids = []  # To store the IDs of the players in the team
        team_names = []  # To store the names of the players in the team
        for index in selected_indices[::-1]:  # Iterate in reverse to avoid indexing issues
            player_id, player_name = player_list[index]
            team_ids.append(player_id)
            team_names.append(player_name)
            player_list.pop(index)
        teams.append(team_ids)  # Store the IDs in the teams list
        team_names_display.append(team_names)  # Store the names for display
        update_listboxes()

    # Function to dissolve a team
    def dissolve_team():
        """
        Dissolve a selected team and return its players to the available list.
        """
        selected_indices = team_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No team selected", "Please select a team to dissolve.")
            return
        for index in selected_indices[::-1]:  # Iterate in reverse to avoid indexing issues
            team_ids = teams.pop(index)  # Get the IDs of the dissolved team
            team_names = team_names_display.pop(index)  # Get the names of the dissolved team
            # Reintegrate the players into the available player list
            for player_id, player_name in zip(team_ids, team_names):
                player_list.append([player_id, player_name])
        update_listboxes()

    # Function to finish and close the window
    def finish():
        """
        Close the main loop and destroy the window.
        """
        root.quit()
        root.destroy()

    # Function to update the Listboxes
    def update_listboxes():
        """
        Update the player and team Listboxes with current data.
        """
        # Update the list of available players
        player_listbox.delete(0, tk.END)
        for player in player_list:
            player_listbox.insert(tk.END, player[1])

        # Update the list of created teams (displaying player names)
        team_listbox.delete(0, tk.END)
        for team_names in team_names_display:
            team_listbox.insert(tk.END, ', '.join(team_names))

    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Super Team Creator - From SPC")
    root.configure(bg='#191919')  # Dark background

    # Button style
    button_style = {
        'bg': '#191919',
        'fg': '#ecf0f1',
        'font': ('Helvetica', 14),
        'relief': tk.RAISED,
        'borderwidth': 2
    }

    # Frame for Listboxes and Scrollbars
    listbox_frame = tk.Frame(root, bg='#191919')
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Listbox to display available players
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

    # Scrollbar for the player Listbox
    player_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=player_listbox.yview)
    player_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    player_listbox.config(yscrollcommand=player_scrollbar.set)

    # Listbox to display created teams (player names)
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

    # Scrollbar for the team Listbox
    team_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=team_listbox.yview)
    team_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    team_listbox.config(yscrollcommand=team_scrollbar.set)

    # Frame for buttons (arranged vertically)
    button_frame = tk.Frame(root, bg='#191919')
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    # Buttons arranged vertically
    create_team_button = tk.Button(button_frame, text="Create a team", command=create_team, **button_style)
    create_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    dissolve_team_button = tk.Button(button_frame, text="Dissolve a team", command=dissolve_team, **button_style)
    dissolve_team_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    finish_button = tk.Button(button_frame, text="Finished !", command=finish, **button_style)
    finish_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

    # Initialize the Listboxes
    update_listboxes()

    # Start the main loop
    root.mainloop()

    # Save and return the list of teams after closing the window
    save_teams(teams)
    return teams