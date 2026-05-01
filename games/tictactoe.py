import pygame          # game window, drawing, and events
import numpy as np     # board stored as a 2D array
import sys             # sys.argv for player names, sys.exit to close
from base_class import Basegame  # shared board, turn, save_result logic

EMPTY    = 0   # cell has no piece
PLAYER_1 = 1   # player 1's value on the board
PLAYER_2 = 2   # player 2's value on the board

BG_RED    = ( 50,  15,  15)   # dark red background — shown during player 1's turn
BG_BLUE   = ( 15,  15,  50)   # dark blue background — shown during player 2's turn
BG_DRAW   = ( 30,  30,  30)   # neutral dark background — shown on draw
G_COLOUR  = (120, 120, 120)   # grid line colour
RED       = (220,  50,  50)   # X colour
BLUE      = ( 50,  50, 220)   # O colour
YELLOW    = (255, 220,   0)   # win message colour
GRAY      = (160, 160, 160)   # draw message colour
WHITE     = (255, 255, 255)
DARK_BLUE   = (  0,  80, 100)   # button colour (normal) — used in main menu buttons
LIGHT_BLUE  = (  0, 125, 255)   # button colour (hovered) — used in main menu buttons
RUSTIC_GREY = (105, 105, 105)   # end screen button normal colour
GOLD        = (255, 220,   0)   # end screen button hover colour

GRID_SIZE   = 10                                      # 10×10 board
WIN_LENGTH  = 5                                       # need 5 in a row to win
BOX_SIZE    = 60                                      # each cell is 60×60 pixels
MARGIN_SIZE = 40                                      # pixel gap around the board
TOT_SIZE    = MARGIN_SIZE + GRID_SIZE * BOX_SIZE      # pixel coordinate of the board's far edge
WIDTH       = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE  # total window width
HEIGHT      = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE + 80  # +80 for the status bar at the bottom
MINES=[(3,4),(5,6),(4,3),(8,6),(8,7),(4,6),(2,4),(2,3),(4,4)]


class TicTacToe(Basegame):
    GAME_NAME  = "tictactoe"  # used when saving match results to history.csv
    WIN_LENGTH = 5            # need 5 in a row to win

    def make_move(self, row, col):
        if self.board[row][col] != EMPTY:  # cell already taken — reject the move
            return False
        if (row,col) in MINES:
            self.board[row][col] = 3-self.turn   # place current player's piece
        else:
            self.board[row][col]=self.turn
        return True

    def check_win(self):
        b = (self.board == self.turn).astype(int)  # binary mask — 1 where current player has a piece, 0 elsewhere
        n = self.size - self.WIN_LENGTH + 1        # number of valid window start positions along any axis

        # sliding window trick — shift b by 0,1,2,3,4 and add; any cell summing to 5 means 5 in a row
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

        return False  # no 5-in-a-row found in any direction

    def is_draw(self):
        return not np.any(self.board == EMPTY)  # no empty cells left — board is full

    def draw_board(self, screen, font_piece, msg_font, status, status_c, bg):
        screen.fill(bg)  # fill background with the current player's colour

        for i in range(GRID_SIZE + 1):      # draw GRID_SIZE+1 lines to form GRID_SIZE columns/rows
            x = MARGIN_SIZE + i * BOX_SIZE
            y = MARGIN_SIZE + i * BOX_SIZE
            pygame.draw.line(screen, G_COLOUR, (x, MARGIN_SIZE), (x, TOT_SIZE), 1)  # vertical line
            pygame.draw.line(screen, G_COLOUR, (MARGIN_SIZE, y), (TOT_SIZE, y), 1)  # horizontal line

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cx = MARGIN_SIZE + col * BOX_SIZE + BOX_SIZE // 2  # pixel centre x of this cell
                cy = MARGIN_SIZE + row * BOX_SIZE + BOX_SIZE // 2  # pixel centre y of this cell

                if self.board[row][col] == PLAYER_1:
                    img = font_piece.render("X", True, RED)
                    screen.blit(img, img.get_rect(center=(cx, cy)))   # draw X centred in cell
                elif self.board[row][col] == PLAYER_2:
                    img = font_piece.render("O", True, BLUE)
                    screen.blit(img, img.get_rect(center=(cx, cy)))   # draw O centred in cell

        msg = msg_font.render(status, True, status_c)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 35)))  # status bar at bottom centre
        pygame.display.flip()  # push everything drawn this frame to the screen


