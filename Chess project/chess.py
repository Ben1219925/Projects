import pygame
import sys
import copy
#import stockfish

# def start_menu():
#     font = pygame.font.Font(None, 36)
#     text1 = font.render("1. Play against the computer", True, (0, 0, 0))
#     text2 = font.render("2. Play against a friend", True, (0, 0, 0))
#     option1_rect = text1.get_rect(center=(board_size/2, board_size/2 - text1.get_height()))
#     option2_rect = text2.get_rect(center=(board_size/2, board_size/2 + text2.get_height()))
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  # Left mouse button
#                     # Check if the mouse click is within the button bounds
#                     if option1_rect.collidepoint(event.pos):
#                         # Option 1: Play against the computer
#                         return "computer"
#                     elif option2_rect.collidepoint(event.pos):
#                         # Option 2: Play against a human
#                         return "multiplayer"
        
#         # Draw the menu options on the screen
#         board_surface.fill((255, 255, 255))
#         board_surface.blit(text1, option1_rect)
#         board_surface.blit(text2, option2_rect)
        
#         pygame.display.flip()

# def computer_level_menu():
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if pygame.K_0 <= event.key <= pygame.K_9:
#                     level = event.key - pygame.K_0  # Map key to corresponding level
#                     return level
#                 elif event.key == pygame.K_ESCAPE:
#                     # Return to previous menu if Escape key is pressed
#                     return None

#         # Draw the level options on the screen
#         board_surface.fill((255, 255, 255))
#         font = pygame.font.Font(None, 36)
#         levels = ["Level 0", "Level 5", "Level 10", "Level 15", "Level 20"]
#         for i, level in enumerate(levels):
#             text = font.render(f"{i}. {level}", True, (0, 0, 0))
#             board_surface.blit(text, (board_size/2 - text.get_width()/2, board_size/2 - text.get_height()/2 + i*50))

#         pygame.display.flip()

def find_bking(board):
    for row in range(8):
        for col in range(8):
            if board[row][col] == "bking":
                return (row,col)
            
def find_wking(board):
    for row in range(8):
        for col in range(8):
            if board[row][col] == "wking":
                return (row,col)

