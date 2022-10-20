from copy import deepcopy
from warnings import warn


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
        if position is not None:
            self.n = len(position[0])
        else:
            self.n = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(start, end):
    """Returns a list steps as a path from the given start to the given end"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append([0, start_node])

    # Loop until you find the end
    while len(open_list) > 0:
        open_list = sorted(open_list, key=sorthelp)
        # open_list = sorted(open_list, key=sorthelp_h)
        open_list.reverse()
        # Get the current node
        f, current_node = open_list.pop()

        # Pop current off open list, add to closed list
        # closed_list.append(current_node)

        # Found the goal
        if current_node.position == end_node.position:
            '''if current_node.n == 7:
                # to force optimal solution this should take next item from open_list, not break to error
                if current_node.g > 21:
                    break
            elif current_node.n == 5:
                # same
                if current_node.g > 11:
                    break'''
            #else:
            if True:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

        # Generate children
        children = []
        switchable_positions = []
        for i in range(current_node.n):
            for j in range(current_node.n):
                if current_node.position[i][j] != end_node.position[i][j]:
                    switchable_positions.append([i, j])

        switched_nodes = []
        switchpairs = []
        for first_position in switchable_positions:
            for second_position in switchable_positions:
                switchpairs.append([first_position, second_position])
                switched_node = deepcopy(current_node)
                i, j = first_position[0], first_position[1]
                m, n = second_position[0], second_position[1]
                if (i == m) and (j == n):
                    pass
                elif [second_position, first_position] in switchpairs:
                    pass
                elif switched_node.position[i][j][0] == switched_node.position[m][n][0]:
                    pass
                else:
                    switched_node.position[i][j], switched_node.position[m][n] = (
                        switched_node.position[m][n],
                        switched_node.position[i][j],
                    )
                    switched_nodes.append(switched_node)

        for new_state in switched_nodes:
            # Create new node
            new_node = Node(current_node, new_state.position)
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            already_in_closed = False
            # Child is on the closed list
            for closed_child in closed_list:
                if child.position == closed_child.position:
                    # print('but here we are')
                    already_in_closed = True
                    break

            # Create the f, g, and h values
            if not already_in_closed:
                child.g = current_node.g + 1
                if child.g > 25:
                    break
                else:
                    temph = 0
                    for i in range(child.n):
                        for j in range(child.n):
                            # print('current node',current_node.position[i][j])
                            # print('new node',end_node.position[i][j])
                            if child.position[i][j] != end_node.position[i][j]:
                                temph += 2

                    # child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    #    (child.position[1] - end_node.position[1]) ** 2
                    # )
                    child.h = temph
                    print(child.h)

                    # input()
                    child.f = child.g + child.h
                    # print('or or here?')
                    # Child is already in the open list
                    # if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                    #   continue
                    qlen = len(open_list)
                    if qlen == 0:
                        open_list.append([child.f, child])
                    else:
                        skip = False
                        for i in range(qlen):
                            pass
                            # open_node = open_list[i][1]
                            # if (open_node.position == child.position) and (open_node.g > child.g):
                            #    skip = True
                            # elif open_node.h == child.h:
                            #    skip = True
                        if skip:
                            pass

                        else:
                            # print(child.h)
                            f_val = int(child.f)
                            open_list.append([f_val, child])
                        # Add the child to the open list

    warn("Couldn't get a path to destination")
    return None


def sorthelp(item):
    return item[0]


def main(startwaffle, endwaffle):
    path = astar(startwaffle, endwaffle)
    i = 0
    for item in path:
        print(" ")
        for line in item:
            print(line)
        print("Step ", i)
        i += 1


if __name__ == "__main__":
    """startwaffle = [
        ["f", "b", "o", "u", "e"],
        ["g", " ", "i", " ", "u"],
        ["l", "s", "o", "o", "m"],
        ["g", " ", "e", " ", "l"],
        ["o", "e", "m", "n", "a"],
    ]"""

    """startwaffle = [
        ["s", "c", "g", "o", "l"],
        ["n", " ", "n", " ", "d"],
        ["i", "n", "d", "e", "e"],
        ["r", " ", "i", " ", "u"],
        ["f", "f", "a", "r", "e"],
    ]"""

    """endwaffle = [
        ["f", "u", "g", "u", "e"],
        ["o", " ", "l", " ", "n"],
        ["l", "o", "o", "s", "e"],
        ["i", " ", "b", " ", "m"],
        ["o", "m", "e", "g", "a"],
    ]"""
    """endwaffle = [
        ["s", "n", "a", "r", "l"],
        ["n", " ", "i", " ", "e"],
        ["u", "n", "d", "i", "d"],
        ["f", " ", "e", " ", "g"],
        ["f", "o", "r", "c", "e"],
    ]"""

    startwaffle = [
        ["h", "e", "n", "r", "e", "u", "b"],
        ["q", " ", "n", " ", "i", " ", "t"],
        ["m", "e", "r", "l", "u", "r", "e"],
        ["e", " ", "e", " ", "q", " ", "a"],
        ["d", "u", "u", "o", "t", "a", "d"],
        ["o", " ", "o", " ", "d", " ", "y"],
        ["i", "e", "e", "a", "r", "n", "c"],
    ]

    endwaffle = [
        ["n", "u", "n", "n", "e", "r", "y"],
        ["o", " ", "u", " ", "q", " ", "i"],
        ["m", "a", "r", "q", "u", "e", "e"],
        ["a", " ", "t", " ", "a", " ", "l"],
        ["d", "o", "u", "b", "t", "e", "d"],
        ["i", " ", "r", " ", "o", " ", "e"],
        ["c", "h", "e", "e", "r", "e", "d"],
    ]

    main(startwaffle, endwaffle)
