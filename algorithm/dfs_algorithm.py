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

def dfs(problem):
    start_node = Node(problem.initial_state)
    if problem.goal_test(start_node.state):
        return start_node
    frontier = [start_node]
    explored = set()
    explored.add(start_node.state)
    while frontier:
        node = frontier.pop()
        for child_state in problem.get_successors(node.state):
            child = Node(child_state, node, node.cost + 1)
            if child.state not in explored and child not in frontier:
                explored.add(child.state)
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None

def ids(problem):
    depth = 0
    visited = []
    while depth < 100:
        result = dls(problem, depth, visited)
        if result != -1:
            return result
        depth += 1
        visited = []

def dls(problem, limit, visited=[]):
    return recursive_dls(Node(problem.initial_state), problem, limit, visited)

def recursive_dls(node, problem, limit, visited):
    visited.append(node)
    if problem.goal_test(node.state):
        return node
    elif limit == 0:
        return -1  # cutoff
    else:
        cutoff_occurred = False
        for child_state in problem.get_successors(node.state):
            child = Node(child_state, node, node.cost + 1)
            if not_in_visited(visited, child_state) or in_but_better(visited, child):
                result = recursive_dls(child, problem, limit - 1, visited)
                if result == -1:  # cutoff
                    cutoff_occurred = True
                elif result is not None:
                    return result
        if cutoff_occurred:
            return -1  # cutoff
        else:
            return None  # failure

def not_in_visited(visited, child_state):
    return child_state not in [node.state for node in visited]

def in_but_better(visited, node):
    for visited_node in visited:
        if visited_node.state == node.state and visited_node.cost > node.cost:
            visited.remove(visited_node)
            return True
    return False
