import random
import rushhour
import util


class Node:

    def __init__(self, state, parent=None, value=0, depth=0):
        self.state = state
        self.parent = parent
        self.value = value    # f(n) = g(n) + h(n) for A*; unused for BFS/DFS
        self.depth = depth   # g(n) = number of actions from root

    def path(self):
        """Returns the list of states from the root node to this node."""
        nodes = []
        node = self
        while node is not None:
            nodes.append(node.state)
            node = node.parent
        return list(reversed(nodes))


class Agent:

    def random_walk(self, state, n):
        """
        Performs a random walk of n steps through the state space.
        Returns the list of n states visited (reconstructed from the final node).
        """
        node = Node(state)
        for _ in range(n - 1):
            actions = node.state.actions()
            if not actions:
                break
            action = random.choice(actions)
            next_state = node.state.execute(action)
            node = Node(next_state, parent=node, depth=node.depth + 1)
        return node.path()

    def _search(self, state, pop_front=True, heuristic=None):
        """
        Base graph-search algorithm shared by BFS, DFS, and A*.

        pop_front=True  -> BFS (FIFO) or A* (sorted FIFO)
        pop_front=False -> DFS (LIFO)
        heuristic       -> callable h(state) used for A*; None for BFS/DFS
        """
        h0 = heuristic(state) if heuristic else 0
        initial = Node(state, parent=None, value=h0, depth=0)
        open_list = [initial]
        closed = set()
        count = 0

        while open_list:
            # Select next node to consider
            if pop_front:
                node = open_list.pop(0)
            else:
                node = open_list.pop()

            state_str = str(node.state)
            if state_str in closed:
                continue

            closed.add(state_str)
            count += 1

            # Print path from root to current node
            util.pprint(node.path())

            # Check for goal
            if node.state.is_goal():
                print(count)
                return node

            # Expand: add successors not yet closed
            for action in node.state.actions():
                next_state = node.state.execute(action)
                if str(next_state) not in closed:
                    g = node.depth + 1
                    h = heuristic(next_state) if heuristic else 0
                    child = Node(next_state, parent=node, value=g + h, depth=g)
                    open_list.append(child)

            # Keep open list sorted by f(n) for A*
            if heuristic:
                open_list.sort(key=lambda nd: nd.value)

        return None

    def bfs(self, state):
        """Breadth-first search (FIFO open list, no heuristic)."""
        return self._search(state, pop_front=True, heuristic=None)

    def dfs(self, state):
        """Depth-first search (LIFO open list, no heuristic)."""
        return self._search(state, pop_front=False, heuristic=None)

    def a_star(self, state, heuristic):
        """A* search (sorted FIFO open list with f(n) = g(n) + h(n))."""
        return self._search(state, pop_front=True, heuristic=heuristic)