def get_valid_moves(piece_type, piece_color, row, col, board):
    """
    Returns a list of valid moves for a given chess piece at a given position on the board.
    piece_type: the type of piece ("king", "queen", "rook", "bishop", "knight", or "pawn")
    piece_color: the color of the piece ("white" or "black")
    row: the row index of the piece's current position (0-7)
    col: the column index of the piece's current position (0-7)
    board: a 2D list representing the current state of the chess board
    """
    valid_moves = []
    
    # Check the type of piece and get its valid moves
    if piece_type == "king":
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1), (0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row = row + dy
            new_col = col + dx
            if (0 <= new_row < 8 and 0 <= new_col < 8) and (board[new_row][new_col] == " " or board[new_row][new_col][0] != piece_color):
                #if not check(new_board):
                valid_moves.append((new_row,new_col))
           
                
        pass
    elif piece_type == "queen":
        # Check for valid moves in all 8 directions
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1), (0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " ":
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "rook":
        # Check for valid moves in all 4 directions
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " ":
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "bishop":
        # Check for valid moves in all 4 diagonal directions
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " ":
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color:
                    valid_moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "knight":
        for dx, dy in ((1,2), (-1,2), (-1,-2), (1,-2), (2,1), (-2,1), (-2,-1), (2,-1)):
            new_row = row + dy
            new_col = col + dx
            if (0 <= new_row < 8 and 0 <= new_col < 8) and (board[new_row][new_col] == " " or board[new_row][new_col][0] != piece_color):
                valid_moves.append((new_row, new_col))
        pass
    elif piece_type == "pawn":
        # white pieces move + rows, black moves - rows
        if piece_color == "b":
            # Check if pawn can move one square forward
            if row > 0 and board[row-1][col] == " " :
                valid_moves.append((row-1, col))
                # Check if pawn can move two squares forward (if in starting position)
                if row == 6 and board[row-2][col] == " ":
                    valid_moves.append((row-2, col))
            # Check if pawn can capture diagonally to the left
            if row > 0 and col > 0 and board[row-1][col-1] != " " and board[row-1][col-1][0] != piece_color:
                valid_moves.append((row-1, col-1))
            # Check if pawn can capture diagonally to the right
            if row > 0 and col < 7 and board[row-1][col+1] != " " and board[row-1][col+1][0] != piece_color:
                valid_moves.append((row-1, col+1))
        elif piece_color == "w":
            # Check if pawn can move one square forward
            if row < 7 and board[row+1][col] == " ":
                valid_moves.append((row+1, col))
                # Check if pawn can move two squares forward (if in starting position)
                if row == 1 and board[row+2][col] == " ":
                    valid_moves.append((row+2, col))
            # Check if pawn can capture diagonally to the left
            if row < 7 and col > 0 and board[row+1][col-1] != " " and board[row+1][col-1][0] != piece_color:
                valid_moves.append((row+1, col-1))
            # Check if pawn can capture diagonally to the right
            if row < 7 and col < 7 and board[row+1][col+1] != " " and board[row+1][col+1][0] != piece_color:
                valid_moves.append((row+1, col+1))
        pass
    
    return valid_moves    
    

def check_for_check(row, col, new_row, new_col, board):
   """
   Checks if the piece's move would put the king into check.
   True if the move would put the king into check, False otherwise.
   """
   # Make a copy of the board so that we don't modify the original board.
   new_board = copy.deepcopy(board)
   # Move the piece to the new location.
   new_board[new_row][new_col] = new_board[row][col]
   new_board[row][col] = " "
   # Check if the king is in check on the new board.
   in_check, crow, ccol, king_color = check(new_board)
   if in_check and white_turn and king_color == "w":
       return True
   elif in_check and not white_turn and king_color == "b":
       return True
   #other wise false
   return False

def all_valid_moves(piece_type,piece_color,row,col,board):
    valid_moves = []
    
    # Check the type of piece and get its valid moves
    if piece_type == "king":
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1), (0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row = row + dy
            new_col = col + dx
            if (0 <= new_row < 8 and 0 <= new_col < 8) and (board[new_row][new_col] == " " or board[new_row][new_col][0] != piece_color) and not check_for_check(row,col,new_row,new_col,board):
                valid_moves.append((new_row,new_col))
            
        pass
    elif piece_type == "queen":
        # Check for valid moves in all 8 directions
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1), (0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " " and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                    break
                elif board[new_row][new_col][0] == piece_color:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "rook":
        # Check for valid moves in all 4 directions
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " " and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                    break
                elif board[new_row][new_col][0] == piece_color:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "bishop":
        # Check for valid moves in all 4 diagonal directions
        for dx, dy in ((1,1), (-1,-1), (-1,1), (1,-1)):
            new_row, new_col = row + dy, col + dx
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == " " and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                elif board[new_row][new_col][0] != piece_color and not check_for_check(row,col,new_row,new_col,board):
                    valid_moves.append((new_row, new_col))
                    break
                elif board[new_row][new_col][0] == piece_color:
                    break
                new_row += dy
                new_col += dx
        pass
    elif piece_type == "knight":
        for dx, dy in ((1,2), (-1,2), (-1,-2), (1,-2), (2,1), (-2,1), (-2,-1), (2,-1)):
            new_row = row + dy
            new_col = col + dx
            if (0 <= new_row < 8 and 0 <= new_col < 8) and (board[new_row][new_col] == " " or board[new_row][new_col][0] != piece_color) and not check_for_check(row,col,new_row,new_col,board):
                valid_moves.append((new_row, new_col))
        pass
    elif piece_type == "pawn":
        # white pieces move + rows, black moves - rows
        if piece_color == "b":
            # Check if pawn can move one square forward
            if row > 0 and board[row-1][col] == " " and not check_for_check(row,col,row-1,col,board):
                valid_moves.append((row-1, col))
                # Check if pawn can move two squares forward (if in starting position)
                if row == 6 and board[row-2][col] == " " and not check_for_check(row,col,row-2,col,board):
                    valid_moves.append((row-2, col))
            # Check if pawn can capture diagonally to the left
            if row > 0 and col > 0 and board[row-1][col-1] != " " and board[row-1][col-1][0] != piece_color and not check_for_check(row,col,row-1,col-1,board):
                valid_moves.append((row-1, col-1))
            # Check if pawn can capture diagonally to the right
            if row > 0 and col < 7 and board[row-1][col+1] != " " and board[row-1][col+1][0] != piece_color and not check_for_check(row,col,row-1,col+1,board):
                valid_moves.append((row-1, col+1))
        elif piece_color == "w":
            # Check if pawn can move one square forward
            if row < 7 and board[row+1][col] == " " and not check_for_check(row,col,row+1,col,board):
                valid_moves.append((row+1, col))
                # Check if pawn can move two squares forward (if in starting position)
                if row == 1 and board[row+2][col] == " " and not check_for_check(row,col,row+2,col,board):
                    valid_moves.append((row+2, col))
            # Check if pawn can capture diagonally to the left
            if row < 7 and col > 0 and board[row+1][col-1] != " " and board[row+1][col-1][0] != piece_color and not check_for_check(row,col,row+1,col-1,board):
                valid_moves.append((row+1, col-1))
            # Check if pawn can capture diagonally to the right
            if row < 7 and col < 7 and board[row+1][col+1] != " " and board[row+1][col+1][0] != piece_color and not check_for_check(row,col,row+1,col+1,board):
                valid_moves.append((row+1, col+1))
        pass
    
    return valid_moves
    
def highlight_valid_moves(piece_type, piece_color, row, col, board):
    """
    Highlights all valid moves for a given chess piece at a given position on the board.
    piece_type: the type of piece ("king", "queen", "rook", "bishop", "knight", or "pawn")
    piece_color: the color of the piece ("white" or "black")
    row: the row index of the piece's current position (0-7)
    col: the column index of the piece's current position (0-7)
    board: a 2D list representing the current state of the chess board
    """
    valid_moves = all_valid_moves(piece_type, piece_color, row, col, board)
    for move in valid_moves:
        pygame.draw.rect(board_surface, (0, 255, 0), (move[1]*square_size, move[0]*square_size, square_size, square_size), width=3)
    if piece_type == "king":
        #castling rules
        #1.The king is not currently in check.
        #2.Neither the king nor the rook has previously moved.
        #3.There are no pieces between the king and the rook.
        #4.The king does not pass through or finish on a square that is attacked by an enemy piece.
        #check for white long casling 
        if white_turn and check(board)[3] != "w" and not wking_moved and not w0rook_moved and board[0][1] == " " and board[0][2] == " "  and board[0][3] == " " and not check_for_check(0,4,0,2,board) and not check_for_check(0,4,0,3,board):
            valid_moves.append((0,2))
            #highlight in orange
            pygame.draw.rect(board_surface, (0,0,255), (2*square_size, 0*square_size, square_size, square_size), width=4)
        #check for white short casling 
        if white_turn and check(board)[3] != "w" and not wking_moved and not w7rook_moved and board[0][5] == " " and board[0][6] == " " and not check_for_check(0,4,0,5,board) and not check_for_check(0,4,0,6,board):
            valid_moves.append((0,6))
            #highlight in orange
            pygame.draw.rect(board_surface, (0,0,255), (6*square_size, 0*square_size, square_size, square_size), width=4)
        #check for black long casling 
        if not white_turn and check(board)[3] != "b" and not bking_moved and not b0rook_moved and board[7][1] == " " and board[7][2] == " "  and board[0][3] == " " and not check_for_check(7,4,7,2,board) and not check_for_check(7,4,7,3,board):
            valid_moves.append((7,2))
            #highlight in orange
            pygame.draw.rect(board_surface, (0,0,255), (2*square_size, 7*square_size, square_size, square_size), width=4)
        #check for black short casling 
        if not white_turn and check(board)[3] != "b" and not bking_moved and not b7rook_moved and board[7][5] == " " and board[7][6] == " " and not check_for_check(7,4,7,5,board) and not check_for_check(7,4,7,6,board):
            valid_moves.append((7,6))
            #highlight in orange
            pygame.draw.rect(board_surface, (0,0,255), (6*square_size, 7*square_size, square_size, square_size), width=4)
    return valid_moves

def set_board(board):
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect(j * square_size, i * square_size, square_size, square_size)
            if (i + j) % 2 == 0:
                pygame.draw.rect(board_surface, (209, 139, 71), rect)
            else:
                pygame.draw.rect(board_surface, (255, 206, 158), rect)
            if board[i][j] != " ":
                piece_image = piece_images[("white" if board[i][j][0] == "w" else "black", board[i][j][1:])]
                board_surface.blit(piece_image, rect)
            
    
def check(board):
    check = False
    rows = []
    cols = []
    king_color = " "
    bking_row, bking_col = find_bking(board)
    wking_row, wking_col = find_wking(board)
    for row in range(8):
        for col in range(8):
            piece_type = board[row][col][1:]
            piece_color = board[row][col][0]
            valid_moves = get_valid_moves(piece_type, piece_color, row, col, board)
            if (bking_row,bking_col) in valid_moves:
                check = True
                #location of the piece puting the king in check
                rows.append(row)
                cols.append(col)
                #color of the king in check
                king_color = "b"
            if (wking_row,wking_col) in valid_moves:
                check = True
                #location of the piece puting the king in check
                rows.append(row)
                cols.append(col)
                #color of the king in check
                king_color = "w"
    return (check,rows,cols,king_color)

def highlight_check(board):
    in_check,row,col,king_color = check(board)
    bking_row, bking_col = find_bking(board)
    wking_row, wking_col = find_wking(board)
    if in_check:
        if king_color == "b":
            pygame.draw.rect(board_surface, (255, 0, 0), (bking_col*square_size, bking_row*square_size, square_size, square_size), width=3)
            for i in range(len(col)):
                pygame.draw.rect(board_surface, (255, 0, 0), (col[i]*square_size, row[i]*square_size, square_size, square_size), width=3)
            pygame.display.update()
        else:
            pygame.draw.rect(board_surface, (255, 0, 0), (wking_col*square_size, wking_row*square_size, square_size, square_size), width=3)
            for i in range(len(col)):
                pygame.draw.rect(board_surface, (255, 0, 0), (col[i]*square_size, row[i]*square_size, square_size, square_size), width=3)
            pygame.display.update()

def checkmate(board):
    no_moves = True
    valid_moves = []
    in_check, rows, cols, king_color = check(board)
    if in_check:
        for row in range(8):
            for col in range(8):
                piece_type = board[row][col][1:]
                piece_color = board[row][col][0]
                if king_color == "w" and piece_color == "w":
                    valid_moves.append(all_valid_moves(piece_type, piece_color, row, col, board))
                elif king_color == "b" and piece_color == "b":
                    valid_moves.append(all_valid_moves(piece_type, piece_color, row, col, board))
        for move in valid_moves:
            if move != []:
                no_moves = False
        if no_moves:
            return (True,king_color)
        
    return (False,king_color)

def stalemate(board):
    no_moves = True
    valid_moves = []
    in_check, rows, cols, king_color = check(board)
    if not in_check:
        for row in range(8):
            for col in range(8):
                piece_type = board[row][col][1:]
                piece_color = board[row][col][0]
                if white_turn and piece_color == "w":
                    valid_moves.append(all_valid_moves(piece_type, piece_color, row, col, board))
                elif not white_turn and piece_color == "b":
                    valid_moves.append(all_valid_moves(piece_type, piece_color, row, col, board))
        for move in valid_moves:
            if move != []:
                no_moves = False
        if no_moves:
            return True
    return False
pygame.init()


# Set up the board surface
piece_size = 90 #size of the piece image in pixels
board_size = piece_size * 8  # the size of the board in pixels
board_surface = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess")


# Load the images for the pieces
piece_images = {}
for color in ("white", "black"):
    for piece_type in ("king", "queen", "rook", "bishop", "knight", "pawn"):
        piece_images[(color, piece_type)] = pygame.image.load(f"images/{color}_{piece_type}.png")

# Define the starting positions of the pieces
starting_board = [
    ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"],
    ["wpawn"] * 8,
    [" "] * 8,
    [" "] * 8,
    [" "] * 8,
    [" "] * 8,
    ["bpawn"] * 8,
    ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
]

# Define the size of each square on the board
square_size = board_size // 8

set_board(starting_board)

# # Create an instance of Stockfish engine
# engine = stockfish.Stockfish("/stockfish_15.1_win_x64_avx2/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe")

board = copy.deepcopy(starting_board)
prev_click = None
white_turn = True
piece_moved = False
in_check = False
bking_moved = False
wking_moved = False
b0rook_moved = False
b7rook_moved = False
w0rook_moved = False
w7rook_moved = False

# #start menu loop
# while True:
#     option = start_menu()
#     if option == "computer":
        
#     elif option == "multiplayer":
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if prev_click is None:  # first click
                #get click position
                piece_mouse_pos = pygame.mouse.get_pos()
                # Determine the row and column of the click on the board
                row = piece_mouse_pos[1] // square_size
                col = piece_mouse_pos[0] // square_size
                piece_type = board[row][col][1:]
                piece_color = board[row][col][0]
                if (piece_color == 'w' and white_turn) or (piece_color == 'b' and not white_turn):
                    valid_moves = highlight_valid_moves(piece_type, piece_color, row, col, board)
                    prev_click = (row, col)
            else:  # second click
                #get click position
                piece_mouse_pos = pygame.mouse.get_pos()
                # Determine the row and column of the click on the board
                selected_row = piece_mouse_pos[1] // square_size
                selected_col = piece_mouse_pos[0] // square_size
                if (selected_row, selected_col) in valid_moves:
                    # Move the piece to the clicked square
                    board[selected_row][selected_col] = board[prev_click[0]][prev_click[1]]
                    board[prev_click[0]][prev_click[1]] = " "
                    #check if piece was pawn to prep for promotion
                    if board[selected_row][selected_col][1:] == "pawn":
                        #if white and at row 7 change to queen
                        if board[selected_row][selected_col][0] == "w" and selected_row == 7:
                            board[selected_row][selected_col] = "wqueen"
                        #if black and at row 0 change to queen
                        if board[selected_row][selected_col][0] == "b" and selected_row == 0:
                            board[selected_row][selected_col] = "bqueen"
                    #set up for castling
                    #move rook for white long castling
                    if board[selected_row][selected_col] == "wking" and prev_click[1] == 4 and selected_col == 2:
                        board[0][3] = "wrook"
                        board[0][0] = " "
                    #move rook for white short castling
                    if board[selected_row][selected_col] == "wking" and prev_click[1] == 4 and selected_col == 6:
                        board[0][5] = "wrook"
                        board[0][7] = " "
                    #move rook for black long castling
                    if board[selected_row][selected_col] == "bking" and prev_click[1] == 4 and selected_col == 2:
                        board[0][3] = "brook"
                        board[0][0] = " "
                    #move rook for black short castling
                    if board[selected_row][selected_col] == "bking" and prev_click[1] == 4 and selected_col == 6:
                        board[7][5] = "brook"
                        board[7][7] = " "
                    #if rook or king moves set their move equal to true
                    if board[selected_row][selected_col] == "bking":
                        bking_moved = True
                    if board[selected_row][selected_col] == "wking":
                        wking_moved = True
                    if board[selected_row][selected_col] == "brook" and prev_click[0] == 0:
                         b0rook_moved = True
                    if board[selected_row][selected_col] == "brook" and prev_click[0] == 7:
                         b7rook_moved = True
                    if board[selected_row][selected_col] == "wrook" and prev_click[0] == 0:
                         w0rook_moved = True
                    if board[selected_row][selected_col] == "wrook" and prev_click[0] == 7:
                         w7rook_moved = True 
                     
                    piece_moved = True
                set_board(board)
                if piece_moved:
                    highlight_check(board)
                    # Reset the selected piece and valid moves and switch turns
                    white_turn = not white_turn
                piece_moved = False
                prev_click = None
                valid_moves = []
            # Check if game over
        if checkmate(board)[0]:
            show_menu = True
            #set up end menu
            winner_menu_width = board_size // 2  # Width of the menu (same as window width)
            winner_menu_height = board_size // 2  # Height of the menu
            winner_menu_background_color = (50, 50, 50)  # Background color of the menu
            winner_text_color = (255, 255, 255)  # Color of the text in the menu
            winner_menu_surface = pygame.Surface((winner_menu_width, winner_menu_height))
            winner_menu_surface.fill(winner_menu_background_color)
            win_color = " "
            winner_menu_x = (board_size - winner_menu_width) // 2
            winner_menu_y = (board_size - winner_menu_height) // 2
            
            
            if checkmate(board)[1] == "b":
                win_color = "White"
            else:
                win_color = "Black"
            # Display win message or perform other actions
            font = pygame.font.Font(None, 50)
            win_message = font.render(f"{win_color} wins!", True, winner_text_color)
            win_message_rect = win_message.get_rect(center=(board_size // 2, winner_menu_height - 30))
            # Rematch button
            button_text = font.render("Rematch?", True, winner_text_color)
            button_rect = button_text.get_rect(center=(board_size // 2, winner_menu_height + 40))
            if show_menu:
                #draw the menu
                board_surface.blit(winner_menu_surface, (winner_menu_x, winner_menu_y))
                #draw the winner text
                board_surface.blit(win_message, win_message_rect)
                #draw the rematch button
                board_surface.blit(button_text,button_rect)
            
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    #reset the game
                    set_board(starting_board)
                    board = copy.deepcopy(starting_board)
                    show_menu = False
        if stalemate(board):
            show_menu = True
            #set up end menu
            winner_menu_width = board_size // 2  # Width of the menu (same as window width)
            winner_menu_height = board_size // 2  # Height of the menu
            winner_menu_background_color = (50, 50, 50)  # Background color of the menu
            winner_text_color = (255, 255, 255)  # Color of the text in the menu
            winner_menu_surface = pygame.Surface((winner_menu_width, winner_menu_height))
            winner_menu_surface.fill(winner_menu_background_color)
            win_color = " "
            winner_menu_x = (board_size - winner_menu_width) // 2
            winner_menu_y = (board_size - winner_menu_height) // 2
            
            # Display win message or perform other actions
            font = pygame.font.Font(None, 50)
            win_message = font.render("It's a tie!", True, winner_text_color)
            win_message_rect = win_message.get_rect(center=(board_size // 2, winner_menu_height - 30))
            # Rematch button
            button_text = font.render("Rematch?", True, winner_text_color)
            button_rect = button_text.get_rect(center=(board_size // 2, winner_menu_height + 40))
            if show_menu:
                #draw the menu
                board_surface.blit(winner_menu_surface, (winner_menu_x, winner_menu_y))
                #draw the winner text
                board_surface.blit(win_message, win_message_rect)
                #draw the rematch button
                board_surface.blit(button_text,button_rect)
            
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    #reset the game
                    set_board(starting_board)
                    board = copy.deepcopy(starting_board)
                    show_menu = False
        

        pygame.display.flip()
