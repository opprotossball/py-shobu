import random

class RandomBot:

    def choose_move(s, position):
        mv = random.choice(position.get_legal_moves())
        print(mv.to_string())
        return mv
    