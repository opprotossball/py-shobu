from matches.game_master import GameMaster
from matches.visualization import Visualization

if __name__ == '__main__':
    v = Visualization()
    v.start()
    gm = GameMaster(30, True, v.display_game)
    gm.play_game()
