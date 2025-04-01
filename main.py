import pygame
import sys
import openai

# Set your OpenAI API key here
openai.api_key = "key"

# Define board format (global)
board_format = [
    [None, 'w', None, 'w', None, 'w', None, 'w'],
    ['w', None, 'w', None, 'w', None, 'w', None],
    [None, 'w', None, 'w', None, 'w', None, 'w'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['b', None, 'b', None, 'b', None, 'b', None],
    [None, 'b', None, 'b', None, 'b', None, 'b'],
    ['b', None, 'b', None, 'b', None, 'b', None]
]
pygame.init()

# Screen Sizes
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def draw_squares(screen):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(screen)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    pygame.quit()
    sys.exit()


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, screen):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(screen, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)
        if self.king:
            crown = pygame.image.load('crown.png')
            crown = pygame.transform.scale(crown, (44, 25))
            screen.blit(crown, (self.x - crown.get_width() // 2, self.y - crown.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()


class Board:
    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        # Initialize valid moves dictionary
        moves = {}

        # If the piece is a king, it can move both directions (up and down)
        directions = [-1, 1] if piece.king else [piece.direction]

        # For each direction a king can move, check the diagonals
        for direction in directions:
            moves.update(self._traverse_direction(piece.row + direction, piece.col - 1, piece, direction))
            moves.update(self._traverse_direction(piece.row + direction, piece.col + 1, piece, direction))

        return moves

    def _traverse_direction(self, row, col, piece, direction):
        moves = {}
        if 0 <= row < ROWS and 0 <= col < COLS:
            target = self.get_piece(row, col)
            # If the square is empty, it's a valid move
            if target == 0:
                moves[(row, col)] = []
            # If there's an opponent's piece, check if a jump is possible
            elif target.color != piece.color:
                jump_row, jump_col = row + direction, col + (col - piece.col)
                if 0 <= jump_row < ROWS and 0 <= jump_col < COLS and self.get_piece(jump_row, jump_col) == 0:
                    moves[(jump_row, jump_col)] = [target]



        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            global board_format
            board_format[piece.row][piece.col] = None
            if piece.color == WHITE:
                self.white_left -= 1
            else:
                self.red_left -= 1

        # Check if the game is over
        if self.white_left == 0:
            print("Red wins!")
            self.end_game("Red Wins!")
        elif self.red_left == 0:
            print("White wins!")
            self.end_game("White Wins!")

    def end_game(self, message):
        # Show the game over message and quit
        font = pygame.font.Font(None, 200)
        text = font.render(message, True, (125, 255, 125))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing
        pygame.quit()
        sys.exit()

    def __init__(self):
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        draw_squares(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def move(self, piece, row, col):
        global board_format
        self.board[piece.row][piece.col], self.board[row][col], board_format[piece.row][piece.col], board_format[row][
            col] = self.board[row][col], self.board[piece.row][piece.col], board_format[row][col], \
        board_format[piece.row][piece.col]
        piece.move(row, col)

        # If the piece reaches the last row, promote it to a king
        if row == 0 or row == ROWS - 1:
            piece.make_king()
            board_format[row][col] = 'W' if piece.color == WHITE else 'B'  # Update to uppercase for kings
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_visual_board(self):
        """Return a visual representation of the board."""
        visual_board = []
        for row in range(ROWS):
            visual_row = []
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    visual_row.append('-')
                elif piece.color == WHITE:
                    visual_row.append('w' if not piece.king else 'W')
                else:
                    visual_row.append('b' if not piece.king else 'B')
            visual_board.append(visual_row)
        return visual_board

    def update_board_format(self):
        """Updates the global board format based on the board state."""
        global board_format
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    board_format[row][col] = None
                elif piece.color == WHITE:
                    board_format[row][col] = 'w' if not piece.king else 'W'
                else:
                    board_format[row][col] = 'b' if not piece.king else 'B'


class Game:
    def __init__(self, screen):
        self._init()
        self.screen = screen

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.board.update_board_format()  # Initialize board format

    def update(self):
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
            self.inquire_gpt()
        else:
            self.turn = RED

        # After changing the turn, check for the game over condition
        if self.board.white_left == 0:
            self.board.end_game("Red Wins!")
        elif self.board.red_left == 0:
            self.board.end_game("White Wins!")

    def inquire_gpt(self):
        global board_format
        visual_board = self.board.get_visual_board()

        # Get all valid moves for the current turn (all white pieces)
        all_valid_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == WHITE:
                    valid_moves = self.board.get_valid_moves(piece)
                    for move in valid_moves:
                        start_square = f"{chr(col + 97)}{8 - row}"
                        end_square = f"{chr(move[1] + 97)}{8 - move[0]}"
                        all_valid_moves.append(f"{start_square} to {end_square}")

        # Prepare the message with all possible valid moves
        messages = [
            {"role": "system", "content": (
                "You are an extremely skilled checkers AI playing as white. Your goal is to choose the best possible move "
                "from the provided list of valid moves. Ensure the move follows standard checkers rules and is legal for the white pieces.\n"
                "The best possible move is to jump another piece without being jumped back."
                "It is extremely important to keep your pieces. Whenever an opurtunity arrives to save a piece, take that chance."
                "You should cling to the sides of the board."
                "Try to avoid the player jumping your pieces."
                "Try to think what will happen in the game a few moves ahead."
                "The most important thing in checkers is to have more pieces than your oponent."
                "Remember that in checkers if you have a jump, you may take it."
                "Try to stop the player from getting multiple jumps in a row."
                "If no moves are available, respond with 'No moves available.'\n\n"
                "Provide the best move based on the list of options.\n\n"
                "The format of each move is 'start_square to end_square' (e.g., 'b6 to a5'). "
                "Only output the best move without additional explanation."
            )},
            {"role": "user", "content": (
                    "Current board state:\n"
                    "\n".join([" ".join(row) for row in visual_board]) + "\n"
                                                                         "You are playing as white. Below are the valid moves:\n"
                                                                         "\n".join(all_valid_moves) + "\n"
                                                                                                      "What is the best legal move?"
            )}
        ]

        success = False
        while not success:
            print("Requesting a move from the AI...")

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=1,
                    max_tokens=100
                )

                # Extract and parse the AI's move
                response_text = response['choices'][0]['message']['content'].strip()
                print(f"AI response: {response_text}")

                # Parse the AI's move
                start, end = response_text.split(" to ")
                start_col, start_row = start[0], start[1]
                end_col, end_row = end[0], end[1]

                # Convert board notation to indices
                column_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
                start_col_idx = column_mapping[start_col]
                end_col_idx = column_mapping[end_col]
                start_row_idx = 8 - int(start_row)
                end_row_idx = 8 - int(end_row)

                # Check piece ownership and validity of move
                piece = self.board.get_piece(start_row_idx, start_col_idx)
                if piece and piece.color == WHITE:
                    valid_moves = self.board.get_valid_moves(piece)
                    if (end_row_idx, end_col_idx) in valid_moves:
                        # Make the move if it's valid
                        self.board.move(piece, end_row_idx, end_col_idx)
                        # Capture any pieces in the move
                        skipped = valid_moves[(end_row_idx, end_col_idx)]
                        if skipped:
                            self.board.remove(skipped)

                        # Redraw the board and mark success
                        print(f"AI successfully moved from {start} to {end}")
                        self.update()  # Redraw the board
                        success = True
                    else:
                        print(f"Illegal move from AI: Move to {end} is not valid for the piece at {start}. Retrying...")
                else:
                    print(f"Invalid move from AI: No piece found at {start} or wrong color. Retrying...")

            except Exception as e:
                print(f"Error processing AI move: {e}")

            # Switch turn to the player after a valid move
        self.change_turn()


if __name__ == "__main__":
    main()
