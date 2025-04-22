import copy

def is_threatened(pos, user_king, user_boat, board):
    threatened = set()

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

    if user_king:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = user_king.row + dr, user_king.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    threatened.add((r, c))

    return pos in threatened


def evaluate_state(game_state):
    if not game_state.ai_king:
        return -1000  # Losing is very bad
    if not game_state.user_king:
        return 1000  # Winning is very good

    ai_pos = (game_state.ai_king.row, game_state.ai_king.col)
    threatened = is_threatened(ai_pos, game_state.user_king, game_state.user_boat, game_state.board)
    
    score = 0
    if threatened:
        score -= 100

    if game_state.user_king:
        uk_dist = abs(game_state.ai_king.row - game_state.user_king.row) + abs(game_state.ai_king.col - game_state.user_king.col)
        score -= uk_dist * 2  # prefer closer to attack

    if game_state.user_boat:
        ub_dist = abs(game_state.ai_king.row - game_state.user_boat.row) + abs(game_state.ai_king.col - game_state.user_boat.col)
        score += ub_dist  # prefer farther from boat

    return score


def minimax(game_state, depth, maximizing_player):
    if depth == 0 or not game_state.running:
        return evaluate_state(game_state), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in game_state.ai_king.valid_moves(game_state.board):
            new_state = copy.deepcopy(game_state)
            ai_piece = new_state.ai_king
            new_state.move_piece(ai_piece, move[0], move[1])
            eval_score, _ = minimax(new_state, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None
        user_king = game_state.user_king
        user_boat = game_state.user_boat
        user_pieces = [p for p in [user_king, user_boat] if p]

        for piece in user_pieces:
            for move in piece.valid_moves(game_state.board):
                new_state = copy.deepcopy(game_state)
                new_piece = new_state.get_piece(piece.row, piece.col)
                if new_piece:
                    new_state.move_piece(new_piece, move[0], move[1])
                    eval_score, _ = minimax(new_state, depth - 1, True)
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move
        return min_eval, best_move


def get_ai_move(ai_king, game_state):
    _, best_move = minimax(game_state, depth=2, maximizing_player=True)
    return best_move
