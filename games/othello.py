import numpy as np
import pygame
import sys
from game import Basegame
EMPTY=0
PLAYER_1=1
PLAYER_2=2
BG       = ( 30,  30,  30)
G_COLOUR = (120, 120, 120)
RED      = (220,  50,  50)
BLUE     = ( 50,  50, 220)
YELLOW   = (255, 220,   0)
GRAY     = (160, 160, 160)
WHITE    = (255, 255, 255)
GRID_SIZE   = 8
BOX_SIZE    = 60
MARGIN_SIZE = 40
TOT_SIZE    = MARGIN_SIZE + GRID_SIZE * BOX_SIZE
WIDTH  = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE
HEIGHT = GRID_SIZE * BOX_SIZE + 2 * MARGIN_SIZE + 80
class Othello:
 def make_board(Basegame):
    def __init__(self,p1,p2,screen):
      super().__init__(p1,p2,8)
      self.screen=screen
      self.board[3][3]=1
      self.board[4][4]=1
      self.board[3][4]=2
      self.board[4][3]=2
      self.cell_size = 70
      self.offset = 50
      self.font = pygame.font.SysFont('Arial', 20, bold=True)
    def get_valid_moves(self,player):
      moves=[]
      opponent=3-player
      directions=[(1,0),(-1,0),(1,1),(-1,-1),(0,1),(0,-1),(-1,1),(1,-1)]
      for i in range(self.size):
       for j in range(self.size):
         if self.board != 0:
           continue
         for dr,dc in directions:
           nr=i+dr
           nc=j+dc
           if 0<=nr<self.size and 0<=nc<self.size and self.board[nr][nc]==opponent:
             while 0<=nr<self.size and 0<=nc<self.size:
               if self.board[nr][nc]==0:
                 break
               if self.board[nr][nc]==player:
                 moves.append(i,j)
                 break
               nr=nr+dr
               nc=nc+dc
             else:continue
      return list(set(moves))
    def make_move(self,r,c):
      valid_moves=self.get_valid_moves(self.turn)
      if (r,c) not in valid_moves:
        return False
      self.board[r][c]=self.turn
      opponent=3-self.turn
      directions=[(0,1),(0,-1),(1,1),(1,0),(1,-1),(-1,0),(-1,1),(-1,-1)]
      for dr,dc in directions:
        flip=[]
        nr=r+dr
        nc=c+dc
        while 0<=nr<self.size and 0<=nc<self.size and self.board[nr][nc]==opponent:
          flip.append(nr,nc)
          nr=nr+dr
          nc=nc+dc
        if 0<=nr<self.size and 0<=nc<self.size and self.board[nr][nc]==self.turn:
          for i,j in flip:
            self.board[i][j]=self.turn
        self.switch_turn()
        if not self.get_valid_moves(self.player):
          self.switch_turn()
          if not self.get_valid_moves(self.player):
            self.check_win_condition()
        return True
    def draw(self):
      self.screen.fill((40,40,40))
      pygame.draw.rect(self.screen,(34,139,34),(self.offset,self.offset,560,560))
      for r in range(self.size):
        for c in range(self.size):
          rect=pygame.Rect(self.offset+c*70,self.offset+r*70,70,70)
          pygame.draw.rect(self.screen,(0,0,0),rect,1)
          if self.board[r, c] != 0:
           color = (0, 0, 0) if self.board[r, c] == 1 else (255, 255, 255)
           pygame.draw.circle(self.screen, color, rect.center, 30)

        p1_s = np.sum(self.board == 1)
        p2_s = np.sum(self.board == 2)
        txt = f"{self.p1}: {p1_s} | {self.p2}: {p2_s} | Turn: {self.p1 if self.turn==1 else self.p2}"
        self.screen.blit(self.font.render(txt, True, (255, 255, 255)), (self.offset, 30))
    def check_win(self):
      if not get_valid_moves(1) and not get_valid_moves(2):
        c1=np.sum(self.board==1)
        c2=np.sum(self.board==2)
        if c1>c2:
          return self.p1
        if c2>c1:
          return self.p2
        return "Draw"
      return None
    def main():
      pygame.init()
      p1=sys.argv[1]
      p2=sys.argv[2]
      screen=screen.display.set_mode((720,720))
      pygame.display.set_caption("OTHELLO")
      game=Othello(p1,p2,screen)
      clock=pygame.time.Clock()
      while True:
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
          if event.type==pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            c=(mx-game.offset) // 70
            r=(my-game.offset) // 70
            game.make_move(r,c)
        game.draw()
        winner=game.check_win()
        if winner:
          pygame.time.wait(300)
          pygame.quit()
          sys.exit()
        pygame.display.flip()
        clock.tick(60)
    if __name__=="__main__":
      main()


   
