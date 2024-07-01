from game.shobu import *
import traceback
import time

class Arena:
    
    def __init__(s, max_moves, logging=True, visualization=None):
        s.max_moves = max_moves
        s.logging = logging
        s.visualization = visualization

    # each bot must have choose_move method
    def play_game(s, black_bot, white_bot, position=None):
        game = Shobu() if position is None else Shobu.from_string(position)
        moves_played = 0
        while game.winner == 0:
            if s.visualization is not None:
                s.visualization(game.to_string())
            player_to_go = 1 if game.white_to_go else 0
            print(player_to_go)
            position = game.to_string()
            print(position)
            try:
                bot = white_bot if game.white_to_go else black_bot
                move = bot.choose_move(game.clone())
                game.make_move(move)
            except Exception as e:
                if s.logging:
                    print(traceback.format_exc())
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
        if s.visualization is not None:
            s.visualization(game.to_string())
        winner = 0 if game.winner == -1 else 1
        print('Game ended! Winner is:')
        print(winner)

    def bot_test(s, black_bot, white_bot, position=None):
        minimax_calls = [[], []]
        move_times = [[], []]
        game = Shobu() if position is None else Shobu.from_string(position)
        moves_played = 0
        while game.winner == 0:
            if s.visualization is not None:
                s.visualization(game.to_string())
            player_to_go = 1 if game.white_to_go else 0
            print(player_to_go)
            position = game.to_string()
            print(position)
            try:
                bot = white_bot if game.white_to_go else black_bot
                start_time = time.time()
                move = bot.choose_move(game.clone())
                move_times[int(game.white_to_go)].append(time.time() -  start_time)
                minimax_calls[int(game.white_to_go)].append(bot.minimax_calls)
                game.make_move(move)
            except Exception as e:
                if s.logging:
                    print(traceback.format_exc())
                if player_to_go == 0:
                    winner = 1
                else:
                    winner = 0
                print(winner)
                return winner, minimax_calls, move_times
            moves_played += 1
            # if too many moves were made player that made last move loses  
            if moves_played == s.max_moves:
                winner = 1 if game.white_to_go else 0
                if s.logging:
                    print('Maximal number of moves reached')
                print(winner)
                return winner, minimax_calls, move_times
        if s.visualization is not None:
            s.visualization(game.to_string())
        winner = 0 if game.winner == -1 else 1
        print('Game ended! Winner is:')
        print(winner)
        return winner, minimax_calls, move_times

    def play_positions(s, bot_1_class, bot_2_class, positions):
        minimax_calls = [[], []]
        move_times = [[], []]
        wins = [0, 0]
        for position in positions:
            for bot_1_black in [True, False]:
                if bot_1_black:
                    black_bot = bot_1_class()
                    white_bot = bot_2_class()
                else:
                    black_bot = bot_2_class()
                    white_bot = bot_1_class()
                winner, calls, times = s.bot_test(black_bot, white_bot, position)
                if bot_1_black:
                    wins[winner] += 1
                else: 
                    wins[winner - 1] += 1
                for c in calls[int(not bot_1_black)]:
                    minimax_calls[0].append(c)
                for c in calls[int(bot_1_black)]:
                    minimax_calls[1].append(c)
                for t in times[int(not bot_1_black)]:
                    move_times[0].append(t)
                for t in times[int(bot_1_black)]:
                    move_times[1].append(t)
        avg_calls = [sum(c) / len(c) for c in minimax_calls]
        avg_time = [sum(t) / len(t) for t in move_times]
        print(f'wins:\n    bot_1: {wins[0]}\n    bot_2: {wins[1]}')
        print(f'avg calls:\n   bot_1: {round(avg_calls[0], 2)}\n   bot_2: {round(avg_calls[1], 2)}')
        print(f'avg time:\n   bot_1: {round(avg_time[0], 6)}\n   bot_2: {round(avg_time[1], 6)}')


        


        