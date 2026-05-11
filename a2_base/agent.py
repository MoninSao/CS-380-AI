import random
import game


class RandomPlayer(game.Player):

    def choose_action(self, state):
        return random.choice(state.actions(self.char))


class MinimaxPlayer(game.Player):

    def choose_action(self, state):
        self._cache = {}
        opponent = 'O' if self.char == 'X' else 'X'
        best_action = None
        best_value = float('-inf')
        for action in state.actions(self.char):
            next_state = state.clone()
            next_state.execute(action)
            value = self._minimax(next_state, opponent, depth=1)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action

    def _minimax(self, state, char, depth):
        key = (str(state), char)
        if key in self._cache:
            return self._cache[key]

        if state.game_over():
            base = -1 if state.loser() == self.char else 1
            result = base / depth
            self._cache[key] = result
            return result

        next_char = 'O' if char == 'X' else 'X'

        if char == self.char:
            best = float('-inf')
            for action in state.actions(char):
                next_state = state.clone()
                next_state.execute(action)
                best = max(best, self._minimax(next_state, next_char, depth + 1))
        else:
            best = float('inf')
            for action in state.actions(char):
                next_state = state.clone()
                next_state.execute(action)
                best = min(best, self._minimax(next_state, next_char, depth + 1))

        self._cache[key] = best
        return best
