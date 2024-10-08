import pygame
import os
import sys
import copy

#Game Settings
board_size = 5

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (225, 225, 225)
RED = (200, 84, 75)

class Game:
    #Initiate the game
    def __init__(self, background_color, board_size):
        pygame.init()
        info = pygame.display.Info()

        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.board_size = board_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
        self.color = background_color

        self.cell_size = self.screen_height // (2 * self.board_size)
        self.image_size_offset = self.cell_size * 0.25

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.x_img = pygame.image.load(os.path.join(script_dir, 'X.png'))
        self.o_img = pygame.image.load(os.path.join(script_dir, 'O.png'))
        image_size = self.cell_size - self.image_size_offset
        self.x_img = pygame.transform.scale(self.x_img, (image_size, image_size))
        self.o_img = pygame.transform.scale(self.o_img, (image_size, image_size))

        self.current_player = "X"
        self.winner = None
        self.board = [[None for i in range(self.board_size)] for i in range(self.board_size)]

        self.title_font = pygame.font.Font(None, 74)
        self.subtitle_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 35)
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(self.color)

        pygame.display.flip()
        self.running = True

    def draw_grid(self, cell_size):
        for i in range(1, self.board_size):
            #Vertical
            x_pos_start = (self.screen_width / 2) - (cell_size * (self.board_size / 2)) + (cell_size * i)
            x_pos_end = (self.screen_height / 2) - (cell_size * (self.board_size / 2))
            pygame.draw.line(
                self.screen,
                DARK_GREY,
                (x_pos_start, x_pos_end),
                (x_pos_start, x_pos_end + (cell_size * self.board_size)),
                3
            )
            pygame.draw.circle(self.screen, DARK_GREY, (x_pos_start, x_pos_end), 5)
            pygame.draw.circle(self.screen, DARK_GREY, (x_pos_start, x_pos_end + (cell_size * self.board_size)), 5)

            #Horizontal
            y_pos_start = (self.screen_height / 2) - (cell_size * (self.board_size / 2)) + (cell_size * i)
            y_pos_end = (self.screen_width / 2) - (cell_size * (self.board_size / 2))
            pygame.draw.line(
                self.screen,
                DARK_GREY,
                (y_pos_end, y_pos_start),
                (y_pos_end + (cell_size * self.board_size), y_pos_start),
                3
            )
            pygame.draw.circle(self.screen, DARK_GREY, (y_pos_end, y_pos_start), 5)
            pygame.draw.circle(self.screen, DARK_GREY, (y_pos_end + (cell_size * self.board_size), y_pos_start), 5)

        pygame.display.flip()

    def get_clicked_cell(self, mouse_pos):
        x_pos_start = (self.screen_width / 2) - (self.cell_size * (self.board_size / 2))
        x_pos_end = x_pos_start + self.cell_size * self.board_size
        y_pos_start = (self.screen_height / 2) - (self.cell_size * (self.board_size / 2))
        y_pos_end = y_pos_start + self.cell_size * self.board_size

        if(x_pos_start <= mouse_pos[0] <= x_pos_end and
           y_pos_start <= mouse_pos[1] <= y_pos_end):
            col = int((mouse_pos[0] - x_pos_start) // self.cell_size)
            row = int((mouse_pos[1] - y_pos_start) // self.cell_size)

            print(f"Clicked position: {mouse_pos}, Row: {row}, Col: {col}")

            if 0 <= row < self.board_size and 0 <= col < self.board_size:
                return (row, col)
        else:
            return None
        
    def draw_move(self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            print(f"Invalid move: Row {row}, Col {col} out of bounds.")
            return

        x_pos_start = (self.screen_width / 2) - (self.cell_size * (self.board_size / 2))
        y_pos_start = (self.screen_height / 2) - (self.cell_size * (self.board_size / 2))

        x = x_pos_start + col * self.cell_size
        y = y_pos_start + row *self. cell_size

        if self.current_player == "X":
            self.screen.blit(self.x_img, (x + self.image_size_offset / 2, y + self.image_size_offset / 2))
            self.board[row][col] = "X"
        else:
            self.screen.blit(self.o_img, (x + self.image_size_offset / 2, y + self.image_size_offset / 2))
            self.board[row][col] = "O"
        
        self.winner = self.check_winner()

        if self.winner:
            if self.winner == "Draw":
                self.display_text("It's a Draw!", self.screen_width // 2, 150, self.subtitle_font)
            else:
                self.display_text(f"{self.winner} Wins!", self.screen_width // 2, 150, self.subtitle_font)
            self.display_text("Press R to Start Again!", self.screen_width // 2, self.screen_height - 50, self.font)
        self.current_player = "O" if self.current_player == "X" else "X"

        pygame.display.flip()
    
    def display_text(self, text, x, y, font):
        text_surface = font.render(text, True, DARK_GREY)
        text_rect = text_surface.get_rect(center=(x, y))

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
    
    def check_winner(self):
        for row in self.board:
            if all(cell == 'X' for cell in row):
                return 'X'
            if all(cell == 'O' for cell in row):
                return 'O'

        for col in range(self.board_size):
            if all(self.board[row][col] == 'X' for row in range(self.board_size)):
                return 'X'
            if all(self.board[row][col] == 'O' for row in range(self.board_size)):
                return 'O'

        if all(self.board[i][i] == 'X' for i in range(self.board_size)):
            return 'X'
        if all(self.board[i][i] == 'O' for i in range(self.board_size)):
            return 'O'
        if all(self.board[i][self.board_size - 1 - i] == 'X' for i in range(self.board_size)):
            return 'X'
        if all(self.board[i][self.board_size - 1 - i] == 'O' for i in range(self.board_size)):
            return 'O'

        if all(cell is not None for row in self.board for cell in row):
            return 'Draw'
        return None
    
    def restart_game(self):
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "X"
        self.winner = None
        self.screen.fill(self.color) 
        self.display_text("Tic Tac Toe", self.screen_width // 2, 75, self.title_font)
        self.draw_grid(self.cell_size)
        pygame.display.flip()

class AStar:
    def __init__(self, board, board_size, ai):
        self.board = copy.deepcopy(board)
        self.ai = ai
        self.player = "O" if ai == "X" else "X"
        self.board_size = board_size

    def heuristic(self, board, row, col):
        board[row][col] = self.ai
        if self.is_winner(board, self.ai):
            board[row][col] = None
            return 100
        
        board[row][col] = self.player
        if self.is_winner(board, self.player):
            board[row][col] = None
            return 90

        board[row][col] = None

        if (row, col) == (self.board_size // 2, self.board_size // 2):
            return 50

        corners = [(0, 0), (0, self.board_size - 1), (self.board_size - 1, 0), (self.board_size - 1, self.board_size - 1)]
        if (row, col) in corners:
            return 40

        return 30

    def is_winner(self, board, player):
        for row in board:
            if all(cell == player for cell in row):
                return True

        for col in range(len(board)):
            if all(board[row][col] == player for row in range(len(board))):
                return True

        if all(board[i][i] == player for i in range(len(board))):
            return True
        if all(board[i][len(board) - 1 - i] == player for i in range(len(board))):
            return True

        return False

    def get_possible_moves(self, board):
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] is None:
                    moves.append((row, col))
        return moves

    def find_best_move(self):
        best_move = None
        best_score = -float('inf')

        for move in self.get_possible_moves(self.board):
            row, col = move

            h = self.heuristic(self.board, row, col)

            if h > best_score:
                best_score = h
                best_move = move

            if best_score == 100:
                break

        return best_move
