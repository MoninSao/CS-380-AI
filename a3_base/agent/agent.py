import json
import os
import random

from .state import State


class Q_State(State):
    '''Augments the game state with Q-learning information'''

    def __init__(self, string):
        super().__init__(string)

        # key stores the state's key string (see notes in _compute_key())
        self.key = self._compute_key()

    def _compute_key(self):
        '''
        Returns a key used to index this state.

        The key should reduce the entire game state to something much smaller
        that can be used for learning. When implementing a Q table as a
        dictionary, this key is used for accessing the Q values for this
        state within the dictionary.
.
        '''

        row_key = str(self.frog_y).zfill(2)

        window = []
        for dy in (-1, 0, 1):
            for dx in (-2, -1, 0, 1, 2):
                cell = self.get(self.frog_x + dx, self.frog_y + dy)
                window.append(cell if cell is not None else '_')

        return row_key + ''.join(window)

    def reward(self, prev_y=None):
        '''Returns a reward value for the state.'''

        if self.at_goal:
            return self.score
        elif self.is_done:
            return -10
        else:
            # small bonus for moving toward the goal (row 0 is the top)
            if prev_y is not None and self.frog_y < prev_y:
                return 0.5
            return 0


class Agent:

    def __init__(self, train=None):

        # train is either a string denoting the name of the saved
        # Q-table file, or None if running without training
        self.train = train

        # q is the dictionary representing the Q-table
        self.q = {}

        # name is the Q-table filename
        # (you likely don't need to use or change this)
        self.name = train or 'q'

        # path is the path to the Q-table file
        # (you likely don't need to use or change this)
        self.path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'train', self.name + '.json')

        # Q-learning hyperparameters
        self.alpha = 0.5    # learning rate
        self.gamma = 0.9    # discount factor
        self.epsilon = 0.1  # exploration probability

        # previous (S, A) pair for the Bellman update
        self.prev_state = None
        self.prev_action = None

        self.load()

    def load(self):
        '''Loads the Q-table from the JSON file'''
        try:
            with open(self.path, 'r') as f:
                self.q = json.load(f)
            if self.train:
                print('Training {}'.format(self.path))
            else:
                print('Loaded {}'.format(self.path))
        except IOError:
            if self.train:
                print('Training {}'.format(self.path))
            else:
                raise Exception('File does not exist: {}'.format(self.path))
        return self

    def save(self):
        '''Saves the Q-table to the JSON file'''
        with open(self.path, 'w') as f:
            json.dump(self.q, f)
        return self

    def choose_action(self, state_string):
        '''
        Returns the action to perform.

        This is the main method that interacts with the game interface:
        given a state string, it should return the action to be taken
        by the agent.


        '''
        state = Q_State(state_string)
        key = state.key

        # initialize unseen state in Q-table
        if key not in self.q:
            self.q[key] = {a: 0.0 for a in State.ACTIONS}

        # Bellman update using the previous (S, A) pair
        if self.train and self.prev_state is not None:
            r = state.reward(prev_y=self.prev_state.frog_y)
            max_q_next = max(self.q[key].values())
            prev_key = self.prev_state.key
            prev_a = self.prev_action
            self.q[prev_key][prev_a] = (
                (1 - self.alpha) * self.q[prev_key][prev_a]
                + self.alpha * (r + self.gamma * max_q_next)
            )
            self.save()

        # episode is over — reset tracking and return no-op
        if state.is_done:
            self.prev_state = None
            self.prev_action = None
            return '_'

        # ε-greedy action selection
        if self.train and random.random() < self.epsilon:
            action = random.choice(State.ACTIONS)
        else:
            action = max(self.q[key], key=lambda a: self.q[key][a])

        self.prev_state = state
        self.prev_action = action
        return action
