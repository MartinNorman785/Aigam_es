import pygame

import colours as c
from pieces import Bishop, Horse, King, Pawn, Queen, Rook




class Board:

  pygame.font.init()
  font_for_message = pygame.font.SysFont("dejavusans", 35, True)

  def __init__(self):
    self.selected = None
    self.reset_board()
    

  def print_out(self):
    for row in self.board:
      print(row)
  

  def stalemate(self, turn):
    selected = self.selected
    for row in self.board:
      for spot in row:
        if spot is not None and spot.colour == turn:
          self.selected = spot
          if len(spot.possible_move_locations(self)) >= 1:
            self.selected = selected
            return False
    self.selected = selected
    return True


  def checkmate(self, turn):
    king = self.white_king if turn == 'White' else self.black_king
    
    selected = self.selected

    check, peice = king.in_check(self.board, checking_piece=True)
    if check:
      for row in self.board:
        for spot in row:

          if spot is not None and spot.colour == turn:
            self.selected = spot
            if len(spot.possible_move_locations(self)) >= 1:
              self.selected = selected
              return False
      self.selected = selected
      return True
    return False

              


  def draw(self, win, turn):
    colour = c.BLACK
    
    for row in range(8):
      for col in range(8):
        if colour == c.WHITE: colour = c.BROWN
        else: colour = c.WHITE
        if self.selected is not None and self.selected.row == row and self.selected.column == col:
           pygame.draw.rect(win, c.YELLOW, (120 + col*70, 100 + row*70, 70, 70))
        else:
          pygame.draw.rect(win, colour, (120 + col*70, 100 + row*70, 70, 70))

      if colour == c.WHITE: colour = c.BROWN
      else: colour = c.WHITE

    
    # Drawing the pieces
    for row in self.board:
      for square in row:
        if square is not None:
          square.draw(win)
    
    if self.selected is not None:
      spots = self.selected.possible_move_locations(self)
      for spot in spots:
        pygame.draw.circle(win, c.GREY, (spot[1]*70+155, spot[0]*70 + 135), 10)


    king = self.white_king if turn == 'White' else self.black_king
    if self.checkmate(turn):
      message = f"Checkmate. {king.colour} wins"
    elif king.in_check(self.board):
      message = f"{king.colour}'s turn: Check"
    elif self.stalemate(turn):
      message = f"Draw: Stalemate"
    else:
      message = f"{king.colour}'s turn"

    text = self.font_for_message.render(message, True, c.WHITE)

    width = text.get_width()
    height = text.get_height()
    win.blit(text, (400-width/2, 40 - height/2))
    
    

  def get_click_loc(self, pos):
    for row in range(8):
      for col in range(8):
        if pos[0] > 120 + col*70 and pos[0] < 190 + col*70 and pos[1] > 100 + row*70 and pos[1] < 170 + row*70:
          return (row, col)
    return None



  def reset_board(self):
    self.black_king = King(0,4, "Black")
    self.white_king = King(7,4, "White")

    top_row = [
      Rook(0,0, "Black"),
      Horse(0,1, "Black"),
      Bishop(0,2, "Black"),
      Queen(0,3, "Black"),
      self.black_king,
      Bishop(0,5, "Black"),
      Horse(0,6, "Black"),
      Rook(0,7, "Black")
    ]
    
    top2_row = [
      Pawn(1,0, "Black"),
      Pawn(1,1, "Black"),
      Pawn(1,2, "Black"),
      Pawn(1,3, "Black"),
      Pawn(1,4, "Black"),
      Pawn(1,5, "Black"),
      Pawn(1,6, "Black"),
      Pawn(1,7, "Black")
    ]
    
    bottom_row = [
      Rook(7,0, "White"),
      Horse(7,1, "White"),
      Bishop(7,2, "White"),
      Queen(7,3, "White"),
      self.white_king,
      Bishop(7,5, "White"),
      Horse(7,6, "White"),
      Rook(7,7, "White")
    ]
    
    bottom2_row = [
      Pawn(6,0, "White"),
      Pawn(6,1, "White"),
      Pawn(6,2, "White"),
      Pawn(6,3, "White"),
      Pawn(6,4, "White"),
      Pawn(6,5, "White"),
      Pawn(6,6, "White"),
      Pawn(6,7, "White")
    ]
    
    nonerow = [
      None,
      None,
      None,
      None,
      None,
      None,
      None,
      None
    ]
    
    self.board = [
      top_row,
      top2_row,
      nonerow,
      nonerow.copy(),
      nonerow.copy(),
      nonerow.copy(),
      bottom2_row,
      bottom_row
    ]