from matches.arena import Arena
from bots.human_player import HumanPlayer
from bots.bot import ShobuBot
from bots.ref_bot import RefBot
from bots.random_bot import RandomBot
from matches.visualization import Visualization
from game.shobu import Shobu, Move
from matches.tournament import tournament

def play_match():
    human = RandomBot()
    ref_bot = RefBot()
    bot = ShobuBot()
    visualization = Visualization()
    visualization.start()
    arena = Arena(50, visualization=visualization.display_game)
    arena.play_game(human, bot)

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
    bot_1_path = 'tmp/rust-shobu.exe'
    bot_2_path = 'tmp/bot.exe'
    positions_path = 'resources/32_positions.txt'
    visualization = Visualization()
    visualization.start()
    tournament(bot_1_path, bot_2_path, positions_path, max_moves=50, visualization=visualization.display_game)

if __name__ == '__main__':
    play_tournamnet()
