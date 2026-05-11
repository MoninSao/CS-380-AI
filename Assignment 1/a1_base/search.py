import util
import rushhour
from agent import Agent

DEFAULT_STATE = rushhour.DEFAULT_STATE


def heuristic(state):
    # find the rightmost column occupied by x on EXIT_Y
    x_right = -1
    for col in range(state.SIZE):
        if state.get(col, state.EXIT_Y) == 'x':
            x_right = col

    if x_right == -1:
        return 0  # 'x' not on board should not happen

    # count how many distinct vehicles between x's right end and the exit column
    blockers = set()
    for col in range(x_right + 1, state.SIZE):
        c = state.get(col, state.EXIT_Y)
        if c != 'x' and c != rushhour.Cell.EMPTY:
            blockers.add(c)

    # +1 for the move(s) 'x' itself needs to reach the exit
    return len(blockers) + 1


if __name__ == '__main__':

    cmd = util.get_arg(1)
    if cmd:

        string = util.get_arg(2) or DEFAULT_STATE
        state = rushhour.State(string)
        agent = Agent()

        if cmd == 'random':
            states = agent.random_walk(state, 8)
            util.pprint(states)

        elif cmd == 'bfs':
            agent.bfs(state)

        elif cmd == 'dfs':
            agent.dfs(state)

        elif cmd == 'a_star':
            agent.a_star(state, heuristic)
