import copy
import heapq
import time


def solution_mapping(scrambled, solution, solved_at_start):
    mapping = {}
    for char in set(scrambled):  # Use set to avoid duplicate characters
        positions = [
            i
            for i, s_char in enumerate(solution)
            if s_char == char and i not in solved_at_start
        ]
        mapping[char] = positions
    return mapping


def main(scrambled, solution):
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

    if len(solution) == 49:
        success = 20
    elif len(solution) == 25:
        success = 10
    # to know when a perfect solution is found we need to know the number of required cycles
    # if a 5x5 waffle has 14 unsolved tiles and can be solved in 10 moves
    # then 10 moves to solve 14 tiles means 4 double swaps (8 solved) and 6 single swaps (6 solved)
    # 14 - 10 = 4 double swaps = 4 cycles because each cycle ends with a double swap
    ideal_cycles_number = unsolved_tiles - success

    mapping = solution_mapping(scrambled, solution, solved_at_start)

    # generate starting swaps
    for i in range(len(scrambled)):
        if i not in solved_at_start:
            # for index, char in enumerate(solution):
            #    if char == scrambled[i]:
            for index in mapping[scrambled[i]]:
                localcycle = [i, index]
                newwholecycle = [localcycle]
                priority = 0
                for cycle in newwholecycle:
                    if len(cycle) == 2:
                        priority += 2 * 10000

                heapq.heappush(bigstack, (-priority, newwholecycle))

    while bigstack:
        _, wholecycle = heapq.heappop(bigstack)
        visitedlist = copy.deepcopy(solved_at_start)
        # print(wholecycle)

        for cycle in wholecycle:
            for i in cycle:
                visitedlist.append(i)
        if len(visitedlist) == len(solution):

            solutionstack.append(wholecycle)
            if len(wholecycle) == ideal_cycles_number:
                print("Optimal solution:")
                print(wholecycle)
                break

            continue

        localcycle = wholecycle[-1]
        # would be faster to look up the required character at this position
        # then look up the possible positions in the map
        for index, char in enumerate(solution):
            # character is one we're looking for
            if char == scrambled[localcycle[-1]]:
                # skip current index if same position
                if localcycle[-1] != index:

                    # index already checked
                    if index in localcycle:
                        # if index points to beginning of current cycle, open a new cycle
                        if index == localcycle[0]:
                            whole_frozen = frozenset(
                                frozenset(item) for item in wholecycle
                            )
                            if whole_frozen in cyclopedia:
                                continue
                            else:
                                cyclopedia.add(whole_frozen)

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
                                        cyclesumprio = 0
                                        for cycle in newwholecycle:
                                            cyclesumprio += 100
                                            if len(cycle) == 2:
                                                priority += 2 * 10000
                                            elif len(cycle) == 3:
                                                priority += 1000
                                            elif len(cycle) == 4:
                                                priority += 100

                                        heapq.heappush(
                                            bigstack, (-priority, newwholecycle)
                                        )
                    else:
                        if index not in visitedlist:
                            newwholecycle = copy.deepcopy(wholecycle)
                            newwholecycle[-1].append(index)
                            priority = 0
                            cyclesumprio = 0
                            for cycle in newwholecycle:
                                cyclesumprio += 100
                                if len(cycle) == 2:
                                    priority += 2 * 10000
                                elif len(cycle) == 3:
                                    priority += 1000
                                elif len(cycle) == 4:
                                    priority += 100

                            heapq.heappush(bigstack, (-priority, newwholecycle))

    # Sort bigstack by the number of sublists in each list
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
        print("".join(scrambled_list))
        break

    # Record the end time
    end_time = time.time()

    # Calculate the total runtime
    total_runtime = end_time - start_time

    # Print the total runtime
    print(f"Total optimal path finding routine runtime: {total_runtime:.2f} seconds")


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
    main(scrambled, solution)
