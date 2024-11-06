from copy import deepcopy
from warnings import warn


class Node:
    """A node class for A* Pathfinding"""

    # more like BFS on rails

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
    closed_set = set()
    open_set = set()

    # Add the start node
    open_list.append([0, node_start])
    open_set.add(node_start.position)

    # Loop until you find the end
    print("trying to solve waffle. this might take a minute")
    while len(open_list) > 0:
        open_list = sorted(open_list, key=sorthelp)
        # Get the current node
        f, node_current = open_list.pop(0)
        # print("currently at step ", node_current.g, "with f-value", node_current.f)

        # Found the goal
        if node_current.position == node_end.position:
            path = []
            current = node_current
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate neighbours
        neighbours = []
        switchable_positions = []
        for i in range(len(node_current.position)):
            if node_current.position[i] != node_end.position[i]:
                switchable_positions.append(i)

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
                        #  to switch chars convert str to list and back to str
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

            # Append
            if new_state.position not in closed_set:
                if new_state.position not in open_set:
                    new_node = Node(node_current, new_state.position)
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
                    if neighbour.position in closed_set:
                        closed = True

                    if closed is False:
                        in_open = False
                        # the important part
                        # distance estimation f only goes down for swaps resulting in 2 greens
                        # everything else might just be an intermediate step
                        # f = 1 / ( total tiles to solve - solved tiles + max total moves - done moves)
                        neighbour.f = 1 / (
                            neighbour.tosolve
                            - neighbour.h
                            + neighbour.moves
                            - neighbour.g
                        )
                        if neighbour.position in open_set:
                            in_open = True

                        if in_open is False:
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

    # inw = "piltaz i nzonoca a ghvale"
    # outw = "pizzai o ltangoc a nhalve"
    # inw =  'duernr l eimtaee o tdvvee'
    # outw = 'demonr e eutteri a vdelve'
    # inw = 'ondfrd a laoieaf e glgnel'
    # outw = 'odderf o eflinga n alegal'
    # inw = "henreubq n i tmerluree e q aduuotado o d yieearnc"
    # outw = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
    # inw = 'tcvcsrou o r dbpneares o i itsueiett e g coiehkar'
    # outw = 'revisito e e rbandageo t s etouristi r c ocheckup'
    # inw = "gtoage t nnlseio l idekny"
    # outw = "goingl n eaislen e kdotty"
    # inw = "csroeu z votoaen f aeertr"
    # outw = "curver o nafootz s eeater"
    # inw = "adotpwet a b rahscocde n e dtpibueen r h rtrgceuh"
    # outw = "chopperh u r eabscondt t d htributee n c aragweed"
    inw = "tcvcsrou o r dbpneares o i itsueiett e g coiehkar"
    outw = "revisito e e rbandageo t s etouristi r c ocheckup"
    main(inw, outw)
