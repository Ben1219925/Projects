import pygame
import sys
import numpy as np
import stockfish

#convert from board matrix to FEN
def board_to_fen(board):
    """
    converts board matrix into FEN string to setup for Stockfish functions.
    ex. format: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -
    Piece placement:
    White is Uppercase
    Black is lowercase
    Numbers represent empty " " spaces
    Active color: "w" on white's turn, and "b" on black's turn.
    Castling rights:
    "K" for white kingside castling 
    "Q" for white queenside castling 
    "k" for black kingside castling 
    "q" for black queenside castling 
    En passant square:
    If there is no en passant square, a hyphen ("-") is used.
    Otherwise, it indicates the square on which a capturing pawn can land to
    perform an en passant capture.
    """
    piece_mapping = {
        "brook": "r",
        "bknight": "n",
        "bbishop": "b",
        "bqueen": "q",
        "bking": "k",
        "bpawn": "p",
        "wrook": "R",
        "wknight": "N",
        "wbishop": "B",
        "wqueen": "Q",
        "wking": "K",
        "wpawn": "P"
    }
    fen = ""
    en_passant_capture = (0,0)
    col_map = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    spaces = 0
    castle_right = True

    for row in range(8):
        for col in range(8):
            if board[row][col] == " ":
                spaces += 1
                if col == 7:
                    fen += str(spaces)
                    spaces = 0
            else:
                if spaces > 0:
                    fen += str(spaces)
                spaces = 0
                fen += piece_mapping[board[row][col]]
            #check for en_passant
            if en_passant and row == 4:
                if col != 0 and board[row][col-1] == "wpawn":
                    en_passant_capture = (row+1,col-1)
                elif col != 7 and board[row][col+1] == "wpawn":
                    en_passant_capture = (row+1,col+1)
        if row < 7:
            fen+= "/"
    if white_turn:
        turn = " w "
    else:
        turn = " b "
    fen+= turn
    
    #check for white long casling 
    if not wking_moved and not w0rook_moved:
        fen += "Q"
        castle_right = True
    #check for white short casling 
    if not wking_moved and not w7rook_moved:
        fen+= "K"
        castle_right = True
    #check for black long casling 
    if not bking_moved and not b0rook_moved:
        fen += "q" 
        castle_right = True   
    #check for black short casling 
    if not bking_moved and not b7rook_moved:
        fen += "k"
        castle_right = True
    if not castle_right:
        fen += "-"
        
    if en_passant_capture != (0,0):
        en_passant_row, en_passant_col = en_passant_capture
        fen_col = col_map[en_passant_col]
        fen_row = str(abs(en_passant_row -8))
        fen += " "
        fen += fen_col
        fen += fen_row
    else:
        fen += " -"
    
    
    return fen
                

#convert best move to matrix board notation
def fen_to_board(move):
    col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    row = abs(int(move[1])-8)
    col = col_map[move[0]]
    selected_row = abs(int(move[3])-8)
    selected_col = col_map[move[2]]
    
    return ((row,col),(selected_row,selected_col))
    

