import pygame
import sys

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
                valid_moves.append((new_row, new_col))
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
    
def highlight_valid_moves(piece_type, piece_color, row, col, board):
    """
    Highlights all valid moves for a given chess piece at a given position on the board.
    piece_type: the type of piece ("king", "queen", "rook", "bishop", "knight", or "pawn")
    piece_color: the color of the piece ("white" or "black")
    row: the row index of the piece's current position (0-7)
    col: the column index of the piece's current position (0-7)
    board: a 2D list representing the current state of the chess board
    """
    valid_moves = get_valid_moves(piece_type, piece_color, row, col, board)
    for move in valid_moves:
        pygame.draw.rect(board_surface, (0, 255, 0), (move[1]*square_size, move[0]*square_size, square_size, square_size), width=3)
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
    
def check(color, row, col, next_valid_moves,board):
    if color == "w":
        if (bking_row,bking_col) in next_valid_moves:
            pygame.draw.rect(board_surface, (255, 0, 0), (bking_col*square_size, bking_row*square_size, square_size, square_size), width=3)
            pygame.draw.rect(board_surface, (255, 0, 0), (col*square_size, row*square_size, square_size, square_size), width=3)
            pygame.display.update()
            return True
    if color == "b":
        if (wking_row,wking_col) in next_valid_moves:
            pygame.draw.rect(board_surface, (255, 0, 0), (wking_col*square_size, wking_row*square_size, square_size, square_size), width=3)
            pygame.draw.rect(board_surface, (255, 0, 0), (col*square_size, row*square_size, square_size, square_size), width=3)
            pygame.display.update()
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

# Main game loop
board = starting_board
prev_click = None
white_turn = True
piece_moved = False
wking_row = 0
wking_col = 4
bking_row = 7
bking_col = 4
in_check = False


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
                    #check if peace moved was the king
                    if board[selected_row][selected_col][1:] == "king" and board[selected_row][selected_col][0] == "w":
                        wking_row = selected_row
                        wking_col = selected_col
                    if board[selected_row][selected_col][1:] == "king" and board[selected_row][selected_col][0] == "b":
                        bking_row = selected_row
                        bking_col = selected_col
                    piece_moved = True
                set_board(board)

                if piece_moved:
                    next_valid_moves = get_valid_moves(piece_type, piece_color, selected_row, selected_col, board)
                    if not in_check:
                        check(piece_color, selected_row, selected_col, next_valid_moves,board)
                    # Reset the selected piece and valid moves and switch turns
                    white_turn = not white_turn
                piece_moved = False
                prev_click = None
                valid_moves = []

    pygame.display.flip()
