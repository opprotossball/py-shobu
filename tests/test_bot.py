from game.shobu import Shobu, Move
from bots.bot import ShobuBot
import unittest

class BotTest(unittest.TestCase):

    def test_winning_as_black(self):
        positions = ['b w_b_____________ wb______________ wb______________ wb______________']
        for position in positions:
            game = Shobu.from_string(position)
            bot = ShobuBot()
            move = bot.choose_move(game)
            game.make_move(move)
            self.assertEqual(game.winner, -1)
        
        
    def test_winning_as_white(self):
        positions = ['w bw______________ bw______________ b_w_____________ bw______________']
        for position in positions:
            game = Shobu.from_string(position)
            bot = ShobuBot()
            move = bot.choose_move(game)
            game.make_move(move)
            self.assertEqual(game.winner, 1)

if __name__ == '__main__':
    unittest.main()