#MENUS
def start_menu():
    font = pygame.font.Font(None, 50)
    one_player = font.render("Single player", True, (255, 255, 255))
    two_player = font.render("Multiplayer", True, (255, 255, 255))
    quit_game = font.render("Exit", True, (255,255,255))
    one_player_rect = one_player.get_rect(center=(board_size/1.5, board_size/2 - 3*one_player.get_height()))
    two_player_rect = two_player.get_rect(center=(board_size/1.5, board_size/2 - two_player.get_height()))
    quit_rect = quit_game.get_rect(center=(board_size/1.5,board_size/2 + quit_game.get_height()))
    # Load the image for the background
    background_image = pygame.image.load("images/start_background.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is within the button bounds
                if one_player_rect.collidepoint(event.pos):
                    # Option 1: Play against the computer
                    return "single"
                elif two_player_rect.collidepoint(event.pos):
                    # Option 2: Play against a human
                    return "multiplayer"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        # Draw the background image onto the screen
        board_surface.blit(background_image, (0, 0))
        # Draw the menu options on the screen
        board_surface.blit(one_player, one_player_rect)
        board_surface.blit(two_player, two_player_rect)
        board_surface.blit(quit_game, quit_rect)
        
        pygame.display.flip()
    
def wpromotion_menu(piece_x,piece_y):
    queen_img = piece_images["white","queen"]
    bishop_img = piece_images["white","bishop"]
    knight_img = piece_images["white","knight"]
    rook_img = piece_images["white","rook"]
    
    # Define the size of the buttons based on the image dimensions
    button_width = queen_img.get_width()
    button_height = queen_img.get_height()
    
    # Calculate the position of the menu based on the piece coordinates
    #if on the left side of the board display right
    if piece_x < 360:
        menu_x = piece_x + button_width
    #otherwise display on the left
    else:
        menu_x = piece_x - button_width
    # Create Rect objects for the buttons
    queen_button = pygame.Rect(menu_x, piece_y, button_width, button_height)
    bishop_button = pygame.Rect(menu_x, piece_y  + button_height , button_width, button_height)
    rook_button = pygame.Rect(menu_x, piece_y  + (button_height ) * 2, button_width, button_height)
    knight_button = pygame.Rect(menu_x, piece_y + (button_height ) * 3, button_width, button_height)
    # Create a background surface
    background_surface = pygame.Surface((button_width, button_height * 4 ))
    background_surface.fill((255,255,255))  # Set the background color
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if queen_button.collidepoint(event.pos):
                    return "wqueen"
                elif bishop_button.collidepoint(event.pos):
                    return "wbishop"
                elif rook_button.collidepoint(event.pos):
                    return "wrook"
                elif knight_button.collidepoint(event.pos):
                    return "wknight"
                    
        # Draw the background surface onto the screen
        board_surface.blit(background_surface, (menu_x, piece_y))
    
    
        # Draw the buttons with the respective images
        board_surface.blit(queen_img, queen_button)
        board_surface.blit(bishop_img, bishop_button)
        board_surface.blit(rook_img, rook_button)
        board_surface.blit(knight_img, knight_button)
    
        # Update the display
        pygame.display.flip()
            
    
def bpromotion_menu(piece_x, piece_y):
    queen_img = piece_images["black","queen"]
    bishop_img = piece_images["black","bishop"]
    knight_img = piece_images["black","knight"]
    rook_img = piece_images["black","rook"]
    
    # Define the size of the buttons based on the image dimensions
    button_width = queen_img.get_width()
    button_height = queen_img.get_height()
    
    # Calculate the position of the menu based on the piece coordinates
    if piece_x < 360:
        menu_x = piece_x + button_width
    #otherwise display on the left
    else:
        menu_x = piece_x - button_width
    # Create Rect objects for the buttons
    if option == "multiplayer":
        queen_button = pygame.Rect(menu_x, piece_y, button_width, button_height)
        bishop_button = pygame.Rect(menu_x, piece_y  + button_height, button_width, button_height)
        rook_button = pygame.Rect(menu_x, piece_y  + (button_height ) * 2, button_width, button_height)
        knight_button = pygame.Rect(menu_x, piece_y + (button_height ) * 3, button_width, button_height)
    else:
        #the menu needs to be higher to stay on the screen for single player mode
        queen_button = pygame.Rect(menu_x, piece_y - button_height * 4, button_width, button_height)
        bishop_button = pygame.Rect(menu_x, piece_y  - button_height * 3 , button_width, button_height)
        rook_button = pygame.Rect(menu_x, piece_y  - button_height  * 2, button_width, button_height)
        knight_button = pygame.Rect(menu_x, piece_y - button_height , button_width, button_height)
    # Create a background surface
    background_surface = pygame.Surface((button_width, button_height * 4 ))
    background_surface.fill((200, 200, 200))  # Set the background color
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if queen_button.collidepoint(event.pos):
                    return "bqueen"
                elif bishop_button.collidepoint(event.pos):
                    return "bbishop"
                elif rook_button.collidepoint(event.pos):
                    return "brook"
                elif knight_button.collidepoint(event.pos):
                    return "bknight"
                    
        if option == "single":
            # Draw the background surface onto the screen
            board_surface.blit(background_surface, (menu_x, piece_y - button_height * 4))
        else:
            # Draw the background surface onto the screen
            board_surface.blit(background_surface, (menu_x, piece_y))

    
        # Draw the buttons with the respective images
        board_surface.blit(queen_img, queen_button)
        board_surface.blit(bishop_img, bishop_button)
        board_surface.blit(rook_img, rook_button)
        board_surface.blit(knight_img, knight_button)
    
        # Update the display
        pygame.display.flip()
        
def computer_level_menu():
    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    
    # Set up fonts
    FONT = pygame.font.Font(None, 32)
    
    # Set up buttons
    button_texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    buttons = []
    button_width = 200
    button_height = 40
    spacing = 20
    total_button_height = len(button_texts) * button_height + (len(button_texts) - 1) * spacing
    start_y = (board_size - total_button_height) // 2
    for i, text in enumerate(button_texts):
        button_x = (board_size - button_width) // 2
        button_y = start_y + i * (button_height + spacing)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)        
        button = {"rect": button_rect, "text": text}
        buttons.append(button)
    background_image = pygame.image.load("images/computer_level.jpg")

    
    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        # Perform actions based on button click
                        if button["text"] == "Level 1":
                            return 0
                        elif button["text"] == "Level 2":
                            return 5
                        elif button["text"] == "Level 3":
                            return 10
                        elif button["text"] == "Level 4":
                            return 15
                        elif button["text"] == "Level 5":
                            return 20
    
        # Draw the background image onto the screen
        board_surface.blit(background_image, (0, 0))    
        # Draw buttons
        for button in buttons:
            pygame.draw.rect(board_surface, GRAY, button["rect"])
            pygame.draw.rect(board_surface, BLACK, button["rect"], 2)
            text_surf = FONT.render(button["text"], True, BLACK)
            text_rect = text_surf.get_rect(center=button["rect"].center)
            board_surface.blit(text_surf, text_rect)
    
        # Update the display
        pygame.display.flip()


