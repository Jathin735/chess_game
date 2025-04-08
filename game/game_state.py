from game_pieces.king_piece import King
from game_pieces.boat_piece import Boat

class GameState:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.user_king = King("user", 7, 4)    # bottom center
        self.user_boat = Boat("user", 7, 0)    # bottom-left
        self.ai_king = King("ai", 0, 4)        # top center

        self.board[7][4] = self.user_king
        self.board[7][0] = self.user_boat
        self.board[0][4] = self.ai_king

        self.turn = "user"
        self.points = 1000
        self.running = True

    def switch_turn(self):
        self.turn = "ai" if self.turn == "user" else "user"

    def get_piece(self, row, col):
        return self.board[row][col]

    def move_piece(self, piece, new_row, new_col):
        old_row, old_col = piece.row, piece.col

        # Check for capturing
        target = self.board[new_row][new_col]
        if target:
            if target.team != piece.team:
                if isinstance(target, King) and target.team == "ai":
                    self.points += 100
                    self.board[new_row][new_col] = None
                    print("🎯 System King captured!")
                elif isinstance(target, King) and target.team == "user":
                    self.points -= 100
                    print("💀 User King lost!")

        # Move the piece
        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.move(new_row, new_col)

        # Deduct points
        self.points -= piece.cost

        # Check for end condition
        if self.points <= 0:
            self.running = False

        self.switch_turn()
