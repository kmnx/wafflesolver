import heapq
import time
import json


# waffles are reduced to strings to find the shortest path between permutations
# like this:
# scrambled = "henreubq n i tmerluree e q aduuotado o d yieearnc"
# solution = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
# (but without spaces)
# cycle decomposition:
# first letter in the scrambled string is h, but we want n. so we look where to find an n
# there's an n at position 2 (but already correct), 9, and 48
# so the first swaps we can create are [0,9] and [0,48]
# next we check those two how they should continue
# at position 9 should be "u". there's a u at 6 and 28
# so the new cycles are [0,9],[9,6] and [0,9],[9,28]
# if the next index points to the beginning, we store it and start a new cycle
# this continues until every index has been visited
# the idea is that the more cycles we have, the shorter the path, because the best cycle is one that solves two positions in one move
# Simplified Example:
# to transform dbaca into aabcd
# you could swap [[0,2],[2,1],[1,4]] (one cycle with 3 swaps, each move solving 1 position)
# or [0,4],[1,2] (two cycles with 1 swaps each), each move solving two positions
# so more cycles means less moves to solve the puzzle


# helper to create a map of characters to possible solution positions
def solution_mapping(scrambled, solution, solved_at_start):
    mapping = {}
    # Use set to avoid duplicate characters
    for char in set(scrambled):
        positions = [
            i
            for i, s_char in enumerate(solution)
            if s_char == char and i not in solved_at_start
        ]
        mapping[char] = positions
    return mapping


# helper to make the solution swaps human readable
def convert_indices_to_xy(cycle, max_moves):
    all_moves = []
    if max_moves == 10:
        index_map = {
            0: "1,1",
            1: "1,2",
            2: "1,3",
            3: "1,4",
            4: "1,5",
            5: "2,1",
            6: "2,3",
            7: "2,5",
            8: "3,1",
            9: "3,2",
            10: "3,3",
            11: "3,4",
            12: "3,5",
            13: "4,1",
            14: "4,3",
            15: "4,5",
            16: "5,1",
            17: "5,2",
            18: "5,3",
            19: "5,4",
            20: "5,5",
        }
    elif max_moves == 20:
        index_map = {
            0: "1,1",
            1: "1,2",
            2: "1,3",
            3: "1,4",
            4: "1,5",
            5: "1,6",
            6: "1,7",
            7: "2,1",
            8: "2,3",
            9: "2,5",
            10: "2,7",
            11: "3,1",
            12: "3,2",
            13: "3,3",
            14: "3,4",
            15: "3,5",
            16: "3,6",
            17: "3,7",
            18: "4,1",
            19: "4,3",
            20: "4,5",
            21: "4,7",
            22: "5,1",
            23: "5,2",
            24: "5,3",
            25: "5,4",
            26: "5,5",
            27: "5,6",
            28: "5,7",
            29: "6,1",
            30: "6,3",
            31: "6,5",
            32: "6,7",
            33: "7,1",
            34: "7,2",
            35: "7,3",
            36: "7,4",
            37: "7,5",
            38: "7,6",
            39: "7,7",
        }

    for item in cycle:
        item = item[::-1]  # reverse tuple
        for l, index in enumerate(item):
            all_moves.append([index_map[index], index_map[item[l + 1]]])
            if l == len(item) - 2:
                break
    print(all_moves)


