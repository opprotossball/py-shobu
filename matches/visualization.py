import pygame
import sys
from game.shobu import *
import threading
import time

class Visualization:
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

    def start(self):
        thread = threading.Thread(target=self.__start)
        thread.start()
        # give it time to init lol
        time.sleep(0.5)

    def __start(self):
        # Initialize Pygame
        pygame.init()
        # Screen dimensions
        self.SCREEN_WIDTH = (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE * 2 + self.BOARD_MARGIN * 3
        self.SCREEN_HEIGHT = (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE * 2 + self.BOARD_MARGIN * 3
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("SHOBU")
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()

    def draw_board(self, board_str, x_offset, y_offset, board_color):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                pygame.draw.rect(
                    self.screen,
                    board_color,
                    [
                        (self.MARGIN + self.TILE_SIZE) * j + self.MARGIN + x_offset,
                        (self.MARGIN + self.TILE_SIZE) * i + self.MARGIN + y_offset,
                        self.TILE_SIZE,
                        self.TILE_SIZE
                    ]
                )
                tile_value = board_str[i * self.BOARD_SIZE + j]
                if tile_value != '_':
                    color = self.WHITE if tile_value == 'w' else self.BLACK
                    # Draw stone with border
                    pygame.draw.circle(
                        self.screen,
                        self.STONE_BORDER,
                        [
                            (self.MARGIN + self.TILE_SIZE) * j + self.MARGIN + x_offset + self.TILE_SIZE // 2,
                            (self.MARGIN + self.TILE_SIZE) * i + self.MARGIN + y_offset + self.TILE_SIZE // 2
                        ],
                        self.TILE_SIZE // 2 - self.MARGIN + 2  # Outer border
                    )
                    pygame.draw.circle(
                        self.screen,
                        color,
                        [
                            (self.MARGIN + self.TILE_SIZE) * j + self.MARGIN + x_offset + self.TILE_SIZE // 2,
                            (self.MARGIN + self.TILE_SIZE) * i + self.MARGIN + y_offset + self.TILE_SIZE // 2
                        ],
                        self.TILE_SIZE // 2 - self.MARGIN  # Inner stone
                    )

    def parse_boards_from_string(self, boards_str):
        boards = boards_str[2:].split()
        return boards

    def display_game(self, boards_str):
        boards = self.parse_boards_from_string(boards_str)
        clock = pygame.time.Clock()
        self.screen.fill(self.BACKGROUND_COLOR)
        # Draw four boards in a 2x2 layout with different colors
        self.draw_board(boards[2], self.BOARD_MARGIN, self.BOARD_MARGIN, self.BLACK_BOARD)
        self.draw_board(boards[3], (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.BOARD_MARGIN, self.WHITE_BOARD)
        self.draw_board(boards[0], self.BOARD_MARGIN, (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.BLACK_BOARD)
        self.draw_board(boards[1], (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.WHITE_BOARD)
        pygame.display.flip()
        clock.tick(60)
