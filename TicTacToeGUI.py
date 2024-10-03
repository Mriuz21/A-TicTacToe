import pygame

class Game:
    def __init__(self, screen_width, screen_height, background_color):
        (self.screen_width, self.screen_height) = (screen_width, screen_height)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.color = background_color
        
        pygame.display.set_caption('Tic Tac Toe')
        self.screen.fill(self.color)

        pygame.display.flip()
        self.running = True

    def draw_grid(self, board_size):
        for x in range(board_size):
            for y in range(board_size):
                rect = pygame.Rect(x, y, 20, 20)
                pygame.draw.rect(self.screen, (255,255,255), rect, 1)

def main():
    screen_width = 800
    screen_height = 450
    RED = (200, 84, 75)
    game = Game(screen_width, screen_height, background_color=RED)

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        pygame.display.update()
if __name__ == "__main__":
    main()