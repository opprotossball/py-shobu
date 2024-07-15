import pygame
import sys
import threading
import time
from game.shobu import Shobu, Move
import os

class VisualPlayer:
    BOARD_SIZE = 4
    TILE_SIZE = int(100 * 0.75)  
    MARGIN = int(10 * 0.75)      
    BOARD_MARGIN = int(40 * 0.75)  
    WHITE = (248, 248, 248)
    BLACK = (84, 81, 80)
    STONE_BORDER = (0, 0, 0)  # Border color for stones
    BLACK_BOARD = (181, 136, 99)
    WHITE_BOARD = (240, 217, 181)
    BACKGROUND_COLOR = (40, 40, 40)  # Background color for the game
    SELECTED_PASSIVE_COLOR = (0, 255, 0)  
    SELECTED_AGGRESSIVE_COLOR = (255, 0, 0) 
    SELECTED_TARGET_COLOR = (0, 0, 255)

    def __init__(self):
        self.selected_passive = (None, None)
        self.selected_aggressive = (None, None)
        self.direction = None
        self.move = None
        self.move_chosen_event = threading.Event()
        self.boards_str = "b ________________ ________________ ________________ ________________"

    def start(self):
        thread = threading.Thread(target=self.__start, daemon=True)
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.check_click(x, y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.try_make_move()
            self.display_game(self.boards_str)  # Redraw the game state after handling events
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        os._exit(0)

    def piece_on_tile(self, board_str, board_id, tile):
        id = 2 + 17 * board_id + tile
        match board_str[id]:
            case '_':
                return Shobu.EMPTY_TILE
            case 'b':
                return Shobu.BLACK_PIECE
            case 'w':
                return Shobu.WHITE_PIECE
            
    def try_make_move(self):
        if self.selected_passive == (None, None) or self.selected_aggressive == (None, None) or self.direction == None:
            self.reset_selection()
            self.eprint('Move not selected!')
            return
        white_passive = self.selected_passive[0] % 2 == 1
        home_aggressive = self.selected_passive[0] + self.selected_aggressive[0] != 3
        passive_from = Shobu.readable_2_internal(self.selected_passive[1])
        aggressive_from = Shobu.readable_2_internal(self.selected_aggressive[1])
        if self.direction in Shobu.DIRECTIONS.values():
            is_double = False
            direction = self.direction
        else:
            is_double = True
            direction = self.direction // 2
        game = Shobu.from_string(self.boards_str)
        move = Move(white_passive, home_aggressive, passive_from, aggressive_from, is_double, direction)
        try:
            game.make_move(move)
            print(move.to_string())
            self.move_chosen_event.set()
            self.move = move
        except:
            self.reset_selection()
            self.eprint('Move cannot be played!')
            return

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def draw_board(self, board_str, x_offset, y_offset, board_color):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                tile_color = board_color
                board_id, tile_id = self.get_tile_and_board_id(x_offset, y_offset, i, j)
                if (board_id, tile_id) == self.selected_passive:
                    tile_color = self.SELECTED_PASSIVE_COLOR
                elif (board_id, tile_id) == self.selected_aggressive:
                    tile_color = self.SELECTED_AGGRESSIVE_COLOR
                pygame.draw.rect(
                    self.screen,
                    tile_color,
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
        self.boards_str = boards_str
        boards = self.parse_boards_from_string(boards_str)
        clock = pygame.time.Clock()
        self.screen.fill(self.BACKGROUND_COLOR)
        # Draw four boards in a 2x2 layout with different colors
        for i in range(4):
            self.draw_board(boards[i], *self.board(i))
        self.validate_direction()
        self.draw_borders()
        pygame.display.flip()
        clock.tick(60)

    def board(self, i):
        return [
            (self.BOARD_MARGIN, (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.BLACK_BOARD),
            ((self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.WHITE_BOARD),
            (self.BOARD_MARGIN, self.BOARD_MARGIN, self.BLACK_BOARD),
            ((self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE + self.BOARD_MARGIN * 2, self.BOARD_MARGIN, self.WHITE_BOARD)
        ][i]

    def boards_iterator(self):
        for i in range(4):
            yield self.board(i)

    def validate_direction(self):
        if self.direction == None:
            return
        if self.selected_passive == (None, None) and self.selected_aggressive == (None, None):
            self.direction = None
            return
        if self.selected_passive != (None, None):
            selected = Shobu.readable_2_internal(self.selected_passive[1]) + self.direction
            if not Shobu.valid_tile(selected):
                self.direction = None
                return
        if self.selected_aggressive != (None, None):
            selected = Shobu.readable_2_internal(self.selected_aggressive[1]) + self.direction
            if not Shobu.valid_tile(selected):
                self.direction = None
                return

    def draw_borders(self):
        if self.direction == None:
            return
        if self.selected_passive != (None, None):
            selected = Shobu.readable_2_internal(self.selected_passive[1]) + self.direction
            if not Shobu.valid_tile(selected):
                return
            self.draw_border((self.selected_passive[0], Shobu.internal_2_readable(selected)), True)
        if self.selected_aggressive != (None, None):
            selected = Shobu.readable_2_internal(self.selected_aggressive[1]) + self.direction
            if not Shobu.valid_tile(selected):
                return
            self.draw_border((self.selected_aggressive[0], Shobu.internal_2_readable(selected)), False)

    def draw_border(self, tile, is_passive):
        board_id, tile_id = tile
        x, y = self.get_tile_center(board_id, tile_id)
        color = self.SELECTED_PASSIVE_COLOR if is_passive else self.SELECTED_AGGRESSIVE_COLOR
        pygame.draw.rect(
            self.screen,
            color,
            [
                x - self.TILE_SIZE // 2,
                y - self.TILE_SIZE // 2,
                self.TILE_SIZE,
                self.TILE_SIZE
            ],
            5  # Border thickness
        )

    def check_click(self, x, y):
        for board_id, (x_offset, y_offset, _) in enumerate(self.boards_iterator()):
            if x_offset <= x < x_offset + (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE and y_offset <= y < y_offset + (self.TILE_SIZE + self.MARGIN) * self.BOARD_SIZE:
                col = (x - x_offset) // (self.TILE_SIZE + self.MARGIN)
                row = (y - y_offset) // (self.TILE_SIZE + self.MARGIN)
                tile_id = row * self.BOARD_SIZE + col
                if board_id == self.selected_passive[0]:
                    if tile_id == self.selected_passive[1]:
                        self.selected_passive = (None, None)
                    else:
                        self.update_direction(board_id, self.selected_passive[1], tile_id)
                elif board_id == self.selected_aggressive[0]:
                    if tile_id == self.selected_aggressive[1]:
                        self.selected_aggressive = (None, None)
                    else:
                        self.update_direction(board_id, self.selected_aggressive[1], tile_id)
                elif self.selected_passive == (None, None) and self.valid_move(board_id, tile_id, True):
                    self.selected_passive = (board_id, tile_id)
                elif self.selected_aggressive == (None, None) and self.valid_move(board_id, tile_id, False):
                    self.selected_aggressive = (board_id, tile_id)
                else:
                    self.reset_selection()
                break
    
    def valid_move(self, board_id, tile_id, is_passive):
        if self.piece_on_tile(self.boards_str, board_id, tile_id) != self.active_player():
            return False
        if is_passive:
            if self.active_player() == Shobu.BLACK_PIECE and board_id > 1:
                return False
            if self.active_player() == Shobu.WHITE_PIECE and board_id < 2:
                return False
            if self.selected_aggressive != (None, None):
                if (board_id + self.selected_aggressive[0]) % 2 == 0:
                    return False
        else:
            if self.selected_passive != (None, None):
                if (board_id + self.selected_passive[0]) % 2 == 0:
                    return False
        return True

    def active_player(self):
        match self.boards_str[0]:
            case 'b':
                return Shobu.BLACK_PIECE
            case 'w':
                return Shobu.WHITE_PIECE

    def update_direction(self, board_id, origin, target):
        diff = Shobu.readable_2_internal(target) - Shobu.readable_2_internal(origin) 
        if self.piece_on_tile(self.boards_str, board_id, target) != self.active_player() and diff in Shobu.DIRECTIONS.values() or (diff % 2 == 0 and diff // 2 in Shobu.DIRECTIONS.values()):
            self.direction = diff
        else:
            self.direction = None

    def reset_selection(self):
        self.selected_passive = (None, None)
        self.selected_aggressive = (None, None)
        self.direction = None

    def get_tile_center(self, board_id, tile_id):
        x_offset, y_offset, _ = self.board(board_id)
        row = tile_id // self.BOARD_SIZE
        col = tile_id % self.BOARD_SIZE
        center_x = (self.MARGIN + self.TILE_SIZE) * col + self.MARGIN + x_offset + self.TILE_SIZE // 2
        center_y = (self.MARGIN + self.TILE_SIZE) * row + self.MARGIN + y_offset + self.TILE_SIZE // 2
        return center_x, center_y

    def get_tile_and_board_id(self, x_offset, y_offset, i, j):
        for board_id, (board_x, board_y, _) in enumerate(self.boards_iterator()):
            if x_offset == board_x and y_offset == board_y:
                tile_id = i * self.BOARD_SIZE + j
                return board_id, tile_id
        return None, None

    def choose_move(s, position_string):
        s.reset_selection()
        s.display_game(position_string)
        s.move = None
        s.move_chosen_event.clear()
        s.move_chosen_event.wait()
        s.move_chosen_event.clear()
        s.reset_selection()
        return s.move

if __name__ == '__main__':
    player = VisualPlayer()
    player.start()
    