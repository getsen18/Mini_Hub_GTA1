import pygame
import numpy as np
import sys

ROWS_NUM=7
COLS_NUM=7
WIN_LENGTH=4

def create_board(row,col):
    board = np.zeros((row,col))
    return board

def drop_ball(board,row,col,ball):
    
    board[row][col] = ball

def valid_loc(board,col):
    if board[ROWS_NUM-1][col] == 0:
        return True
    else:
        return False

def next_open_row(board,col):
    for r in range(ROWS_NUM):
        if board[r][col] == 0:
            return r
        
def print_board(board):
    print(np.flip(board,0))




board = create_board(ROWS_NUM,COLS_NUM)
print_board(board)
game_done = False 
turn = 0




while not game_done:
    #Input of Player 1
    if turn == 0:

        col = int(input("Player1 plz give your input col: "))
        if valid_loc(board,col):
            row = next_open_row(board,col)
            drop_ball(board,row,col,1)
        print_board(board)

    else:

        col = int(input("Player2 plz give your input col:"))
        if valid_loc(board,col):
            row = next_open_row(board,col)
            drop_ball(board,row,col,2)
        print_board(board)
        
    turn +=1
    turn = turn%2

def is_winning_ball(board,ball):
    b = (board == ball).astype(int)
    n = ROWS_NUM - WIN_LENGTH + 1

    # horizontal
    horiz = sum(b[:, k:n+k] for k in range(WIN_LENGTH))
    if np.any(horiz == WIN_LENGTH):
        return True

    # vertical
    verti = sum(b[k:n+k, :] for k in range(WIN_LENGTH))
    if np.any(verti == WIN_LENGTH):
        return True

    # main diagonal
    diag = sum(b[k:n+k, k:n+k] for k in range(WIN_LENGTH))
    if np.any(diag == WIN_LENGTH):
        return True

    # anti-diagonal 
    b_flip = np.fliplr(b)
    adiag  = sum(b_flip[k:n+k, k:n+k] for k in range(WIN_LENGTH))
    if np.any(adiag == WIN_LENGTH):
        return True

    return False

def draw_board(board):
    SQUARE_SIZE=100
    RADIUS=int(SQUARE_SIZE/2 -5)
    screen = pygame.display.set_mode(size)
    WIDTH=COLS_NUM*SQUARE_SIZE
    HEIGHT=(ROWS_NUM+1)*SQUARE_SIZE
    size=(WIDTH,HEIGHT)
    for c in COLS_NUM:
        for r in ROWS_NUM:
            pygame.draw.rect(screen,BLUE,c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.circle(screen,BLACK,int(c*(SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2),RADIUS))

    for c in range(COLS_NUM):
	    for r in range(ROWS_NUM):		
		    if board[r][c] == 1:
			    pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), HEIGHT-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
          




SQUARE_SIZE=100
RADIUS=int(SQUARE_SIZE/2 -5)
screen = pygame.display.set_mode(size)
WIDTH=COLS_NUM*SQUARE_SIZE
HEIGHT=(ROWS_NUM+1)*SQUARE_SIZE
size=(WIDTH,HEIGHT)

draw_board(board)


    
    



