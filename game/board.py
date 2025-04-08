import pygame
from config import SQUARE_SIZE, ROWS, COLS, WHITE, GRAY
from .game_state import GameState

# Load once
boat_img = pygame.image.load("assets/boat.png")
user_king_img = pygame.image.load("assets/king.png")
ai_king_img = pygame.image.load("assets/system_king.png")

# Scale to fit board squares
boat_img = pygame.transform.scale(boat_img, (SQUARE_SIZE, SQUARE_SIZE))
user_king_img = pygame.transform.scale(user_king_img, (SQUARE_SIZE, SQUARE_SIZE))
ai_king_img = pygame.transform.scale(ai_king_img, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(win, game_state: GameState):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            piece = game_state.get_piece(row, col)
            if piece:
                if piece.__class__.__name__ == "Boat":
                    win.blit(boat_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                elif piece.team == "user":
                    win.blit(user_king_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                else:
                    win.blit(ai_king_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))
