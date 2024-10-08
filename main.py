import pygame
import os
from TicTacToeGUI import Game, AStar

# Game Settings
board_size = 3

# Colors
RED = (71, 166, 142)

class Main:
    def __init__(self):
        self.game = Game(background_color=RED, board_size=board_size)
        self.ai = AStar(self.game.board, board_size, "O")

    def run(self): 
        self.game.draw_grid(self.game.cell_size)
        self.game.display_text("Tic Tac Toe", self.game.screen_width // 2, 75, self.game.title_font)

        while self.game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.game.winner is None:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_cell = self.game.get_clicked_cell(mouse_pos)
                    if clicked_cell:
                        row, col = clicked_cell
                        if self.game.board[row][col] is None:
                            self.game.draw_move(row, col)
                            self.ai.board[row][col] = "X"
                            self.check_ai_move()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.restart_game()
                        self.ai = AStar(self.game.board, board_size, "O")
                    elif event.key == pygame.K_ESCAPE:
                        self.game.running = False

            pygame.display.update()

    def check_ai_move(self):
        if self.game.current_player == "O" and not self.game.winner:
            best_move = self.ai.find_best_move()
            if best_move:
                row, col = best_move
                if self.game.board[row][col] is None:
                    self.game.draw_move(row, col)
                    self.game.board[row][col] = "O"
                    self.ai.board[row][col] = "O"
                    if self.game.check_winner():
                        print(f"{self.game.winner} wins!")

if __name__ == "__main__":
    main = Main()
    main.run()
