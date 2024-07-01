import argparse
import random
from game.shobu import Shobu, Move

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('position_count', type=int)
    parser.add_argument('n_moves', type=int)
    args = parser.parse_args()
    for _ in range(args.position_count):
        game = Shobu()
        for _ in range(args.n_moves):
            game.make_move(random.choice(game.get_legal_moves()))
        print(game.to_string())