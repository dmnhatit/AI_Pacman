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