import numpy as np    # board stored as a 2D array
import pygame         # game window, drawing, and events
import sys            # sys.argv for player names, sys.exit to close
import os
from base_class import Basegame  # shared board, turn, save_result logic

EMPTY    = 0   # cell has no piece
PLAYER_1 = 1   # player 1's piece value on the board
PLAYER_2 = 2   # player 2's piece value on the board

GRID_SIZE   = 8   # 8×8 board
BOX_SIZE    = 60  # each cell is 60×60 pixels
MARGIN_SIZE = 40  # pixel offset from window edge to board edge


class Othello(Basegame):
    GAME_NAME = "othello"  # used when saving match results to history.csv

    def __init__(self, p1, p2, screen):
        super().__init__(p1, p2, 8)    # 8×8 board, player names, turn=1 — from Basegame
        self.screen    = screen
        self.board[3][3] = 2           # standard Othello starting position — 4 pieces in centre
        self.board[4][4] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.cell_size = 70            # pixel size of each drawn cell
        self.offset    = 50            # pixel gap between window edge and board start
        self.font      = pygame.font.SysFont('Arial', 20, bold=True)  # for the score text at top

    def get_valid_moves(self, player):
        moves    = []
        opponent = 3 - player  # players are 1 and 2, so 3-p always gives the other
        directions = [(1,0),(-1,0),(1,1),(-1,-1),(0,1),(0,-1),(-1,1),(1,-1)]  # all 8 directions
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:  # skip cells that already have a piece
                    continue
                for dr, dc in directions:
                    nr = i + dr   # step one cell in this direction
                    nc = j + dc
                    # first neighbour must be an opponent piece to bother walking further
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == opponent:
                        # walk in direction — valid move only if we find our own piece closing the bracket
                        while 0 <= nr < self.size and 0 <= nc < self.size:
                            if self.board[nr][nc] == 0:        # hit empty cell — no bracket, stop
                                break
                            if self.board[nr][nc] == player:   # found our own piece — bracket closed
                                moves.append((i, j))
                                break
                            nr = nr + dr   # keep walking along this direction
                            nc = nc + dc
                        else:
                            continue  # while exited without break (went off board) — not valid
        return list(set(moves))  # remove duplicates — two directions can validate the same cell

    def make_move(self, r, c):
        valid_moves = self.get_valid_moves(self.turn)
        if (r, c) not in valid_moves:   # clicked cell is not a legal move
            return False
        self.board[r][c] = self.turn    # place our piece
        opponent = 3 - self.turn        # same 3-p trick to get opponent value
        directions = [(0,1),(0,-1),(1,1),(1,0),(1,-1),(-1,0),(-1,1),(-1,-1)]
        for dr, dc in directions:
            flip = []            # opponent pieces sandwiched in this direction
            nr   = r + dr
            nc   = c + dc
            while 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == opponent:
                flip.append((nr, nc))   # collect opponent pieces as we walk
                nr = nr + dr
                nc = nc + dc
            if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == self.turn:
                for i, j in flip:
                    self.board[i][j] = self.turn  # only flip if our piece closes the bracket at the end
        self.switch_turn()
        if not self.get_valid_moves(self.turn):
            self.switch_turn()  # skip turn if the next player has no valid moves
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))  # black background — only the board area gets green
        board_px = self.size * self.cell_size  # total pixel width/height of the board
        pygame.draw.rect(self.screen, (0, 100, 0), (self.offset, self.offset, board_px, board_px))  # green only inside the board

        # draw the square grid lines
        for i in range(self.size + 1):
            pygame.draw.line(self.screen, (0, 0, 0),
                (self.offset + i * self.cell_size, self.offset),
                (self.offset + i * self.cell_size, self.offset + self.size * self.cell_size), 2)  # vertical line
            pygame.draw.line(self.screen, (0, 0, 0),
                (self.offset, self.offset + i * self.cell_size),
                (self.offset + self.size * self.cell_size, self.offset + i * self.cell_size), 2)  # horizontal line

        for r in range(self.size):
            for c in range(self.size):
                cx = self.offset + c * self.cell_size + self.cell_size // 2  # pixel centre x of this cell
                cy = self.offset + r * self.cell_size + self.cell_size // 2  # pixel centre y of this cell
                if self.board[r, c] != 0:  # only draw a circle if a piece is there
                    color = (0, 0, 0) if self.board[r, c] == 1 else (255, 255, 255)  # player 1 = black, player 2 = white
                    pygame.draw.circle(self.screen, color, (cx, cy), 30)

        p1_s = np.sum(self.board == 1)   # count player 1's pieces
        p2_s = np.sum(self.board == 2)   # count player 2's pieces
        txt  = f"{self.p1}: {p1_s} | {self.p2}: {p2_s} | Turn: {self.player_name()}"  # score + turn display
        self.screen.blit(self.font.render(txt, True, (255, 255, 255)), (self.offset, 30))

    def check_win(self):
        if not self.get_valid_moves(1) and not self.get_valid_moves(2):  # game over when both players are stuck
            c1 = np.sum(self.board == 1)   # count player 1's pieces
            c2 = np.sum(self.board == 2)   # count player 2's pieces
            if c1 > c2:
                return self.p1   # player 1 wins
            if c2 > c1:
                return self.p2   # player 2 wins
            return "Draw"        # equal pieces — it's a draw
        return None  # game is still ongoing


def main():
    p1     = sys.argv[1] if len(sys.argv) > 1 else "Player 1"  # read player names from command line
    p2     = sys.argv[2] if len(sys.argv) > 2 else "Player 2"
    pygame.init()

    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("OTHELLO")
    game   = Othello(p1, p2, screen)  # create a new game instance
    clock  = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                c = (mx - game.offset) // 70   # convert pixel x to column index
                r = (my - game.offset) // 70   # convert pixel y to row index
                if 0 <= c < 8 and 0 <= r < 8:  # make sure click is inside the board
                    game.make_move(r, c)

        game.draw()
        winner = game.check_win()
        if winner:
            pygame.display.flip()
            pygame.time.wait(2000)  # pause 2 seconds so players can see the result
            if winner != "Draw":
                loser = game.p2 if winner == game.p1 else game.p1  # the other player loses
                game.save_result(winner, loser)  # write result to history.csv
            pygame.quit()
            sys.exit()

        pygame.display.flip()   # push everything drawn this frame to the screen
        clock.tick(60)          # cap at 60 FPS


if __name__ == "__main__":
    main()
