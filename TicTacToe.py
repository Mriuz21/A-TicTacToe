class TicTacToe :
    def __init__(self,size):
        #This constructor is used to initialize a size*size board
        self.size = size
        self.board = [None] *(size*size)
        self.currentPlayer = 'X'
    def print_board(self):
        for i in range(self.size):
            rows = []
            for j in range(self.size):
                index = i*self.size+j
                if self.board[index] is not None:
                    rows.append(self.board[index])
                else:
                    rows.append(" ")
            print("|".join(rows))
            if i < self.size -1:
                print("-" * (self.size * 2 - 1))  # Print a separator line


game = TicTacToe(5)
game.print_board()
