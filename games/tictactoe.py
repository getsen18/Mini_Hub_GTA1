import pygame
import numpy as np
import sys

EMPTY    = 0
PLAYER_1 = 1
PLAYER_2 = 2

BG       = ( 30,  30,  30)
G_COLOUR = (120, 120, 120)
RED      = (220,  50,  50)
BLUE     = ( 50,  50, 220)
YELLOW   = (255, 220,   0)
GRAY     = (160, 160, 160)
WHITE    = (255, 255, 255)

GRID_SIZE   = 10
WIN_LENGTH  = 5
BOX_SIZE    = 60
MARGIN_SIZE = 40
TOT_SIZE    = MARGIN_SIZE + GRID_SIZE * BOX_SIZE

WIDTH  = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE
HEIGHT = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE + 80


def make_board():
    return np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)


def check_winner(board, player):
    b = (board == player).astype(int)
    n = GRID_SIZE - WIN_LENGTH + 1

    # horizontal
    horiz = sum(b[:, k:n+k] for k in range(WIN_LENGTH))
    if np.any(horiz == WIN_LENGTH):
        return True

    # vertical
    verti = sum(b[k:n+k, :] for k in range(WIN_LENGTH))
    if np.any(verti == WIN_LENGTH):
        return True

    # main diagonal (top-left to bottom-right)
    diag = sum(b[k:n+k, k:n+k] for k in range(WIN_LENGTH))
    if np.any(diag == WIN_LENGTH):
        return True

    # anti-diagonal (top-right to bottom-left)
    b_flip = np.fliplr(b)
    adiag  = sum(b_flip[k:n+k, k:n+k] for k in range(WIN_LENGTH))
    if np.any(adiag == WIN_LENGTH):
        return True

    return False


def draw_board(screen, board, font_piece, msg_font, status, status_c):
    screen.fill(BG)

    for i in range(GRID_SIZE + 1):
        x = MARGIN_SIZE + i * BOX_SIZE
        y = MARGIN_SIZE + i * BOX_SIZE
        pygame.draw.line(screen, G_COLOUR, (x, MARGIN_SIZE), (x, TOT_SIZE), 1)
        pygame.draw.line(screen, G_COLOUR, (MARGIN_SIZE, y), (TOT_SIZE, y), 1)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cx = MARGIN_SIZE + col * BOX_SIZE + BOX_SIZE // 2
            cy = MARGIN_SIZE + row * BOX_SIZE + BOX_SIZE // 2

            if board[row][col] == PLAYER_1:
                img = font_piece.render("X", True, RED)
                screen.blit(img, img.get_rect(center=(cx, cy)))
            elif board[row][col] == PLAYER_2:
                img = font_piece.render("O", True, BLUE)
                screen.blit(img, img.get_rect(center=(cx, cy)))

    msg = msg_font.render(status, True, status_c)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 35)))

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("10x10 Tic Tac Toe")

    font_piece = pygame.font.SysFont("Arial", 42, bold=True)
    font_msg   = pygame.font.SysFont("Arial", 20, bold=True)

    clock = pygame.time.Clock()

    board          = make_board()
    current_player = PLAYER_1
    game_over      = False
    status         = "Player 1's turn"
    status_c       = WHITE

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board          = make_board()
                current_player = PLAYER_1
                game_over      = False
                status         = "Player 1's turn"
                status_c       = WHITE

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over:
                    continue

                mx, my = event.pos
                col = (mx - MARGIN_SIZE) // BOX_SIZE
                row = (my - MARGIN_SIZE) // BOX_SIZE

                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if board[row][col] == EMPTY:
                        board[row][col] = current_player

                        if check_winner(board, current_player):
                            name     = "1" if current_player == PLAYER_1 else "2"
                            status   = f"Player {name} WINS!   press R to restart"
                            status_c = YELLOW
                            game_over = True

                        elif not np.any(board == EMPTY):
                            status   = "It's a DRAW!   press R to restart"
                            status_c = GRAY
                            game_over = True

                        else:
                            if current_player == PLAYER_1:
                                current_player = PLAYER_2
                                status   = "Player 2's turn"
                                status_c = BLUE
                            else:
                                current_player = PLAYER_1
                                status   = "Player 1's turn"
                                status_c = RED

        draw_board(screen, board, font_piece, font_msg, status, status_c)


main()
