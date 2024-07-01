import random
from game.shobu import Shobu

class ZorbristHashing:

    def random_long(s):
        return random.randint(0, 2**64 - 1)
    
    def __init__(s, seed=None):
        if seed is not None:
            random.seed(seed)
        s.white_to_go = s.random_long()
        s.white_pieces = [s.random_long() for _ in range(64)]
        s.black_pieces = [s.random_long() for _ in range(64)]

    def get_hash(s, position):
        res = s.white_to_go if position.white_to_go else 0
        for i, board in enumerate(position.all_boards()):
            for j in position.board_iterator():
                if board[j] == Shobu.WHITE_PIECE:
                    res ^= s.white_pieces[16 * i + Shobu.internal_2_readable(j)]
                elif board[j] == Shobu.BLACK_PIECE:
                    res ^= s.black_pieces[16 * i + Shobu.internal_2_readable(j)]
        return res

    def update_hash_move(s, hash, move, position):
        hash ^= s.white_to_go
        passive_board = 2 * int(position.white_to_go) + int(move.white_passive_board)
        aggressive_board = 2 * int(position.white_to_go == move.home_aggressive_board) + int(not move.white_passive_board)
        pieces = s.white_pieces if position.white_to_go else s.black_pieces
        diff = 2 * move.direction if move.is_double_move else move.direction
        hash ^= pieces[16 * passive_board + Shobu.internal_2_readable(move.passive_from)]
        hash ^= pieces[16 * passive_board + Shobu.internal_2_readable(move.passive_from + diff)]
        hash ^= pieces[16 * aggressive_board + Shobu.internal_2_readable(move.aggressive_from)]
        hash ^= pieces[16 * aggressive_board + Shobu.internal_2_readable(move.aggressive_from + diff)]
        pushed_from, pushed_to = position.push_from_to(move)
        if pushed_from == -1:
            return hash
        opponets_pieces = s.black_pieces if position.white_to_go else s.white_pieces
        hash ^= opponets_pieces[16 * aggressive_board + Shobu.internal_2_readable(pushed_from)]
        if pushed_to != -1:
            hash ^= opponets_pieces[16 * aggressive_board + Shobu.internal_2_readable(pushed_to)]
        return hash

    def update_hash_undo(s, hash, move, position, pushed_from):
        hash ^= s.white_to_go
        passive_board = 2 * int(not position.white_to_go) + int(move.white_passive_board)
        aggressive_board = 2 * int(not position.white_to_go == move.home_aggressive_board) + int(not move.white_passive_board)
        pieces = s.black_pieces if position.white_to_go else s.white_pieces
        diff = 2 * move.direction if move.is_double_move else move.direction
        hash ^= pieces[16 * passive_board + Shobu.internal_2_readable(move.passive_from)]
        hash ^= pieces[16 * passive_board + Shobu.internal_2_readable(move.passive_from + diff)]
        hash ^= pieces[16 * aggressive_board + Shobu.internal_2_readable(move.aggressive_from)]
        hash ^= pieces[16 * aggressive_board + Shobu.internal_2_readable(move.aggressive_from + diff)]
        if pushed_from == -1:
            return hash
        pushed_to = move.aggressive_from + diff + move.direction
        opponets_pieces = s.white_pieces if position.white_to_go else s.black_pieces
        hash ^= opponets_pieces[16 * aggressive_board + Shobu.internal_2_readable(pushed_from)]
        if position.valid_tile(pushed_to):
            hash ^= opponets_pieces[16 * aggressive_board + Shobu.internal_2_readable(pushed_to)]
        return hash
