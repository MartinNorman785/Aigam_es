import pygame

import chessboard as b
import colours as c
from chesspieces import Bishop, Horse, King, Pawn, Queen, Rook


EMPTY = 'empty space'

def main(win):
  """
  The python script for running the game Chess in python


  Will both play Chess and have the option of implementing the AI

  Paramaters
  ----------------
  win: Pygame Display
    A pygame display that is set to size (800, 700)
    Will be used to display the output of the game
  """

  # Initialising pygame
  pygame.init()

  board = b.Board()

  turn = "White"

  # Main loop
  run = True
  while run:

    win.fill(c.GREY)

    board.draw(win, turn)

    # Checking for user input
    for event in pygame.event.get():

      # If pygame is closed
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        run = False
        pygame.quit()

      # If a location is pressed
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        loc = board.get_click_loc(pos)
        if loc is not None:
          if board.board[loc[0]][loc[1]] is not None and board.board[loc[0]][loc[1]].colour == turn:
            board.selected = board.board[loc[0]][loc[1]]
            
          elif board.selected is not None:
              moves = board.selected.possible_move_locations(board)

              if loc in moves:
                # Castling moves for the Rook
                if board.selected.peice_name.split()[1] == 'King':
                  if loc[1] == board.selected.column + 2:
                    board.board[board.selected.row][-1].column = board.selected.column + 1
                    board.board[board.selected.row][board.selected.column + 1] = board.board[board.selected.row][-1] 
                    board.board[board.selected.row][-1] = None
                    board.board[board.selected.row][board.selected.column + 1].moved = True
                  if loc[1] == board.selected.column - 2:
                    board.board[board.selected.row][0].column = board.selected.column - 1
                    board.board[board.selected.row][board.selected.column - 1] = board.board[board.selected.row][0] 
                    board.board[board.selected.row][0] = None
                    board.board[board.selected.row][board.selected.column - 1].moved = True
                

                taken = board.board[loc[0]][loc[1]]
                
                board.board[board.selected.row][board.selected.column] = None
                board.board[loc[0]][loc[1]] = board.selected
                

                board.selected.row = loc[0]
                board.selected.column = loc[1]

                board.selected.moved = True

                if board.selected.peice_name.split()[1] == 'Pawn':
                  if loc[0] == 0:
                    board.board[loc[0]][loc[1]] = Queen(loc[0], loc[1], "White")
                  elif loc[0] == 7:
                    board.board[loc[0]][loc[1]] = Queen(loc[0], loc[1], "Black")

                turn = 'Black' if turn == 'White' else 'White'
                board.selected = None

                board.print_out()
                print()

                '''
                if board.checkmate(turn):
                  print(f"Checkmate {turn} loses")
                elif board.stalemate(turn):
                  print("Stalemate")
                '''

            

    # Processing the updates to the display
    pygame.display.update()
  pygame.quit()



if __name__ == "__main__":

  # Initialising a pygame window
  pygame.init()
  win = pygame.display.set_mode((800,700))


  # Running the main code
  main(win)
