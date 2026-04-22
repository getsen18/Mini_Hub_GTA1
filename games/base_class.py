import numpy as np
class Basegame:
   def __init__(self,p1,p2,size):
      self.p1=p1
      self.p2=p2
      self.size=size
      self.board=np.zeros((size,size))
      self.turn=1
   def switch_turn(self):
      self.turn=2 if self.turn==1 else 1  
   def player_name(self):
      return self.p1 if self.turn==1 else self.p2