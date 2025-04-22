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

    def move_piece(self, piece, new_row, new_col, announce=True):
        old_row, old_col = piece.row, piece.col
        captured = self.board[new_row][new_col]

        # Clear old position
        self.board[old_row][old_col] = None

        # Check capture
        if captured and captured.team != piece.team:
            if isinstance(captured, King):
                if captured.team == "ai":
                    self.ai_king = None
                    if announce:
                        self.points += 100
                    self.running = False
                elif captured.team == "user":
                    self.user_king = None
                    if announce:
                        self.points -= 100
                    self.running = False

        # Move piece to new position
        self.board[new_row][new_col] = piece
        piece.move(new_row, new_col)

        # Deduct cost only for real moves
        if announce:
            self.points -= piece.cost

        # End game if points drop to 0 or below
        if self.points <= 0:
            self.running = False

        # Only switch turn for real moves
        if self.running and announce:
            self.switch_turn()
