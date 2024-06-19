from shobu import *
import random 
import unittest

class ShobuTest(unittest.TestCase):

    def test_undo(self):
        n_moves = 12
        undo = 6
        seeds = [2137, 789, 8, 45, 123]
        for seed in seeds:
            game = Shobu()
            random.seed(seed)
            pos = ''
            for i in range(n_moves):
                if i == n_moves - undo:
                    pos = game.to_string()
                game.make_move(random.choice(game.get_legal_moves()))
            for _ in range(undo):
                game.undo_move()
            self.assertEqual(game.to_string(), pos)

    def test_clone(self):
        n_moves = 12
        seeds = [2137, 789, 8, 45, 123]
        for seed in seeds:
            game = Shobu()
            random.seed(seed)
            for i in range(n_moves):
                game.make_move(random.choice(game.get_legal_moves()))
            pos = game.to_string()
            clone = game.clone()
            self.assertEqual(clone.to_string(), pos)

    def test_move_count(self):
        game = Shobu()
        self.assertEqual(len(game.get_legal_moves()), 232)

    def random_play_out(self, seed):
        random.seed(seed)
        game = Shobu()
        while game.winner == 0:
            game.make_move(random.choice(game.get_legal_moves()))
        
    def test_random_playouts(self):
        seeds = [2137, 789, 8, 45, 123]
        for seed in seeds:
            try:
                self.random_play_out(seed)
            except Exception as e:
                self.fail(f'failed: {e}')

if __name__ == '__main__':
    unittest.main()