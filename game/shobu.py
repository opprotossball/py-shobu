class Move:

    # tile must be in game internal coordinates
    def __init__(s, white_passive_board: bool, home_aggressive_board: bool, passive_from: int, aggressive_from: int, is_double_move: bool, direction: int):
        s.white_passive_board = white_passive_board
        s.home_aggressive_board = home_aggressive_board
        s.passive_from = passive_from
        s.aggressive_from = aggressive_from
        s.is_double_move = is_double_move
        s.direction = direction

    @staticmethod
    def from_string(move):
        is_double_move = move[0] == '2'
        index = 1 if is_double_move else 0
        direction_chars = ""
        while index < len(move) and move[index].isupper():
            direction_chars += move[index]
            index += 1
        direction = Shobu.DIRECTIONS[direction_chars]
        white_passive_board = move[index] == 'w'
        index += 1
        passive_from_start = index
        while index < len(move) and move[index].isdigit():
            index += 1
        passive_from = Shobu.readable_2_internal(int(move[passive_from_start:index]))
        home_aggressive_board = move[index] == 'h'
        index += 1
        aggressive_from_start = index
        while index < len(move) and move[index].isdigit():
            index += 1
        aggressive_from = Shobu.readable_2_internal(int(move[aggressive_from_start:index]))
        return Move(
            white_passive_board=white_passive_board,
            home_aggressive_board=home_aggressive_board,
            passive_from=passive_from,
            aggressive_from=aggressive_from,
            is_double_move=is_double_move,
            direction=direction
        )
    
    def to_string(s):
        notation = '2' if s.is_double_move else ''
        dir_string = list(Shobu.DIRECTIONS.keys())[list(Shobu.DIRECTIONS.values()).index(s.direction)]
        for char in dir_string:
            if char.isupper():
                notation += char
        notation += 'w' if s.white_passive_board else 'b'
        notation += str(Shobu.internal_2_readable(s.passive_from))
        notation += 'h' if s.home_aggressive_board else 'f'
        notation += str(Shobu.internal_2_readable(s.aggressive_from))
        return notation
    
