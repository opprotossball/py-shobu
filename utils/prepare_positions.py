import argparse
import random
from game.shobu import Shobu, Move

def piece_on_tile(board_str, board_id, tile):
    id = 2 + 17 * board_id + tile
    match board_str[id]:
        case '_':
            return Shobu.EMPTY_TILE
        case 'b':
            return Shobu.BLACK_PIECE
        case 'w':
            return Shobu.WHITE_PIECE
        
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