#GAME LOGIC
def find_king(board):
    bking_row, bking_col = np.where(board == "bking")
    wking_row, wking_col = np.where(board == "wking")
    return ((bking_row[0],bking_col[0]),(wking_row[0],wking_col[0]))


def get_valid_moves(en_passant,piece_type, piece_color, row, col, board):
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
        if option == "multiplayer":
            #whoever's turn it is will move - rows
            if (piece_color == "w" and white_turn) or (piece_color == "b" and not white_turn):
                # Check if pawn can move one square forward
                if row > 0 and board[row-1][col] == " ":
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
                if en_passant and row == 3:
                    if piece_color == "w":
                        if col != 0 and board[row][col-1] == "bpawn":
                            valid_moves.append((row-1,col-1))

                        elif col != 7 and board[row][col+1] == "bpawn":
                            valid_moves.append((row-1,col+1))

                    if piece_color == "b":
                        if col != 0 and board[row][col-1] == "wpawn":
                            valid_moves.append((row-1,col-1))

                        elif col != 7 and board[row][col+1] == "wpawn":
                            valid_moves.append((row-1,col+1))
            else:
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
        else:
            # white pieces move - rows, black moves + rows
            if piece_color == "w":
                # Check if pawn can move one square forward
                if row > 0 and board[row-1][col] == " ":
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
                if en_passant and row == 3:
                    if col != 0 and board[row][col-1] == "bpawn":
                        valid_moves.append((row-1,col-1))
                    elif col != 7 and board[row][col+1] == "bpawn":
                        valid_moves.append((row-1,col+1))
                                
            elif piece_color == "b":
                # Check if pawn can move one square forward
                if row < 7 and board[row+1][col] == " ":
                    valid_moves.append((row+1, col))
                    # Check if pawn can move two squares forward (if in starting position)
                    if row == 1 and board[row+2][col] == " ":
                        valid_moves.append((row+2, col))
                # Check if pawn can capture diagonally to the left
                if row < 7 and col > 0 and board[row+1][col-1] != " " and board[row+1][col-1][0] != piece_color :
                    valid_moves.append((row+1, col-1))
                # Check if pawn can capture diagonally to the right
                if row < 7 and col < 7 and board[row+1][col+1] != " " and board[row+1][col+1][0] != piece_color:
                    valid_moves.append((row+1, col+1))
                

            pass
    
    return valid_moves    

def draw(board):
    #if both players only have king, 1 knight and bishops or 2knight no bishops left return True
    pieces = ["wqueen","bqueen","wrook","brook","wpawn","bpawn"]
    if not np.any(np.isin(pieces,board)) and ((np.sum(board == "wknight") < 3 and np.sum(board == "wbishop") == 0) or (np.sum(board == "wbishop") <2 and np.sum(board == "wknight") == 0)) and ((np.sum(board == "bknight") < 3 and np.sum(board == "bbishop") == 0) or (np.sum(board == "bbishop") < 2 and np.sum(board == "bknight") == 0)):
        return True
    
    return False
    

def check_for_check(row, col, new_row, new_col, board):
   """
   Checks if the piece's move would put the king into check.
   True if the move would put the king into check, False otherwise.
   """
   # Make a copy of the board so that we don't modify the original board.
   new_board = np.copy(board)
   # Move the piece to the new location.
   new_board[new_row][new_col] = new_board[row][col]
   new_board[row][col] = " "
   cur_in_check, row, col, cur_king_color = check(board)
   # Check if the king is in check on the new board.
   in_check, crow, ccol, king_color = check(new_board)
   (bking_row,bking_col),(wking_row,wking_col) = find_king(new_board)
   #if kings would "put each other in check" return true
   if (bking_row,bking_col) in get_valid_moves(en_passant, "king", "w", wking_row, wking_col, new_board)  or (wking_row,wking_col) in get_valid_moves(en_passant, "king", "b", bking_row, bking_col, new_board):
       return True
   #if you are currently in check but can put the other king in check still return True
   if cur_in_check and white_turn and cur_king_color == "w" and king_color == "b":
       return True
   if cur_in_check and not white_turn and cur_king_color == "b" and king_color == "w":
       return True
   if in_check and white_turn and king_color == "w":
       return True
   elif in_check and not white_turn and king_color == "b":
       return True
   #other wise false
   return False