def show_end_screen(screen, clock, message, msg_color):
    font_title = pygame.font.SysFont("Arial", 38, bold=True)
    font_btn   = pygame.font.SysFont("Arial", 26, bold=True)
    btn_w, btn_h = 200, 55
    cx = WIDTH // 2
    btn_again = pygame.Rect(cx - btn_w - 20, HEIGHT // 2 + 30, btn_w, btn_h)  # "Play Again" button rect
    btn_home  = pygame.Rect(cx + 20,         HEIGHT // 2 + 30, btn_w, btn_h)  # "Home" button rect

    hom_bg = pygame.transform.scale(pygame.image.load("hom.png"), (WIDTH, HEIGHT))  # fresh load for end screen background

    while True:
        screen.blit(hom_bg, (0, 0))  # hom.png background
        title = font_title.render(message, True, msg_color)
        screen.blit(title, title.get_rect(centerx=cx, y=HEIGHT // 2 - 50))  # result message at centre

        mouse = pygame.mouse.get_pos()

        color = GOLD if btn_again.collidepoint(mouse) else RUSTIC_GREY  # rustic grey → gold on hover
        pygame.draw.rect(screen, color, btn_again, border_radius=10)
        lbl = font_btn.render("Play Again", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=btn_again.center))

        color = GOLD if btn_home.collidepoint(mouse) else RUSTIC_GREY  # rustic grey → gold on hover
        pygame.draw.rect(screen, color, btn_home, border_radius=10)
        lbl = font_btn.render("Home", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=btn_home.center))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_again.collidepoint(mouse):
                    return "again"   # caller restarts the game
                if btn_home.collidepoint(mouse):
                    return "home"    # caller exits to hub


def main():
    p1 = sys.argv[1] if len(sys.argv) > 1 else "Player 1"  # read player names from command line
    p2 = sys.argv[2] if len(sys.argv) > 2 else "Player 2"

    pygame.init()
    screen     = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("10x10 Tic Tac Toe")
    font_piece = pygame.font.SysFont("Arial", 42, bold=True)  # large font for X and O
    font_msg   = pygame.font.SysFont("Arial", 20, bold=True)  # smaller font for status bar
    clock      = pygame.time.Clock()

    while True:   # outer loop — handles Play Again
        game      = TicTacToe(p1, p2, GRID_SIZE)  # fresh board each round
        game_over = False
        status    = f"{p1}'s turn"
        status_c  = WHITE
        end_msg   = ""
        end_color = WHITE

        while not game_over:
            clock.tick(60)
            bg = BG_RED if game.turn == PLAYER_1 else BG_BLUE  # background colour shows whose turn it is

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    col = (mx - MARGIN_SIZE) // BOX_SIZE  # convert pixel x to column index
                    row = (my - MARGIN_SIZE) // BOX_SIZE  # convert pixel y to row index

                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:  # make sure click is inside the board
                        if game.make_move(row, col):      # returns False if cell already occupied
                            if game.check_win():
                                winner    = game.player_name()
                                loser     = game.p2 if game.turn == PLAYER_1 else game.p1  # the other player loses
                                game.save_result(winner, loser)  # write result to history.csv
                                end_msg   = f"{winner} WINS!"
                                end_color = YELLOW
                                game.draw_board(screen, font_piece, font_msg, end_msg, end_color, bg)
                                pygame.time.wait(1500)    # pause 1.5s so players can see the win state
                                game_over = True

                            elif game.is_draw():
                                end_msg   = "It's a DRAW!"
                                end_color = GRAY
                                game.draw_board(screen, font_piece, font_msg, end_msg, end_color, BG_DRAW)
                                pygame.time.wait(1500)
                                game_over = True

                            else:
                                game.switch_turn()                          # no win yet — next player's turn
                                status   = f"{game.player_name()}'s turn"
                                status_c = BLUE if game.turn == PLAYER_2 else RED

            if not game_over:
                game.draw_board(screen, font_piece, font_msg, status, status_c, bg)  # redraw every frame

        choice = show_end_screen(screen, clock, end_msg, end_color)
        if choice == "home":
            pygame.quit()
            sys.exit()
        # "again" → outer while restarts with a fresh game


if __name__ == "__main__":
    main()
