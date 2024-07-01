from game.shobu import Shobu, Move

class HumanPlayer:

    def choose_move(s, position):
        return s.get_input(position)
    
    def get_input(s, position):
        game = position.clone()
        inp = input()
        try:
            move = Move.from_string(inp)
            # for validation
            game.make_move(move)
            return move
        except:
            print('Invalid move, try again!')
            return s.get_input(position)