def all_valid_moves(en_passant, piece_type,piece_color,row,col,board):
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
        if option == "multiplayer":
            #whoever's turn it is will move - rows
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
            if en_passant and row == 3:
                if piece_color == "w":
                    if col != 0 and board[row][col-1] == "bpawn" and not check_for_check(row,col,row-1,col-1,board) and col-1 == abs(en_passant_col - 7):
                        valid_moves.append((row-1,col-1))
                    elif col != 7 and board[row][col+1] == "bpawn" and not check_for_check(row,col,row-1,col+1,board) and col+1 == abs(en_passant_col - 7):
                        valid_moves.append((row-1,col+1))
                if piece_color == "b":
                    if col != 0 and board[row][col-1] == "wpawn" and not check_for_check(row,col,row-1,col-1,board) and col-1 == abs(en_passant_col - 7):
                        valid_moves.append((row-1,col-1))
                    elif col != 7 and board[row][col+1] == "wpawn" and not check_for_check(row,col,row-1,col+1,board) and col+1 == abs(en_passant_col - 7):
                        valid_moves.append((row-1,col+1))
        else:
            # white pieces move - rows, black moves + rows
            if piece_color == "w":
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
                if en_passant and row == 3:
                    if col != 0 and board[row][col-1] == "bpawn" and col-1 == en_passant_col:
                        valid_moves.append((row-1,col-1))
                    elif col != 7 and board[row][col+1] == "bpawn" and col+1 == en_passant_col:
                        valid_moves.append((row-1,col+1))
            elif piece_color == "b":
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
                if en_passant and row == 4:
                    if col != 0 and board[row][col-1] == "wpawn" and col-1 == en_passant_col:
                        valid_moves.append((row+1,col-1))
                    elif col != 7 and board[row][col+1] == "wpawn" and col+1 == en_passant_col:
                        valid_moves.append((row+1,col+1))

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
    valid_moves = all_valid_moves(en_passant, piece_type, piece_color, row, col, board)
    for move in valid_moves:
        pygame.draw.rect(board_surface, (0, 255, 0), (move[1]*square_size, move[0]*square_size, square_size, square_size), width=3)
    if piece_type == "king":
        (bking_row,bking_col),(wking_row,wking_col) = find_king(board)
        #castling rules
        #1.The king is not currently in check.
        #2.Neither the king nor the rook has previously moved.
        #3.There are no pieces between the king and the rook.
        #4.The king does not pass through or finish on a square that is attacked by an enemy piece.
        #check for white long casling 
        if white_turn and check(board)[3] != "w" and not wking_moved and not w0rook_moved and board[wking_row][wking_col - 3] == " " and board[wking_row][wking_col -2] == " "  and board[wking_row][wking_col -1] == " " and not check_for_check(wking_row,wking_col,wking_row,wking_col -2,board) and not check_for_check(wking_row,wking_col,wking_row,wking_col -1,board):
            valid_moves.append((wking_row,wking_col -2))
            #highlight in blue
            pygame.draw.rect(board_surface, (0,0,255), ((wking_col -2)*square_size, wking_row*square_size, square_size, square_size), width=4)
        #check for white short casling 
        if white_turn and check(board)[3] != "w" and not wking_moved and not w7rook_moved and board[wking_row][wking_col + 2] == " " and board[wking_row][wking_col + 1] == " " and not check_for_check(wking_row,wking_col,wking_row,wking_col +2,board) and not check_for_check(wking_row,wking_col,wking_row,wking_col +1,board):
            valid_moves.append((wking_row,wking_col +2))
            #highlight in blue
            pygame.draw.rect(board_surface, (0,0,255), ((wking_col +2)*square_size, wking_row*square_size, square_size, square_size), width=4)
        #check for black long casling 
        if not white_turn and check(board)[3] != "b" and not bking_moved and not b0rook_moved and board[bking_row][bking_col - 3] == " " and board[bking_row][bking_col -2] == " "  and board[bking_row][bking_col -1] == " " and not check_for_check(bking_row,bking_col,bking_row,bking_col -2,board) and not check_for_check(bking_row,bking_col,bking_row,bking_col -1,board):
            valid_moves.append((bking_row,bking_col -2))
            #highlight in blue
            pygame.draw.rect(board_surface, (0,0,255), ((bking_col -2)*square_size, bking_row*square_size, square_size, square_size), width=4)
        #check for black short casling 
        if not white_turn and check(board)[3] != "b" and not bking_moved and not b7rook_moved and board[bking_row][bking_col + 2] == " " and board[bking_row][bking_col + 1] == " " and not check_for_check(bking_row,bking_col,bking_row,bking_col +2,board) and not check_for_check(bking_row,bking_col,bking_row,bking_col +1,board):
            valid_moves.append((bking_row,bking_col +2))
            #highlight in blue
            pygame.draw.rect(board_surface, (0,0,255), ((bking_col +2)*square_size, bking_row*square_size, square_size, square_size), width=4)
    return valid_moves

def set_board(board):
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(board_surface, (255, 206, 158), rect)
            else:
                pygame.draw.rect(board_surface, (209, 139, 71), rect)
            if board[row][col] != " ":
                piece_image = piece_images[("white" if board[row][col][0] == "w" else "black", board[row][col][1:])]
                board_surface.blit(piece_image, rect)
            
    
