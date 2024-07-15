import subprocess
import threading
from game.shobu import Shobu, Move
import traceback
import time
import queue

BLACK_WIN = 0
WHITE_WIN = 1
DRAW = 2

def read_stderr(process, log_queue):
    for line in iter(process.stderr.readline, ''):
        log_queue.put(line.strip())
    process.stderr.close()

def play_vs_bot(playing_as_white, visual_player, bot_path, position=None, max_moves=50):
    times = [[], []]
    bot_process = subprocess.Popen(bot_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2)
    bot_log = queue.Queue()
    black_thread = threading.Thread(target=read_stderr, args=(bot_process, bot_log))
    black_thread.start()

    game = Shobu() if position is None else Shobu.from_string(position)
    moves_played = 0
    while game.winner == 0:
        visual_player.display_game(game.to_string())
        player_to_go = 1 if game.white_to_go else 0
        print(player_to_go)
        position = game.to_string()
        print(position)
        try:
            if playing_as_white == game.white_to_go:
                move = visual_player.choose_move(game.to_string())
                start_time = time.time()
                time_elapsed = time.time() - start_time
                times[int(game.white_to_go)].append(time_elapsed)
                game.make_move(move)
            else:
                # Write to the bot's stdin
                bot_process.stdin.write(str(player_to_go) + "\n")
                bot_process.stdin.flush()
                bot_process.stdin.write(position + "\n")
                bot_process.stdin.flush()
                # Record the start time, read the move from stdout, and calculate elapsed time
                start_time = time.time()
                move = bot_process.stdout.readline().strip()
                time_elapsed = time.time() - start_time
                times[int(game.white_to_go)].append(time_elapsed)
                # Read the bot's stderr for new output
                print()
                while not bot_log.empty():
                    stderr_output = bot_log.get()
                    if stderr_output:
                        print(f"white: {stderr_output}")
                print()
                print(move)
                # Process the move
                game.make_move(Move.from_string(move))
        except Exception:
            print(traceback.format_exc())
            _, bot_stderr = bot_process.communicate()
            if bot_stderr:
                print("black bot stderr:")
                print(bot_stderr)
            winner = BLACK_WIN if player_to_go == 1 else WHITE_WIN
            return winner, times
        moves_played += 1
        # If too many moves were made player that made last move loses  
        if moves_played == max_moves:
            print('Maximum number of moves reached')
            return DRAW, times
        visual_player.display_game(game.to_string())
    winner = BLACK_WIN if game.winner == -1 else WHITE_WIN
