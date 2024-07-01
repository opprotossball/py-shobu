from game.shobu import *
from utils.zorbrist_hashing import ZorbristHashing
import random 
import unittest

class ShobuTest(unittest.TestCase):

    def test_hash_updateing(self):
        n_pre_moves = 4
        seeds = [2137, 789, 8, 45, 123]
        for seed in seeds:
            zobrist = ZorbristHashing()
            game = Shobu()
            random.seed(seed)
            for _ in range(n_pre_moves):
                game.make_move(random.choice(game.get_legal_moves()))
            hash1 = zobrist.get_hash(game)
            move = random.choice(game.get_legal_moves())
            hash2 = zobrist.update_hash_move(hash1, move, game)
            game.make_move(move)
            to_undo, pushed_from = game.move_history[-1]
            hash2 = zobrist.update_hash_undo(hash2, to_undo, game, pushed_from)
            game.undo_move()
            self.assertEqual(hash1, hash2)

if __name__ == '__main__':
    unittest.main()