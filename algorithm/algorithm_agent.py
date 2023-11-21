class Node:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.cost = cost

    def get_path(self):
        node, path_back = self, []
        while node:
            path_back.append(node.state)
            node = node.parent
        return list(reversed(path_back))

    def path_cost(self):
        node, total_cost = self, 0
        while node.parent:
            total_cost += node.cost
            node = node.parent
        return total_cost

    def get_directions(self):
        path = self.get_path()
        directions = []
        for i in range(1, len(path)):
            dx = path[i][0] - path[i - 1][0]
            dy = path[i][1] - path[i - 1][1]
            if dx == 1:
                directions.append("DOWN")
            elif dx == -1:
                directions.append("UP")
            elif dy == 1:
                directions.append("RIGHT")
            elif dy == -1:
                directions.append("LEFT")
        return directions


class Problem:
    def __init__(self, maze, initial_state, goal_state):
        self.maze = maze
        self.initial_state = initial_state
        self.goal_state = goal_state

    def goal_test(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = [
            (state[0] + dx, state[1] + dy)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
        ]
        successors = [
            (x, y)
            for x, y in successors
            if 0 <= x < len(self.maze)
            and 0 <= y < len(self.maze[0])
            and self.maze[x][y] != 0
        ]
        return successors
