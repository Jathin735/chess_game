import random
import copy

def is_threatened(pos, user_king, user_boat, board):
    threatened = set()

    # Boat's range (straight lines)
    if user_boat:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = user_boat.row + dr, user_boat.col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    threatened.add((r, c))
                elif board[r][c].team != user_boat.team:
                    threatened.add((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    # King's 1-tile attack range
    if user_king:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = user_king.row + dr, user_king.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    threatened.add((r, c))

    return pos in threatened


def evaluate_position(ai_king_pos, user_king, user_boat, board):
    if is_threatened(ai_king_pos, user_king, user_boat, board):
        return -100  # Threatened = bad
    else:
        # Favor being farther from threats
        uk_dist = abs(ai_king_pos[0] - user_king.row) + abs(ai_king_pos[1] - user_king.col)
        ub_dist = abs(ai_king_pos[0] - user_boat.row) + abs(ai_king_pos[1] - user_boat.col)
        return uk_dist + ub_dist


def get_ai_move(ai_king, game_state):
    best_score = float("-inf")
    best_move = None

    for move in ai_king.valid_moves(game_state.board):
        # Simulate move
        new_board = copy.deepcopy(game_state.board)

        # Fake move the AI king
        new_ai_king = copy.deepcopy(ai_king)
        new_ai_king.row, new_ai_king.col = move
        new_board[ai_king.row][ai_king.col] = None
        new_board[move[0]][move[1]] = new_ai_king

        # Evaluate
        score = evaluate_position(move, game_state.user_king, game_state.user_boat, new_board)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move
