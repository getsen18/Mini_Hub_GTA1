import sys
import time
import os
import subprocess
from games import tictactoe
from games import othello
from games import connect4
if len(sys.argv != 3):
   print("Try givin correct command lil bro")
   sys.exit()
player1=sys.argv[1]
player2=sys.argv[2]
def save_result(winner,loser,game_name):
   date=time.strftime("%Y-%m-%d")
   with open("history.csv") as f:
      f.write(f"{winner},{loser},{data},{game_name}")
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen, font):
        pygame.draw.rect(screen, (100, 200, 255), self.rect)
        label = font.render(self.text, True, (0, 0, 0))
        screen.blit(label, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
def show_leaderboard(screen, font):
    result = subprocess.run(
        ["bash", "leaderboard.sh"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.split("\n")

    screen.fill((255, 255, 255))

    y = 50
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (50, y))
        y += 30