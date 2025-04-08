class Boat:
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col
        self.cost = 20

    def move(self, row, col):
        self.row = row
        self.col = col

    def valid_moves(self, board):
        moves = []

        # Straight line directions only: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].team != self.team:
                    moves.append((r, c))  # Can capture
                    break
                else:
                    break
                r += dr
                c += dc

        return moves
