# Matthieu Schulz, 2019
# London, United Kingdom

from board import *
from random import Random
import math

class Player:
    def __init__(self, seed=None):
        self.list_of_heights = []
        self.best_rotation = 0
        self.best_position = 0


    def check_holes(self, board):
        num_of_holes = 0
        for x in range (board.width):
           for y in range (board.height):
              if (x,y) not in  board.cells:
                  if (x+1,y) in board.cells and (x-1,y) in board.cells and  (x, y+1) in board.cells and (x,y-1) in board.cells:
                      num_of_holes += 1
        return num_of_holes

    def check_height(self, board):
       self.list_of_heights = [0] * board.width

       for x in range (board.width):
           for y in reversed(range(board.height)):
               if (x,y) in board.cells:
                  height = board.height - y
                  self.list_of_heights[x] = height
       total_height = sum(self.list_of_heights)
       return total_height

    def check_smoothness(self, board):
        smoothness = 0
        print(self.list_of_heights)
        for i in range(board.width-1):
            smoothness += abs(self.list_of_heights[i+1] - self.list_of_heights[i])
        return smoothness

    def clear_lines(self, board, old_score):
        new_score = board.score
        bonus = new_score - old_score
        num_of_cleared_lines = 0

        if bonus < 101:
          num_of_cleared_lines = 1
        elif bonus < 401:
          num_of_cleared_lines = 2
        elif bonus < 801:
           num_of_cleared_lines = 3
        elif bonus < 1601:
           num_of_cleared_lines = 4

        return num_of_cleared_lines

    def bestMove(self, board):
       a = -0.510066
       b = 0.760666
       c = -0.35663
       d = -0.184483
       score = 0
       best_score = -90000000000000
       best_rotation = -900000000000
       best_position = -900000000000

       for rotation in range (0,4):

           for position in range (0,board.width):

                sandbox = board.clone()
                for i in range(0, rotation):
                    if sandbox.falling is not None:
                        sandbox.rotate(Rotation.Anticlockwise)
                if position < 4.5:
                    for i in range(0, abs(5-position)):
                       if sandbox.falling is not None:
                        sandbox.move(Direction.Left)
                else:
                    for i in range(0, position - 4):
                       if sandbox.falling is not None:
                        sandbox.move(Direction.Right)

                try:
                    if sandbox.falling is not None:
                        sandbox.move(Direction.Drop)
                except NoBlockException:
                    pass
                print("Heuristics:",(self.check_height(sandbox)),(self.clear_lines(sandbox, board.score)),(self.check_holes(sandbox)),(self.check_smoothness(sandbox)))
                score =  a * (self.check_height(sandbox)) + b * (self.clear_lines(sandbox, board.score)) + c * (self.check_holes(sandbox)) + d * (self.check_smoothness(sandbox))
                
                if score > best_score:
                    best_score = score
                    self.best_rotation = rotation
                    self.best_position = position


    def board_move(self,board, best_rotation, best_position):
        moves_list = []
        moves_list.clear()

        print(best_rotation, best_position)
        for i in range(0,best_rotation):
            moves_list.append(Rotation.Anticlockwise)
        if best_position < 5:
            for i in range(0, abs(5-best_position)):
                moves_list.append(Direction.Left)
        else:
            for i in range(0, best_position - 4):
                moves_list.append(Direction.Right)
        if board.falling is not  None:
            moves_list.append(Direction.Drop)

        if board.falling is not  None:
            return moves_list

    def choose_action(self, board):
        self.bestMove(board)

        return self.board_move(board, self.best_rotation, self.best_position)

SelectedPlayer = Player