def main(scrambled, solution):
    priority = 0
    scrambled = [c for c in scrambled if c != " "]
    solution = [c for c in solution if c != " "]
    start_time = time.time()
    cyclopedia = set()
    solutionstack = []
    big_heapqueue = []
    visited_list = tuple()
    unvisited_list = []
    unsolved_tiles = 0
    # remove already solved positions
    visited_list = tuple(
        i for i in range(len(scrambled)) if scrambled[i] == solution[i]
    )
    unvisited_list = [i for i in range(len(scrambled)) if i not in visited_list]

    # how many tiles to solve?
    for i in range(len(scrambled)):
        if scrambled[i] != solution[i]:
            unsolved_tiles += 1

    # lenght of solution is either 40 or 21. 49 and 25 are the lengths if spaces are included
    if len(solution) in [40, 49]:
        max_moves = 20
    elif len(solution) in [21, 25]:
        max_moves = 10

    # To know when a perfect solution is found we need to know the number of required cycles.
    # If a 5x5 waffle has 14 unsolved tiles and can be solved in 10 moves
    # then 10 moves to solve 14 tiles means 4 double swaps (8 solved) and 6 single swaps (6 solved)
    # 14 - 10 = 4 double swaps = 4 cycles because each cycle ends with a double swap
    ideal_cycles_number = unsolved_tiles - max_moves

    # map characters to possible solution positions so we can look them up faster
    mapping = solution_mapping(scrambled, solution, visited_list)

    # first pass to find all double swaps
    doubles = tuple()
    start_rem = set()
    for i in unvisited_list:
        for index in mapping[scrambled[i]]:
            if (index not in visited_list) and (i not in visited_list):
                if scrambled[i] == solution[index] and scrambled[index] == solution[i]:
                    doubles += ((i, index),)
                    visited_list += (i, index)
                    start_rem.add(i)
                    start_rem.add(index)
    for i in start_rem:
        unvisited_list.remove(i)

    # second pass to generate starting swaps
    for i in unvisited_list:
        # go over the map to find indices to create the next possible swaps
        for index in mapping[scrambled[i]]:
            if (index not in visited_list) and (i not in visited_list):
                next_visited_list = visited_list + (i, index)
                local_cycle = (i, index)
                next_whole_cycle = doubles + (local_cycle,)
                # giving -20000 priority for each double swap and
                # treat the next cycle as if it were a double swap too
                priority = (len(doubles) * -20000) - 20000
                # print("Initial Priority:", priority)
                heapq.heappush(
                    big_heapqueue, (priority, [next_whole_cycle, next_visited_list])
                )

    # try generating cycles as long as there are still any on the heapqueue
    while big_heapqueue:
        # print("Current Heap Size:", len(big_heapqueue))
        # print("len visited:", len(visited_list))
        priority, heap_item = heapq.heappop(big_heapqueue)
        whole_cycle, visited_list = heap_item

        # we visited everything so we must be done
        if len(visited_list) == len(solution):

            # for the wafflegame.com we already know the number of ideal cycles
            if len(whole_cycle) == ideal_cycles_number:
                solutionstack.append(whole_cycle)
                print("Optimal solution:")
                print(whole_cycle)
                convert_indices_to_xy(whole_cycle, max_moves)
                break

            continue

        local_cycle = whole_cycle[-1]
        # lookup next required character positions
        next_possible_indices = mapping[scrambled[local_cycle[-1]]]
        for index in next_possible_indices:
            # case 1: end of cycle points to start, finish and open a new one
            if index == local_cycle[0]:
                # make hashable sets to avoid visiting the same cycle twice
                whole_frozen = frozenset(whole_cycle)
                if whole_frozen in cyclopedia:
                    continue
                else:
                    cyclopedia.add(whole_frozen)

                # new cycle lets go
                for i in unvisited_list:
                    for index in mapping[scrambled[i]]:
                        if (index not in visited_list) and (i not in visited_list):
                            next_priority = priority
                            # magic values!
                            # since we're adding a new cycle we're assigning a high priority to the
                            # next cycle to ensure it'll be on top of the heapqueue

                            prio_mod = next_priority - 20000
                            next_whole_cycle = whole_cycle + ((i, index),)
                            next_visited_list = visited_list + (i, index)

                            # und hepp!
                            heapq.heappush(
                                big_heapqueue,
                                (prio_mod, [next_whole_cycle, next_visited_list]),
                            )
            # case 2: end of cycle points to an unvisited index, continue the cycle
            else:
                if index not in visited_list:
                    next_priority = priority
                    next_whole_cycle = whole_cycle[:-1] + (local_cycle + (index,),)
                    next_visited_list = visited_list + (index,)
                    # we're extending the last cycle and have to adjust priority accordingly
                    if len(next_whole_cycle[-1]) == 3:
                        prio_mod = next_priority + 19000  # +20000 - 1000
                    elif len(next_whole_cycle[-1]) == 4:
                        prio_mod = next_priority + 900  # +1000 - 100
                    elif len(next_whole_cycle[-1]) == 5:
                        prio_mod = next_priority + 90  # +100 - 10
                    elif len(next_whole_cycle[-1]) == 6:
                        prio_mod = next_priority + 9  # +10 - 1
                    elif len(next_whole_cycle[-1]) == 7:
                        prio_mod = next_priority + 1  # +1 - 0
                    else:
                        prio_mod = next_priority

                    heapq.heappush(
                        big_heapqueue, (prio_mod, [next_whole_cycle, next_visited_list])
                    )

    # verify solution
    for item in solutionstack:
        scrambled_list = list(scrambled)
        swapcount = 0
        for cycle in item:
            swapcount += len(cycle) - 1
            cycle = list(cycle)
            cycle.reverse()
            for i in range(len(cycle) - 1):
                scrambled_list[cycle[i]], scrambled_list[cycle[i + 1]] = (
                    scrambled_list[cycle[i + 1]],
                    scrambled_list[cycle[i]],
                )
        print("Swaps: ", swapcount)
        if solution != scrambled_list:
            print("ERROR: Solution does not match!")
            input()
            print("Expected solution:", solution)
            print("Computed solution:", scrambled_list)
        break

    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Total optimal path finding routine runtime: {total_runtime:.2f} seconds")
    print(" ")


# scrambled = "DBDFAFECBCAE"
# solution = "AABBCCDDEEFF"
# waffle 310
# scrambled = "csroeu z votoaen f aeertr"
# solution = "curver o nafootz s eeater"
# scrambled = "thfeccun h t isistasni n i husitisgl g o ndigceiu"
# solution = "deficiti i h osustainc h l iunitings n c hsuggest"
# scrambled = "adotpwet a b rahscocde n e dtpibueen r h rtrgceuh"
# solution = "chopperh u r eabscondt t d htributee n c aragweed"
# scrambled = "tcvcsrou o r dbpneares o i itsueiett e g coiehkar"
# solution = "revisito e e rbandageo t s etouristi r c ocheckup"
scrambled = "henreubq n i tmerluree e q aduuotado o d yieearnc"
solution = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
if __name__ == "__main__":
    with open("collected_puzzles_and_solutions.json") as f:
        archive_list = json.load(f)
    # archive_list = brotlidecompress.main()
    start_time = time.time()
    puzzle_count = 0
    for item in archive_list:
        puzzle_count += 1
        print(item)
        main(item[0], item[1])
    end_time = time.time()
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total runtime: {total_runtime:.2f} seconds for {puzzle_count} puzzles")
