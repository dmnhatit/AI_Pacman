#%%
from collections import deque
import heapq


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


class PriorityQueue:
    def __init__(self):
        self.elements = []  # list các phần từ được duy trì thứ tự heapq
        self.entry_finder = (
            {}
        )  # sử dụng để theo dõi vị trí của từng phần tử trong self.elements.
        self.REMOVED = (
            "<removed-task>"  # thằng số đánh dấu phần tử bị loại bỏ khỏi hàng đợi.
        )
        self.counter = 0  # biến sử dụng để đảm bảo sự duy nhất

    # kiểm tra hàng đợi có đang rỗng
    def empty(self):
        return not self.entry_finder

    # thêm item với mức độ ưu tiên vào hàng đợi. Nếu item đã tồn tại thì loại bỏ item đó để thay bằng item mới
    def put(self, item, priority):
        if item in self.entry_finder:
            self.remove(item)
        entry = [priority, self.counter, item]
        self.counter += 1
        self.entry_finder[item] = entry
        heapq.heappush(self.elements, entry)

    # Loại bỏ item khỏi dict entry_finder và đánh dấu remove trong self.elements
    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED

    # lấy item ra khỏi hàng đợi và xoá nó khỏi dict entry_finder
    def get(self):
        while self.elements:
            priority, count, item = heapq.heappop(self.elements)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                return item
        raise KeyError("get from an empty priority queue")

    # được sử dụng để kiểm tra xem một phần tử có tồn tại trong hàng đợi ưu tiên hay không
    def __contains__(self, item):
        return item in self.entry_finder


# [REFERENCES]
# https://gist.github.com/jchacks/63a05a5c81785b7dcefffa12d23e3b17


def bfs(problem):
    start_node = Node(problem.initial_state)
    if problem.goal_test(start_node.state):
        return start_node
    frontier = deque([start_node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.state)
        for child_state in problem.get_successors(node.state):
            child = Node(child_state, node, node.cost + 1)
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None


def ucs(problem):
    start_node = Node(problem.initial_state)
    frontier = PriorityQueue()
    frontier.put(start_node, start_node.cost)
    explored = set()
    while not frontier.empty():
        current_node = frontier.get()
        if problem.goal_test(current_node.state):
            return current_node
        explored.add(current_node.state)
        for child_state in problem.get_successors(current_node.state):
            # if problem.maze[child_state[0]][child_state[1]] == 5: //có trọng số
            #     child_node = Node(child_state, current_node, current_node.cost + 1)
            # else:
            #     child_node = Node(child_state, current_node, current_node.cost + 5)
            child_node = Node(child_state, current_node, current_node.cost + 1)
            if child_state not in explored and child_node not in frontier:
                frontier.put(child_node, child_node.cost)
            elif (
                child_node in frontier
                and child_node.cost < frontier.entry_finder[child_node][0]
            ):
                frontier.put(child_node, child_node.cost)
    return None


if __name__ == "__main__":
    # maze = [
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # 1: obstacle position
    #     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    # ]

    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],   # 0: obstacle position
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 2, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    problem = Problem(maze, (1, 1), (16, 22))
    node_bfs = bfs(problem)
    node_ucs = ucs(problem)
    if node_bfs is not None:
        print(node_bfs.get_directions())
        print(node_bfs.cost)
    else:
        print("No solution")

    if node_ucs is not None:
        print(node_ucs.get_directions())
        print(node_ucs.cost)
    else:
        print("No solution")

    if node_ucs is not None and node_bfs is not None:
        if node_bfs.get_directions() == node_ucs.get_directions():
            print("same")
# %%