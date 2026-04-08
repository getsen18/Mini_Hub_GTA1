import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe  –  10x10")
clock = pygame.time.Clock()

BG       = (15,  15,  28)    
GRID     = (70,  70, 110)  
P1_COLOR = (240,  80,  80)   
P2_COLOR = ( 80, 170, 255)  
WIN_CLR  = (255, 215,   0)   
HOVER    = ( 50,  50,  80)   


ROWS = COLS = 10    
WIN_LENGTH  = 5       
CELL        = 50    
BOARD_PX    = CELL * ROWS                   
OFFSET_X    = (WIDTH  - BOARD_PX) //2   
OFFSET_Y    = 110                          

font_large  = pygame.font.SysFont("Arial", 42, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small  = pygame.font.SysFont("Arial", 20)

PLAYER_NAMES = {1: "Player 1", 2: "Player 2"}
SYMBOLS      = {1: "X",        2: "O"}



def new_board():
    return [[0] * COLS for _ in range(ROWS)]


def draw_x(surface, cx, cy, size, color):
    
    h = size // 2
    pygame.draw.line(surface, color, (cx - h, cy - h), (cx + h, cy + h), 3)
    pygame.draw.line(surface, color, (cx + h, cy - h), (cx - h, cy + h), 3)


def check_winner(board, player):
    n = WIN_LENGTH
    for r in range(ROWS):
        for c in range(COLS - n + 1):
            if all(board[r][c + k] == player for k in range(n)):
                return [(r, c + k) for k in range(n)]
    for r in range(ROWS - n + 1):
        for c in range(COLS):
            if all(board[r + k][c] == player for k in range(n)):
                return [(r + k, c) for k in range(n)]
    for r in range(ROWS - n + 1):
        for c in range(COLS - n + 1):
            if all(board[r + k][c + k] == player for k in range(n)):
                return [(r + k, c + k) for k in range(n)]
    for r in range(ROWS - n + 1):
        for c in range(n - 1, COLS):
            if all(board[r + k][c - k] == player for k in range(n)):
                return [(r + k, c - k) for k in range(n)]
    return None 


def is_board_full(board):
    return all(board[r][c] != 0 for r in range(ROWS) for c in range(COLS))


