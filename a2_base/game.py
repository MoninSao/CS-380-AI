import util


class Player:

    def __init__(self, char):
        self.char = char

    def choose_action(self, state):
        raise NotImplementedError


class Game:

    def __init__(self, state, player1, player2):
        self.state = state
        self.players = {player1.char: player1, player2.char: player2}
        self.player1 = player1

    def play(self):
        state = self.state
        states = [state.clone()]
        current_char = self.player1.char

        while not state.game_over():
            player = self.players[current_char]
            action = player.choose_action(state)
            state.execute(action)
            util.pprint(state)
            states.append(state.clone())
            current_char = 'O' if current_char == 'X' else 'X'

        return state.loser(), states
