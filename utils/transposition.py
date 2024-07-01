class Transposition:

    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2
    
    def __init__(s, zobrist, depth, flag, eval, best_move=None):
        s.zobrist = zobrist
        s.depth = depth
        s.flag = flag
        s.eval = eval
        s.best_move = best_move
        