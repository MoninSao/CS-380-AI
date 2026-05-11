import sys
import util
from munch import State
from game import Game
from human import HumanPlayer
from agent import RandomPlayer, MinimaxPlayer


def make_player(name, char):
    if name == 'human':
        return HumanPlayer(char)
    elif name == 'random':
        return RandomPlayer(char)
    elif name == 'minimax':
        return MinimaxPlayer(char)
    else:
        print(f'Unknown player type: {name}. Choose from [human, random, minimax].')
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 main.py <player1> <player2>')
        print('Player types: human, random, minimax')
        sys.exit(1)

    player1 = make_player(sys.argv[1], 'X')
    player2 = make_player(sys.argv[2], 'O')

    state = State()
    g = Game(state, player1, player2)
    loser, states = g.play()

    print(f'\n{loser} loses')
    print('\nGame sequence:')
    util.pprint(states)