class Shobu:

    EMPTY_TILE = 0
    OUT_OF_BOARD = -255
    BLACK_PIECE = -1
    WHITE_PIECE = 1
    DIRECTIONS = {
        'U': -8,
        'UR': -7,
        'R': 1,
        'DR': 9,
        'D': 8,
        'DL': 7,
        'L': -1,
        'UL': -9,
    }

    def __init__(s):   
        s.white_to_go = False
        s.winner = 0
        s.move_history = []
        s.__init_boards()

    def __init_boards(s):
        s.boards = [
            [s.__new_board(), s.__new_board()],
            [s.__new_board(), s.__new_board()]
        ]

    def occupied(s, tile_content):
        return tile_content == Shobu.WHITE_PIECE or tile_content == Shobu.BLACK_PIECE

    def board_to_readable(s, board):
        return [board[i] for i in s.board_iterator()]

    def all_boards(s):
        for l in s.boards:
            for board in l:
                yield board

    def undo_move(s):
        s.white_to_go = not s.white_to_go
        s.winner = 0
        move, pushed_from = s.move_history.pop()
        player_piece = Shobu.WHITE_PIECE if s.white_to_go else Shobu.BLACK_PIECE
        passive_board = s.get_board(s.white_to_go, move.white_passive_board)
        aggressive_board = s.get_board(s.white_to_go == move.home_aggressive_board, not move.white_passive_board)
        diff = 2 * move.direction if move.is_double_move else move.direction
        passive_board[move.passive_from + diff] = Shobu.EMPTY_TILE
        passive_board[move.passive_from] = player_piece
        aggressive_board[move.aggressive_from + diff] = Shobu.EMPTY_TILE
        aggressive_board[move.aggressive_from] = player_piece
        pushed_to = move.aggressive_from + diff + move.direction
        if pushed_from != -1:
            pushed_piece = Shobu.BLACK_PIECE if s.white_to_go else Shobu.WHITE_PIECE
            aggressive_board[pushed_from] = pushed_piece
            if aggressive_board[pushed_to] != Shobu.OUT_OF_BOARD:
                aggressive_board[pushed_to] = Shobu.EMPTY_TILE

    def can_be_played(s, board, origin, direction, is_double, is_aggressive):
        to = origin + (2 * direction) if is_double else origin + direction
        # goes out of board
        if board[to] == Shobu.OUT_OF_BOARD: 
            return False
        # blocked by friendly
        if board[to] == board[origin]:
            return False
        if not is_aggressive:
            # non-aggressive blocked by enemy
            if board[to] != Shobu.EMPTY_TILE:
                return False
            # jumps over piece
            if is_double and board[origin + direction] != Shobu.EMPTY_TILE:
                return False
        else:
            if is_double:
                # jumps over friendly
                if board[origin + direction] == board[origin]:
                    return False
                # double move push blocked - more than 1 stone in path
                pieces = 0
                for i in range(1, 4):
                    if s.occupied(board[origin + i * direction]):
                        pieces += 1
                if pieces > 1:
                    return False
            else:
                # single move push blocked
                if board[to] != Shobu.EMPTY_TILE and s.occupied(board[to + direction]):
                    return False
        return True
    
    def is_push_over(s, move):
        aggressive_board = s.get_board(s.white_to_go == move.home_aggressive_board, not move.white_passive_board)
        diff = 2 * move.direction if move.is_double_move else move.direction
        pushed_to =  move.aggressive_from + diff + move.direction
        pushed = aggressive_board[move.aggressive_from + diff] != Shobu.EMPTY_TILE or aggressive_board[move.aggressive_from + move.direction] != Shobu.EMPTY_TILE
        return pushed and aggressive_board[pushed_to] == Shobu.OUT_OF_BOARD
    
    def push_from_to(s, move):
        aggressive_board = s.get_board(s.white_to_go == move.home_aggressive_board, not move.white_passive_board)
        diff = 2 * move.direction if move.is_double_move else move.direction
        pushed_to = move.aggressive_from + diff + move.direction
        ret = -1 if aggressive_board[pushed_to] == Shobu.OUT_OF_BOARD else pushed_to
        if aggressive_board[move.aggressive_from + diff] != Shobu.EMPTY_TILE:
            return move.aggressive_from + diff, ret
        if move.is_double_move and aggressive_board[move.aggressive_from + move.direction] != Shobu.EMPTY_TILE:
            return move.aggressive_from + move.direction, ret
        return -1, -1 

    def __check_winner(s, board):
        if board.count(Shobu.WHITE_PIECE) == 0:
            s.winner = -1
        if board.count(Shobu.BLACK_PIECE) == 0:
            s.winner = 1

    def make_move(s, move):
        if s.winner != 0:
            raise Exception('Game has ended!')
        passive_board = s.get_board(s.white_to_go,  move.white_passive_board)
        aggressive_board = s.get_board(s.white_to_go == move.home_aggressive_board, not move.white_passive_board)
        if not s.can_be_played(passive_board, move.passive_from, move.direction, move.is_double_move, False):
            raise Exception('Passive part of move cannot be played!')
        if not s.can_be_played(aggressive_board, move.aggressive_from, move.direction, move.is_double_move, True):
            raise Exception('Aggressive part of move cannot be played!')
        diff = 2 * move.direction if move.is_double_move else move.direction
        # make passive part
        passive_board[move.passive_from + diff] = passive_board[move.passive_from]
        passive_board[move.passive_from] = Shobu.EMPTY_TILE
        # push
        pushed_from = -1
        if aggressive_board[move.aggressive_from + diff] != Shobu.EMPTY_TILE:
            pushed_from = move.aggressive_from + diff
        elif move.is_double_move and aggressive_board[move.aggressive_from + move.direction] != Shobu.EMPTY_TILE:
            pushed_from = move.aggressive_from + move.direction
        if pushed_from != -1:
            pushed_to = move.aggressive_from + diff + move.direction
            pushed_piece = aggressive_board[pushed_from]
            aggressive_board[pushed_from] = Shobu.EMPTY_TILE
            if aggressive_board[pushed_to] == Shobu.OUT_OF_BOARD:
                s.__check_winner(aggressive_board)
            else:
                aggressive_board[pushed_to] = pushed_piece
        # make aggressive part
        aggressive_board[move.aggressive_from + diff] = aggressive_board[move.aggressive_from]
        aggressive_board[move.aggressive_from] = Shobu.EMPTY_TILE
        s.white_to_go = not s.white_to_go
        s.move_history.append((move, pushed_from))

    @staticmethod
    def from_string(string):
        instance = Shobu()
        parts = string.split(' ')
        instance.white_to_go = parts[0] == 'w'
        boards = parts[1:]
        for white_home in range(2):
            for white_board in range(2):
                board_string = boards[white_home * 2 + white_board]
                board = instance.get_board(bool(white_home), bool(white_board))
                for i, char in enumerate(board_string):
                    tile = Shobu.readable_2_internal(i)
                    if char == '_':
                        board[tile] = Shobu.EMPTY_TILE
                    elif char == 'w':
                        board[tile] = Shobu.WHITE_PIECE
                    elif char == 'b':
                        board[tile] = Shobu.BLACK_PIECE
        return instance
    
    def clone(s):
        return Shobu.from_string(s.to_string())

    def __new_board(s):
        board = []
        for i in range(64):
            if not s.valid_tile(i):
                board.append(Shobu.OUT_OF_BOARD)
            elif i // 8 == 2:
                board.append(Shobu.WHITE_PIECE)
            elif i // 8 == 5:
                board.append(Shobu.BLACK_PIECE)
            else:
                board.append(Shobu.EMPTY_TILE)
        return board

    def board_iterator(s):
        for i in range(4):
            for j in range(4):
                yield j + 18 + (8 * i)

    def get_board(s, white_home, white_board):
        return s.boards[int(white_home)][int(white_board)]

    def valid_tile(s, tile):
        return tile > 15 and tile < 47 and tile % 8 > 1 and tile % 8 < 6
    
    def to_string(s):
        res = 'w' if s.white_to_go else 'b'
        for white_home in range(2):
            for white_board in range(2):
                res += ' '
                board = s.get_board(white_home, white_board)
                for i in s.board_iterator():
                    if board[i] == Shobu.EMPTY_TILE:
                        res += '_'
                    elif board[i] == Shobu.WHITE_PIECE:
                        res += 'w'
                    elif board[i] == Shobu.BLACK_PIECE:
                        res += 'b'
        return res

    def piece_iterator(s, board, white_player):
        piece = Shobu.WHITE_PIECE if white_player else Shobu.BLACK_PIECE
        for i in s.board_iterator():
            if board[i] == piece:
                yield i

    def __moves_for_boards(s, white_passive_board, home_aggressive_board, double_moves):
        passive_board = s.get_board(s.white_to_go, white_passive_board)
        aggressive_board = s.get_board(s.white_to_go == home_aggressive_board, not white_passive_board)
        for passive_from in s.piece_iterator(passive_board, s.white_to_go):
            for direction in Shobu.DIRECTIONS.values():
                if not s.can_be_played(passive_board, passive_from, direction, double_moves, False):
                    continue
                for aggressive_from in s.piece_iterator(aggressive_board, s.white_to_go):
                    if s.can_be_played(aggressive_board, aggressive_from, direction, double_moves, True):
                        yield Move(white_passive_board, home_aggressive_board, passive_from, aggressive_from, double_moves, direction)

    def get_legal_moves(s):
        moves = []
        for white_board in [True, False]:
            for aggressive_home in [True, False]:
                for double_moves in [True, False]:
                    for move in s.__moves_for_boards(white_board, aggressive_home, double_moves):
                        moves.append(move)
        return moves

    def move_generator(s):
        for white_board in [True, False]:
            for aggressive_home in [True, False]:
                for double_moves in [True, False]:
                    for move in s.__moves_for_boards(white_board, aggressive_home, double_moves):
                        yield move
    
    @staticmethod
    def readable_2_internal(tile):
        return 18 + (tile % 4) + 8 * (tile // 4)
    
    @staticmethod
    def internal_2_readable(tile):
        return tile - 4 * ((tile - 18) // 8) - 18 
    