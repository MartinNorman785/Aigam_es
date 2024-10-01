import pygame, os


class Piece():
  PIECE_SIZE = 70
  
  def __init__(self, row, column, colour, piece):
    self.onboard = True
    
    self.row = row
    self.column = column
    self.colour = colour

    self.moved = False

    self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs",f"{piece}{colour}.png")), (self.PIECE_SIZE, self.PIECE_SIZE))

  def __repr__(self):
    return self.peice_name

  def draw(self, win):
    win.blit(self.img, (self.column*70+120, self.row*70 + 100))

  def check_moves_valid(func):
    def inner(self, board):
        moves = func(self, board.board)
        spots = []

        king = board.white_king if board.selected.colour == "White" else board.black_king

        for move in moves:
          b = board.board
          taken = b[move[0]][move[1]]
          
          inital_spot = (board.selected.row, board.selected.column)

          b[inital_spot[0]][inital_spot[1]] = None
          b[move[0]][move[1]] = board.selected
          
          if king == self:
            king.column = move[1]
            king.row = move[0]

          
          if not king.in_check(b):
            spots.append(move)

          if king == self:
            king.row = inital_spot[0]
            king.column = inital_spot[1]

          b[inital_spot[0]][inital_spot[1]] = board.selected
          b[move[0]][move[1]] = taken
        return spots
    return inner

class Pawn(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} Pawn"

    super().__init__(row, column, colour, "Pawn")
  
  @Piece.check_moves_valid
  def possible_move_locations(self, board):
    locations = []

    if self.colour == "White":
      direction = -1
    else:
      direction = 1

    if not self.moved and board[self.row+direction*2][self.column] is None:
      locations.append((self.row+direction*2,self.column))

    if board[self.row+direction][self.column] is None:
      locations.append((self.row+direction,self.column))

    if self.column + 1 <= 7:
      if board[self.row+direction][self.column+1] is not None and board[self.row+direction][self.column+1].colour != self.colour:
        locations.append((self.row+direction,self.column+1))

    if self.column - 1 >= 0:
      if board[self.row+direction][self.column-1] is not None and board[self.row+direction][self.column-1].colour != self.colour:
        locations.append((self.row+direction,self.column-1))
    
    return locations

class Rook(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} Rook"
    super().__init__(row, column, colour, "Rook")
  
  @Piece.check_moves_valid
  def possible_move_locations(self, board):
    locations = []
    for d in [(0,1),(1,0),(-1,0),(0,-1)]:
      more_spaces = True
      loc = (self.row, self.column)
      while more_spaces:
        
        loc = (loc[0]+d[0],loc[1]+d[1])
        if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
          more_spaces = False
        elif board[loc[0]][loc[1]] is None:
          locations.append(loc)
        elif board[loc[0]][loc[1]].colour == self.colour:
          more_spaces = False
        else:
          locations.append(loc)
          more_spaces = False
    return locations


      

class Bishop(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} Bishop"
    super().__init__(row, column, colour, "Bishop")

  @Piece.check_moves_valid
  def possible_move_locations(self, board):
    locations = []
    for d in [(1,1),(1,-1),(-1,1),(-1,-1)]:
      more_spaces = True
      loc = (self.row, self.column)
      while more_spaces:

        loc = (loc[0]+d[0],loc[1]+d[1])
        if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
          more_spaces = False
        elif board[loc[0]][loc[1]] is None:
          locations.append(loc)
        elif board[loc[0]][loc[1]].colour == self.colour:
          more_spaces = False
        else:
          locations.append(loc)
          more_spaces = False

    return locations


