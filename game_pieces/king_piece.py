class King:
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col
        self.cost = 10

    def move(self, row, col):
        self.row = row
        self.col = col

    def valid_moves(self, board):
        moves = []
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].team != self.team:
                    moves.append((r, c))
        return moves
