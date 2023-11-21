import math

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # PATH-COST to the node
        self.h = 0 # heuristic to the goal: straight-line distance hueristic
        self.f = 0 # evaluation function f(n) = g(n) + h(n)

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
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
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Expansion: Generate children
        children = []
        for new_position in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
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
            child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
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

def directionStep(path):
    direction = []
    for i in range(len(path)-1):
        if (path[i+1][0]-path[i][0]==0 and path[i+1][1]-path[i][1]==1):
            direction.append("RIGHT")
        elif (path[i+1][0]-path[i][0]==0 and path[i+1][1]-path[i][1]==-1):
            direction.append("LEFT")
        elif (path[i+1][0]-path[i][0]==-1 and path[i+1][1]-path[i][1]==0):
            direction.append("UP")
        else:
            direction.append("DOWN")
    return direction


if __name__ == '__main__':
    maze =     [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
                [0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,1,0],
                [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
                [0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0],
                [0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,0],
                [0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0],
                [0,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,1,1,0],
                [0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0],
                [0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0],
                [0,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,1,0],
                [0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0],
                [0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0],
                [0,1,0,0,0,0,0,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0],
                [0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0],
                [0,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,1,1,0],
                [0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0],
                [0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,1,1,0],
                [0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0],
                [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
                [0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,1,0],
                [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    start = (0, 0)
    goal = (23, 23)

    path = astar(maze, start, goal)
    print(path)

    print(directionStep(path))
