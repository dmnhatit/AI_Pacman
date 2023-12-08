import math

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # PATH-COST to the node
        self.h = 0 # heuristic to the goal
        self.f = 0 # evaluation function f(n) = g(n) + h(n)
    
    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]
    
    def path_cost(self):
        return self.g

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
    
    def __eq__(self, other):
        return self.position == other.position

def heuristic(node, start_node, end_node, name_heuristic):
    dx=abs(node.position[0] - end_node.position[0])
    dy=abs(node.position[1] - end_node.position[1])
    dx_start_end=abs(start_node.position[0] - end_node.position[0])
    dy_start_end=abs(start_node.position[1] - end_node.position[1])
    dx_start_current=abs(start_node.position[0] - node.position[0])
    dy_start_current=abs(start_node.position[1] - node.position[1])
    a=math.sqrt((dx ** 2) + (dy ** 2))
    b=math.sqrt((dx_start_end ** 2) + (dy_start_end ** 2))
    c=math.sqrt((dx_start_current ** 2) + (dy_start_current ** 2))
    cos = abs(((b**2 + c**2 - a**2) / (2 * b * c)))
    if (name_heuristic=="euclidean"):
        return math.sqrt((dx ** 2) + (dy ** 2))
    if (name_heuristic=="manhattan"):
        return dx+dy
    if (name_heuristic=="euclidean_no_square"):
        return (dx ** 2) + (dy ** 2)
    if (name_heuristic=="angle_euclidean"):
        return (dx+dy) - cos
    
def astar(problem, name_heuristic):
    maze=problem.maze
    # Create start and end node
    start_node = Node(None, problem.initial_state)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, problem.goal_state)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []    # frontier queue
    closed_list = []  # explored set
    
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if we found the goal
        if current_node == end_node:
            return current_node, len(closed_list)
        # Expansion: Generate children
        children = []
        for new_position in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            #Evaluate child in closed list or opened list
            is_closed_child = False
            is_opened_child = False

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    is_closed_child = True
                    break
            if is_closed_child:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Update for cost
            if maze[child.position[0]][child.position[1]] == 5:
                child.g = current_node.g + 40      
            child.h = heuristic(child, start_node, end_node, name_heuristic)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node:
                    is_opened_child = True
                    if child.f < open_node.f:
                        open_node = child
                        open_node.parent = current_node

            # Add the child to the open list
            if not is_opened_child:
                open_list.append(child)

def astar_euclidean(problem):
    return astar(problem,"euclidean")

def astar_euclidean_no_square(problem):
    return astar(problem,"euclidean_no_square")

def astar_manhattan(problem):
    return astar(problem,"manhattan")

def astar_angle_euclidean(problem):
    return astar(problem,"angle_euclidean")

if __name__ == '__main__':
    maze =     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0],
                [0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 5, 1, 0, 0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 0, 1, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    problem = Problem(maze, (1, 1), (19, 16))

    result, count_closed_node = astar_angle_euclidean(problem)

    print(result.get_directions())
    print(count_closed_node)

'''
Tài liệu tham khảo: Code tham khảo bài tập tuần 8 của thầy Trần Nhật Quang
'''