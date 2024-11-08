import copy
import heapq
import time
import json


# to maybe make things more clear:
# waffles are reduced to strings to find the shortest path
# they look like this:
# scrambled = "henreubq n i tmerluree e q aduuotado o d yieearnc"
# solution = "nunneryo u q imarqueea t a ldoubtedi r o echeered"
# ... but now without spaces
# cycle decomposition is not hard in theory:
# first letter is h but we want n. so we look where to find an n
# there's an n at position 2 (but already correct), 9, and 48
# so the first cycles we can create are [0,9] and [0,48]
# next we check those two how they should continue
# at position 9 should be "u". there's a u at 6 and 28
# so two new cycles are [0,9],[9,6] and [0,9],[9,28]
# if the next index points to the beginning we start a new cycle
# this continues until every index has been visited
# the idea is that the more cycles we have, the shorter the path, because the best cycle is one that solves two positions in one move
# because to transform dbaca into aabcd
# you could [[0,2],[2,1],[1,4]] (one cycle)
# or [0,4],[1,2] (two cycles), each solving two positions at once

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


# just a helper to make the solution swaps human readable
def convert_indices_to_xy(cycle):
    all_moves = []
    n = 0
    for item in cycle:
        n += len(item)
    n = n - len(cycle)
    print(n)
    if n == 10:
        indexmap = {
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
    elif n == 20:
        indexmap = {
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
    else:
        print("something is wrong, ideal move number is off")
        input()
    for item in cycle:
        item.reverse()
        for l, index in enumerate(item):
            all_moves.append([indexmap[index], indexmap[item[l + 1]]])
            if l == len(item) - 2:
                break
    print(all_moves)


def main(scrambled, solution):
    scrambled = [c for c in scrambled if c != " "]
    solution = [c for c in solution if c != " "]
    start_time = time.time()
    cyclopedia = set()
    solutionstack = []
    bigstack = []
    solved_at_start = []
    unsolved_tiles = 0
    # weed out already solved positions
    for i in range(len(scrambled)):
        if scrambled[i] == solution[i]:
            solved_at_start.append(i)
    # how many tiles to solve?
    for i in range(len(scrambled)):
        if scrambled[i] != solution[i]:
            unsolved_tiles += 1
    # print(len(solution))
    # looks weird because i started with strings that included spaces
    if len(solution) in [40, 49]:
        success = 20
    elif len(solution) in [25, 21]:
        success = 10
    # to know when a perfect solution is found we need to know the number of required cycles
    # if a 5x5 waffle has 14 unsolved tiles and can be solved in 10 moves
    # then 10 moves to solve 14 tiles means 4 double swaps (8 solved) and 6 single swaps (6 solved)
    # 14 - 10 = 4 double swaps = 4 cycles because each cycle ends with a double swap
    ideal_cycles_number = unsolved_tiles - success

    # map characters to possible solution positions so we can look them up faster
    mapping = solution_mapping(scrambled, solution, solved_at_start)

    # generate starting swaps
    for i in range(len(scrambled)):
        if i not in solved_at_start:
            for index in mapping[scrambled[i]]:
                localcycle = [i, index]
                newwholecycle = [localcycle]
                priority = 0
                # 2-cycles are the most valuable ones, so they get the highest priority
                for cycle in newwholecycle:
                    if len(cycle) == 2:
                        priority += 2 * 10000
                # and throw em on the heapqueue
                heapq.heappush(bigstack, (-priority, newwholecycle))
    # yeah my heapqueue is called bigstack, sue me
    while bigstack:
        # pop a cycle
        _, wholecycle = heapq.heappop(bigstack)
        # visitedlist filled with solved positions to avoid revisiting them
        visitedlist = copy.deepcopy(solved_at_start)

        for cycle in wholecycle:
            for i in cycle:
                # add the visited positions to the visitedlist
                visitedlist.append(i)
        # we visited everything so we must be done
        if len(visitedlist) == len(solution):

            solutionstack.append(wholecycle)
            # for the wafflegame.com we already know the number of ideal cycles
            if len(wholecycle) == ideal_cycles_number:
                print("Optimal solution:")
                print(wholecycle)
                convert_indices_to_xy(wholecycle)
                break

            continue

        localcycle = wholecycle[-1]
        # would be faster to look up the required character at this position
        # then look up the possible positions in the map
        # but we're already at sub-second speed so i don't care any more
        for index, char in enumerate(solution):
            # character is one we're looking for
            if char == scrambled[localcycle[-1]]:
                # skip current index if same position
                if localcycle[-1] != index:
                    # index already checked
                    if index in localcycle:
                        # if index points to beginning of current cycle, open a new cycle
                        if index == localcycle[0]:
                            # make hashable sets to avoid visiting the same cycle twice
                            whole_frozen = frozenset(
                                frozenset(item) for item in wholecycle
                            )
                            if whole_frozen in cyclopedia:
                                continue
                            else:
                                cyclopedia.add(whole_frozen)
                            # new cycle lets go
                            nextlocalcycle = []
                            for i in range(len(scrambled)):
                                for index, char in enumerate(solution):
                                    if (
                                        (char == scrambled[i])
                                        and i not in visitedlist
                                        and index not in visitedlist
                                    ):

                                        newwholecycle = copy.deepcopy(wholecycle)
                                        nextlocalcycle = [i, index]
                                        newwholecycle.append(nextlocalcycle)
                                        priority = 0
                                        # magic values! that I made up.
                                        # 2-cycles are the most valuable ones
                                        # the priority determines the order in which the cycles are popped from the heapqueue
                                        for cycle in newwholecycle:
                                            if len(cycle) == 2:
                                                priority += 2 * 10000
                                            elif len(cycle) == 3:
                                                priority += 1000
                                            elif len(cycle) == 4:
                                                priority += 100
                                        # und hepp!
                                        heapq.heappush(
                                            bigstack, (-priority, newwholecycle)
                                        )
                    else:
                        # next index still not visited, add it to the current cycle
                        if index not in visitedlist:
                            newwholecycle = copy.deepcopy(wholecycle)
                            newwholecycle[-1].append(index)
                            priority = 0
                            for cycle in newwholecycle:
                                if len(cycle) == 2:
                                    priority += 2 * 10000
                                elif len(cycle) == 3:
                                    priority += 1000
                                elif len(cycle) == 4:
                                    priority += 100

                            heapq.heappush(bigstack, (-priority, newwholecycle))

    # Sort bigstack by the number of sublists in each list
    # which is kinda pointless now that I think about it since we know exactly when a perfect solution was found
    # so it should only contain 1 item.
    # ah well please sort my item
    sorted_solutionstack = sorted(solutionstack, key=len, reverse=True)

    for item in sorted_solutionstack:
        scrambled_list = copy.deepcopy(list(scrambled))
        swapcount = 0
        for cycle in item:
            swapcount += len(cycle) - 1
            cycle.reverse()
            for i in range(len(cycle) - 1):
                scrambled_list[cycle[i]], scrambled_list[cycle[i + 1]] = (
                    scrambled_list[cycle[i + 1]],
                    scrambled_list[cycle[i]],
                )
        print("Swaps: ", swapcount)
        # print("".join(scrambled_list))
        break

    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
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
    for item in archive_list:
        print(item)
        main(item[0], item[1])
