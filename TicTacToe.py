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
<<<<<<< HEAD
    def make_move(self,row,col):
        index = row * self.size + col
        if self.board[index] is None:
            self.board[index] = self.currentPlayer
            if self.currentPlayer == 'X':
                self.currentPlayer = '0'
            else:
                self.currentPlayer = 'X'    
        else: print("Invalid cell")
game = TicTacToe(3)
game.print_board()


=======

    def make_move(self, row, col):
        index = row * self.size + col
>>>>>>> 2eabd5e4ba159efeb3d00522d61c792e137e3686
