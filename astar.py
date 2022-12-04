from copy import deepcopy
from warnings import warn


class Node:
    """A node class for A* Pathfinding"""

    # more like "guided BFS"
    # h-function seems wrong but works well enough

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        if position is not None:
            if len(position) == 25:
                self.n = 5
            if len(position) == 49:
                self.n = 7
        else:
            self.n = 0
        if self.n == 5:
            self.tosolve = 15
            self.moves = 10
        elif self.n == 7:
            self.tosolve = 28
            self.moves = 20

    def __eq__(self, other):
        return self.position == other.position


def astar(start, end):
    """Returns a list of steps as a path from given start to given end"""

    # Create start and end node
    node_start = Node(None, start)
    node_start.g = node_start.h = node_start.f = 0
    node_end = Node(None, end)
    node_end.g = node_end.h = node_end.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()
    open_set = set()

    # Add the start node
    open_list.append([0, node_start])
    open_set.add(node_start.position)

    # Loop until you find the end
    print("trying to solve waffle. this might take a minute")
    while len(open_list) > 0:
        # print("waffles closed:", len(closed_list))

        open_list = sorted(open_list, key=sorthelp)
        # open_list.reverse()
        # Get the current node
        f, node_current = open_list.pop(0)
        # print("currently at step ", node_current.g)
        # print("with f-value", node_current.f)
        closed_list.add(node_current.position)

        # Found the goal
        not_quite = False
        if node_current.position == node_end.position:
            path = []
            current = node_current
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate neighbours
        if not_quite is False:
            neighbours = []
            switchable_positions = []
            unsolved_tiles = 0
            for i in range(len(node_current.position)):
                if node_current.position[i] != node_end.position[i]:
                    switchable_positions.append(i)
                    unsolved_tiles += 1

            switched_nodes = []
            switchpairs = []
            for m in range(len(switchable_positions)):
                for n in range(m, len(switchable_positions)):

                    i, j = switchable_positions[m], switchable_positions[n]
                    if [j, i] in switchpairs:
                        pass
                    elif i == j:
                        pass

                    else:
                        if (node_current.position[j] == node_end.position[i]) or (
                            node_current.position[i] == node_end.position[j]
                        ):
                            switched_node = deepcopy(node_current)
                            switched_node_list = [c for c in switched_node.position]
                            switched_node_list[i], switched_node_list[j] = (
                                switched_node_list[j],
                                switched_node_list[i],
                            )
                            switched_node_str = "".join(switched_node_list)
                            switched_node.position = switched_node_str
                            switched_nodes.append(switched_node)
                            switchpairs.append([i, j])

            for new_state in switched_nodes:
                # Create new node
                new_node = Node(node_current, new_state.position)
                # Append
                if new_node.position not in closed_list:
                    neighbours.append(new_node)

            # Loop through children
            for neighbour in neighbours:
                # Create the f, g, and h values
                neighbour.g = node_current.g + 1
                temph = 0
                for i in range(len(neighbour.position)):
                    if neighbour.position[i] != node_end.position[i]:
                        temph += 1
                neighbour.h = temph
                skipit = False

                if neighbour.n == 5:
                    if neighbour.g > 10:
                        skipit = True
                elif neighbour.n == 7:
                    if neighbour.g > 20:
                        skipit = True

                if skipit is False:
                    if temph == node_current.h:
                        pass
                    elif temph == 0:
                        open_list.append([neighbour.f, neighbour])
                        open_set.add(neighbour.position)
                    else:
                        closed = False
                        if neighbour.position in closed_list:
                            closed = True
                            # print('already closed')
                            break
                        if closed is False:
                            in_open = False
                            if neighbour.position in open_set:
                                in_open = True

                            if in_open is False:
                                # what's the weight?
                                # neighbour.f = neighbour.g + neighbour.h
                                # 1/(solved + remaining)
                                # best so far
                                neighbour.f = 1 / (
                                    neighbour.tosolve
                                    - neighbour.h
                                    + neighbour.moves
                                    - neighbour.g
                                )
                                if neighbour.f < node_current.f:
                                    open_list = []
                                open_list.append([neighbour.f, neighbour])
                                open_set.add(neighbour.position)

    warn("Couldn't get a path to destination")
    return None


def sorthelp(item):
    return item[0]


def main(startwaffle, endwaffle):
    # startwaffle = [c for c in startwaffle]
    # endwaffle = [c for c in endwaffle]
    path = astar(startwaffle, endwaffle)
    s = 0
    for index, result in enumerate(path):
        head = 0
        if len(result) == 25:
            n = 5
        elif len(result) == 49:
            n = 7
        if index == 0:
            prev_waffle = [[0 for x in range(n)] for y in range(n)]
        current_waffle = [[0 for x in range(n)] for y in range(n)]
        for i in range(n):
            for j in range(n):
                current_waffle[i][j] = result[head]
                head += 1
        switches = []
        for x in range(len(current_waffle)):
            string = ""
            for y in range(len(current_waffle)):
                char = current_waffle[x][y]
                string = string + char + " "
                if index > 0:
                    if current_waffle[x][y] != prev_waffle[x][y]:
                        switches.append([[y + 1, x + 1], prev_waffle[x][y]])
            print(string)
        print("Step ", s)
        s += 1
        print(switches)
        print(" ")
        prev_waffle = deepcopy(current_waffle)


if __name__ == "__main__":

    inw = "piltaz i nzonoca a ghvale"
    outw = "pizzai o ltangoc a nhalve"
    # inw =  'duernr l eimtaee o tdvvee'
    # outw = 'demonr e eutteri a vdelve'
    # inw = 'ondfrd a laoieaf e glgnel'
    # outw = 'odderf o eflinga n alegal'
    # inw = "henreubq n i tmerluree e q aduuotado o d yieearnc"
    # outw = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
    # inw = 'tcvcsrou o r dbpneares o i itsueiett e g coiehkar'
    # outw = 'revisito e e rbandageo t s etouristi r c ocheckup'
    main(inw, outw)
