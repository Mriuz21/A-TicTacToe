import pygame
import os
import sys

#Game Settings
board_size = 3

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (225, 225, 225)
RED = (200, 84, 75)

class Game:
    #Initiate the game
    def __init__(self, screen_width, screen_height, background_color):
        pygame.init()
        info = pygame.display.Info()

        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
        self.color = background_color

        self.cell_size = self.screen_height // (2 * board_size)
        self.image_size_offset = self.cell_size * 0.25

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.x_img = pygame.image.load(os.path.join(script_dir, 'X.png'))
        self.o_img = pygame.image.load(os.path.join(script_dir, 'O.png'))
        image_size = self.cell_size - self.image_size_offset
        self.x_img = pygame.transform.scale(self.x_img, (image_size, image_size))
        self.o_img = pygame.transform.scale(self.o_img, (image_size, image_size))

        self.current_player = "X"
        self.winner = None
        self.board = [[None for i in range(board_size)] for i in range(board_size)]

        self.title_font = pygame.font.Font(None, 74)
        self.subtitle_font = pygame.font.Font(None, 50)
        self.font = pygame.font.Font(None, 35)
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(self.color)

        pygame.display.flip()
        self.running = True

    def draw_grid(self, board_size, cell_size):
        for i in range(1, board_size):
            #Vertical
            x_pos_start = (self.screen_width / 2) - (cell_size * (board_size / 2)) + (cell_size * i)
            x_pos_end = (self.screen_height / 2) - (cell_size * (board_size / 2))
            pygame.draw.line(
                self.screen,
                DARK_GREY,
                (x_pos_start, x_pos_end),
                (x_pos_start, x_pos_end + (cell_size * board_size)),
                3
            )
            pygame.draw.circle(self.screen, DARK_GREY, (x_pos_start, x_pos_end), 5)
            pygame.draw.circle(self.screen, DARK_GREY, (x_pos_start, x_pos_end + (cell_size * board_size)), 5)

            #Horizontal
            y_pos_start = (self.screen_height / 2) - (cell_size * (board_size / 2)) + (cell_size * i)
            y_pos_end = (self.screen_width / 2) - (cell_size * (board_size / 2))
            pygame.draw.line(
                self.screen,
                DARK_GREY,
                (y_pos_end, y_pos_start),
                (y_pos_end + (cell_size * board_size), y_pos_start),
                3
            )
            pygame.draw.circle(self.screen, DARK_GREY, (y_pos_end, y_pos_start), 5)
            pygame.draw.circle(self.screen, DARK_GREY, (y_pos_end + (cell_size * board_size), y_pos_start), 5)

        pygame.display.flip()

    def get_clicked_cell(self, mouse_pos):
        x_pos_start = (self.screen_width / 2) - (self.cell_size * (board_size / 2))
        x_pos_end = x_pos_start + self.cell_size * board_size
        y_pos_start = (self.screen_height / 2) - (self.cell_size * (board_size / 2))
        y_pos_end = y_pos_start + self.cell_size * board_size

        if(x_pos_start <= mouse_pos[0] <= x_pos_end and
           y_pos_start <= mouse_pos[1] <= y_pos_end):
            #Get col and row for cell
            col = int((mouse_pos[0] - x_pos_start) // self.cell_size)
            row = int((mouse_pos[1] - y_pos_start) // self.cell_size)

            print(f"Clicked position: {mouse_pos}, Row: {row}, Col: {col}")

            if 0 <= row < board_size and 0 <= col < board_size:
                return (row, col)
        else:
            return None
        
    def draw_move(self, row, col):
        if row < 0 or row >= board_size or col < 0 or col >= board_size:
            print(f"Invalid move: Row {row}, Col {col} out of bounds.")
            return

        x_pos_start = (self.screen_width / 2) - (self.cell_size * (board_size / 2))
        y_pos_start = (self.screen_height / 2) - (self.cell_size * (board_size / 2))

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
        #Rows
        for row in self.board:
            if all(cell == 'X' for cell in row):
                return 'X'
            if all(cell == 'O' for cell in row):
                return 'O'

        #Columns
        for col in range(board_size):
            if all(self.board[row][col] == 'X' for row in range(board_size)):
                return 'X'
            if all(self.board[row][col] == 'O' for row in range(board_size)):
                return 'O'

        #Diagonals
        if all(self.board[i][i] == 'X' for i in range(board_size)):
            return 'X'
        if all(self.board[i][i] == 'O' for i in range(board_size)):
            return 'O'
        if all(self.board[i][board_size - 1 - i] == 'X' for i in range(board_size)):
            return 'X'
        if all(self.board[i][board_size - 1 - i] == 'O' for i in range(board_size)):
            return 'O'

        #Draw if all cells are occupied
        if all(cell is not None for row in self.board for cell in row):
            return 'Draw'
        return None
    
    def restart_game(self):
        # Reset the board
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "X"
        self.winner = None
        self.screen.fill(self.color) 
        self.display_text("Tic Tac Toe", self.screen_width // 2, 75, self.title_font)
        self.draw_grid(board_size, self.cell_size)
        pygame.display.flip()

def main():
    game = Game(0, 0, background_color=RED)
    
    game.draw_grid(board_size, game.cell_size)
    game.display_text("Tic Tac Toe", game.screen_width // 2, 75, game.title_font)
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game.winner == None:
                mouse_pos = pygame.mouse.get_pos()
                clicked_cell = game.get_clicked_cell(mouse_pos)
                if clicked_cell:
                    row, col = clicked_cell
                    if game.board[row][col] == None:
                        game.draw_move(row, col) 
                    print(f"Cell clicked: {clicked_cell}")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    game.running = False
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()