class Queen(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} Queen"
    super().__init__(row, column, colour, "Queen")
  
  @Piece.check_moves_valid
  def possible_move_locations(self, board):
    locations = []
    for d in [(1,1),(1,-1),(-1,1),(-1,-1), (0,1),(1,0),(-1,0),(0,-1)]:
      more_spaces = True
      loc = (self.row, self.column)
      while more_spaces:

        loc = (loc[0]+d[0],loc[1]+d[1])
        if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
          more_spaces = False
        elif board[loc[0]][loc[1]] is None:
          locations.append(loc)
        elif board[loc[0]][loc[1]].colour == self.colour:
          more_spaces = False
        else:
          locations.append(loc)
          more_spaces = False
    return locations

class Horse(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} Horse"
    super().__init__(row, column, colour, "Horse")
    
  @Piece.check_moves_valid
  def possible_move_locations(self, board):
    locations = []
    for d in [(1,2), (2,1), (-1,2), (-2,1), (2,-1), (1,-2), (-2,-1), (-1,-2)]:
      loc = (self.row+d[0], self.column+d[1])
      if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
          more_spaces = False
      elif board[loc[0]][loc[1]] is None or board[loc[0]][loc[1]].colour != self.colour:
        locations.append(loc)
    return locations

class King(Piece):
  def __init__(self, row, column, colour):
    self.peice_name = f"{colour} King"
    super().__init__(row, column, colour, "King")

  @Piece.check_moves_valid

  def possible_move_locations(self, board):
    locations = []
    for d in [(1,1),(1,-1),(-1,1),(-1,-1), (0,1),(1,0),(-1,0),(0,-1)]:
      loc = (self.row+d[0], self.column+d[1])
      if loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7:
          more_spaces = False
      elif board[loc[0]][loc[1]] is None:
        locations.append(loc)
      elif board[loc[0]][loc[1]].colour == self.colour:
        pass
      else:
        locations.append(loc)

    if not self.moved and all([board[self.row][x] is None for x in (1,2,3)]) :
      if not board[self.row][0].moved and not self.in_check(board)and (self.row, self.column-1) in locations:
        locations.append((self.row, self.column-2))
    if not self.moved and all([board[self.row][x] is None for x in (-2,-3)]):
      if not board[self.row][-1].moved and not self.in_check(board) and (self.row, self.column+1) in locations:
        locations.append((self.row, self.column+2))

    return locations

  def in_check(self, board, checking_piece=False):
      movement_types_cont = {
          "BishopQueen": [(1, 1), (1, -1), (-1, 1), (-1, -1)],
          "RookQueen": [(0, 1), (1, 0), (-1, 0), (0, -1)],
      }

      p_direction = -1 if self.colour == "White" else 1

      movement_types_one = {
          "Horse": [(1, 2), (2, 1), (-1, 2), (-2, 1), (2, -1), (1, -2), (-2, -1), (-1, -2)],
          "Pawn": [(p_direction, 1), (p_direction, -1)],
      }

      # Check continuous movement threats (Bishop, Rook, Queen)
      for pieces, movement_type in movement_types_cont.items():
          for d in movement_type:
              loc = (self.row, self.column)
              while True:
                  loc = (loc[0] + d[0], loc[1] + d[1])
                  if not (0 <= loc[0] <= 7 and 0 <= loc[1] <= 7):
                      break
                  if board[loc[0]][loc[1]] is None:
                      continue
                  elif board[loc[0]][loc[1]].colour == self.colour:
                      break
                  else:
                      if board[loc[0]][loc[1]].peice_name.split()[1] in pieces:
                          if checking_piece:
                              return True, board[loc[0]][loc[1]]
                          return True
                      break

      # Check single movement threats (Horse, Pawn)
      for pieces, movement_type in movement_types_one.items():
          for d in movement_type:
              loc = (self.row + d[0], self.column + d[1])
              if 0 <= loc[0] <= 7 and 0 <= loc[1] <= 7:
                  if board[loc[0]][loc[1]] is not None and board[loc[0]][loc[1]].colour != self.colour:
                      if board[loc[0]][loc[1]].peice_name.split()[1] in pieces:
                          if checking_piece:
                              return True, board[loc[0]][loc[1]]
                          return True

      if checking_piece:
          return False, None
      return False

