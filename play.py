import pygame
import sys
from shobu import *
import threading

# Constants
BOARD_SIZE = 4
TILE_SIZE = 50
MARGIN = 5
BOARD_MARGIN = 20
WHITE = (248, 248, 248)
BLACK = (84, 81, 80)
STONE_BORDER = (0, 0, 0)  # Border color for stones
BLACK_BOARD = (181, 136, 99)
WHITE_BOARD = (240, 217, 181)
BACKGROUND_COLOR = (40, 40, 40)  # Background color for the game

# Initialize Pygame
pygame.init()

# Screen dimensions 
SCREEN_WIDTH = (TILE_SIZE + MARGIN) * BOARD_SIZE * 2 + BOARD_MARGIN * 3
SCREEN_HEIGHT = (TILE_SIZE + MARGIN) * BOARD_SIZE * 2 + BOARD_MARGIN * 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SHOBU")

def draw_board(board_str, x_offset, y_offset, board_color):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.rect(
                screen,
                board_color,
                [
                    (MARGIN + TILE_SIZE) * j + MARGIN + x_offset,
                    (MARGIN + TILE_SIZE) * i + MARGIN + y_offset,
                    TILE_SIZE,
                    TILE_SIZE
                ]
            )
            tile_value = board_str[i * BOARD_SIZE + j]
            if tile_value != '_':
                color = WHITE if tile_value == 'w' else BLACK
                # Draw stone with border
                pygame.draw.circle(
                    screen,
                    STONE_BORDER,
                    [
                        (MARGIN + TILE_SIZE) * j + MARGIN + x_offset + TILE_SIZE // 2,
                        (MARGIN + TILE_SIZE) * i + MARGIN + y_offset + TILE_SIZE // 2
                    ],
                    TILE_SIZE // 2 - MARGIN + 2  # Outer border
                )
                pygame.draw.circle(
                    screen,
                    color,
                    [
                        (MARGIN + TILE_SIZE) * j + MARGIN + x_offset + TILE_SIZE // 2,
                        (MARGIN + TILE_SIZE) * i + MARGIN + y_offset + TILE_SIZE // 2
                    ],
                    TILE_SIZE // 2 - MARGIN  # Inner stone
                )

def parse_boards_from_string(boards_str):
    boards = boards_str[2:].split()
    return boards

def display_game(boards_str):
    boards = parse_boards_from_string(boards_str)
    clock = pygame.time.Clock()
    screen.fill(BACKGROUND_COLOR)
    # Draw four boards in a 2x2 layout with different colors
    draw_board(boards[0], BOARD_MARGIN, BOARD_MARGIN, BLACK_BOARD)
    draw_board(boards[1], (TILE_SIZE + MARGIN) * BOARD_SIZE + BOARD_MARGIN * 2, BOARD_MARGIN, WHITE_BOARD)
    draw_board(boards[2], BOARD_MARGIN, (TILE_SIZE + MARGIN) * BOARD_SIZE + BOARD_MARGIN * 2, WHITE_BOARD)
    draw_board(boards[3], (TILE_SIZE + MARGIN) * BOARD_SIZE + BOARD_MARGIN * 2, (TILE_SIZE + MARGIN) * BOARD_SIZE + BOARD_MARGIN * 2, BLACK_BOARD)
    pygame.display.flip()
    clock.tick(60)

def play_game_thread():
    gm = GameMaster(30, True, display_game)
    gm.play_game()

play_game_thread = threading.Thread(target=play_game_thread)
play_game_thread.start()

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

play_game_thread.join()
pygame.quit()
sys.exit()