def check(board):
    check = False
    rows = []
    cols = []
    king_color = " "
    (bking_row,bking_col),(wking_row,wking_col) = find_king(board)
    for row in range(8):
        for col in range(8):
            if board[row][col] != " ":
                piece_type = board[row][col][1:]
                piece_color = board[row][col][0]
                valid_moves = get_valid_moves(en_passant,piece_type, piece_color, row, col, board)
                if (bking_row,bking_col) in valid_moves:
                    check = True
                    #location of the piece puting the king in check
                    rows.append(row)
                    cols.append(col)
                    #color of the king in check
                    king_color = "b"
                elif (wking_row,wking_col) in valid_moves:
                    check = True
                    #location of the piece puting the king in check
                    rows.append(row)
                    cols.append(col)
                    #color of the king in check
                    king_color = "w"
                    
    return (check,rows,cols,king_color)

def highlight_check(board):
    in_check,row,col,king_color = check(board)
    (bking_row,bking_col),(wking_row,wking_col) = find_king(board)

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
    return (in_check,row,col,king_color)
        

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
                    valid_moves.append(all_valid_moves(en_passant,piece_type, piece_color, row, col, board))
                elif king_color == "b" and piece_color == "b":
                    valid_moves.append(all_valid_moves(en_passant,piece_type, piece_color, row, col, board))
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
                    valid_moves.append(all_valid_moves(en_passant,piece_type, piece_color, row, col, board))
                elif not white_turn and piece_color == "b":
                    valid_moves.append(all_valid_moves(en_passant,piece_type, piece_color, row, col, board))
        for move in valid_moves:
            if move != []:
                no_moves = False
        if no_moves:
            return True
    return False

def game_over(board):
    if stalemate(board) or checkmate(board)[0] or draw(board):
        return True
    return False



pygame.init()
pygame.mixer.init()

#COMPUTER LOGIC
stockfish_path = 'stockfish_15.1_win_x64/stockfish-windows-2022-x86-64.exe'
stockfish = stockfish.Stockfish(stockfish_path)
# Set up the board surface
piece_size = 90 #size of the piece image in pixels
board_size = piece_size * 8  # the size of the board in pixels
board_surface = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess")
# Define the starting positions of the pieces
starting_board = np.array([
    ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
    ["bpawn"] * 8,
    [" "] * 8,
    [" "] * 8,
    [" "] * 8,
    [" "] * 8,
    ["wpawn"] * 8,
    ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"],
])

# Define the size of each square on the board
square_size = board_size // 8
#start menu
option = start_menu()
if option == "single":
    level = computer_level_menu()

# Load the images for the pieces
piece_images = {}
for color in ("white", "black"):
    for piece_type in ("king", "queen", "rook", "bishop", "knight", "pawn"):
        piece_images[(color, piece_type)] = pygame.image.load(f"images/{color}_{piece_type}.png")

board = np.copy(starting_board)
set_board(board)

prev_click = None
white_turn = True
piece_moved = False
bking_moved = False
wking_moved = False
b0rook_moved = False
b7rook_moved = False
w0rook_moved = False
w7rook_moved = False
en_passant = False
capture = False
castling = False
sound_played = False
close_menu = False
#set stockfish level
if option == "single":
    stockfish.set_skill_level(level)


