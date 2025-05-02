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

## Run the web server (beta)
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
