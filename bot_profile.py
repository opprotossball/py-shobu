import cProfile
from main import test_on_positions

if __name__ == '__main__':
    cProfile.run('test_on_positions()')
