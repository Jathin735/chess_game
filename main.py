import pygame
from config import WIDTH, HEIGHT, SQUARE_SIZE, FPS, GREEN, WHITE, GRAY
from game.board import draw_board
from game.game_state import GameState
from ai.search import get_ai_move

AI_MOVE_EVENT = pygame.USEREVENT + 1  # Custom event ID for AI delay

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def highlight_moves(win, moves):
    for row, col in moves:
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(win, GREEN, rect, 3)

def highlight_threat_zones(win, danger_squares):
    RED = (255, 0, 0)
    for row, col in danger_squares:
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(win, RED, rect, 2)

def get_threatened_squares(game_state):
    threatened = set()
    user_king = game_state.user_king
    user_boat = game_state.user_boat
    board = game_state.board

    if user_boat:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
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
                r = user_king.row + dr
                c = user_king.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    threatened.add((r, c))

    return threatened

def draw_game_over(win, points, winner=None):
    font = pygame.font.SysFont('arial', 50)
    small_font = pygame.font.SysFont('arial', 30)

    text = font.render("Game Over", True, (255, 0, 0))
    score_text = small_font.render(f"Final Points: {points}", True, (0, 0, 0))

    if winner == "user":
        winner_text = small_font.render("You Win!", True, (0, 100, 0))
    elif winner == "ai":
        winner_text = small_font.render("AI Wins!", True, (200, 0, 0))
    else:
        winner_text = small_font.render("Draw!", True, (100, 100, 100))

    restart_text = small_font.render("Press R to Restart", True, (0, 0, 0))

    win.fill(WHITE)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, 180))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 240))
    win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, 280))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 340))
    pygame.display.update()

def game_loop(win):
    clock = pygame.time.Clock()
    game_state = GameState()

    selected_piece = None
    valid_moves = []
    ai_delay_started = False
    ai_timer_start_time = 0  # Tracks AI delay start

    font = pygame.font.SysFont('arial', 24)

    while game_state.running:
        clock.tick(FPS)
        draw_board(win, game_state)

        if selected_piece:
            highlight_moves(win, valid_moves)

        danger_zones = get_threatened_squares(game_state)
        highlight_threat_zones(win, danger_zones)

        if game_state.turn == "ai" and ai_delay_started:
            thinking_text = font.render("AI is thinking...", True, (0, 0, 0))
            win.blit(thinking_text, (WIDTH // 2 - thinking_text.get_width() // 2, HEIGHT - 40))

            pygame.draw.rect(win, (180, 180, 180), (WIDTH // 2 - 100, HEIGHT - 20, 200, 10), 0)

            elapsed = pygame.time.get_ticks() - ai_timer_start_time
            progress = min(1.0, elapsed / 3000.0)
            pygame.draw.rect(win, (0, 120, 0), (WIDTH // 2 - 100, HEIGHT - 20, int(200 * progress), 10), 0)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and game_state.turn == "user":
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                if selected_piece:
                    if (row, col) in valid_moves:
                        game_state.move_piece(selected_piece, row, col)
                        selected_piece = None
                        valid_moves = []
                        ai_delay_started = False
                    else:
                        selected_piece = None
                        valid_moves = []
                else:
                    piece = game_state.get_piece(row, col)
                    if piece and piece.team == "user":
                        selected_piece = piece
                        valid_moves = piece.valid_moves(game_state.board)
                    else:
                        selected_piece = None
                        valid_moves = []

            if event.type == AI_MOVE_EVENT and game_state.turn == "ai":
                ai_king = game_state.ai_king
                move = get_ai_move(ai_king, game_state)
                if move:
                    game_state.move_piece(ai_king, *move)
                pygame.time.set_timer(AI_MOVE_EVENT, 0)
                ai_delay_started = False

        if game_state.turn == "ai" and not ai_delay_started:
            pygame.time.set_timer(AI_MOVE_EVENT, 3000)
            ai_timer_start_time = pygame.time.get_ticks()
            ai_delay_started = True

        if game_state.points <= 0 or game_state.ai_king is None or game_state.user_king is None:
            game_state.running = False

    winner = None
    if game_state.user_king is None:
        winner = "ai"
    elif game_state.ai_king is None:
        winner = "user"

    draw_game_over(win, game_state.points, winner)
    return True

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Custom Chess Game")

    run = True
    while run:
        game_over = game_loop(win)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False

    pygame.quit()

if __name__ == "__main__":
    main()
