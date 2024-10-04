import copy

class AStar:
    def __init__(self, board, player):
        self.board = copy.deepcopy(board)
        self.player = player
        self.opponent = "O" if player == "X" else "X"
    
    def heuristic(self, board):
        score = 0
        for row in board:
            if row.count(self.player) > 0 and row.count(self.opponent) == 0:
                score += 1
        for col in range(len(board)):
            column = [board[row][col] for row in range(len(board))]
            if column.count(self.player) > 0 and column.count(self.opponent) == 0:
                score += 1
        diag1 = [board[i][i] for i in range(len(board))]
        diag2 = [board[i][len(board)-i-1] for i in range(len(board))]
        if diag1.count(self.player) > 0 and diag1.count(self.opponent) == 0:
            score += 1
        if diag2.count(self.player) > 0 and diag2.count(self.opponent) == 0:
            score += 1
        return score
    
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
            new_board = copy.deepcopy(self.board)
            new_board[row][col] = self.player
            g = 1
            h = self.heuristic(new_board)  

            f = g + h 

            if f > best_score:
                best_score = f
                best_move = move

        return best_move
