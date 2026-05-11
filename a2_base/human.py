import game


class HumanPlayer(game.Player):

    def choose_action(self, state):
        actions = state.actions(self.char)
        for i, action in enumerate(actions):
            print(f'{i}: {action}')
        index = int(input('Please choose an action: '))
        return actions[index]
