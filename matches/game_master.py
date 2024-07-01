from game.shobu import *

class GameMaster:
    
    def __init__(s, max_moves, logging=False, visualization=None):
        s.max_moves = max_moves
        s.logging = logging
        s.visualization = visualization

    def play_game(s):
        game = Shobu()
        moves_played = 0
        while game.winner == 0:
            if s.visualization is not None:
                s.visualization(game.to_string())
            player_to_go = 1 if game.white_to_go else 0
            print(player_to_go)
            position = game.to_string()
            print(position)
            bot_move = input()
            try:
                move = Move.from_string(bot_move)
                game.make_move(move)
            except Exception as e:
                if s.logging:
                    print(e)
                if player_to_go == 0:
                    print(1)
                else:
                    print(0)
                return
            moves_played += 1
            # if too many moves were made player that made last move loses  
            if moves_played == s.max_moves:
                winner = 1 if game.white_to_go else 0
                if s.logging:
                    print('Maximal number of moves reached')
                print(winner)
                return
        winner = 0 if game.winner == -1 else 1
        print(winner)

if __name__ == '__main__':
    gm = GameMaster(max_moves=50, logging=True)
    gm.play_game()
