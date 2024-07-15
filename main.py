from matches.arena import Arena
from bots.human_player import HumanPlayer
from bots.bot import ShobuBot
from bots.ref_bot import RefBot
from bots.random_bot import RandomBot
from matches.visualization import Visualization
from game.shobu import Shobu, Move
from bots.visual_player import VisualPlayer
from matches.tournament import tournament
from matches.play_vs_bot import play_vs_bot

def play_match():
    human = HumanPlayer()
    ref_bot = RefBot()
    bot = ShobuBot()
    visualization = Visualization()
    visualization.start()
    arena = Arena(50, visualization=visualization.display_game)
    arena.play_game(human, bot, position="b w_b_____________ wb______________ wb______________ w______________b")

def test_on_positions():
    path = 'resources/classic_game.txt'
    # path = 'resources/test_positions.txt'
    # path = 'resources/32_positions.txt'
    with open(path) as f:
        positions = f.readlines()
    bot_1_class = ShobuBot
    bot_2_class = RefBot
    visualization = Visualization()
    visualization.start()
    arena = Arena(50, visualization=visualization.display_game, logging=True)
    arena.play_positions(bot_1_class, bot_2_class, positions)

def duplicate_positions():
    path = 'resources/64_positions.txt'
    positions = {}
    with open(path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line in positions:
            print(f'duplicate: {i}')
        positions.add(line)

def play_tournamnet():
    #bot_2_path = 'tmp/shoman.exe'
    bot_1_path = 'tmp/v7.exe'
    bot_2_path = 'tmp/v7.exe'
    positions_path = 'resources/classic_game.txt'
    #positions_path = 'resources/32_positions.txt'
    visualization = Visualization()
    visualization.start()
    tournament(bot_1_path, bot_2_path, positions_path, max_moves=50, visualization=visualization.display_game, pause=False)

def play_bot(playing_as_white):
    bot = 'tmp/v8.exe'
    player = VisualPlayer()
    player.start()
    play_vs_bot(playing_as_white, player, bot)

if __name__ == '__main__':
    #play_tournamnet()
    play_bot(False)
