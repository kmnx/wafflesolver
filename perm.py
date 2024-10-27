import copy

class Node:
    def __init__(self, cycles=None, cycle=None, stack=None, visited=None, solution_indices=None):
        self.cycles = []
        self.cycle = []
        self.stack = []
        self.visited = visited
        self.solution_indices = solution_indices

def cycle_decomposition(scrambled, solution):
    # Create a mapping of indices for each character in the solution string
    solution_indices = {}
    for i, char in enumerate(solution):
        if char not in solution_indices:
            solution_indices[char] = []
        solution_indices[char].append(i)
    
    # Initialize visited list and cycles list
    big_stack = []
    solutionstack = []
    visited = [False] * len(scrambled)
    cycles = []
    start_node = Node([], visited=visited, solution_indices=solution_indices)
    big_stack.append(start_node)
    # Function to explore cycles
    def explore_cycle(cycle=[],start_index=0):
        cycle = cycle
        stack = [start_index]
        while stack:
            index = stack.pop()
            if not current_node.visited[index]:
                current_node.visited[index] = True
                current_node.cycle.append(index)
                char = scrambled[index]
                if char in current_node.solution_indices:
                    if len(current_node.solution_indices[char]) > 1:
                        for i in current_node.solution_indices[char]:
                            print(current_node.solution_indices[char],i)
                            if not current_node.visited[i]:
                                next_index = i

                                new_node = copy.deepcopy(current_node)
                                
                                new_node.stack.append(next_index)
                                big_stack.append(new_node)
                            else:
                                current_node.cycles.append(current_node.cycle)
                                current_node.cycle = []
                                big_stack.append(current_node)
                    else:
                        if not current_node.visited[char]:
                            next_index = current_node.visited[char]

                            new_node = copy.deepcopy(current_node)
                            
                            new_node.stack.append(next_index)
                            big_stack.append(new_node)

                        
                        
                        
                        
                        
                            
        

    # Explore all cycles
    while big_stack:
        current_node = big_stack.pop()
        if len(current_node.cycle) == 12:
            print(current_node.cycle)
        if current_node.stack:
            start_index = current_node.stack.pop()
            cycle = current_node.cycle
            if current_node.visited[start_index]:
                if len(cycle) > 1:
                    current_node.cycles.append(cycle)
                    big_stack.append(current_node)
                    continue
            else:
                explore_cycle(cycle,start_index)
                continue
            
        else:
            for i in range(len(scrambled)):
                if not current_node.visited[i]:
                    explore_cycle(i)
                    
        if current_node.visited.count(True) == len(scrambled):
            solutionstack.append(current_node)

    # Apply the cycles to transform scrambled into solution
    
    while solutionstack:
        scrambled_list = copy.deepcopy(list(scrambled))
        current_node = solutionstack.pop()
        for cycle in current_node.cycles:
            #cycle.reverse()
            for i in range(len(cycle) - 1):
                scrambled_list[cycle[i]], scrambled_list[cycle[i + 1]] = scrambled_list[cycle[i + 1]], scrambled_list[cycle[i]]
    
        print(''.join(scrambled_list))

# Test the program with the provided strings
scrambled = "DBDFAFECBCAE"
solution = "AABBCCDDEEFF"
final_string = cycle_decomposition(scrambled, solution)

# Check if the final string matches the solution
if final_string == solution:
    print("Successfully transformed scrambled string into the solution!")
else:
    print("Transformation failed to match the solution.")