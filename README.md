# Mini Hub GTA1

A two-player game hub where both players log in through the terminal and then pick a game from a graphical menu. Play, see the leaderboard, check the stats, and decide if you want another round or call it a day.

Done by Geetha Sri and Teenu Anand

# what do i need

Python 3.10 or above, and these three packages:

pygame-ce
numpy
matplotlib

we nee to use git bash 
as terminals change the speed of the game is varying as of now git bash is working fine for us so use git bash to run commands


Just run:
pip install pygame-ce numpy matplotlib

You also need Bash with `sha256sum` available — comes default on Linux/macOS, use Git Bash on Windows.



# Running it

Go to the project folder and run:

bash main.sh

Both players enter their username and password. First time? It'll ask if you want to register. Once both are in, the game hub opens up.



# Folder structure


Mini_Hub_GTA1/
── main.sh           — where everything starts — handles login for both players
── game.py           — the main hub window, game picker, charts, and post-game flow
── leaderboard.sh    — prints wins/losses/ratio to the terminal after each game
── history.csv       — every match ever played gets logged here
── users.tsv         — stores usernames and their SHA-256 hashed passwords
── home.png          — background for the main menu screen
── hom.png           — background for the post-game screens
── tictactoe.png     — game card image shown in the menu
── othello.png       — game card image shown in the menu
── connect4.png      — game card image shown in the menu
── games/
    ─ base_class.py — the parent class all three games inherit from
    ─ tictactoe.py  — 10×10 board, need 5 in a row to win
    ─ othello.py    — 8×8 Reversi with disc flipping
    ─ connect4.py   — 7×7 gravity drop, 4 in a row wins




# The games

Tic-Tac-Toe is a 10 × 10 grid format , Get 5 in a row — horizontal, vertical, or diagonal for a win

Othello is a 8 × 8 grid format. Have more discs than your opponent when neither of you can move that is a win.

Connect 4 is a  7 × 7 grid. Drop 4 coins in a row — any direction that is a win for whoever does it first

#After each game

Once a game ends it goes through three steps before asking if you want to play again:

1. Terminal prints the leaderboard — you pick whether to sort by wins, losses, or W/L ratio
2. Hub window shows a bar chart of the top 5 players and a pie chart of which games get played most
3. Choose to go back to the menu or quit

