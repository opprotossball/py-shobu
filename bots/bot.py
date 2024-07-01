from game.shobu import Shobu, Move
from utils.zorbrist_hashing import ZorbristHashing
from utils.hash_table import HashTable
from utils.transposition import Transposition

class ShobuBot:

    INF = 999999
    PIECE_VALUE = 10
    # SQUARED_MATERIAL_ADVANTAGE_VALUE = 7
    MAX_DEPTH = 3
    MOBILITY_WEIGHT = 0.2
    TRANSPOSITION_TABLE_SIZE = 2**20 + 7
    BLACK_PST = [
        2, 5, 5, 2, 
        2, 3, 3, 2,
        2, 2, 2, 2,
        1, 2, 2, 1
    ]
    WHITE_PST = [
        1, 2, 2, 1,
        2, 2, 2, 2,
        2, 3, 3, 2,
        2, 5, 5, 2
    ]
    
    def __init__(s):
        s.zobrist = ZorbristHashing()
        s.minimax_calls = 0
        s.tt_hits = 0
        s.transposition_table = HashTable(size_limit=ShobuBot.TRANSPOSITION_TABLE_SIZE)

    def choose_move(s, position):
        s.minimax_calls = 0
        s.tt_hits = 0
        position_hash = s.zobrist.get_hash(position)
        eval, move_id = s.negamax(position, position_hash, ShobuBot.MAX_DEPTH, -ShobuBot.INF, ShobuBot.INF, 1 if position.white_to_go else -1)
        return position.get_legal_moves()[move_id]

    # def guess_move_strength(s, position, move):
    #     pst = ShobuBot.WHITE_PST if position.white_to_go else ShobuBot.BLACK_PST
    #     diff = 2 * move.direction if move.is_double_move else move.direction
    #     score = pst[Shobu.internal_2_readable(move.passive_from + diff)] 
    #     score -= pst[Shobu.internal_2_readable(move.passive_from)] 
    #     score += pst[Shobu.internal_2_readable(move.aggressive_from + diff)] 
    #     score -= pst[Shobu.internal_2_readable(move.aggressive_from)]
    #     return score

    def sign(s, v):
        return -1 if v < 0 else 1

    def eval(s, position):
        eval = 0
        for board in position.all_boards():
            for i in position.board_iterator():
                if board[i] == Shobu.WHITE_PIECE:
                    eval += ShobuBot.PIECE_VALUE
                    eval += ShobuBot.WHITE_PST[position.internal_2_readable(i)]
                elif board[i] == Shobu.BLACK_PIECE:
                    eval -= ShobuBot.PIECE_VALUE
                    eval -= ShobuBot.BLACK_PST[position.internal_2_readable(i)]
        # eval = 0
        # for board in position.all_boards():
        #     for i in position.board_iterator():
        #         material_advantage = 0
        #         if board[i] == Shobu.WHITE_PIECE:
        #             material_advantage += 1
        #             eval += ShobuBot.WHITE_PST[position.internal_2_readable(i)]
        #         elif board[i] == Shobu.BLACK_PIECE:
        #             material_advantage -= 1
        #             eval -= ShobuBot.BLACK_PST[position.internal_2_readable(i)]
        #         eval += s.sign(material_advantage) *  ShobuBot.SQUARED_MATERIAL_ADVANTAGE_VALUE * (material_advantage ** 2)
                
        # mobility = len(position.get_legal_moves()) * ShobuBot.MOBILITY_WEIGHT
        # eval += mobility if position.white_to_go else -mobility
        return eval

    # returns (eval, best move id) tuple
    def negamax(s, position, position_hash, depth, alpha, beta, active_player):
        # print(s.zorbrist.get_hash(position))
        s.minimax_calls += 1
        alpha_org = alpha

        transposition = s.transposition_table.get(position_hash)
        if transposition is not None and transposition.zobrist == position_hash and transposition.depth >= depth:
            s.tt_hits += 1
            if transposition.flag == Transposition.EXACT:
                return transposition.eval, transposition.best_move
            elif transposition.flag == Transposition.LOWER_BOUND:
                alpha = max(alpha, transposition.eval)
            elif transposition.flag == Transposition.UPPER_BOUND:
                beta = min(beta, transposition.eval)

            if alpha >= beta:
                return transposition.eval, transposition.best_move 

        if position.winner != 0:
            return active_player * position.winner * (10000.0 + depth), 0
        
        if depth == 0:
            return active_player * s.eval(position), 0
        
        i = 0
        best_eval = -ShobuBot.INF
        best_move = 0
        # moves.sort(key=lambda m: s.guess_move_strength(position, m), reverse=True)
        # for move in position.move_generator()
        for move in position.move_generator():
            # make move
            current_hash = s.zobrist.update_hash_move(position_hash, move, position)
            position.make_move(move)
            # recursive call
            eval, _ = s.negamax(position, current_hash, depth - 1, -beta, -alpha, -active_player)
            eval = -eval
            # undo move
            # to_undo, pushed_from = position.move_history[-1]
            # position_hash = s.zobrist.update_hash_undo(current_hash, move, position, pushed_from)
            position.undo_move()
            # update eval
            if eval > best_eval:
                best_eval = eval
                best_move = i
            alpha = max(alpha, best_eval)
            if alpha >= beta:
                break
            i += 1

        # add record to transposition table
        flag = Transposition.EXACT
        if best_eval <= alpha_org:
            flag = Transposition.UPPER_BOUND
        if best_eval >= beta:
            flag = Transposition.LOWER_BOUND
        entry = Transposition(position_hash, depth, flag, best_eval, best_move)
        s.transposition_table[position_hash] = entry
        return best_eval, best_move
        
if __name__ == '__main__':
    bot = ShobuBot()
    while True:
        playing_as = int(input())       
        position = Shobu.from_string(input())
        print(bot.choose_move(position).to_string())
