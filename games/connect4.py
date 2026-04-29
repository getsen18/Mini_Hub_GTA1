import pygame          # game window, drawing, and events
import numpy as np     # board stored as a 2D array
import sys             # sys.argv for player names, sys.exit to close
from base_class import Basegame  # shared board, turn, save_result logic

BOARD_COLOR  = (105, 105, 105)   # rustic grey — outer board
BLACK        = (0,   0,   0)
PLAYER1_COLOR = (107, 142,  35)  # olive green — player 1
PLAYER2_COLOR = (245, 235, 210)  # cream/beige — player 2
SQUARE_SIZE = 100                          # each cell is 100×100 pixels
RADIUS = int(SQUARE_SIZE / 2 - 5)         # piece radius — slightly smaller than the cell
WHITE = (255,255,255)


class Connect4(Basegame):
    GAME_NAME  = "connect4"   # used when saving match results to history.csv
    ROWS       = 7            # 7 rows in the grid
    COLS       = 7            # 7 columns in the grid
    WIN_LENGTH = 4            # need 4 in a row to win

    def is_valid(self, col):
        return self.board[self.ROWS - 1][col] == 0  # top row empty — column still has space

    def next_open_row(self, col):
        for r in range(self.ROWS):        # scan from bottom row upward
            if self.board[r][col] == 0:
                return r                  # lowest empty row — gravity effect

    def drop(self, col):
        row = self.next_open_row(col)     # find where the piece will land
        self.board[row][col] = self.turn  # place current player's piece there

    def check_win(self):
        b = (self.board == self.turn).astype(int)  # binary mask — 1 where current player has a piece, 0 elsewhere
        n = self.ROWS - self.WIN_LENGTH + 1        # number of valid window start positions along any axis

        # sliding window trick — shift b by 0,1,2,3 columns and add; any cell summing to 4 means 4 in a row
        horiz = sum(b[:, k:n+k] for k in range(self.WIN_LENGTH))
        if np.any(horiz == self.WIN_LENGTH):
            return True

        verti = sum(b[k:n+k, :] for k in range(self.WIN_LENGTH))  # same trick but sliding rows top-to-bottom
        if np.any(verti == self.WIN_LENGTH):
            return True

        diag = sum(b[k:n+k, k:n+k] for k in range(self.WIN_LENGTH))  # shift both row and col together — checks main diagonal
        if np.any(diag == self.WIN_LENGTH):
            return True

        b_flip = np.fliplr(b)  # mirror horizontally so anti-diagonal becomes main diagonal
        adiag = sum(b_flip[k:n+k, k:n+k] for k in range(self.WIN_LENGTH))  # reuse diagonal check on flipped board
        if np.any(adiag == self.WIN_LENGTH):
            return True

        return False  # no 4-in-a-row found in any direction

    def draw(self, screen, width, height):
        for c in range(self.COLS):
            for r in range(self.ROWS):
                pygame.draw.rect(screen, BOARD_COLOR, (c*SQUARE_SIZE, r*SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # rustic grey cell background
                pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), int(r*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)  # empty hole

        for c in range(self.COLS):
            for r in range(self.ROWS):
                if self.board[r][c] == 1:
                    # height - ... flips y — row 0 is at the bottom but pygame draws y=0 at the top
                    pygame.draw.circle(screen, PLAYER1_COLOR, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, PLAYER2_COLOR, (int(c*SQUARE_SIZE + SQUARE_SIZE/2), height - int(r*SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)


def main():
    p1 = sys.argv[1] if len(sys.argv) > 1 else "Player 1"  # read player names from command line
    p2 = sys.argv[2] if len(sys.argv) > 2 else "Player 2"

    pygame.init()
    WIDTH  = Connect4.COLS * SQUARE_SIZE          # total window width in pixels
    HEIGHT = (Connect4.ROWS + 1) * SQUARE_SIZE    # +1 extra row at top for the hover preview strip
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect 4")
    myfont = pygame.font.SysFont("monospace", 75, bold=True)  # large bold font for the win/draw message
    clock  = pygame.time.Clock()

    game        = Connect4(p1, p2, Connect4.ROWS)  # create a new game instance
    game_done   = False
    winner_name = None
    loser_name  = None

    game.draw(screen, WIDTH, HEIGHT)  # show empty board before first move
    pygame.display.update()

    while not game_done:
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))  # clear the top hover strip each frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                posx  = event.pos[0]                           # horizontal mouse position
                color = PLAYER1_COLOR if game.turn == 1 else PLAYER2_COLOR  # show the current player's colour
                pygame.draw.circle(screen, color, (posx, SQUARE_SIZE // 2), RADIUS)  # floating piece follows mouse

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col  = int(posx // SQUARE_SIZE)                 # convert pixel x to column index

                if game.is_valid(col):                         # only drop if column isn't full
                    game.drop(col)                             # place piece at lowest open row

                    if game.check_win():
                        winner_name = game.player_name()
                        loser_name  = game.p2 if game.turn == 1 else game.p1  # the other player loses
                        color = PLAYER1_COLOR if game.turn == 1 else PLAYER2_COLOR
                        label = myfont.render(f"{winner_name} Wins!", 1, color)
                        screen.blit(label, (40, 10))
                        game_done = True
                    elif np.all(game.board != 0):              # no empty cells left — it's a draw
                        label = myfont.render("It's a DRAW!", 1, WHITE)
                        screen.blit(label, (40, 10))
                        game_done = True
                    else:
                        game.switch_turn()                     # no win yet — next player's turn

        game.draw(screen, WIDTH, HEIGHT)  # redraw board with the newly placed piece
        pygame.display.update()
        clock.tick(60)  # cap at 60 FPS

        if game_done:
            pygame.time.wait(3000)  # pause 3 seconds so players can see the result

    if winner_name:
        game.save_result(winner_name, loser_name)  # write result to history.csv

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
