<p align="center">
<img src="SPC_assets/banner.png" alt="Banner SPC" style="width:100%">
</p>

# Super Python Calculator

A complete calculator for scoring tournament for Super Animal Royale. It supports solo, duo and squads, offer the possibilitie to export leaderboards and its highly customizable !

## Features

The project is still being developped, but here are what the script can do so far :

- No limits for the numbers of games and let the games be added or removed with ease
- Autodectection of the players throughout an entire event
- Option to ban player while adjusting the placement
- Tools to easely create teams and not struggle with PlayfabID
- Supporting scoring preset depending on the number of players, placement and kills
- Customization of the colors and the font of exported graphics
- Web server to display the leaderboard in real time (beta)

You can always ask new feature of course (Don't know if I'll code them tho)

## Running SPC

To run the code, download the lastest version, unzip the file, and open the program called "Super.Python.Calculator.py" with your favorite python IDE. Install the missing libraries if needed and run the code !


### Adding rounds

To add a new round, simply copy the /getplayers data into a .txt file and place it in the same folder as this script. The rounds will then be included in the scoring.

Also be sure to not use the SPC_ prefix for the rounds, Otherwise, they may get excluded or even overriten and you could lose data



### Edit the scoring

To create a new scoring preset:

1. Navigate to the `SPC_scoring_presets` folder.
2. Create a new Python file (e.g., `SPC_custom_preset.py`).
3. Define the following functions in the file:
   - `kill_points(placement, kills, total_players)`: Returns the points for kills.
   - `placement_points(placement, kills, total_players)`: Returns the points for placement.
   - `masterkill(masterkill_status, total_players)`: Returns the bonus points for achieving the highest kills in a round.
4. Save the file.

To load your custom preset:

1. Open `Super.Python.Calculator.py`.
2. Locate the line:
   ```python
   from SPC_scoring_presets.SPC_sp_spi import kill_points, placement_points, masterkill
   ```
3. Replace `SPC_sp_spi` with the name of your custom preset file (without the `.py` extension). For example:
   ```python
   from SPC_scoring_presets.SPC_custom_preset import kill_points, placement_points, masterkill
   ```
4. Save the changes and run the program.



### Edit the colors of the graphs

To customize the colors of the graphs:

1. Navigate to the `SPC_color_schemes` folder.
2. Open the file `SPC_cs_v4.json` to modify the existing color scheme, or create a new JSON file (e.g., `SPC_custom_colors.json`) with the following structure: (It's of course an exemple for some colors, maybe duplicate a file an edit it might be a great idea)
   ```json
   { 
    "background_color": "#272727",
    
    "title_color": "#00ff00",
    "date_color": "#28ad36",
    "points_color": "#00ff00",

    "legend_border_color": "#28ad36",
    "legend_text_color": "#00ff00",

    "gradient_colors": ["#00ff00","#195719"],
      ...
   }
   ```
3. Save the file in the `SPC_color_schemes` folder.

To load your custom color scheme:

1. Open `Super.Python.Calculator.py`.
2. Locate the line:
   ```python
   color_scheme = "SPC_color_schemes/SPC_cs_v4.json"
   ```
3. Replace `SPC_cs_v4.json` with the name of your custom file (e.g., `SPC_custom_colors.json`):
   ```python
   color_scheme = "SPC_color_schemes/SPC_custom_colors.json"
   ```
4. Save the changes and run the program.

The updated colors will be applied the next time you run the program.



### Change the font used

To customize the font used in the graphs:

1. Navigate to the `SPC_fonts` folder.
2. Add your custom font file (e.g., `MyCustomFont.ttf`) to this folder.
3. Open `Super.Python.Calculator.py`.
4. Locate the following lines:
   ```python
   add_custom_fonts = True
   font_path = "SPC_fonts/Rubik.ttf"
   ```
5. Replace `"SPC_fonts/Rubik.ttf"` with the path to your custom font file. For example:
   ```python
   font_path = "SPC_fonts/MyCustomFont.ttf"
   ```
6. Save the changes and run the program.

The updated font will be applied globally to all graphs the next time you run the program.

### Run the web server (beta)
You can now open a web server ! It's very not that great, but hey, at least it's available !
(You may need to run another instance of python for this to work, and it may not work on all OS)

How to proceed ? (one method among many)
0. Make sure you have the required libraries installed (Flask, Flask-Cors, etc.). You may also need to follow a tutorial to configure ngrok
1. Open the file in the SPC_web folder called `SPC_web.py` with python (I run it without IDE, since VS doesnt support two instances of python at the same time)
2. When you launch the script, you should these lines in the console:
   ```
    * ngrok tunnel: NgrokTunnel: "https://4db8-37-65-10-130.ngrok-free.app" -> "http://localhost:5000"
   * Local:        http://127.0.0.1:5000
   * Serving Flask app 'web'
   * Debug mode: off
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://192.168.1.135:5000
   ```
   you'll just need to copy the first link (the one with ngrok) and paste it in your browser ! (Make sure you don't close the console, or the server will stop running. Also the url changes every time you run the script, so you'll need to copy it again if you close the tab)
3. Now when you'll launch the SPC.py script, you'll be able to see the leaderboard in your browser ! (You may need to refresh the page if you already had it open)