en_passant_turn = 0
move_sound = pygame.mixer.Sound("sounds/move-self.wav")
capture_sound = pygame.mixer.Sound("sounds/capture.wav")
win_sound = pygame.mixer.Sound("sounds/medieval-fanfare-6826.wav")
check_sound = pygame.mixer.Sound("sounds/move-check.wav")
castling_sound = pygame.mixer.Sound("sounds/castle.wav")
promotion_sound = pygame.mixer.Sound("sounds/promote.wav")
stalemate_sound = pygame.mixer.Sound("sounds/stalemate.wav")

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if option == "single" and not white_turn and  not game_over(board):
            fen_board = board_to_fen(board)
            stockfish.set_fen_position(fen_board)
            best_move = stockfish.get_best_move()
            ((cur_row,cur_col),(selected_row,selected_col)) = fen_to_board(best_move)
            #check if piece is being captured
            if board[selected_row][selected_col] != " ":
                capture = True
            # Move the piece to the clicked square
            board[selected_row][selected_col] = board[cur_row][cur_col]
            board[cur_row][cur_col] = " "
    
            #check if piece was pawn
            if board[selected_row][selected_col][1:] == "pawn":
                if abs((selected_row - cur_row)) == 2 and ((selected_col > 0 and board[selected_row][selected_col -1] == "wpawn") or (selected_col < 7 and board[selected_row][selected_col +1] == "wpawn")):
                    en_passant = True
                    en_passant_col = selected_col
                if abs(selected_col - cur_col) == 1 and en_passant:
                    if board[selected_row+1][selected_col] == "wpawn":
                        board[selected_row+1][selected_col] = " "
                        en_passant = False
                        en_passant_turn = 0
                    elif board[selected_row-1][selected_col] == "wpawn":
                        board[selected_row-1][selected_col] = " "
                        en_passant = False
                        en_passant_turn = 0
                #if pawn reaches the end of the board promote
                if selected_row == 0:
                    board[selected_row][selected_col] = "bqueen"
                    promotion_sound.play()
                
            #set up for castling
            #move rook for white long castling
            if board[selected_row][selected_col] == "wking" and cur_col == 4 and selected_col == 2:
                board[cur_row][3] = "wrook"
                board[cur_row][0] = " "
                castling = True
            #move rook for white short castling
            if board[selected_row][selected_col] == "wking" and cur_col == 4 and selected_col == 6:
                board[cur_row][5] = "wrook"
                board[cur_row][7] = " "
                castling = True
            #move rook for black long castling
            if board[selected_row][selected_col] == "bking" and cur_col == 4 and selected_col == 2:
                board[cur_row][3] = "brook"
                board[cur_row][0] = " "
                castling = True
            #move rook for black short castling
            if board[selected_row][selected_col] == "bking" and cur_col == 4 and selected_col == 6:
                board[cur_row][5] = "brook"
                board[cur_row][7] = " "
                castling = True
            #if rook or king moves set their move equal to true
            if board[selected_row][selected_col] == "bking":
                bking_moved = True
            if board[selected_row][selected_col] == "wking":
                wking_moved = True
            if board[selected_row][selected_col] == "brook" and cur_col == 0:
                  b0rook_moved = True
            if board[selected_row][selected_col] == "brook" and cur_col == 7:
                  b7rook_moved = True
            if board[selected_row][selected_col] == "wrook" and cur_col == 0:
                  w0rook_moved = True
            if board[selected_row][selected_col] == "wrook" and cur_col == 7:
                  w7rook_moved = True 
            piece_moved = True
            set_board(board)
            if piece_moved:
                in_check,row,col,king_color = highlight_check(board)
                #play sound effects:
                #if piece was captured play capture sound
                if capture and not in_check:
                    capture_sound.play()
                #if in check play check sound effect
                elif in_check:
                    check_sound.play()
                #if castling play sound effect
                elif castling:
                    castling_sound.play()
                #otherwise play move sound effect
                else:
                    move_sound.play()
                # Reset the selected piece and valid moves and switch turns
                white_turn = not white_turn
                if option == "multiplayer":
                    flipped_board = pygame.transform.rotate(board_surface, 180)
                    board_surface.blit(flipped_board, (0,0))
                    board = np.rot90(board,2)
                    set_board(board)
                    highlight_check(board)
                if en_passant:
                    en_passant_turn+=1
            piece_moved = False
            prev_click = None
            valid_moves = []
            capture = False
            castling = False
        
        
            if en_passant_turn >=2:
                en_passant_turn = 0
                en_passant = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if prev_click is None:  # first click
                # Determine the row and column of the click on the board
                row = event.pos[1] // square_size
                col = event.pos[0] // square_size
                piece_type = board[row][col][1:]
                piece_color = board[row][col][0]
                if (piece_color == 'w' and white_turn) or (piece_color == 'b' and not white_turn):
                    valid_moves = highlight_valid_moves(piece_type, piece_color, row, col, board)
                    prev_click = (row, col)
            else:  # second click
                # Determine the row and column of the click on the board
                selected_row = event.pos[1] // square_size
                selected_col = event.pos[0] // square_size
                if (selected_row, selected_col) in valid_moves:
                    #check if piece is being captured
                    if board[selected_row][selected_col] != " ":
                        capture = True
                    # Move the piece to the clicked square
                    board[selected_row][selected_col] = board[prev_click[0]][prev_click[1]]
                    board[prev_click[0]][prev_click[1]] = " "
        
                    #check if piece was pawn
                    if board[selected_row][selected_col][1:] == "pawn":
                        if board[selected_row][selected_col][0] == "w":
                            if abs((selected_row - prev_click[0])) == 2 and ((selected_col > 0 and board[selected_row][selected_col -1] == "bpawn") or (selected_col < 7 and board[selected_row][selected_col +1] == "bpawn")):
                                en_passant = True
                                en_passant_col = selected_col
                            if abs(selected_col - prev_click[1]) == 1 and en_passant:
                                if board[selected_row+1][selected_col] == "bpawn":
                                    board[selected_row+1][selected_col] = " "
                                    capture = True
                                elif board[selected_row-1][selected_col] == "bpawn":
                                    board[selected_row-1][selected_col] = " "
                                    capture = True
                    
                            
                        if board[selected_row][selected_col][0] == "b":
                            if abs((selected_row - prev_click[0])) == 2 and ((selected_col > 0 and board[selected_row][selected_col -1] == "wpawn") or (selected_col < 7 and board[selected_row][selected_col +1] == "wpawn")):
                                en_passant = True
                                en_passant_col = selected_col
                            if abs(selected_col - prev_click[1]) == 1 and en_passant:
                                if board[selected_row+1][selected_col] == "wpawn":
                                    board[selected_row+1][selected_col] = " "
                                    en_passant = False
                                    en_passant_turn = 0
                                elif board[selected_row-1][selected_col] == "wpawn":
                                    board[selected_row-1][selected_col] = " "
                                    en_passant = False
                                    en_passant_turn = 0
                        #if pawn reaches the end of the board promote
                        if board[selected_row][selected_col][0] == "w" and (selected_row == 7 or selected_row == 0):
                            promotion_piece = wpromotion_menu(event.pos[0],event.pos[1])
                            board[selected_row][selected_col] = promotion_piece
                            promotion_sound.play()
                        #if pawn reaches the end of the board promote
                        if board[selected_row][selected_col][0] == "b" and (selected_row == 0 or selected_row == 7):
                            promotion_piece = bpromotion_menu(event.pos[0],event.pos[1])
                            board[selected_row][selected_col] = promotion_piece
                            promotion_sound.play()
                        
                    #set up for castling
                    #move rook for white long castling
                    if board[selected_row][selected_col] == "wking" and prev_click[1] == 4 and selected_col == 2:
                        board[prev_click[0]][3] = "wrook"
                        board[prev_click[0]][0] = " "
                        castling = True
                    #move rook for white short castling
                    if board[selected_row][selected_col] == "wking" and prev_click[1] == 4 and selected_col == 6:
                        board[prev_click[0]][5] = "wrook"
                        board[prev_click[0]][7] = " "
                        castling = True
                    #move rook for black long castling
                    if board[selected_row][selected_col] == "bking" and prev_click[1] == 4 and selected_col == 2:
                        board[prev_click[0]][3] = "brook"
                        board[prev_click[0]][0] = " "
                        castling = True
                    #move rook for black short castling
                    if board[selected_row][selected_col] == "bking" and prev_click[1] == 4 and selected_col == 6:
                        board[prev_click[0]][5] = "brook"
                        board[prev_click[0]][7] = " "
                        castling = True
                    #if rook or king moves set their move equal to true
                    if board[selected_row][selected_col] == "bking":
                        bking_moved = True
                    if board[selected_row][selected_col] == "wking":
                        wking_moved = True
                    if board[selected_row][selected_col] == "brook" and prev_click[1] == 0:
                         b0rook_moved = True
                    if board[selected_row][selected_col] == "brook" and prev_click[1] == 7:
                         b7rook_moved = True
                    if board[selected_row][selected_col] == "wrook" and prev_click[1] == 0:
                         w0rook_moved = True
                    if board[selected_row][selected_col] == "wrook" and prev_click[1] == 7:
                         w7rook_moved = True 
                    piece_moved = True
                set_board(board)
                if piece_moved:
                    in_check,row,col,king_color = highlight_check(board)
                    #play sound effects:
                    #if piece was captured play capture sound
                    if capture and not in_check:
                        capture_sound.play()
                    #if in check play check sound effect
                    elif in_check:
                        check_sound.play()
                    #if castling play sound effect
                    elif castling:
                        castling_sound.play()
                    #otherwise play move sound effect
                    else:
                        move_sound.play()
                    # Reset the selected piece and valid moves and switch turns
                    white_turn = not white_turn
                    if option == "multiplayer":
                        flipped_board = pygame.transform.rotate(board_surface, 180)
                        board_surface.blit(flipped_board, (0,0))
                        board = np.rot90(board,2)
                        set_board(board)
                        highlight_check(board)
                    if en_passant:
                        en_passant_turn+=1
                piece_moved = False
                prev_click = None
                valid_moves = []
                capture = False
                castling = False

            
                if en_passant_turn >=2:
                    en_passant_turn = 0
                    en_passant = False
            # Check if game over
        if checkmate(board)[0]:
            show_menu = True
            #set up end menu
            winner_menu_width = board_size // 2  # Width of the menu (same as window width)
            winner_menu_height = board_size // 2  # Height of the menu
            winner_menu_surface = pygame.Surface((winner_menu_width, winner_menu_height))
            win_color = " "
            winner_menu_x = (board_size - winner_menu_width) // 2
            winner_menu_y = (board_size - winner_menu_height) // 2
            
            
            if checkmate(board)[1] == "b":
                win_color = "White"
                winner_text_color = (255, 255, 255)  # Color of the text in the menu
                winner_menu_background_color = (50, 50, 50)  # Background color of the menu
                winner_menu_surface.fill(winner_menu_background_color)


            else:
                win_color = "Black"
                winner_text_color = (0,0,0)  # Color of the text in the menu
                winner_menu_background_color = (230,230,230)  # Background color of the menu
                winner_menu_surface.fill(winner_menu_background_color)


            # Display win message or perform other actions
            win_font = pygame.font.Font(None, 80)
            font = pygame.font.Font(None, 50)
            win_message = win_font.render(f"{win_color} wins!", True, winner_text_color)
            win_message_rect = win_message.get_rect(center=(board_size // 2, winner_menu_height - 80))
            # Rematch button
            button_text = font.render("Rematch?", True, winner_text_color)
            button_rect = button_text.get_rect(center=(board_size // 2, winner_menu_height))
            #return to winning board
            return_button_text = font.render("See winning board", True, winner_text_color)
            return_button_rect = button_text.get_rect(center=((board_size // 2) -68, winner_menu_height + 80))
            if show_menu and not close_menu:
                #draw the menu
                board_surface.blit(winner_menu_surface, (winner_menu_x, winner_menu_y))
                #draw the winner text
                board_surface.blit(win_message, win_message_rect)
                #draw the rematch button
                board_surface.blit(button_text,button_rect)
                board_surface.blit(return_button_text,return_button_rect)
                #play winner sound effect
                if not sound_played:
                    win_sound.play()
                    sound_played = True
            
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    #reset the game
                    set_board(starting_board)
                    board = np.copy(starting_board)
                    show_menu = False
                    white_turn = True
                    bking_moved = False
                    wking_moved = False
                    b0rook_moved = False
                    b7rook_moved = False
                    w0rook_moved = False
                    w7rook_moved = False
                    capture = False
                    castling = False
                    sound_played = False
                if return_button_rect.collidepoint(event.pos):
                    close_menu = True
                    set_board(board)


        if stalemate(board):
            show_menu = True
            #set up end menu
            winner_menu_width = board_size // 2  # Width of the menu (same as window width)
            winner_menu_height = board_size // 2  # Height of the menu
            winner_menu_background_color = (50, 50, 50)  # Background color of the menu
            winner_text_color = (255, 255, 255)  # Color of the text in the menu
            winner_menu_surface = pygame.Surface((winner_menu_width, winner_menu_height))
            winner_menu_surface.fill(winner_menu_background_color)
            winner_menu_x = (board_size - winner_menu_width) // 2
            winner_menu_y = (board_size - winner_menu_height) // 2
            #return to board
            return_button_text = font.render("See final board", True, winner_text_color)
            return_button_rect = button_text.get_rect(center=((board_size // 2) -60, winner_menu_height + 80))
            
            # Display win message or perform other actions
            font = pygame.font.Font(None, 50)
            win_message = font.render("Stalemate!", True, winner_text_color)
            win_message_rect = win_message.get_rect(center=(board_size // 2, winner_menu_height - 30))
            # Rematch button
            button_text = font.render("Rematch?", True, winner_text_color)
            button_rect = button_text.get_rect(center=(board_size // 2, winner_menu_height + 40))
            if show_menu and not close_menu:
                #draw the menu
                board_surface.blit(winner_menu_surface, (winner_menu_x, winner_menu_y))
                #draw the winner text
                board_surface.blit(win_message, win_message_rect)
                #draw the rematch button
                board_surface.blit(button_text,button_rect)
                board_surface.blit(return_button_text,return_button_rect)

                if not sound_played:
                    stalemate_sound.play()
                    sound_played = True
            
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    #reset the game
                    set_board(starting_board)
                    board = np.copy(starting_board)
                    show_menu = False
                    bking_moved = False
                    wking_moved = False
                    b0rook_moved = False
                    b7rook_moved = False
                    w0rook_moved = False
                    w7rook_moved = False
                    capture = False
                    castling = False
                    white_turn = True
                    sound_played = False
                if return_button_rect.collidepoint(event.pos):
                    close_menu = True
                    set_board(board)

        pygame.display.flip()
        
        if draw(board):
            show_menu = True
            #set up end menu
            winner_menu_width = board_size // 2  # Width of the menu (same as window width)
            winner_menu_height = board_size // 2  # Height of the menu
            winner_menu_background_color = (50, 50, 50)  # Background color of the menu
            winner_text_color = (255, 255, 255)  # Color of the text in the menu
            winner_menu_surface = pygame.Surface((winner_menu_width, winner_menu_height))
            winner_menu_surface.fill(winner_menu_background_color)
            winner_menu_x = (board_size - winner_menu_width) // 2
            winner_menu_y = (board_size - winner_menu_height) // 2
            #return to board
            return_button_text = font.render("See final board", True, winner_text_color)
            return_button_rect = button_text.get_rect(center=((board_size // 2) -60, winner_menu_height + 80))
            # Display win message or perform other actions
            font = pygame.font.Font(None, 50)
            win_message = font.render("Draw!", True, winner_text_color)
            win_message_rect = win_message.get_rect(center=(board_size // 2, winner_menu_height - 30))
            # Rematch button
            button_text = font.render("Rematch?", True, winner_text_color)
            button_rect = button_text.get_rect(center=(board_size // 2, winner_menu_height + 40))
            if show_menu and not close_menu:
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
                    board = np.copy(starting_board)
                    show_menu = False
                    bking_moved = False
                    wking_moved = False
                    b0rook_moved = False
                    b7rook_moved = False
                    w0rook_moved = False
                    w7rook_moved = False
                    capture = False
                    castling = False
                    white_turn = True
                if return_button_rect.collidepoint(event.pos):
                    close_menu = True
                    set_board(board)

        pygame.display.flip()

