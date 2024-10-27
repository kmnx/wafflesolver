import heapq
import time  # Import the time module
start_time = time.time()

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def heuristic(state, goal, g=0, og_unsolved=28):
    if len(state) == 49:
        distance = 20
    else:
        distance = 10
    out_of_place = sum(1 for a, b in zip(state, goal) if a != b)
    #h = distance - g + out_of_place
    # f = 1 / ( total tiles to solve - solved tiles + max total moves - done moves)
    # why does this work relatively well?
    # h1 weird 1/x function
    # 21s runtime
    # seems better than previous one at about 66s
    # only by cheating and removing some check-sets, otherwise 66 seconds
    #h = 1 / (og_unsolved - out_of_place + distance - g) -g
    # what about reducing distance by 1 for doubles and 0.5 for singles
    og_doubles = og_unsolved - 20
    used_doubles = (og_unsolved - out_of_place) -g
    rem_doubles = og_doubles - used_doubles

    solved_tiles = 28 - out_of_place
    doubles = solved_tiles - g
    singles = g - doubles
    rem_moves = 20 - g
    # kinda works, really fast for some solutions, really slow for others
    worst_case = out_of_place - 1
    best_case = out_of_place/2 if out_of_place % 2 == 0 else out_of_place/2 + 1
    h = (worst_case + best_case) / 2

    #h = out_of_place/2
    # what if  doubles get huge bonus
    #h = out_of_place
    #h = 1 / (solved tiles + "distance" )
    #slow
    #h = out_of_place**2
    #bad
    #h = (out_of_place + g) / 20
   
    #h = (out_of_place / 20) * (20-g)
    #h = (out_of_place/28) * (20-g)
    # 55 seconds but underestimates, admissible but not consistent
    #h = out_of_place-(og_unsolved-20)

    # ballooning to millions of nodes
    # h = out_of_place/2
    # balloning to millions of nodes
    #if out_of_place > 16:
    #    h = 8 + (out_of_place-16)
    #else:
    #    h = out_of_place/2

    return h

def a_star(start, goal):
    open_set = []
    dumb_open_set = set()
    og_unsolved = sum(1 for a, b in zip(start, goal) if a != b)
    closed_set = set()
    start_node = Node(start, g=0, h=heuristic(start, goal))
    heapq.heappush(open_set, start_node)
    #dumb_open_set.add(start)
    
    while open_set:
        current_node = heapq.heappop(open_set)
        
        if current_node.state == goal:
            return reconstruct_path(current_node)

        closed_set.add(current_node.state)
        out_of_place = sum(1 for a, b in zip(current_node.state, goal) if a != b)

        if (current_node.g + out_of_place/2 ) > 20:
            #print("huh", current_node.g, out_of_place/2,len(open_set), heuristic(current_node.state, goal,current_node.g,og_unsolved))
            continue
        #print("-----")
        print("g: ", current_node.g, "f: ", current_node.h+current_node.g, "h:",current_node.h,len(open_set))

        for i in range(len(current_node.state)):
            if current_node.state[i] == goal[i]:
                    continue
            
            for j in range(i + 1, len(current_node.state)):
                if (current_node.state[j] == goal[i]) and (current_node.state[j] != goal[j]):
                    new_state = list(current_node.state)
                    new_state[i], new_state[j] = new_state[j], new_state[i]
                    new_state = ''.join(new_state)
                    if new_state in closed_set:
                        continue
                    g = current_node.g + 1
                    #if g == 21:
                    #    print("huh")
                    out_of_place = sum(1 for a, b in zip(new_state, goal) if a != b)

                    if (g + out_of_place/2 ) > 20:
                        continue
                    #if new_state in dumb_open_set:
                        #print("already in open set")
                    #    continue
                    else:
                        #dumb_open_set.add(new_state)
                        h = heuristic(new_state, goal, g, og_unsolved)
                        new_node = Node(new_state, current_node, g, h)
                        #print("-----")
                        #out_of_place_curr = sum(1 for a, b in zip(current_node.state, goal) if a != b)
                        #print(current_node.state, out_of_place_curr, current_node.g, current_node.h,"current f: ",heuristic(current_node.state, goal,current_node.g))
                        #diffstring = ""
                        #for k in range(len(new_state)):
                        #    if new_state[k] == goal[k]:
                        #        diffstring += (new_state[k]).upper()
                        #    else:
                        #        diffstring += new_state[k]
                        #out_of_place_new = sum(1 for a, b in zip(new_state, goal) if a != b)
                        #print(diffstring, out_of_place_new, g, h, "next h: ",heuristic(new_state, goal,g))
                        #if h == current_node.h+2:
                        #    print("h is 2")
                        heapq.heappush(open_set, new_node)

    return -1  # If no solution is found
def main(start,goal):
    return a_star(start,goal)
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    path.reverse()
    for pindex,p in enumerate(path):
        #print(p)
        if len(p) == 49:
            for i in range(7):
                print(' '.join(p[i*7:i*7+7]))
        else:
            for i in range(5):
                print(' '.join(p[i*5:i*5+5]))
        diffstring = ""
        if pindex is not len(path)-1:
            indices = []
            indices.append(pindex+1)
            for i in range(len(p)):
                if p[i] != path[pindex+1][i]:
                    diffstring += "!"
                    if len(p) == 49:
                        indices.append([i//7,i%7,p[i]])
                    else:
                        indices.append([i//5,i%5,p[i]])
                else:
                    diffstring += " "
            print(indices)
                        
    return len(path) - 1  # Number of swaps
#start = "csroeu z votoaen f aeertr"
#goal = "curver o nafootz s eeater"

#start = "thfeccun h t isistasni n i husitisgl g o ndigceiu"
#goal = "deficiti i h osustainc h l iunitings n c hsuggest"
start1 = "adotpwet a b rahscocde n e dtpibueen r h rtrgceuh"
goal2= "chopperh u r eabscondt t d htributee n c aragweed"
start = "tcvcsrou o r dbpneares o i itsueiett e g coiehkar"
goal = "revisito e e rbandageo t s etouristi r c ocheckup"
print(a_star(start, goal))
# Record the end time
end_time = time.time()

# Calculate the total runtime
total_runtime = end_time - start_time

# Print the total runtime
print(f"Total runtime: {total_runtime:.2f} seconds")

