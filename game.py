import sys
import pygame
import time
import numpy as np
import os
import subprocess
from  games.base_class import Basegame
from games import tictactoe
from games import othello
from games import connect4
if len(sys.argv) != 3:
   print("Try giving correct command lil bro")
   sys.exit()
pygame.init()
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH,HEIGHT=screen.get_size()
pygame.display.set_caption("MINI HUB GTA")
#colors
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
BLUE = (100, 150, 255)
font_large = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 24)   
player1=sys.argv[1]
player2=sys.argv[2]   
def save_result(winner,loser,game_name):
   date=time.strftime("%Y-%m-%d")
   with open("history.csv","a") as f:
      f.write(f"{winner},{loser},{date},{game_name}\n")
def show_leaderboard(screen, font):
    os.system("bash leaderboard.sh")
def launch_game(file):
   base_dir = os.path.dirname(os.path.abspath(__file__))
   path=os.path.join(base_dir,"games",file)
   subprocess.Popen([sys.executable,path,player1,player2])
btn1=pygame.Rect(300,100,200,50)
btn2=pygame.Rect(300,200,200,50)
btn3=pygame.Rect(300,300,200,50)
btn4=pygame.Rect(300,400,200,50)
clock=pygame.time.Clock()
while True:
   screen.fill((255,255,255))
   mouse_pos=pygame.mouse.get_pos()
   for event in pygame.event.get():
      if event.type==pygame.QUIT:
         pygame.quit()
         sys.exit()
      if event.type==pygame.MOUSEBUTTONDOWN:
         if event.button==1:
            if btn1.collidepoint(mouse_pos):
               launch_game("tictactoe.py")
            elif btn2.collidepoint(mouse_pos):
               launch_game("othello.py")
            elif btn3.collidepoint(mouse_pos):
               launch_game("connect4.py")
            elif btn4.collidepoint(mouse_pos):
               pygame.quit()
               sys.exit()
   color=(0,125,255) if btn1.collidepoint(mouse_pos) else (0,80,100)
   pygame.draw.rect(screen,color,btn1,border_radius=8)
   screen.blit(font_small.render("TIC TAC TOE",True,(255,255,255)), btn1.move(30,10))
   color=(0,125,255) if btn2.collidepoint(mouse_pos) else (0,80,100)
   pygame.draw.rect(screen,color,btn2,border_radius=8)
   screen.blit(font_small.render("OTHELLO",True,(255,255,255)), btn2.move(50,10))

   color=(0,125,255) if btn3.collidepoint(mouse_pos) else (0,80,100)
   pygame.draw.rect(screen,color,btn3,border_radius=8)
   screen.blit(font_small.render("CONNECT4",True,(255,255,255)), btn3.move(40,10))

   color=(0,125,255) if btn4.collidepoint(mouse_pos) else (0,80,100)
   pygame.draw.rect(screen,color,btn4,border_radius=8)
   screen.blit(font_small.render("QUIT",True,(255,255,255)), btn4.move(70,10))
   pygame.display.flip()
   clock.tick(60)
