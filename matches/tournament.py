import subprocess
from game.shobu import Shobu, Move
import traceback
import time

BLACK_WIN = 0
WHITE_WIN = 1
DRAW = 2

def tournament(bot_1_path, bot_2_path, positions_path, max_moves=50, visualization=None):
    draws = 0
    move_times = [[], []]
    wins = [0, 0]
    with open(positions_path) as f:
        positions = f.readlines()
    for position in positions:
        for bot_1_black in [True, False]:
            winner, times = play_match(bot_1_path, bot_2_path, max_moves, position.strip(), visualization) if bot_1_black else play_match(bot_2_path, bot_1_path, max_moves, position.strip(), visualization)
            if winner == DRAW:
                draws += 1
            elif bot_1_black:
                wins[winner] += 1
            else: 
                wins[winner - 1] += 1
            for t in times[int(not bot_1_black)]:
                move_times[0].append(t)
            for t in times[int(bot_1_black)]:
                move_times[1].append(t)
    avg_time = [sum(t) / len(t) for t in move_times]
    print(f'wins:\n    bot_1: {wins[0]}\n    bot_2: {wins[1]}')
    print(f'draws: {draws}')
    print(f'avg time:\n   bot_1: {round(avg_time[0], 6)}\n   bot_2: {round(avg_time[1], 6)}')    

def play_match(black_bot_path, white_bot_path, max_moves, position=None, visualization=None):
    times = [[], []]
    black_cmd = ['python', black_bot_path] if black_bot_path.endswith('.py') else [black_bot_path]
    white_cmd = ['python', white_bot_path] if white_bot_path.endswith('.py') else [white_bot_path]
    black_process = subprocess.Popen(black_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    white_process = subprocess.Popen(white_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    game = Shobu() if position is None else Shobu.from_string(position)
    moves_played = 0
    while game.winner == 0:
        if visualization is not None:
            visualization(game.to_string())
        player_to_go = 1 if game.white_to_go else 0
        print(player_to_go)
        position = game.to_string()
        print(position)
        try:
            bot_process = white_process if game.white_to_go else black_process
            bot_process.stdin.write(str(player_to_go) + "\n")
            bot_process.stdin.flush()
            bot_process.stdin.write(position + "\n")
            bot_process.stdin.flush()
            start_time = time.time()
            move = bot_process.stdout.readline().strip()
            times[int(game.white_to_go)].append(time.time() -  start_time)
            print(move)
            game.make_move(Move.from_string(move))
        except Exception:
            print(traceback.format_exc())
            # Print output and errors if any (for debugging purposes)
            black_stdout, black_stderr = black_process.communicate()
            white_stdout, white_stderr = white_process.communicate()
            print("black bot stdout:")
            print(black_stdout)
            if black_stderr:
                print("black bot stderr:")
                print(black_stderr)
            print("white bot stdout:")
            print(white_stdout)
            if white_stderr:
                print("white bot stderr:")
                print(white_stderr)
            winner = BLACK_WIN if player_to_go == 1 else WHITE_WIN
            return winner, times
        moves_played += 1
        # if too many moves were made player that made last move loses  
        if moves_played == max_moves:
            print('Maximum number of moves reached')
            return DRAW, times
    if visualization is not None:
        visualization(game.to_string())
    winner = BLACK_WIN if game.winner == -1 else WHITE_WIN
    print(f'Game ended! Winner is: {winner}')
    return winner, times
