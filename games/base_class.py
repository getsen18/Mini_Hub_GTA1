import numpy as np   # numpy for the 2D board array
import os            # for building the history file path
import time          # for getting today's date

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.csv")  # go up two dirs from games/ to reach project root


class Basegame:
    GAME_NAME = ""  # overridden by each game subclass (e.g. "connect4")

    def __init__(self, p1, p2, size):
        self.p1    = p1                       # player 1 name
        self.p2    = p2                       # player 2 name
        self.size  = size                     # board is size × size
        self.board = np.zeros((size, size))   # empty board — 0 means no piece placed
        self.turn  = 1                        # player 1 always goes first

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1  # toggle between player 1 and player 2

    def player_name(self):
        return self.p1 if self.turn == 1 else self.p2  # returns the name of whoever's turn it is

    def save_result(self, winner, loser):
        date = time.strftime("%Y-%m-%d")         # today's date in YYYY-MM-DD format
        with open(HISTORY_FILE, "a", newline='\n') as f:  # newline='\n' stops Windows translating \n → \r\n — bash can't strip the \r
            f.write(f"{winner},{loser},{date},{self.GAME_NAME}\n")  # one line per match
