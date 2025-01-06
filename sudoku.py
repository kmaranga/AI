
############################################################
#Sudoku
############################################################

import collections
import itertools
import copy 
import math 
import random 
import os

############################################################
# Section 1: Sudoku Solver
############################################################

def sudoku_cells():
  cells = []
  for i, j in itertools.product(range(9), range(9)):
    cells.append((i, j))
  return cells
  
def sudoku_arcs():
  set_of_arcs = set()
  for i, j, k in itertools.product(range(9), range(9), range(9)):
    if k != j: 
      first_arc = ((i, j), (i, k))
      second_arc = ((j, i), (k, i))
      set_of_arcs.add(first_arc)
      set_of_arcs.add(second_arc)

  for i, j in itertools.product(range(9), range(9)):
    for ki, kj in itertools.product(range(3), range(3)):
      x = ki + (i // 3) * 3
      y = kj + (j // 3) * 3
      if i != x or j != y: 
        third_arc = ((i, j),(x, y))
        set_of_arcs.add(third_arc)
  return set_of_arcs


def read_board(path):
  board = []
  with open(path) as infile:
    for r, line in enumerate(infile, start = 1):
      board.append([])
        
      for c, number in enumerate(line.strip('\n'), start = 1): 
        if number == '*':
            number = 0
        else:
          number = int(number)
        board[-1].append(number)
  return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
      self.board = board 
      self.map_board = dict()

      for i, j in itertools.product(range(9), range(9)):
        symbol = board[i][j]
        if symbol == 0: 
          self.map_board[(i, j)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9]) 
        if symbol != 0:
          sym_set = set()
          sym_set.add(int(symbol))
          self.map_board[(i, j)] = sym_set
        
    def get_values(self, cell):
      return self.map_board[cell]
       
 #check cases where cell1 has >1 number, check if c2 has 1 number, remove cell2's
      #number from 1
      #if cell2 >1 number, we're ok, check against cell1's # and rmv inconsistent ones
    def remove_inconsistent_values(self, cell1, cell2):
      revised = False
      if (cell1, cell2) in Sudoku.ARCS:
        if len(self.map_board[cell2]) == 1:
          for value_cell2 in self.map_board[cell2]:
            if value_cell2 in self.map_board[cell1]:
              self.map_board[cell1].remove(value_cell2)
              revised = True
     
        return revised 
    
    
    def get_neighbours(self, row, col): 
      neighbour = set()
      for i, j in itertools.product(range(9), range(9)): 
        potential_neighbour = (i, j)
        #if i'm my own potential neighbour don't add me 
        if row == potential_neighbour[0] & col == potential_neighbour[1]: 
          continue
          #add me if we're in the same row
        if row == potential_neighbour[0]: 
          neighbour.add(potential_neighbour)
          #add me if we're in the same col
        if col == potential_neighbour[1]: 
          neighbour.add(potential_neighbour)
        
        #check if we're in the same block
        row_box = math.ceil(row/3)
        col_box = math.ceil(col/3)
        pot_row_box = math.ceil(i/3)
        pot_col_box = math.ceil(j/3)

        #add me if i'm in the same block as you
        if row_box == pot_row_box & col_box == pot_col_box: 
          neighbour.add(potential_neighbour)
      return neighbour


    def infer_ac3(self):
      queue = collections.deque(Sudoku.ARCS)
      while len(queue) != 0: 
        #c1, c2 popped from queue
        curr = queue.popleft() #i wanna pop from the front 
        c1 = curr[0]
        c2 = curr[1]

        if self.remove_inconsistent_values(c1, c2):
          #add the arcs with c1's neighbors to the queue
          for currArc in self.ARCS:
            if currArc[0] == c1:
              queue.append((currArc[1],c1))
      return True
       
    def row_neighbour(self,loc):
      row,col = loc
      rowNeighbour = set()
      for j in range(9):
        pot_neighbour = (row, j)
        if j == col:
          continue
        if j != col:
          rowNeighbour.add(pot_neighbour) #if i'm myself skip me & don't add me to my set?
      return rowNeighbour


    def col_neighbour(self, loc):
      row, col = loc
      colNeighbour = set()
      for i in range(9):
        pot_neighbour = (i, col)
        if i == row: 
          continue 
        if i != row: 
          colNeighbour.add(pot_neighbour)
      return colNeighbour

    def block_neighbour(self, loc):
      i, j = loc
      block = set()
      if (0 <= i <= 2) & (0 <= j <= 2): 
        block = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
        
      elif (0 <= i <= 2) & (3 <= j <= 5): 
        block = {(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)}
        
      elif (0 <= i <= 2) & (6 <= j <= 8): 
        block = {(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)}
      
      elif (3 <= i <= 5) & (0 <= j <= 2):
        block = {(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)}

      elif (3 <= i <= 5) & (3 <= j <= 5):
        block = {(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)}
   
      elif (3 <= i <= 5) & (6 <= j <= 8): 
        block = {(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)}
       
      elif (6 <= i <= 8) & (0 <= j <= 2):
        block = {(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)}
 
      elif (6 <= i <= 8) & (3 <= j <= 5): 
        block = {(6, 3), (6, 4), (6, 5), (7, 3) ,(7, 4), (7, 5), (8, 3), (8, 4), (8, 5)}

      elif (6 <= i <= 8) & (6 <= j <= 8):
        block = {(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)}


      print(block)
      print(loc)

      block.remove(loc)
      return block

    
    def infer_improved(self):
      made_additional_inference = True
      while made_additional_inference:
        self.infer_ac3()
        made_additional_inference = False
        for cell in self.CELLS:
          #if any of its possible values are unique in a row, col, or block:
          if len(self.map_board[cell]) > 1: 
            for curr_value in self.map_board[cell]:
              #row
              showsUp = False 
              for row_cell_neighbor in self.row_neighbour(cell):
                #if value of row_cell_neighbor == cell_value, we haven't found it, else if it isn't in row_cell_neighbor vals, 
                #we got a unique value which my cell can be 
                #print(type(row_cell_neighbor))
                if curr_value in self.get_values(row_cell_neighbor): 
                  showsUp = True 
              
              if not showsUp:
                made_additional_inference= True
                self.map_board[cell] = {curr_value}
                break;
              
              #col
              #col_inference = False
              for col_cell_neighbor in self.col_neighbour(cell):
                if curr_value in self.get_values(col_cell_neighbor): 
                  showsUp = True 
              
              if not showsUp:
                made_additional_inference= True
                self.map_board[cell] = {curr_value}
                break;

              #block 
                #block_inference = False 
              for block_cell_neighbor in self.block_neighbour(cell):
                if curr_value in self.get_values(block_cell_neighbor): 
                  showsUp = True
              
              if not showsUp:
                made_additional_inference= True
                self.map_board[cell] = {curr_value}
                break;

    def is_solved(self):
      for cell in Sudoku.CELLS:
        if len(self.map_board[cell]) != 1:
          return False
      return True 


    def infer_with_guessing(self):
      self.infer_improved()
      for cell in Sudoku.CELLS:
        #if cell is not satisfied: i.e hasn't been given a value
        if len(self.map_board[cell]) > 1: 
          #for each possibility of the cell: 
          for value in self.map_board[cell]:
            #recurse over a deep copy of the board w/ cell set at possibility
            new_board = copy.deepcopy(self.map_board)
            self.map_board[cell] = {value}
            #make a guess in this new board
            self.infer_with_guessing()
            
            if self.is_solved():
              break
            else:
              self.map_board = copy.deepcopy(new_board)
